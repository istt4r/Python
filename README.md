<h1>Python</h1>

This repository is the storatge of a collection of scripts that I have used in the processing of my notion database, the archiving/storage of workouts, and related python scripts.

<b>Demo viewable at:</b> https://docs.google.com/spreadsheets/d/1ViopvzfCvcuMv_1Ps0EqNGq_oKcRmZjA-HzWX9F42ik/edit#gid=1188826729

<h2>Functions:</h2>


<b>ArchiveWorkout</b> - Handles processing the RAW export folder received from Notion. This script explores to folder tree, searching for new workouts, renaming them to a uniform format which includes the workout name and date. The output files are then staged for uploading to the google sheet using Google Sheet API's. 

<b>Standards_Exercise</b> - These scripts are related to the operation of the web scraping project. This involves navigating to [strengthlevels.com](https://strengthlevel.com/strength-standards) and then proceduraly exports the relevant exercise data into a .csv file for later comparisons against my own data.

<b>Polynomial Regression</b> - Using the data collected from my "smart" weight scale, this script served as an opportunity to utilise the Numpy library from Python. This was done to utilise polynomial regression to create a line of best fit for the data, for further statistical exploration/graphing.

<b>Notion Daily Export</b> - Script to automate requesting a database export using the Notion API. Intended for use in a pipeline via Windows Task Scheduler where daily workouts are exported/processed/uploaded/sorted by using respective other functions. Not yet concluded (WIP)

                    
