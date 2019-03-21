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
The CSV dataset has 10,034 rows and 52 columns. Two columns have significant missing values and will be removed from the analysis. The feature to be predicted – is the water point functioning or not? – is imbalanced, and train-test splits were made with stratification to maintain the proportionality of the original datset. After data cleaning, the resulting dataframe has 10,031 rows and 16 columns. Dummy columns (one-hot) were then created for two categorical features, resulting in a dataframe with 24 columns for use in the analysis.
<div>
<P ALIGN=CENTER><img src="images/imbalance.png" alt="drawing" width="430"/>  <img src="images/broken_by_country.png" alt="drawing" width="400"/> </P>
</div>

**The target has imbalanced classes.** When the data is broken out by country, it becomes evident that the distribution of broken water points varies significantly between them:
* India - About 2% of water points (129/5,991) broken
* Malawi - About 9% of water points (153/1730) broken
* Rwanda - About 12% of water points (91/743) broken
* Uganda - About 31% of water points (489/1,567) broken

India accounts for about 60% of the water points in the dataset, and it also has the lowest incidence of broken water points. Therefore, 'India' is assigned as the baseline "dummy" variable in a one-hot encoded (for categorical features) dataframe to be fed into the models.

### Proportion of water points by type of technology - overall and by country:
<div>
<P ALIGN=CENTER><img src="images/function_by_tech.png" alt="drawing" width="550"/>  </P>
</div>

The most common technology in the dataset is the "Phe 6 Handpump," and the technology is also more or less tied for having the lowest proportion of being broken. Therefore, it is assigned as the baseline "dummy" variable in a one-hot encoded (for categorical features) dataframe to be fed into the models.

<div>
<P ALIGN=CENTER><img src="images/function_by_tech_india.png" alt="drawing" width="375"/><img src="images/function_by_tech_malawi.png" alt="drawing" width="375"/>  </P>
</div>
<div>
<P ALIGN=CENTER><img src="images/function_by_tech_rwanda.png" alt="drawing" width="375"/><img src="images/function_by_tech_uganda.png" alt="drawing" width="375"/>  </P>
</div>

There's notable variation by type at the country level, but less so in India. The technologies with the highest rate of being broken fall into the "other" category, which are a number of different technologies, each occuring less than 150 times in the dataset. There is enough variation among the 7 main technology types to suggest it could be a useful predictor.

### Age since original construction plotted against whether the water point is broken or functioning
<div>
<P ALIGN=CENTER><img src="images/dist_by_age.png" alt="drawing" width="550"/> </P>
</div>

The older water points in the dataset are functioning, and broken water points are by and large newer - the opposite of what would be expected.

### Correlation heatmap - categorical features (country and technology type) dummied:
<div>
<P ALIGN=CENTER><img src="images/ cool_heat_annotated.png" alt="drawing" width="700"/> </P>
</div>

Some of the stronger correlations with whether or not the water point is functioning:
* Whether or not it's in India (positive) or in Uganda (negative)                           
* If it is a handpump (positive)
* If it is one of the less common technologies (negative)
* Number of households in the community (positive)
* If it is "improved" and the water source is protected (positive)
* Deemed to have adequate water quality (positive)

### Pair plot:
<div>
<P ALIGN=CENTER><img src="images/pop_pairplot.png" alt="drawing" width="350"/><img src="images/age_pairplot.png" alt="drawing" width="350"/> </P>
</div>
Plotting the target against the continuous variable "num_families_in_community," there seems to be a higher proportion of functioning water points in communities with higher populations, and a higher proportion of broken water points in lower population communities. This, perhaps, could be an issue of prirotiy and funding allocated for maintainance. Similarly, older water points 

## Model fitting:
MVP: Identify coefficients using logistic regression and feature importances using random forests. Tune to optimal hyperparameters. Make a recommendation based on the insights and suggestions for future work.

### Train, test, and holdout datasets:
A holdout dataset (for final model testing) was split off from the full (stratified), cleaned dummied dataframe with 2,007 rows. After the holdout set was removed, a dataset with 6,419 rows was split off for training the models, and the remaining rows were split into a test set (80-20 split). The training and test sets were used to fit and score the models, applying K-fold validation with stratification to deal with imbalanced classes.

### Random Forest Classifier:
<div>
<P ALIGN=CENTER><img src="images/random_forest2.png" style="display: block; margin-left: auto; margin-right: auto;"  width="900"/></P></div>

The training dataset was fit to a random forest classifier model - a supervised ensemble machine learning method - to determine the most important features for predicting the target: water points working or not. The model was run with various n_estimators to identify the best precision score - false negative (the model predicts a water point isn't working when it actually is) is preferred to false positive (a broken water point could then get overlooked):
* Precision with 1000 estimators: 0.982
* Precision with 100 estimators: 0.982
* Precision with 50 estimators: 0.982
* Precision with 25 estimators: 0.982
* Precision with 10 estimators: 0.983

**Confusion matrix for model with n_estimators=10:**<br />
True negative | False positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.07&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.02<br />
--------------|---------------<br />
False negative| True positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.01&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.91<br />
--------------|---------------<br />

**Confusion matrix for model with n_estimators=100:**<br />
True negative | False positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.07&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.02<br />
--------------|---------------<br />
False negative| True positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.01&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.91<br />
--------------|---------------<br />

**Precision is TOO GOOD and the confusion matrix is TOO CONSISTENT.**

One feature (overall_state_of_water-point) was causing data leakage. The feature labels are scores from 1-3, with the worst score (1) equating to "does not function" - essentially the same as the target feature. The model was run again with that feature removed, and two additional methods were used to deal with imbalanced classes: **class_weight='balanced'** and **SMOTE**

**With class_weight='balanced':**
* Precision with 1000 estimators: 0.954
* Precision with 100 estimators: 0.954
* Precision with 50 estimators: 0.954
* Precision with 25 estimators: 0.954
* Precision with 10 estimators: 0.956
* Precision with 2 estimators: 0.96

**Confusion matrix for model with n_estimators=10, 25, 50, 100, 1000:**<br />
True negative | False positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.04&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.04<br />
--------------|---------------<br />
False negative| True positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.03&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.88<br />
--------------|---------------<br />

**With SMOTE:**
* Precision with 1000 estimators: 0.578
* Precision with 100 estimators: 0.578
* Precision with 50 estimators: 0.579
* Precision with 25 estimators: 0.578
* Precision with 10 estimators: 0.58
* Precision with 2 estimators: 0.583

**Confusion matrix for model with n_estimators=10, 25, 50, 100, 1000:**<br />
True negative | False positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.48&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.02<br />
--------------|---------------<br />
False negative| True positive<br />
--------------|---------------<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.02&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.48<br />
--------------|---------------<br />





**Revised feature importances:**
<div>
<P ALIGN=CENTER><img src="images/feat_importances_2.png" alt="drawing" width="800"/></div>




## Logistic Regression:
<div>
<P ALIGN=CENTER><img src="images/logistic_regression.jpg" style="display: block; margin-left: auto; margin-right: auto;"  width="900"/></P></div>
<br />

### Study ongoing...

<br />
<br />
<br />

## **Some reflection:**
* Recommend revising the survey after thorough consultation with stakeholders of the dataset to better identify expectations from the analysis.
* Collect data related to governance, funding, and maintainence for water points so that the models can analyze the contributions of those dynamics on the likelihood of functioning/ breaking
* Run the models on country disaggregated datasets

### Study ongoing...
