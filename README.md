# ECE-143-Team-6
ECE 143: Team 6 Group Project  
Subject: Subtle Asian Dating

# Authors
* Brian Aguirre
* Simon Fong
* Justine Lee
* Mulin Yang

# Presentation
You can view our presentation [here](https://docs.google.com/presentation/d/e/2PACX-1vS6ga2yJyG4DLHy3NqM45bMSaWShGB8QL8UWTp_AIHuywmi9bT1lAvE9VftSEF6QdJfw8IVJLOL5IXH/pub?start=false&loop=false&delayms=3000&slide=id.g5aa6e7467b_1_0):

# File Structure
```
server/                     # Web Server Code
    static/                 # Static Files
        css/
            stylesheet.css
        html/
            index.html
            quiz_men.html
        images/
            favicon.ico
        js/
            index.js
            quiz_men_1.js
    server.py               # Web Server
data_fetching/
    download_mongo_db.py    # Downloads all the responses from the database.
analysis/
    data_analysis.ipynb     # Main Notebook with all graphs.
    plotting.py             # Useful functions for plotting.
    utils.py                # Tools for loading and filtering data.
LICENSE
README.md
```

# How to Run Our Code
Instructions how to run our code.

## Web Server
### Note
Requires a file called `db_key` that contains credentials to the database. Server will not work without it.

### Commands
Run this while in the `server` directory.
```
python server.py --port 5050
```
Now you can visit http://localhost:5050 and see the quiz. Or you can just visit http://subtleasiandating.org/ to see it up and running.

## Data Analysis
### Start Up Jupyter Notebook
While in the root of the repository start the Jupyter Notebook by running:
```
jupyter notebook
```
This should send you into your browser with the Jupyter site running.

### Running the Notebook
Open up the `data_analysis.ipynb` notebook. Click on `Kernel` on the top. Then choose `Restart & Run All`. This should run all our data analysis code and generate the graphs.

![running-notebook](running-notebook.gif)

# Third Party Modules Used
All modules and libraries we used.

## Python
### Web Server
* flask
* pymongo

### Data Analysis
* bson
* numpy
* pandas
* matplotlib
* xlsxwriter
* plotly
* pyviz
* holoviews
* bokeh


## HTML/CSS/Javascript
* jQuery
* Bootstrap

## Other
* AWS
* Nginx
* MongoDB
* mLab
