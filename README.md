# Friend Matchmaking Application
Created an application where users can create an account and find friends based on criteria. Can search for friends based on interest, hobbies, ethnicity, location, etc. Created a fullstack application. Used streamlit (python) for the frontend.

* [Link to Report](https://docs.google.com/document/d/1nOsXLhz1_0SeUuwkMbP8YDQoOhkzi-wV/edit?usp=sharing&ouid=116018696439002773469&rtpof=true&sd=true)
* [Link to Video Demo](https://drive.google.com/file/d/1Lx3dypD48-ZYdNYcGc1286R4l7BDLGmO/view?usp=sharing)

Setup:
======
Please review section Setup Environment in the Report to ensure you have Streamlit set up
Download library 'streamlit' on your local machine
Make sure you do not have the pipenv in the same env as teh main_final.py otehrwise you will get bytearry errors due to
a difference in python versions.

Process the raw data and populate database:
===========================================
python3 main_final.py

Start the front end ui:
=======================
streamlit run frontend.py


SQL Connection Details
======================
Public IP: 34.136.157.91
user: root
passcode: GoRao1!
sql database: finalproj408


Note the rawdata.csv has approx 60,000 records in there. To speed up the demo it is recommened to select 200 records
when running the main file, however there is no restrictions in the program to use all 60,000 records. It should be
noted that entering a large number of records to be inserted can tav=ke a large amount of time and it may appear the
program is hanging.
