## Optimizing Building Footprint Extraction from Satellite Images via Progressive Multi-Image Deep Learning Approaches

This repository is the official implementation of **[Optimizing Building Footprint Extraction from Satellite Images via Progressive Multi-Image Deep Learning Approaches]** by Nakulan Murugan and Prakash Singh Badal. 

<img width="800" height="1200" alt="image" src="https://github.com/user-attachments/assets/b2da6d57-7ac7-41e5-8e58-69addef2538a" />

### Requirements

1. Install the dependencies from requirements.txt file in the repository
```setup
pip install -r requirements.txt
```

### Datasets

#### Downloading the Datasets
1. To download the AICrowd dataset, please go [here](https://www.aicrowd.com/challenges/mapping-challenge-old). You will have to either create an account or sign in to access the training and validation set. Please store the training/validation set inside `<root>/AICrowd/<train | val>` for ease of conversion.

#### Converting the Datasets

Please use our provided dataset converters to process the datasets. For all converters, please look at the individual files for an example of how to use them. 
1. For AICrowd, use `datasets/converters/cocoAnnotationToMask.py`. 

#### Creating the Boundary Weight Maps

In order to train with the exponentially weighted boundary loss, you will need to create the weight maps as a pre-processing step. Please use `datasets/converters/weighted_boundary_processor.py` and follow the example usage. The `inc` parameter is specified for computational reasons. Please decrease this value if you notice very high memory usage. 

**Note:** these maps are not required for evaluation / testing. 

### Training and Evaluation
To train / evaluate the DeepLabV3+ models described in the paper, please use `python run_deeplab.py` or `python run_deeplab.py` with `--evaluate` for your convenience. We employ the following primary command-line arguments:

| Parameter                 | Default       | Description (final argument)  |	
| :------------------------ |:-------------:| :-------------|
| --backbone 	    |	`resnet`         | The DeeplabV3+ backbone **(final method used `resent` as well)**
| --out-stride | 16 | The backbone compression factor **(16)**
| --dataset | `CrowdAI` | The dataset to train / evaluate on (other choices: `spaceNet`, `Urban3D`, `combined`)
| --data-root | `/data/` | **Please replace this with the root folder of the dataset samples that you have stored in your system**
| --workers | 2 | Number of workers for dataset retrieval **(4)**
| --loss-type | `ce_dice` | Type of objective function. Use `wce_dice` for exponentially weighted boundary loss. This repository encompasses the code for the same.
| --fbeta | 1 | The beta value to use with the F-Beta Measure  **(0.5)**
| --dropout | `0.1 0.5` | Dropout values to use in the DeepLabV3+ **(0.3 0.5)**
|--epochs | None | Number of epochs to train **(60 for train, 1 for test)**
| --batch-size| None | Batch size **(4)**
| --test-batch-size| None | Testing Batch Size **(4)**
| --lr | `1e-4` | Learning Rate **(`1e-4`)**
| --weight-decay | `5e-4` | L2 Regularization Constant **(`1e-4`)**
| --gpu-ids | `blank` | GPU Ids (Use `--no-cuda` for only CPU). In our case, we have involved `--cuda` 
| --checkname | None | Experiment name
| --use-wandb | False | Track experiment using WandB **(True in this case)**
| --resume | None | Experiment name to load weights from (i.e. `crowdaideeplab-resnet-crowdai` for `weights/Crowdai/checkpoint.pth.tar`)
| --evalulate | False | **Enable this flag for testing**
| --best-miou | False | **Enable this flag to get best results when testing**
| --incl-bounds | False | **Enable this flag when training with `wce_dice` as a loss**

To train with the progressively increasing dataset, you need to:
1. Create a seperate file for each of the training runs. They must contains the images and corresponding annotations for the same.
2. To get the corresponding annotations, run the `create_filtered_annotations` for 100 image run, `create_train250_annotations` and so on.
3. With the annotations and images now present for each file, you can proceed to run the model.

### Pre-Trained Weights

We provide pre-trained model weights in the `weights/` directory. Please use Git LFS to download these weights. These weights correspond to our best model on all three datasets. It is not necessary to use these weights and the weights can also be obtained from scratch in the training run.

### Results

Our final model is a **DeepLavV3+ module with a Dilated ResNet backbone** trained using the F-Beta Measure + Exponentially Weighted Cross Entropy Loss **(Beta = 0.5)**. We employ the progressively improving dataset training only for the **CrowdAI dataset**. 

Our model shows sustainable improvement as we improve the number of training images progressively. The results obtained are below:

| No. of images | Accuracy | F1 Score | mIoU | 
| --- |------- | ---- | ---- |
| 100 | 37.9% | 65.6% | 21.5% 
| 250 | 38.4% |​ 66.4​% | 21.6​%
| 500 | 38.3% | ​66.2%​ | 21.5​%
| 750 | 38.1​% | 65.8​% | 21.6​%
| 1000 | 38.4%​ | 66.1% |​ 22.1% ​

### Acknowledgements

We would like to thank `aatifjiwani` for his model and paper using which we could build this research. You can find the repository [here](https://github.com/aatifjiwani/rgb-footprint-extract) and the paper [here](https://arxiv.org/abs/2104.01263) 


