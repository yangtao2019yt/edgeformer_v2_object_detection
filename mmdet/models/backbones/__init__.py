from .darknet import Darknet
from .detectors_resnet import DetectoRS_ResNet
from .detectors_resnext import DetectoRS_ResNeXt
from .hourglass import HourglassNet
from .hrnet import HRNet
from .regnet import RegNet
from .res2net import Res2Net
from .resnest import ResNeSt
from .resnet import ResNet, ResNetV1d
from .resnext import ResNeXt
from .ssd_vgg import SSDVGG
from .trident_resnet import TridentResNet
from .swin_transformer import SwinTransformer
from .convnext import ConvNeXt
# convnext_gcc_cvx
from .convnext_gcc_mf import ConvNeXt_mf_gcc
from .convnext_gcc_mf_lg import ConvNeXt_mf_lg_gcc
# convnext_gcc_cvx
from .convnext_gcc_cvx import ConvNeXt_cvx_gcc
from .convnext_gcc_cvx_lg import ConvNeXt_cvx_lg_gcc

__all__ = [
    'RegNet', 'ResNet', 'ResNetV1d', 'ResNeXt', 'SSDVGG', 'HRNet', 'Res2Net',
    'HourglassNet', 'DetectoRS_ResNet', 'DetectoRS_ResNeXt', 'Darknet',
    'ResNeSt', 'TridentResNet', 'SwinTransformer', 'ConvNeXt',
    # gcc nets
    'ConvNeXt_mf_gcc', 'ConvNeXt_mf_lg_gcc', 'ConvNeXt_cvx_gcc', 'ConvNeXt_cvx_lg_gcc',
]
