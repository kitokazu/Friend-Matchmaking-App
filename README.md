# Friend Matchmaking Application
Created an application where users can create an account and find friends based on criteria. Can search for friends based on interest, hobbies, ethnicity, location, etc. Created a fullstack application. Used streamlit (python) for the frontend.

## Setup:
Please review section Setup Environment in the Report to ensure you have Streamlit set up
Download library 'streamlit' on your local machine
Make sure you do not have the pipenv in the same env as teh main_final.py otehrwise you will get bytearry errors due to
a difference in python versions.

* Process the raw data and populate database:
* python3 main_final.py
* Start the front end ui:
* streamlit run frontend.py

Note the rawdata.csv has approx 60,000 records in there. To speed up the demo it is recommened to select 200 records
when running the main file, however there is no restrictions in the program to use all 60,000 records. It should be
noted that entering a large number of records to be inserted can tav=ke a large amount of time and it may appear the
program is hanging.