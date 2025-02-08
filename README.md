# Youtube Data harvesting and warehousing
Problem Statement:

YouTube Data Harvesting and Warehousing is a project that aims to allow users to access and analyze data from multiple YouTube channels. The project utilizes SQLITE3 and Streamlit to create a user-friendly application that allows users to retrieve, store, and query YouTube channel and video data.

Software Requirements :
1.	Microsoft Visual Studio
2.  Youtube API Key
3.  SQLITE3

Installations Required in Microsoft Visual Studio Through Terminal :
PIP INSTALL :
1.	Streamlit
2.	PANDAS
3.	isodate

DOMAIN : Social Media

Approach:

Set up a Streamlit app: Streamlit is a great choice for building data visualization and analysis tools quickly and easily. You can use Streamlit to create a simple UI where users can enter a YouTube channel ID, view the channel details, and select channels to migrate to the data warehouse.

Connect to the YouTube API: You'll need to use the YouTube API to retrieve channel and video data. You can use the Google API client library for Python to make requests to the API.

Store and Clean data : Once you retrieve the data from the YouTube API, store it in a suitable format for temporary storage before migrating to the data warehouse. You can use pandas DataFrames or other in-memory data structures.

Migrate data to a SQLITE3 data warehouse: After you've collected data for multiple channels, you can migrate it to a SQL data warehouse. You can use a SQLITE3 database such as MySQL or PostgreSQL for this.

Query the SQLITE3 data warehouse: You can use SQLITE3 queries to join the tables in the SQLITE3 data warehouse and retrieve data for specific channels based on user input. You can use a Python SQLITE3 library such as SQLAlchemy to interact with the SQLITE3 database.

Display data in the Streamlit app: Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.

Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing the data SQLITE3 as a warehouse, querying the data warehouse with SQLITE3, and displaying the data in the Streamlit app.

