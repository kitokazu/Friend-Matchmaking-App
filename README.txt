#README

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