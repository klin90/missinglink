# Missing Link

Overview and Motivation
-----------------------

My motivation for this project is twofold. The first comes from personal experience, as a diner. When I visited my girlfriend in Richmond, VA, I was disappointed to find a lack of good Chinese restaurants. There were only a handful of restaurants with a large number of ratings, and even those restaurants only averaged 4 stars. Finally, when we did try the few 4 star restaurants, I was sorely disappointed. Surely, I thought, someone could come in and start a better restaurant, and capture this market!

My second motivation comes from one of my friends, who has worked with local chefs to start a variety of local restaurants. While there are many factors to success, competition is important, and I realized something that could benefit my friend would be an analysis of competition strength in his area. In particular, when it comes to different types of restaurants, is there anything missing?

Data Source
-----------

For exploratory analysis, I used the Yelp Challenge Dataset, available at the URL https://www.yelp.com/dataset_challenge. This dataset contains information about restaurants and reviews from 11 cities. Out of the collection, I only used the "business" dataset. Future analysis will use specific Yelp review data, also available as part of the Challenge Dataset.

Ultimately, for this project, we will also need data from a larger set of cities, partially available through Yelp's API.

Exploratory Data Analysis
-------------------------

**Market Segmentation**: I took every category used to describe restaurants, and ordered them by frequency. I took only categories with over 350 restaurants, and by doing so removed the rarely used categories.

**Scoring Metric**: To score each city + category combination, I took a weighted average of average review squared. The average is taken over all restaurants in the city and category, and is weighted by number of reviews received.

**Analysis by City**: I created a plot of low-scoring categories in every city.

Methodology
-----------

We can improve on the exploratory analysis and expand it in through the following:​
* Optimizing Segmentation: We can do this by clustering the attributes and categories. In particular, this will allow us to narrow our market segments for larger cities. In addition, we will be able to account for factors such as the effect of Mexican restaurants on the Tex-Mex market.
* Optimizing the Scoring Metric: This is the most challenging task, since there is little historical data available for supervised learning. However, we can still improve our basic metric through:
    * Bayesian Analysis: Create predictions for future average review for restaurants with a low number of current reviews.
    * Bins: Another approach (instead of the Bayesian approach) could be to sort restaurants into bins of high/low average rating, and high/low number of reviews received.
