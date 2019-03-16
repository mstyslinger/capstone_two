# **Is there Water?**
<div>
<P ALIGN=CENTER><img src="images/smokestack2.png" style="display: block; margin-left: auto; margin-right: auto;"  width="800"/></P></div>

Climate change impacts are increasingly being observed ahead of predicted timeframes, while progress on national targets for greenhouse gas (GHG) emissions reductions are falling short. More dramatic global impacts like shrinking ice caps and glaciers, ocean temperature rise, and storm intensity are well-reported, **the more nuanced impacts of climate change on livelihoods and development prospects** for countries around the world are less understood.

### **Question of Climate Justice**
**Because increases in GHG emissions and reductions in carbon sinks are generally a bi-product of economic development, it stands to reason that countries that have contributed more to climate change have more favorable development outcomes** than those that have contributed little. Extending from that logic, **countries with lower development outcomes are more vulnerable to the impacts of climate change**, as a higher proportion of the population is dependent on natural resources for their direct livelihoods. Smallholder farmers around the world, for example, increasingly face crop losses from shifting annual rain patterns and extreme weather events.
<div>
<P ALIGN=CENTER><img src="images/developed.png" alt="drawing" width="390"/>  <img src="images/developing1.png" alt="drawing" width="390"/></p></div>

### The analytics questions:
* Do countries with the highest GHG emissions have higher development outcomes than countries with low emissions?
* Are high and low emitters more or less impacted by the effects of climate change?

### The dataset:
* The analysis was conducted using a dataset from the online World Bank Data Catalog that **compiles national-level summary data on GHG emissions, development outcomes, and climate change impacts for all countries from 1990 - 2010**.
* The original CSV dataset contains 13,512 rows and 28 columns.
Once imported and reshaped, the Pandas dataframe contained only 233 rows with a few hundred fields.
* After some initial exploratory data analysis (EDA), fields were reduced to the following most relevant for answering the research questions:
  - **CO2 emissions (MT) per capita** - captures direct emissions and deforestation)
  - **Per capita Gross National Income (GNI)**
  - **Human Development Index (HDI) score** - a statistic composite index of human-level development outcomes, such as life expectancy and education.
  - **Population living below the international poverty line ($1.25)**  
  - **% of population living below 5 meters above sea level**
  - **% of population exposed to droughts, floods, and extreme temperatures**
* Records with too many missing annual values on under these indicators were removed.
* Annual data were aggregated for each, producing a mean value for each feature.


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
