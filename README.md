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
Separately plotted logged values of CO2 emissions as a function of:
* **GNI (positive correlation)**
* **HDI (negative correlation)**
* **Poverty rate (negative correlation)**

<div>
<P ALIGN=CENTER><img src="images/log_co2_gni.png" alt="drawing" width="330"/>  <img src="images/log_co2_hdi.png" alt="drawing" width="330"/> <img src="images/co2_poverty2.png" alt="drawing" width="330"/> </P>
</div>

The data are not normally distributed, but **there appears to be a linear relationship with each**. Data points, however, are clustered at the low end on both axis.
To investigate further, the feature data were split into two categories - **least developed** and **most developed countries** - using the median value for each feature:

<div>
<P ALIGN=CENTER><img src="images/categorized_gni.png" alt="drawing" width="330"/>  <img src="images/categorized_hdi.png" alt="drawing" width="330"/> <img src="images/categorized_poverty.png" alt="drawing" width="330"/> </P>
</div>

**There does not appear to be a clear relationship in the data between CO2 emissions and climate change impacts:**

<div>
<P ALIGN=CENTER><img src="images/below5m.png" alt="drawing" width="330"/>  <img src="images/extreme_weather.png" alt="drawing" width="330"/> </P>
</div>

## **Linear Regression**
The StatsModel ordinary least squares (OLS) method was applied with all three development features. The resulting OLS summary table shows **statistical significance for two of the three coefficients**, and **the model accounts for 71% of the variance**:
<div>
<P ALIGN=CENTER><img src="images/ols.png" alt="drawing" width="600"/></div>

When the coefficient that was a weaker predictor removed, **the P-values remained essentially the same and the adjusted r-squared reduced** slightly:
<div>
<P ALIGN=CENTER><img src="images/ols_2.0.png" alt="drawing" width="600"/></div>

### **Further investigation of CO2 emissions to GNI**

**To further confirm the appropriateness of GNI** as a predictor of CO2 emissions, the **studentized residuals were plotted**, showing that all but a couple of outliers fit within 3 and -3:
<div>
<P ALIGN=CENTER><img src="images/stdnt_resid.png" alt="drawing" width="500"/></div>

## **Some reflection:**
* The data are summary data compiled from various sources, with likely varying quality of data collection.
* Many **small island countries had to be removed** due to missing data. These countries are likely to be some of the lowest emitters and most vulnerable to climate change.
* The **climate change impact indicators in the data are very broad and don't capture vulnerability of individual countries very well**. A more complex vulnerability index would be more useful.
* The size of **the dataset is limited by the number of countries in the world**. A more sophisticated analysis might be possible if the data had a different kind of boundary, such as **watershed or ecological region**, or by different kind of political boundary like **population clusters or localized market boundaries**
* The goal of this analysis was not to predict unseen data, but to demonstrate an existing relationship between emissions and development outcomes. And therefore the model was not fit on separate training and test sets.

# Further analysis using additional datasets ongoing...
