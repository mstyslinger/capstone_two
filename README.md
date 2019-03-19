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

## **Exploratory data analysis (EDA)**
The CSV dataset has 10,034 rows and 52 columns. Two columns have significant missing values and will be removed from the analysis. The feature to be predicted – is the water point functioning or not? – is imbalanced, and train-test splits were made with stratification to maintain the proportionality of the original datset. After data cleaning, the resulting dataframe has 10,031 rows and 17 columns. A dataframe was also created with dummied categorical features, resulting in one dataset with 24 columns (drop first = True) and another with 27 (all dummies included).
<div>
<P ALIGN=CENTER><img src="images/dist_broken2.png" alt="drawing" width="430"/>  <img src="images/broke_by_country2.png" alt="drawing" width="430"/> </P>
</div>

When the data is broken out by country, it becomes evident that the distribution of broken water points varies significantly by country:
* India - About 2% of water points (129/5,991) broken
* Malawi - About 9% of water points (153/1730) broken
* Rwanda - About 12% of water points (91/743) broken
* Uganda - About 31% of water points (489/1,567) broken

This suggests that country could be a significant predictor of broken water points, though it's important to not that India accounts for about half of water points in the dataset, and the smaller number of data points for each of the other three countries might compromise statistical significance.

### Water points broken by type of technology (mean of values 1 or 0) - overall and by country
<div>
<P ALIGN=CENTER><img src="images/broke_by_tech.png" alt="drawing" width="530"/>  </P>
</div>
<div>
<P ALIGN=CENTER><img src="images/india_broke_by_type.png" alt="drawing" width="375"/><img src="images/malawi_broke_by_type.png" alt="drawing" width="375"/>  </P>
</div>
<div>
<P ALIGN=CENTER><img src="images/rwanda_broke_by_type.png" alt="drawing" width="375"/><img src="images/uganda_broke_by_type.png" alt="drawing" width="375"/>  </P>
</div>

There's notable variation by type, but less so in India. The technologies with the highest rate of being broken fall into the "other" category, which are a number of different technologies, each occuring less than 150 times in the dataset. There is enough variation among the 7 main technology types to suggest it could be a useful predictor.

### Age since original construction plotted against whether the water point is broken or functioning
<div>
<P ALIGN=CENTER><img src="images/broke_age.png" alt="drawing" width="425"/> </P>
</div>

Original construction does not seem to have obvious influence on whether or not the water point is functioning or not

### Correlation heatmap - categorical features (country and technology type) dummied:
<div>
<P ALIGN=CENTER><img src="images/heat4.png" alt="drawing" width="700"/> </P>
</div>

Some of the stronger correlations with whether or not the water point is functioning:
* Whether or not it's in India                              
* If it is a handpump                                       
* Number of households in the community                      
* If it is "improved" and the water source is protected
* Deemed to have adequate water quality
* Engineer has deemed it in "good overall health"

**Pair plots**
**t-SNE plot**

The data are not normally distributed, but **there appears to be a linear relationship with each**. Data points, however, are clustered at the low end on both axis.
To investigate further, the feature data were split into two categories - **least developed** and **most developed countries** - using the median value for each feature:

<div>
<P ALIGN=CENTER><img src="images/below5m.png" alt="drawing" width="330"/>  <img src="images/extreme_weather.png" alt="drawing" width="330"/> </P>
</div>

## Model fitting:
MVP: Identify coefficients using logistic regression and feature importances using random forests. Tune to optimal hyperparameters. Make a recommendation based on the insights and suggestions for future work.

### Train, test, and holdout datasets:
A holdout dataset (for final model testing) was split off from the full, cleaned dummied dataframe with size 2,007 rows. After the holdout set was removed, a dataset with 6,419 rows was split off for training the models, and the remaining rows were split into a test set.

### **Random Forest Classifier**
<div>
<P ALIGN=CENTER><img src="images/random_forest2.png" style="display: block; margin-left: auto; margin-right: auto;"  width="900"/></P></div>

Some lead up...
* n_estimators =
* max_depth = 
* max_features =
<div>
<P ALIGN=CENTER><img src="images/feat_imp.png" alt="drawing" width="600"/></div>

Some interpretation...

## **Logistic Regression**
Some lead up...

Optimization terminated successfully.
         Current function value: 0.071329
         Iterations 10
                                      Results: Logit
==========================================================================================
Model:              Logit                                      Pseudo R-squared: 0.757    
Dependent Variable: water_available_from_point_on_day_of_visit AIC:              955.7210 
Date:               2019-03-18 22:04                           BIC:              1091.0613
No. Observations:   6419                                       Log-Likelihood:   -457.86  
Df Model:           19                                         LL-Null:          -1881.9  
Df Residuals:       6399                                       LLR p-value:      0.0000   
Converged:          1.0000                                     Scale:            1.0000   
No. Iterations:     10.0000                                                               
------------------------------------------------------------------------------------------
                                           Coef.  Std.Err.    z     P>|z|   [0.025  0.975]
------------------------------------------------------------------------------------------
geo_level_1_Malawi                        -1.8831   0.3793  -4.9641 0.0000 -2.6266 -1.1396
geo_level_1_Rwanda                        -5.0479   1.2632  -3.9961 0.0001 -7.5237 -2.5720
geo_level_1_Uganda                        -4.1380   1.2263  -3.3743 0.0007 -6.5416 -1.7344
water_point_type_Mark Ii Handpump          0.2625   0.3639   0.7213 0.4707 -0.4508  0.9757
water_point_type_Phe 6 Handpump            0.8703   0.2960   2.9406 0.0033  0.2902  1.4504
water_point_type_Protected Deep Borehole   4.4543   1.4178   3.1418 0.0017  1.6755  7.2330
water_point_type_Protected Shallow Well    4.3923   1.2613   3.4823 0.0005  1.9202  6.8645
water_point_type_Protected Spring          6.9179   1.3439   5.1478 0.0000  4.2840  9.5518
water_point_type_other                    -1.0588   0.5741  -1.8441 0.0652 -2.1841  0.0665
spring_protection_past_lifespan            1.4209   0.7487   1.8977 0.0577 -0.0467  2.8884
taps_past_lifespan                        -2.1311   0.8038  -2.6513 0.0080 -3.7064 -0.5557
well_past_lifespan                        -0.7633   0.2598  -2.9385 0.0033 -1.2724 -0.2542
pump_past_lifespan                        -0.2229   0.2564  -0.8696 0.3845 -0.7254  0.2795
overall_state_of_water_point              -7.4780   0.6302 -11.8654 0.0000 -8.7133 -6.2428
water_point_improved                      16.8642   1.3353  12.6300 0.0000 14.2472 19.4813
source_protected                           0.1513   0.3139   0.4821 0.6297 -0.4639  0.7665
number_of_users_meets_govt_standard       -0.0503   0.2643  -0.1905 0.8489 -0.5683  0.4676
adequate_water_quality                     4.5818   0.7068   6.4822 0.0000  3.1965  5.9672
adequate_water_quantity                    0.7210   0.3911   1.8434 0.0653 -0.0456  1.4876
water_point_in_good_overall_condition     -4.7777   0.6764  -7.0635 0.0000 -6.1034 -3.4520
==========================================================================================

Some interpretations...

## **Some reflection:**
* Recommend revising the survey after thorough consultation with stakeholders of the dataset to better identify expectations from the analysis.
* More...

# Study ongoing...
