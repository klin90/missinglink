from matplotlib import pyplot as plt
from collections import Counter
import pandas as pd
import numpy as np

# Missing Link
# Identify unfulfilled demand for restaurants by location and category

# import and cleaning

# import Yelp data
df = pd.read_json('yelp_academic_dataset_business.json', lines=True)

# clear out anything that's permanently closed
# it's possible to leave this here in the future
df = df[df['is_open'] == 1]
df = df.drop(['is_open'], axis=1)

# clear out non-restaurants
df = df[df['categories'].apply(str).str.contains("Restaurants")]

# replace Montreal (with accent) with Montreal (without) to merge Montreal, QC
df['city'] = df['city'].replace(u'Montr\xe9al', 'Montreal')

# drop unnecessary columns for now
# in the future it might be possible to use address/neighborhood for larger cities
df = df.drop(['address', 'neighborhood', 'postal_code', 'type'], axis=1)

# strip latitude, longitude, hours, attributes for now too
# in the future it's usable to connect close cities and provide another "category"
df = df.drop(['latitude', 'longitude', 'hours', 'attributes'], axis=1)

df.to_csv('cleaned.csv', index=False)
