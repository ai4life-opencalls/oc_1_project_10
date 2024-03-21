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

The main challenge in this project was the limitations imposed by the device. The final output should be a device-compatible gating strategy. Therefore, just training a classifier couldn't be enough. Also, we can only use the channels that are measured by the device, not any other computed features. Another limitation was about the gates: each gate can generated based on only two channels at max, and we can have a maximum of 14 gates.  
