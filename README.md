# ACNH-Clustering

#### Context
I heard that there were four patterns for weekly turnip prices (large spike, small spike, decreasing and random) 
in Animal Crossing New Horizons and that the current price pattern affected the following week's price pattern. 
Given that there were already tools that took the current week's price patterns into account when predicting turnip prices, 
I wanted to cluster turnip price data from players. 

#### Methods:
- dynamic time warping
- hierarchical clustering
- PCA
- t-SNE

#### Goals:
- preprocess and store weekly turnip price data
- cluster and visualize the data

#### Results:
I manually dealt with changes in data formatting while creating functions to handle missing and invalid values.
The data was re-arranged into four columns (user_id, island_id, price, datetime_observed) so that missing values would not be 
stored within the database while also allowing the data to be restored to the original format which contained columns for each weekday.


All of the data was used for exploratory data analysis while only complete trends containing data from Monday to Saturday were used for clustering.
Hierarchical clustering grouped all of the decreasing trends together while appearing to group most of the large spike trends together.
It did not manage to cluster small spike and random trends together.

#### Other Considerations
Although I managed to visualize the clusters by using PCA and t-SNE to reduce the data's dimensionality, I hope to develop a deeper understanding of techniques for reducing dimensionality.

Given how there is reverse-engineered code regarding turnip prices, further investigation could be made into training a classification model using generated data.

#### References
*Animal Crossing New Horizons* [Game]. (2020). Kyoto: Nintendo.

Maddox Knight. (2020). Maddox Knight's Turnip Mafia (Public Edition). [Data]. Retrieved from https://docs.google.com/spreadsheets/d/1hMmewPJvXw-tmabvccC0nWJdN7zw3aQIQzN3EQ9is6g/edit#gid=370566781
