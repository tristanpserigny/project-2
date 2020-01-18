# Project Three - Project Two Continued!


!["Deal Status" Confusion Matrix](https://github.com/tristanpserigny/project-2/blob/master/Images/model_DealStatus%20(2).PNG)





!["Deal Shark" Confusion Matrix](https://github.com/tristanpserigny/project-2/blob/master/Images/model_DealShark%20(3).PNG)







## Project Proposal

Using the data from the previous project we intend to build a feature that allows a user to input a product description (or pitch) an initial valuation, an asking amount, and the stake in the business they are willing to give up. We will use a machine learning model based on previous successes and failures to determine whether the user inputted description will be successful and which shark is likely to invest.

## Data Cleaning

Our first step is to update our dataset. For our previous project we used Shark Tank data that was based only on the first six seasons. We have recently found an updated version of that same dataset with an additional two seasons. Once that the new dataset has been updated and formatted to our liking, we will re-save the csv file as our new dataset. 

The next step is to clean the data in preparation for machine learning use. We will need to remove stopwords and extra text in the “Descriptions” column cells that aren’t needed. 

## Data Collection and Storage

The new data set will be converted to an AWS document database, instead of a sqlite database. A document database is designed to store semistructured data as JSON-like documents. These databases help developers build and update applications quickly.

## Machine Learning Model

We will use Python NLTK to pre-process the text in the pitches, remove special characters and stop words, and any other identified words that don’t contribute. Then we’ll use the Term Frequency Inverse Document Frequency to convert the text to numeric values. The text data will be combined with the numerical data (valuation, the asking amount, and the stake offered) and modeled with The Naive Bayes Model to compute the probability of a deal.

A second model will be trained against the shark who makes the deal, to determine if a proposed pitch is accepted, which shark will make the deal. We may try other models given available time.

![Model Example](https://res.cloudinary.com/dyd911kmh/image/upload/f_auto,q_auto:best/v1543836883/image_2_rrxvol.png)

## Model Training

Initially, we will experiment and tune the model using a train/test split with scikit-learn, however the model used on the web application will be trained using the full range of data we retrieved from kaggle and other sources.  Our relatively small data set may lead to some issues when it comes to using the trained model, but we will try and see what happens.


## Model Evaluation

We will create a confusion matrix from the model, and then determine a few metrics from it including classification accuracy, classification error, sensitivity, specificity, false positive rate, and precision.

![Eval Example](https://www.dataschool.io/content/images/2015/01/confusion_matrix2.png)

## Model Demonstration

We will be using a web application with a dedicated page to work with the feature. It will have a text area for users to title their product, enter a description, and assign values.  When they click the “submit” button, the page will display some data as to whether the product is likely to be successful on the show, and which sharks are likely to pick the product or not. We would also like to display confidence values if possible.

---

# Project Two - Shark Tank 

## Project Proposal:

Over the years many startup companies have found the initial investments they needed to scale with the help of the “sharks,” who are ready to invest their money for a small stake in the company. The data gives a variety of information related to pitches that have been presented over the first 6 seasons of the shark tank.  The data will allow us to render multiple visualizations that analyze how certain aspects of the pitches can lead to their success or failure. This will be a dashboard page with multiple charts that update from the same data.

## Kaggle Source Data:

### CSV1 columns: 
Deal, description, episode, category, entrepreneurs, location, website, askedFor, exchangeForStake, valuation, season, shark1, shark2, shark3, shark4, shark5, title, episode-season, Multiple Entrepreneurs

### CSV2 columns:
Season_Epi_code, Pitched_Business_Identifier, Pitched_Business_Desc, Deal_Status, Deal_Shark


## Data Cleaning and Storage:

We will need to push our collected csv data through python to clean and organize it. After creating DataFrames from the multiple csv data files, we will merge DataFrames on the pitch title names to make one DataFrame. The DataFrame will be exported as a new csv file and then stored in a SQLite database for use within a Flask application.

## Flask/Bootstrap/CSS:

## Visualizations:

### D3

Shark Data - shows where individual sharks stand in relation to a variety of different factors

### Leaflet

Map that displays the locations of the company/product operating headquarters/origins. This map will include tabs for each company and display the company name and info based on user mouse interaction. 
Heat Map Pitch Value Data - what kind of pitches are the most successful, large asks? Small asks? Large stake offers? Small stake offers? 

![Map Example](https://mapline.com/wp-content/uploads/radial-heat-map-500x333.jpg)

### Tableau

![Bar Example](https://www.theinformationlab.ie/wp-content/uploads/2019/04/9-1.png) 

### Plotly

Industry Pie Data - All, Success, Failure, other factors?!

![Pie Example](https://assets.visme.co/templates/infographics/fullsize/i_Most-Frequently-Used-Visuals-Pie-Chart_full.jpg)

Histograms

## Other chart ideas

Comparison of  # Investor Buy-Ins for each investor on the show

Number of presenters 

Total amount each investor has invested

Average amount on deal per investor vs the total amount of deals taken

Evaluations, Askings, Equity 
Lowest, Highest, Average
Filters: Location, Industry, Year Presented, 
