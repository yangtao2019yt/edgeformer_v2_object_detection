./tools/dist_train.sh \
./configs/resnet50/cascade_mask_rcnn_resnet50_gcc_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco_in1k.py \
8 \
--cfg-options model.pretrained=/workdir/checkpoint/resnet50/res50_gcc/checkpoint-best.pth