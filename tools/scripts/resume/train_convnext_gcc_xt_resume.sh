./tools/dist_train.sh \
./configs/convnext_xt/cascade_mask_rcnn_convnext_gcc_xt_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco_in1k.py \
8 \
--cfg-options model.pretrained=/workdir/checkpoint/cvx/gcc_cvx_tiny0/checkpoint-best-1H2W.pth \
--resume-from {checkpoint_root}/latest.pth