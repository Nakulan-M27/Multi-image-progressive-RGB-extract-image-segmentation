# Training for AICrowd dataset (now with 250 images)
CUDA_VISIBLE_DEVICES=0 python3 run_deeplab.py --backbone=drn_c42 --out-stride=8 --dataset=crowdAI \
    --workers=4 --loss-type=ce_dice --fbeta=1.0 --epochs=50 --batch-size=8 --test-batch-size=4 --weight-decay=1e-4 \
    --gpu-ids=0 --lr=1e-3 --loss-weights 1.0 1.0 --dropout 0.3 0.5 \
    --checkname=aicrowd_deeplab_drn_c42_ce_dice --data-root=./ --use-wandb