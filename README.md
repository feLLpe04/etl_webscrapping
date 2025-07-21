# etl_webscrapping
Data Extraction From Website to Categorize Books Info  

STEPS, that were used in this ETL + API launcher to get insights,  Visualizations. 

ETL Project – Web Scraping with Selenium
This project demonstrates a full ETL (Extract, Transform, Load) pipeline built from scratch using web scraping. It combines tools like Selenium, Pandas, SQLite, Flask, and Dash Plotly to take data from the web and turn it into an interactive dashboard. The process is divided into five key steps:

Step 1: Extraction
Using Selenium, the project scrapes data from Books to Scrape, collecting key information about each book, such as title, price, availability, rating, and optionally, category. The scraped content is stored in a list of dictionaries to prepare it for further processing.

Step 2: Transformation
The raw scraped data is converted into a Pandas DataFrame. During this step, data cleaning and transformation are performed to standardize the values and prepare the dataset for storage.

Step 3: Load
The cleaned DataFrame is saved into a SQLite database, allowing for practical querying and persistent storage. A CSV export is also created as a backup or for optional use in tools like Power BI.

Step 4: API Creation
A Flask-based API is built to serve the data stored in SQLite. The API exposes endpoints that allow structured access to the dataset for use in applications or front-end integrations.

Step 5: Interactive Visualization Dash Ploty 
Finally, Dash Plotly is used to build an interactive dashboard. This web app runs on a local server and allows users to explore the data visually through filters and charts, e.g Rating, Price Range, Keywords even aviability directly in the browser throuhg a server.
