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

![alt-text](map)

### Tableau

![alt-text](bar) 

### Plotly

Industry Pie Data - All, Success, Failure, other factors?!

![alt-text](pie)

Histograms

## Other chart ideas

Comparison of  # Investor Buy-Ins for each investor on the show

Number of presenters 

Total amount each investor has invested

Average amount on deal per investor vs the total amount of deals taken

Evaluations, Askings, Equity 
Lowest, Highest, Average
Filters: Location, Industry, Year Presented, 

[map]: https://mapline.com/wp-content/uploads/radial-heat-map-500x333.jpg “Map Example”

[pie]: https://assets.visme.co/templates/infographics/fullsize/i_Most-Frequently-Used-Visuals-Pie-Chart_full.jpg “Pie Example”

[bar]: https://www.theinformationlab.ie/wp-content/uploads/2019/04/9-1.png “Bar Example”
