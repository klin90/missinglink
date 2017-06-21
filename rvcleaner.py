from matplotlib import pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np
import sys
reload (sys)

##########################################################################
############################## Missing Link ##############################
## Identify unfulfilled demand for restaurants by location and category ##

#######################
### import and cleaning

# import Yelp data
sys.setdefaultencoding('utf8')
df_b = pd.read_json('yelp_academic_dataset_business.json', lines = True)
df_r = pd.read_json('yelp_academic_dataset_review.json', lines = True)

# clear out anything that's permanently closed
# it's possible to leave this here in the future
df_b = df_b[df_b['is_open'] == 1]
df_b = df_b.drop(['is_open'], axis = 1)

# clear out non-restaurants
df_b = df_b[df_b['categories'].apply(str).str.contains("Restaurants")]

# replace Montreal (with accent) with Montreal (without) to merge Montreal, QC
df_b['city'] = df_b['city'].replace(u'Montr\xe9al', 'Montreal')

# drop unnecessary columns for now
# in the future it might be possible to use address/neighborhood for larger cities
df_b = df_b.drop(['address', 'neighborhood', 'postal_code', 'type'], axis = 1)

# strip latitude, longitude, hours, attributes for now too
# in the future it's usable to connect close cities and provide another "category"
df_b = df_b.drop(['latitude', 'longitude', 'hours', 'attributes'], axis = 1)

df_b.to_csv('cleaned.csv', index = False)