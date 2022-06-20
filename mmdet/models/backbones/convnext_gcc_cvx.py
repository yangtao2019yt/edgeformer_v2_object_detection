from functools import partial
import torch
import torch.nn as nn
import torch.nn.functional as F
from timm.models.layers import trunc_normal_, DropPath

from mmcv_custom import load_checkpoint
from mmdet.utils import get_root_logger
from ..builder import BACKBONES

from .modules.gcc_cvx_modules import gcc_cvx_Block, gcc_cvx_Block_2stage, Block, LayerNorm, gcc_Conv2d

@BACKBONES.register_module()
class ConvNeXt_cvx_gcc(nn.Module):
    def __init__(self, in_chans=3, depths=[3, 3, 9, 3], dims=[96, 192, 384, 768], 
                 drop_path_rate=0., layer_scale_init_value=1e-6, out_indices=[0, 1, 2, 3],
                 gcc_stage=1
                 ):
        super().__init__()
        # super(ConvNeXt_cvx_gcc, self).__init__()

        self.downsample_layers = nn.ModuleList() # stem and 3 intermediate downsampling conv layers
        stem = nn.Sequential(
            nn.Conv2d(in_chans, dims[0], kernel_size=4, stride=4),
            LayerNorm(dims[0], eps=1e-6, data_format="channels_first")
        )
        self.downsample_layers.append(stem)
        for i in range(3):
            downsample_layer = nn.Sequential(
                    LayerNorm(dims[i], eps=1e-6, data_format="channels_first"),
                    nn.Conv2d(dims[i], dims[i+1], kernel_size=2, stride=2),
            )
            self.downsample_layers.append(downsample_layer)

        self.stages = nn.ModuleList() # 4 feature resolution stages, each consisting of multiple residual blocks
        dp_rates=[x.item() for x in torch.linspace(0, drop_path_rate, sum(depths))] 
        cur = 0
        stages_fs = [56, 28, 14, 7]
        for i in range(4):
            if i < 2:   # for stage 0 and 1, no gcc
                stage = nn.Sequential(*[
                    Block(dim=dims[i], drop_path=dp_rates[cur + j], layer_scale_init_value=layer_scale_init_value) \
                    for j in range(depths[i])
                ])
            else:       # for stage 2 and 3, gcc modules is used
                gcc_Block = gcc_cvx_Block_2stage if gcc_stage==2 else gcc_cvx_Block
                stage = nn.Sequential(*[
                    gcc_Block(dim=dims[i], drop_path=dp_rates[cur + j], layer_scale_init_value=layer_scale_init_value,
                        # meta_kernel_size=stages_fs[i], instance_kernel_method=None, use_pe=True) \\
                        # Notice: For detection, interpolation_bilinear is used for dynamic resolution
                        meta_kernel_size=stages_fs[i], instance_kernel_method="interpolation_bilinear", use_pe=True) \
                    # if depths[i]//3 < j+1 <= 2*depths[i]//3 else \
                    if 2*depths[i]//3 < j+1 else \
                    Block(dim=dims[i], drop_path=dp_rates[cur + j], layer_scale_init_value=layer_scale_init_value) \
                    for j in range(depths[i]) # here we use gcc in the last 1/3 blocks
                ])                            # e.g., j+1=7 > 9-9//3=6, so block 678 is gcc_block, where block 0~5 is normal
            self.stages.append(stage)
            cur += depths[i]
        
        self.out_indices = out_indices

        norm_layer = partial(LayerNorm, eps=1e-6, data_format="channels_first")
        for i_layer in range(4):
            layer = norm_layer(dims[i_layer])
            layer_name = f'norm{i_layer}'
            self.add_module(layer_name, layer)

        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, (nn.Conv2d, nn.Linear)):
            trunc_normal_(m.weight, std=.02)
            nn.init.constant_(m.bias, 0)
        elif isinstance(m, gcc_Conv2d):
            m.gcc_init()    # convnext like initialization is used for gcc as well
        
    def init_weights(self, pretrained=None):
        def _init_weights(m):
            if isinstance(m, nn.Linear):
                trunc_normal_(m.weight, std=.02)
                if isinstance(m, nn.Linear) and m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.LayerNorm):
                nn.init.constant_(m.bias, 0)
                nn.init.constant_(m.weight, 1.0)

        if isinstance(pretrained, str):
            self.apply(_init_weights)
            logger = get_root_logger()
            load_checkpoint(self, pretrained, strict=False, logger=logger)
        elif pretrained is None:
            self.apply(_init_weights)
        else:
            raise TypeError('pretrained must be a str or None')

    def forward_features(self, x):
        outs = []
        for i in range(4):
            x = self.downsample_layers[i](x)
            x = self.stages[i](x)
            if i in self.out_indices:
                norm_layer = getattr(self, f'norm{i}')
                x_out = norm_layer(x)
                outs.append(x_out)

        return tuple(outs)

    def forward(self, x):
        x = self.forward_features(x)
        return x