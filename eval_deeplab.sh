# Ensure all pretrained weights are located in the weights/ directory

# Evaluation for AICrowd dataset
CUDA_VISIBLE_DEVICES=0 python3 run_deeplab.py --evaluate --backbone=drn_c42 --out-stride=8 \
    --workers=2 --epochs=1 --test-batch-size=3 --gpu-ids=0 \
    --checkname=aicrowd_evaluation --dataset=crowdAI --resume=crowdAI --best-miou \
    --data-root=./ --loss-type=ce_dice
