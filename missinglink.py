from matplotlib import pyplot as plt
from collections import Counter
from ast import literal_eval
import pandas as pd
import numpy as np

# Missing Link
# Identify unfulfilled demand for restaurants by location and category

# import and cleaning
df = pd.read_csv('cleaned.csv')
df['categories'] = df['categories'].apply(literal_eval)

# American cities only
df = df[df['state'].isin(['PA', 'NC', 'IL', 'AZ', 'NV', 'WI', 'OH'])]

# add metropolitan data
# this dataset has one city per state: don't need a lookup table for American cities
df = df.assign(metro=df['state'].map({'PA': 'Pittsburgh',
                                      'NC': 'Charlotte',
                                      'IL': 'Urbana-Champaign',
                                      'AZ': 'Phoenix',
                                      'NV': 'Las Vegas',
                                      'WI': 'Madison',
                                      'OH': 'Cleveland'}))

# scrub out airports, they don't really compete with other restaurants
df = df[~df['name'].str.contains('Airport')]

# shorten 'Event Planning & Services' string
# merge 'Arts and Entertainment' and 'Entertainment'

# failed attempt to use number of categories for each restaurant in order to find fake restaurants
# for now, we'll assume there aren't many fakes - my system weights places with many reviews anyway
# df['cat_length'] = df['categories'].apply(len)
# df = df[df['cat_length'] < 10]


##########################################################################
# categories


def categorize(df, n):
    # creates a categories dataframe from input dataframe, taking categories with over n restaurants
    cats = pd.DataFrame.from_dict(Counter(df['categories'].sum()), orient='index') \
        .reset_index().rename(columns={'index': 'category', 0: 'restaurant_count'})

    # delete categories 'Restaurants' and 'Food'
    cats = cats[(cats['category'] != 'Restaurants') & (cats['category'] != 'Food')]

    # a more complete method would be to cluster categories
    # as proof of concept, we'll just take the top ones for now
    return cats[cats['restaurant_count'] >= n]

# review analysis


def cat_score(df, category, plot):
    # searches input city dataframe for restaurants in given category, scores each restaurant, scores the category,
    # generates a plot of scores if plot = True
    cat_search = df[df['categories'].apply(lambda x: category in x)]
    cat_search = cat_search.assign(score=score(cat_search))

    if plot:
        cat_search['score'].plot(kind='box')

    # category score is RMS square-stars, weighted by number of ratings
    return np.sqrt(cat_search['score'].sum())

# city analysis


def analyze_metro(m):
    city_data = df[df['metro'] == m]
    city_cats = categorize(city_data, 0)

    # merge this categorical data with our original analysis
    city_cats = pd.merge(city_cats, df_cats, how='right', on=['category']).fillna(0)

    # find the ratio of restaurant_count in given metro versus the dataset, normalize by max
    city_cats = city_cats.assign(ratio=city_cats['restaurant_count_x'].div(city_cats['restaurant_count_y'])
                                 * df.size / city_data.size)

    # return scored categories in the metro
    return city_cats.assign(score=city_cats['category'].apply(lambda x: cat_score(city_data, x, False))) \
        .set_index('category')


##########################################################################
# scoring


def score(df):
    # creates a score series based on input category-city dataframe
    # current score metric: square of average rating * percent share of ratings
    return (df['stars'] ** 2) * df['review_count'] / df['review_count'].sum()


##########################################################################
# plots


def plot_score(df_score, city):
    # creates a bar chart of category scores in given city from input scores dataframe
    plt.figure()
    df_sorted = df_score.loc[city].sort_values()
    score_title = 'Competition Strength for Restaurant Categories in ' + city
    score_plot = df_sorted.plot(legend=False, title=score_title, style='o-', xticks=np.arange(len(scores.columns)),
                                rot=90)
    score_plot.set(xlabel = 'Restaurant Category', ylabel = 'Competition Strength')
    score_plot.set_xticklabels(df_sorted.index)
    plt.tight_layout()
    return score_plot


def category_plot(cat, city):
    city_data = df[df['metro'] == city]
    cat_list = city_data[city_data['categories'].apply(lambda x: cat in x)]
    cat_title = 'Aggregated Reviews for ' + cat + ' Restaurants in ' + city
    cat_plot = cat_list.plot(x=['stars'], y=['review_count'], style='o', xlim=(0, 5), legend=False, title=cat_title)
    cat_plot.set(xlabel='Stars Given', ylabel='Number of Reviews')
    return cat_plot


##########################################################################


# take categories with 350+ restaurants
df_cats = categorize(df, 350)

scores = pd.DataFrame(index=df['metro'].unique(), columns=df_cats['category'])

for metro in scores.index:
    metro_scores = analyze_metro(metro)['score']
    scores.loc[metro] = metro_scores

# normalize so each city has the same average category score
# adjust for behavior in each city
scores = scores.sub(scores.mean(axis=1), axis=0) + scores.mean().mean()

# normalize by mean, divide by standard deviation - for each category
# for each category, compare score to the nationwide average
scores_std = (scores - scores.mean()) / scores.std()

# score plots of all metros
plot_score(scores_std, 'Phoenix')
plot_score(scores_std, 'Cleveland')
plot_score(scores_std, 'Charlotte')
plot_score(scores_std, 'Pittsburgh')
plot_score(scores_std, 'Las Vegas')
plot_score(scores_std, 'Madison')
plot_score(scores_std, 'Urbana-Champaign')

# selected categories
category_plot('Event Planning & Services', 'Madison')
category_plot('Bakeries', 'Urbana-Champaign')
category_plot('Coffee & Tea', 'Urbana-Champaign')
category_plot('Diners', 'Urbana-Champaign')
category_plot('Sandwiches', 'Urbana-Champaign')
category_plot('Seafood', 'Urbana-Champaign')
category_plot('Steakhouses', 'Urbana-Champaign')
category_plot('Pubs', 'Las Vegas')
category_plot('Arts & Entertainment', 'Las Vegas')
