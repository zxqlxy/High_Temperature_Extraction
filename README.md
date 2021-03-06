# High Temperature Solar EUV Signal Extraction and Restorion

## Introduction 

Manually extract features from AIA EUV channel images can be tedious and we have sufficient reasons to believe that we 
can extract information we want since each channel is a combination of different ions' emission. Right now we are interested 
in information of high energy emission Fe_XVIII signal. 

Similar projects that utilize deep learning are [HMI-to-AIA Prediction](https://arxiv.org/abs/1903.04538) and [EUV Monitoring](https://doi.org/10.1126/sciadv.aaw6548).

## Preprocess the data to get Fe_XVIII signal
The method is from [A Systematic Survey of High-Temperature Emission in Solar Active Regions](http://dx.doi.org/10.1088/0004-637X/759/2/141) to extract Fe_XVIII signal on 94 by subtracting "warm" signal from 171 and 193.
The data is from [Standford JSOC Database](http://jsoc.stanford.edu/data/aia/synoptic/).

### Week 1
The result of a Fe_XVIII signal full disk [solar picture](pics/20190309_Fe_XVIII.jpg) is obtained from [94 image](pics/20190309_0000_0094.jpg), [171 image](pics/20190309_0000_0171.jpg), [193_image](pics/20190309_0000_0193.jpg).
<p>
  <img src="pics/20190309_Fe_XVIII.jpg" alt="solar picture" width="420" style="float: right;"/>
  <img src="pics/20190309_0000_0094.jpg" alt="94 image" width="420" style="float: right;"/>
  <img src="pics/20190309_0000_0171.jpg" alt="171 image" width="420" style="float: right;"/>
  <img src="pics/20190309_0000_0193.jpg" alt="193 image" width="420" style="float: right;"/>
 </p>


### Week 2
After some preprocessing, I did the first GAN on data on first 3 months of data and I found that the loss function never
converge because it will pick noise around the sun like [this](pics/plot_000900.png). 

Indeed, after I found the maximum points on both 94 and 193. I found that the maximum point of 94 is actually out side of
the sun. While the 193 looks good. Here are the pictures.
<p>
  <img src="pics/max_point_094.jpg" alt="094" width="420" style="float: right;"/>
  <img src="pics/max_point_193.jpg" alt="193" width="420" style="float: right;"/>
</p>

Thus, we need to mask out the data outside of the disk (including the outer part of the disk) to avoid too much noise.
<p>
  <img src="pics/20190309_0000_0094.jpg" alt="094" width="420" style="float: right;"/>
  <img src="pics/20190309_0000_0094_mask.jpg" alt="193" width="420" style="float: right;"/>
</p>
Not only that, we need to normalize the data (it turns out each different picture can have different scale) so that the 
max and min are 1.0 and -1.0 respectively. 

### week 3
Now, the preprocess first mask out (set masked area to minimum of one picture) and then normalize. Also, after some observations, 
the unwanted results (sun flare) occurs mostly when the maximum of the picture is less than 10^8.