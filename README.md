# **Is there Water?**
<div>
<P ALIGN=CENTER><img src="images/water.jpg" style="display: block; margin-left: auto; margin-right: auto;"  width="900"/></P></div>

A Denver non-profit works with district-level governments around the world to assess communities without adequate access to clean water, identify appropriate technologies, and design and construct water points for underserved populations. In 2017, the organization conducted a full census of water points in supported districts of four countries. The census survey included information on location of each water point, the size of the population it serves, physical condition of the hardware, and whether or not the water point was functioning – among other information. The resulting dataset is intended as a tool for local governments in their planning and budgeting for clean water coverage within their jurisdictions.

The organization hopes to use the water point census dataset to better understand the factors that contribute to the likelihood of a waterpoint breaking. In their annual planning, they want to be able to guide local partners on which water points to inspect and earmark funds to support maintenance. This could greatly improve maintenance response times and, ideally, help local governments in their planning to ensure total coverage of clean water access for their constituents.

### The analytics questions:
* What are the key predictors of whether or not a water point is functioning on any given day?
* Is the organization able to identify with reasonable certainty which water points are likely to need maintenance or replacement?

### The dataset:
The water point census data was collected through mobile phone surveys by local engineers who are trained to assess the components of the water point technologies. There is one survey for handpumps and spring-fed taps and another for piped water systems, and the completed surveys are submitted to a cloud aggregator that then exports a CSV file. This analysis will focus on data from handpumps and spring-fed taps. Piped water systems are heavily monitored and managed, and when one is broken it does not go unnoticed. Handpumps, in contrast, in very remote areas can become defunct without governments taking much notice.

The CSV dataset has 10,034 rows and 52 columns. Most columns have no more than 3 missing values. Two columns have significant missing values and will be removed from the analysis. The feature to be predicted – is the water point functioning or not – has 863 entries for ‘not functioning’ (0), and 9,171 entries for ‘functioning’ (1). 

## **Targeted EDA**
Describe...:
* **Heatmap**
* **Pair plots**
* **t-SNE plot**

The data are not normally distributed, but **there appears to be a linear relationship with each**. Data points, however, are clustered at the low end on both axis.
To investigate further, the feature data were split into two categories - **least developed** and **most developed countries** - using the median value for each feature:

<div>
<P ALIGN=CENTER><img src="images/below5m.png" alt="drawing" width="330"/>  <img src="images/extreme_weather.png" alt="drawing" width="330"/> </P>
</div>

## Minimum viable product:
Identify coefficients using logistic regression and feature importances using random forests. Tune to optimal hyperparameters. Make a recommendation based on the insights and suggestions for future work.

## MVP +:
Apply a Naïve Bayes model to the dataset to see how it might be able to predict whether water points are broken or not.

## **Logistic Regression**
Some lead up...
<div>
<P ALIGN=CENTER><img src="images/ols.png" alt="drawing" width="600"/></div>

## **Some reflection:**
* Recommend revising the survey after thorough consultation with stakeholders of the dataset to better identify expectations from the analysis.
* More...

# Study ongoing...
