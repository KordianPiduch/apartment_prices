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



# TO DO
- [x] Create script to scrap information about apartment prices from otodom.pl using python and selenium.  
- [x] data cleaning.
- [ ] eda + feature engineering
- [ ] prepare pipelines for regression models.  
- [ ] try few models (multilinear regressor with and without regularization, Random Forest Regressor).   
- [ ] select and fine-tune most promising models to reach the best model (using GridSearchCV).   
- [ ] make this documentation much better.   
  
   
