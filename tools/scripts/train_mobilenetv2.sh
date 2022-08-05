./tools/dist_train.sh \
./configs/resnet50/cascade_mask_rcnn_resnet50_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco_in1k.py \
8 \
--cfg-options model.pretrained=/workdir/checkpoint/resnet50/res50/checkpoint-best.pth