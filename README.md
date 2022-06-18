# Apartment Prices is Gdynia Estimator: Project Overview

Main goal for this project is to get and prepare data from scratch. Find and build best possible prediction model. 


**Python version:** 3.10.2.  
**Packages:** selenium, pandas, numpy, sklearn, matplotlib, seaborn.  
**Data resource:** https://otodom.pl


# Web scraping
To get data about apartments in Gdynia from otodom.pl I prepared script in 
Python using selenium package to get following information:
- title
- address
- price
- price per square meter
- area
- number of rooms
- floor
- outdoor facilities (balcony, backyard, terrace)
- parking (parking spot or garage available or not)
- market 
- build year
- type of building
- elevator (yes / no)
- heating type 

During scraping the data I could clean data a little bit more, but i deided to do almost all cleaning in Pandas.


# Data cleaning
After scraping the data, I needed to prepare it for EDA and modeling process. 
I made following changes:
- values without meaning (like "ask for price") replaced with NaN
- numeric data:
  - price and price per square meter was stripped from any symbols
  - prices in EUR was replaced with prices in PLN (based on area and price per square meters in pln)
  - area, rooms changes to floats
  - apartment floor was transform into two column with apartment floor and max number of floors in building.
  - new columns for information about outdoor facilities  
  - new column with building age 
- new columns about district and street from address column. Column with street was created for apartments without data about district. It's possible to get distrct based on street manually (It will not be done in this project)
- dropped records without price and price per square meter


# EDA
Checked data and plot some graphs. Additional cleaning during eda was nedded. 
Might be usefull:
- 1753 observations
- 75% houses has price below 1 000 000 pln. (1363 observations)


# Model building
For price predictions I decided to use mean absolute error as metric, becuase it's easy to interpret. I tried few models, including: Linear Regression, Lasso, Radnom Forest and Gradient Boost. Also I tried neural network with sklearn MLPRegressor, but the results wasn't nescessery good. I Decided to go forward with Gradient Boost Regressore and fine-tune it with grid search. 

I tried some diferrent grid search params, and I decided to choose second model because it's generalize better. 

	     train	|  test
mae	   123664 |  165291
r2	   0.8  	|  0.63
rmse	 308041 |  377374

Mean Absolute Error equal to 165 291 pln - it's not great, not terrible. Most of apartments in my data got pricetag below 1 000 000 pln, so I checked MAE for those in my test set, and got MAE = 81 784 pln. 


# TO DO
- [x] Create script to scrap information about apartment prices from otodom.pl using python and selenium.  
- [x] data cleaning.
- [x] eda + feature engineering
- [x] prepare pipelines for regression models.  
- [x] try few models.   
- [x] select and fine-tune most promising model using GridSearchCV.   
- [ ] switch to cookiecutter folder structure
- [ ] move all file pth to single config file
- [ ] productionizate model with Flash API
- [ ] make this documentation much better.   
  
   
