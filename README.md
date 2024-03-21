<p align="center">
  <a href="https://ai4life.eurobioimaging.eu/open-calls/">
    <img src="https://github.com/ai4life-opencalls/.github/blob/main/AI4Life_banner_giraffe_nodes_OC.png?raw=true" width="70%">
  </a>
</p>

# Project #10: Image-guided gating strategy for image-enabled cell sorting of phytoplankton
---

In this project, **Moritz Winker** from the European Molecular Biology Laboratory (EMBL) in Heidelberg is using a cutting-edge commercial flow cytometer to sort phytoplankton from lab-grown cultures or field samples. Sorting is traditionally done by selecting features measured by the instrument on the sample and manually drawing a gate defining the range of values in these features that correspond to the cells being selected.  
However, this new instrument is image-enabled and allows exporting not only traditional features but features derived from fluorescent images as well. In addition, it supports the import of gating strategies to the control software. This opens the door to automated analysis of the features and consequently, the generation of a gating strategy that can be uploaded directly to the flow cytometer.  

>"This is at the moment done manually and depends largely on the experience of the user."

The main challenge in this project was the limitations imposed by the device. The final output should be a device-compatible gating strategy. Therefore, just training a classifier couldn't be enough. Also, we can only use the channels that are measured by the device, not any other computed features. Another limitation was about the gates: each gate can be generated based on only two channels at max, and we can have a maximum of 14 gates.  

## Installation
It is highly recommended to use a python environment manager like conda to create a clean environment for the installation.
You can install all the requirements by one command using provided environment config file (env.yml):
```bash
conda env create -f ./env.yml
```

### Requirements
- `python >= 3.9`
- `numpy`
- `matplotlib`
- `pytables`
- `pandas == 1.5.0`
- `scipy == 1.11`
- `scikit-learn`
- `flowkit`
- `jupyterlab`
- `ipywidgets`
- `ipydatagrid`
- `tqdm`

## Pipeline Usage
The whole pipline divided into the three steps:  
1. Transforming raw data into the *Logicle* scale
2. Finding the best channel pairs
3. Creating the gating strategy and save the workspace

In the `pipeline` directory, you can find three notebooks (numbered by steps).  

### 💡 Step One (Logicle Transform):
It is a common practice in flowcytometry that the data get transformed into *log* or *logicle* space as the first step. This transformation helps to have a better visualization of the data and a better separation between species.
The *`1_logicle_transform.ipynb`* notebook is provided to do the logicle transform over the data. In this notebook you need to set the raw data directory which contains your *`fcs`* files, and the directory that you want to save the transformed data (A dialog will be opened to set the directories).


### 💡 Step Two (Selecting Channel Pairs):



### 💡 Step Three (Gating):
