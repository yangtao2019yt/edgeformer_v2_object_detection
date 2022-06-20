# Import coco
ln -s /workdir/data ./data
echo "COCO successfully imported!"

./tools/dist_train.sh \
./configs/convnext/cascade_mask_rcnn_convnext_tiny0.5_patch4_window7_mstrain_480-800_giou_4conv1f_adamw_3x_coco_in1k.py \
8 \
--cfg-options model.pretrained=/workdir/checkpoint/baseline/convnext_tiny0/checkpoint-best.pth