#Main
import mysql.connector
#import streamlit as st
#import pandas as pd

from helper import helper
from populator import populator
from db_operations import db_operations

#sql_host = "35.188.156.95"
#sql_host = "34.136.157.91"
#sql_host = "104.155.181.7"
sql_host = "34.136.157.91"

sql_database = "finalproj408"
#sql_database = "finalproj408test
#sql_database = "test408"

#connectorMySQL Part
#Creates connection with google cloudmysql via the ip address
connection = mysql.connector.connect(
    host = sql_host,
    user = "root",
    password = "GoRao1!"
)

cursor = connection.cursor()

#Creates database if it doesn't exist
query = "CREATE DATABASE IF NOT EXISTS " + sql_database + " character set UTF8 collate utf8_bin;"
cursor.execute(query)

# Reconnect to the database just created
# We do this to connect to the database, not just the ip address
# We set the use_unicode to true as some python environments return bytearrays not strs, this should fix that
connection = mysql.connector.connect(
    host = sql_host,
    user = "root",
    password = "GoRao1!",
    database = sql_database,
    charset = "utf8",
    use_unicode = True
)

cursor = connection.cursor()

def dropTables():
    # #Drop all the old tables to get rid of old data.
    cursor.execute("DROP TABLE IF EXISTS person")
    print("person Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS profile")
    print("profile Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS survey")
    print("survey Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS traits")
    print("traits Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS demographics")
    print("demographics Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS preferences")
    print("preferences Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS languages")
    print("languages Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS staging")
    print("staging Table dropped... ")
    cursor.execute("DROP TABLE IF EXISTS matches")
    print("match Table dropped... ")

def createStaging():
    # Going to create a staging table to hopefully speed things up
    print("Creating staging table")
    query = '''
    CREATE TABLE IF NOT EXISTS staging(
    stagingID  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    userRole VARCHAR(30),
    userName VARCHAR(30),
    passcode INTEGER,
    age INTEGER,
    status  VARCHAR(30),
    sex VARCHAR(10),
    orientation VARCHAR(20),
    body_type INT,
    diet BOOLEAN,
    drinks BOOLEAN,
    drugs BOOLEAN,
    education VARCHAR(100),
    ethnicity VARCHAR(200),
    height INT,
    income INT,
    job VARCHAR(100),
    location VARCHAR(200),
    offspring BOOLEAN,
    pets BOOLEAN,
    religion VARCHAR(100),
    sign VARCHAR(100),
    smokes BOOLEAN,
    english BOOLEAN,
    spanish BOOLEAN,
    french BOOLEAN,
    other BOOLEAN,
    friendMatch INT,
    userID INT
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createLanguages():
    #Create the languages table
    print("Creating languages table")
    query = '''
    CREATE TABLE IF NOT EXISTS languages(
    languageID INTEGER NOT NULL PRIMARY KEY,
    english BOOLEAN,
    spanish BOOLEAN,
    french BOOLEAN,
    other BOOLEAN
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createTraits():
    print("Creating traits table")
    query = '''
    CREATE TABLE IF NOT EXISTS traits(
    traitID  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sex VARCHAR(10),
    height INT,
    body_type INT,
    status VARCHAR(50),
    languageID INTEGER,
    CONSTRAINT FK_languageID FOREIGN KEY (languageID) REFERENCES languages(languageID)
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createPreferences():
    # Creates preferences table
    print("Creating preferences table")
    query = '''
    CREATE TABLE IF NOT EXISTS preferences(
    preferenceID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    diet BOOLEAN,
    drinks BOOLEAN,
    drugs BOOLEAN,
    offspring BOOLEAN,
    pets INT
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createDemographics():
    # Creates demographics table
    print("Creating demographics table")
    query = '''
    CREATE TABLE IF NOT EXISTS demographics(
    demographicsID INTEGER NOT NULL AUTO_INCREMENT  PRIMARY KEY,
    ethnicity VARCHAR(200),
    orientation VARCHAR(20),
    income INT,
    location VARCHAR(200),
    job  VARCHAR(100),
    education  VARCHAR(100),
    religion  VARCHAR(100)
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createProfile():
    # Creates profile table
    print("Creating profile table")
    query = '''
    CREATE TABLE IF NOT EXISTS profile(
    profileID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    traitID INTEGER,
    preferenceID INTEGER,
    demographicsID INTEGER,
    CONSTRAINT FK_traitID FOREIGN KEY (traitID) REFERENCES traits(traitID),
    CONSTRAINT FK_preferenceID FOREIGN KEY (preferenceID) REFERENCES preferences(preferenceID),
    CONSTRAINT FK_demographicsID FOREIGN KEY (demographicsID) REFERENCES demographics(demographicsID)
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createSurvey():
    # Creates survey table
    print("Creating survey table")
    query = '''
    CREATE TABLE IF NOT EXISTS survey(
    surveyID INTEGER NOT NULL PRIMARY KEY,
    traitID INTEGER,
    preferenceID INTEGER,
    demographicsID INTEGER,
    CONSTRAINT FK_surveyTraitID FOREIGN KEY (traitID) REFERENCES traits(traitID),
    CONSTRAINT FK_surveyPreferenceID FOREIGN KEY (preferenceID) REFERENCES preferences(preferenceID),
    CONSTRAINT FK_surveyDemographicsID FOREIGN KEY (demographicsID) REFERENCES demographics(demographicsID)
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createPerson():
    # Create the person table
    # Note: We need to see if the username can have a unique constraint added
    print("Creating person table")
    query = '''
    CREATE TABLE IF NOT EXISTS person(
    userID INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    age INT,
    income INT,
    userName VARCHAR(30),
    passcode INT,
    profileID INTEGER,
    surveyID INTEGER,
    CONSTRAINT FK_profileID FOREIGN KEY (profileID) REFERENCES profile(profileID),
    CONSTRAINT FK_surveyID FOREIGN KEY (surveyID) REFERENCES survey(surveyID)
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createMatch():
    # Create the match table
    print("Creating matches table")
    query = '''
    CREATE TABLE IF NOT EXISTS matches(
    mID INTEGER NOT NULL PRIMARY KEY,
    userName VARCHAR(30),
    friendMatch VARCHAR(30)
    );
    '''
    result = cursor.execute(query)
    connection.commit()

def createTables():
    #creates the tables. Note the order of drops matter due to foregin keys
    createStaging()
    createLanguages()
    createTraits()
    createPreferences()
    createDemographics()
    createProfile()
    createSurvey()
    createPerson()
    createMatch()

def populateStaging():
    # Comment this out for now as we have the data loaded
    print("Updating the staging table")
    cleaned_staging = helper.data_cleaner("staging.csv")
    populator.insert_list(cleaned_staging, cursor, connection, 8)

def populateLanguages():
    print("Updating languages table")

    # Do a simple insert since the languages table is fixed we dont need the csv.
    # This is also faster than reading the csv in(just by a little bit
    languagelist = [(0,0,0,0,1),
                    (1,0,0,0,1),
                    (2,0,0,1,0),
                    (3,0,0,1,1),
                    (4,0,1,0,0),
                    (5,0,1,0,1),
                    (6,0,1,1,0),
                    (7,0,1,1,1),
                    (8,1,0,0,0),
                    (9,1,0,0,1),
                    (10,1,0,1,0),
                    (11,1,0,1,1),
                    (12,1,1,0,0),
                    (13,1,1,0,1),
                    (14,1,1,1,0),
                    (15,1,1,1,1)]


    cursor = connection.cursor()
    query = '''
        INSERT INTO languages (languageID, english, spanish, french, other) VALUES (%s,%s,%s,%s,%s);
        '''
    result = cursor.executemany(query, languagelist)
    result = connection.commit()

def populateTraits():
    print("Updating traits table")
    query = '''
        INSERT INTO traits (sex,height,body_type,status, languageID)
        SELECT sex, height, body_type, status, languageID
        FROM staging
        JOIN languages
        ON staging.english = languages.english
            AND staging.french = languages.french
            AND staging.spanish = languages.spanish
            AND staging.other = languages.other;
        '''
    result = cursor.execute(query)
    connection.commit()

def populatePreferences():
    # # Start with loading in to the preferences Table - already loaded this staic table so dont do
    # print("Updating preferences table")
    # query = '''
    #     INSERT INTO preferences (diet, drinks, drugs, offspring, pets)
    #     SELECT DISTINCT diet, drinks, drugs, offspring, pets
    #     FROM staging
    #     '''
    # result = cursor.execute(query)
    # connection.commit()
    print("Updating preferences table")
    # Do a simple insert since the preferences table is fixed we dont need the csv.
    # This is also faster than reading the csv in(just by a little bit)
    preferenceslist = [(48,1,1,1,1,1),
                    (47,1,1,1,1,0),
                    (46,1,1,1,0,1),
                    (45,1,1,1,0,0),
                    (44,1,1,1,1,1),
                    (43,1,1,1,1,0),
                    (41,1,1,1,0,0),
                    (40,1,1,0,1,1),
                    (39,1,1,0,1,0),
                    (38,1,1,0,0,1),
                    (37,1,1,0,0,0),
                    (36,1,0,1,1,1),
                    (35,1,0,1,1,0),
                    (34,1,0,1,0,1),
                    (33,1,0,1,0,0),
                    (32,1,0,1,1,1),
                    (31,1,0,1,1,0),
                    (30,1,0,1,0,1),
                    (29,1,0,1,0,0),
                    (28,1,0,0,1,1),
                    (27,1,0,0,1,0),
                    (26,1,0,0,0,1),
                    (25,1,0,0,0,0),
                    (24,0,1,1,1,1),
                    (23,0,1,1,1,0),
                    (22,0,1,1,0,1),
                    (21,0,1,1,0,0),
                    (20,0,1,1,1,1),
                    (19,0,1,1,1,0),
                    (18,0,1,1,0,1),
                    (17,0,1,1,0,0),
                    (16,0,1,0,1,1),
                    (15,0,1,0,1,0),
                    (14,0,1,0,0,1),
                    (13,0,1,0,0,0),
                    (12,0,0,1,1,1),
                    (11,0,0,1,1,0),
                    (10,0,0,1,0,1),
                    (9,0,0,1,0,0),
                    (8,0,0,1,1,1),
                    (7,0,0,1,1,0),
                    (6,0,0,1,0,1),
                    (5,0,0,1,0,0),
                    (4,0,0,0,1,1),
                    (3,0,0,0,1,0),
                    (2,0,0,0,0,1),
                    (1,0,0,0,0,0)]

    cursor = connection.cursor()
    query = "INSERT INTO preferences VALUES(%s, %s, %s, %s, %s, %s)"

    result = cursor.executemany(query, preferenceslist)
    result = connection.commit()

def populateDemographics():
    # #Then populate the demographics Table
    print("Updating demographics table")
    query = '''
        INSERT INTO demographics (ethnicity, orientation, income, location, job, education, religion)
        SELECT DISTINCT ethnicity, orientation, income, location, job, education, religion
        FROM staging
        '''
    result = cursor.execute(query)
    connection.commit()

def popProfile(staginglist):
    queryList = []
    for x in staginglist:
        langList = [x[23], x[24], x[25], x[26]]
        langID = populator.langAssociator(langList, cursor)
        langtuple = langID
        stagingtuple = x + langID
        # print(stagingtuple)
        traittuple = populator.find_trait_id(stagingtuple, cursor)
        # print("trait tuple")
        # print(traittuple)
        preferencetuple= traittuple + populator.find_preference_id(stagingtuple, cursor)
        # print("preference tuple")
        # print(preferencetuple)
        demotuple = preferencetuple + populator.find_demographics_id(stagingtuple, cursor)
        queryList.append(demotuple)
    populator.insert_list(queryList, cursor, connection, 5)

def populateProfile():
    # Get all the records from staging that will help us populate profile
    print("Updating Profile table")
    cursor = connection.cursor()
    query = '''
        SELECT *
        FROM  staging
        '''
    result = cursor.execute(query)
    stagingRecords = cursor.fetchall()

    popProfile(stagingRecords)

def populateSurvey():
    print("Updating survey table")

    # For now we will make the survey ID table the same as profile
    # However in the future we may have additional cloumns added and
    # keeping the survey table seperate from profile table
    # will allow for easier changes in the future.
    query = '''
    INSERT INTO survey (traitID, demographicsID, preferenceID, surveyID)
    SELECT  traitID, demographicsID, preferenceID, profileID
    FROM profile;
    '''
    result = cursor.execute(query)
    connection.commit()

def popPerson(staginglist):
    #*****Name does not exist in staging******
    profileList = []
    personList = []
    queryList = []
    emptylist = []
    for x in staginglist:
        langList = [x[23], x[24], x[25], x[26]]
        langID = populator.langAssociator(langList, cursor)

        stagingtuple = x + langID
        traittuple = populator.find_trait_id(stagingtuple, cursor)
        preferencetuple= traittuple + populator.find_preference_id(stagingtuple, cursor)
        demotuple = preferencetuple + populator.find_demographics_id(stagingtuple, cursor)
        profileId = populator.find_profile_id(demotuple, cursor)
        findtuple = demotuple + profileId
        surveyId = populator.find_survey_id(findtuple, cursor)

        persontuple = (x[4], x[15], x[2], x[3], profileId[0], surveyId[0])
        queryList.append(persontuple)
    populator.insert_list(queryList, cursor, connection, 7)

def populatePerson():
    print("Updating person table")
    cursor = connection.cursor()
    query = '''
        SELECT *
        FROM  staging
        '''
    result = cursor.execute(query)
    stagingRecords = cursor.fetchall()
    popPerson(stagingRecords)

def populateMatch():
    # #Then populate the match Table
    print("Updating match table")
    query = '''
        INSERT INTO match (userName, friendMatch)
        SELECT userID, friendMatch
        FROM staging
        '''
    result = cursor.execute(query)
    connection.commit()

def populateTables():
    # This function populates the tables
    populateStaging()
    populateLanguages()
    populateTraits()
    populatePreferences()
    populateDemographics()
    populateProfile()
    populateSurvey()
    populatePerson()
    #populateMatch()

def processData():
    dropTables()
    createTables()
    populateTables()

# main
exec(open("process_initial_data.py").read())

print ("This will populate the data after creating the database " + sql_database + " on instance " + sql_host)
print ("This assumes that the process_raw_data was run and you have the various csv files generated.")
print ("\n\n")
# Process the data, create and populate tables
processData()


# Final output
print("\n\nAll tables populated.")

 #----- FRONT END TEST -----
def webInterface():

    st.title("FIND FRIENDS :)")
    menu = ["Search for Friends", "Sign Up (Add profile)", "SQL"]


    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Search for Friends":
        st.subheader("Find Friends")

        option = st.selectbox("Gender?",("Male","Female"))
        print(option)

        if option == "People Under 30":
            query = "SELECT * FROM person WHERE age < 30"

            query_results = sql_executor(query)

            #Formatting the results as a table using pandas
            query_df = pd.DataFrame(query_results)
            st.dataframe(query_df)


    elif choice == "SQL":
        col1,col2 = st.columns(2)
         #The text box where we can enter SQl queries
        with col1:
            with st.form(key='mysql_query_form'):
                raw_code = st.text_area("SQL Code Here")
                submit_code = st.form_submit_button("Execute")

        # Results Layout Right next to the text box
        with col2:
            if submit_code:
                st.info("Query Submitted")
                st.code(raw_code)

                # #Results
                query_results = sql_executor(raw_code)
                with st.expander("Results"):
                    st.write(query_results)

                #Formatting the results as a table using pandas
                with st.expander("Table Format"):
                    query_df = pd.DataFrame(query_results)
                    st.dataframe(query_df)


    elif choice == "Sign Up (Add profile)":
        st.subheader("Sign Up")
        with st.form(key='login_form'):
            name = st.text_input("Name: ")
            email = st.text_input("Email: ")
            password = st.text_input("Password: ")
            submit_code = st.form_submit_button("Submit")

        if submit_code:
            st.info("Person Created")

    else:
        st.subheader("About")

# ---- ABLE TO RUN THE QUERIES ON THE WEB ----
def sql_executor(raw_code):
    try:
        cursor.execute(raw_code)
        data = cursor.fetchall()
        return data
    except:
        print("Invalid Query")
