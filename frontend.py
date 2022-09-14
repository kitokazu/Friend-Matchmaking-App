from google.protobuf.symbol_database import Default
import mysql.connector
from numpy.lib.function_base import append
from pkg_resources import EntryPoint
import streamlit as st
import pandas as pd
import csv



class frontend():

    # @st.cache  #WE DONT HAVE TO CONNECT TO DATABASE EVERYTIME SPEEDS UP PROCESS
    def __init__(self):
        #connectorMySQL Part
        #Creates connection with google cloudmysql database
        self.connection = mysql.connector.connect(
            host = "34.136.157.91",
            user = "root",
            password = "GoRao1!"
        )
        self.cursor = self.connection.cursor()

        #  34.136.157.91 <------- DOES NOT HAVE DATA

        #  35.188.156.95 <-------- HAS DATA

        query = '''
        CREATE DATABASE IF NOT EXISTS finalproj408 character set UTF8 collate utf8_bin;
        '''
        self.cursor.execute(query)

        # Reconnect to the database just created
        self.connection = mysql.connector.connect(
            host = "34.136.157.91",
            user = "root",
            password = "GoRao1!",
            database = "finalproj408",
            charset = "utf8",
            use_unicode = True,
            autocommit=True
        )

        self.cursor = self.connection.cursor()

    #----- FRONT END TEST -----
    def webInterface(self):
        emailList = []

        st.title("FIND FRIENDS :)")
        menu = ["Admin View", "Delete User", "Use View", "Update User", "Ages Over 30", "California Demographics" , "User View", "Demographics", "Export", "Sign Up (Add profile)", "SQL"]

        choice = st.sidebar.selectbox("Menu", menu)

        # ------- ADMIN VIEW ----------
        if choice == "Admin View":
            st.subheader("Admin View")
            with st.form(key='password'):
                password = st.text_input("Enter Password")
                password_submit = st.form_submit_button("Submit")

                #IF THE PASSWORD IS RIGHT
                if password_submit and password == "123":
                    st.success("Correct Password")
                    option = st.selectbox("Select Filter",("See All",""))
                    st.write(option)

                    st.write("KEY COLUMN INDEX:\n0 = userID\n1 = age\n2 = income\n3 = username\n4 = passcode\n5 = profileID\n6 = surveyID")

                    if option == "See All":
                        query = "SELECT * FROM person"
                        query_results = self.sql_executor(self.cursor, query)

                        #Formatting the results as a table using pandas
                        query_df = pd.DataFrame(query_results)

                        st.dataframe(query_df)
                    if option == "Ages Over 30":
                        st.write("test")

                elif password_submit and password_submit != "123":
                    st.error("Incorrect Password")

        elif choice == "Use View":
            st.subheader("Use View (Displays Usernames and Passwords)")

            with st.form(key='view'):
                view_submit = st.form_submit_button("Submit")

                if view_submit:


                    query = '''
                    CREATE VIEW userView AS
                    SELECT userName, passcode
                    FROM person;
                    '''

                    query_results = self.sql_executor(self.cursor, query)

                    query2 = '''
                    SELECT * FROM userView
                    '''
                    query2_results = self.sql_executor(self.cursor, query2)

                    #Formatting the results as a table using pandas
                    query_df = pd.DataFrame(query2_results)

                    st.dataframe(query_df)

        elif choice == "Demographics":
            st.subheader("Adding Demographics")

            col1, col2, col3 = st.columns(3)

            with col1:

                with st.form(key='demographics'):
                    ethnicity = st.text_input("Enter the ethnicity ")
                    orientation = st.text_input("Enter the orientation ")
                    income = st.text_input("Enter the income ")
                    location = st.text_input("What state / country ")
                    job = st.text_input("What job ")
                    education = st.text_input ("Highest education (high school, undergrad, graduated) ")
                    religion = st.text_input ("Whats the religion ")

                    view_submit = st.form_submit_button("Submit")

                    if view_submit:

                        self.connection.start_transaction()

                        query = "SELECT * FROM demographics WHERE ethnicity = '" + ethnicity + \
                                "'AND orientation = '" + orientation + \
                                "'AND income = '" + income + \
                                "'AND location = '" + location + \
                                "'AND job = '" + job + \
                                "'AND education = '" + education + \
                                "'AND religion = '" + religion + \
                                "';"
                        self.cursor.execute(query)
                        demorec = self.cursor.fetchall()

                        df = pd.DataFrame.from_records(demorec,
                                                    columns = ["demoID",
                                                                "ethnicity",
                                                                "orientation",
                                                                "income",
                                                                "location",
                                                                "job",
                                                                "education",
                                                                "religion"])

            with col2:
                st.subheader("ROLLBACK")
                with st.form(key='rollback'):
                    view_submit = st.form_submit_button("Submit")

                    if view_submit:
                        try:
                            self.connection.rollback()
                            st.success("Successful Rollback")
                        
                        except:
                            st.error("Unsuccesful Rollback")

            with col3:
                st.subheader("Commit")
                with st.form(key="commit"):
                    commit_submit = st.form_submit_button("Submit")

                    if commit_submit:
                        try:
                            val = (ethnicity,orientation,int(income),location,job,education,religion)
                            query = ("INSERT INTO demographics VALUES(default,"
                                    "'" + ethnicity +
                                    "','" +  orientation +
                                    "'," +  income +
                                    ",'" +  location +
                                    "','" +  job +
                                    "','" +  education +
                                    "','" +  religion + "');")
                            st.write(query)

                            try:
                                self.cursor.execute(query)
                                #connection.commit()
                            except self.connection.Error as e:
                                st.write(" * SQL QURY: {0}".format(query))
                                st.write(" * SQL RES: {0}".format(e) )
                            else:
                                st.write ("Duplicate record")
                            # connection.rollback()
                            st.write(self.cursor.fetchall())
                            # st.write(self.cursor.rowcount)
                            st.write(query)

                        except:
                            st.error("Duplicate Record")


                        

        elif choice == "California Demographics":
            st.subheader("California Demographics")
            with st.form(key='california'):
                california_submit = st.form_submit_button("Submit")

                if california_submit:
                    query = '''
                    SELECT ethnicity, count(per.userID) as Num_of_users_in_CA
                    from person per
                    inner join profile p on p.profileID = per.profileID
                    inner join demographics d on p.demographicsID = d.demographicsID
                    where d.location = "california"
                    group by ethnicity;
                    '''
                    query_results = self.sql_executor(self.cursor, query)

                    #Formatting the results as a table using pandas
                    query_df = pd.DataFrame(query_results)

                    st.dataframe(query_df)

        

        elif choice == "Ages Over 30":

            st.subheader("Select Ages Over 30")

            with st.form(key='ages'):
                ages_submit = st.form_submit_button("Submit")
            
                if ages_submit:
                    query = '''
                    SELECT COUNT(*) allCount, (
                        SELECT COUNT(*)
                        FROM person
                        WHERE age > 30
                        ) AS above30Count
                    FROM person;
                    '''
                    query_results = self.sql_executor(self.cursor, query)

                    #Formatting the results as a table using pandas
                    query_df = pd.DataFrame(query_results)

                    agesOver30 = query_df[1][0]

                    st.write(f"There are {agesOver30} people over 30")





        elif choice == "Delete User":
            st.subheader("Delete user by ID")

            with st.form(key='delete'):
                delete = st.text_input("Enter ID to delete")
                delete_submit = st.form_submit_button("Submit")
            
            if delete_submit:

                intdelete = int(delete)
                query = f'''
                DELETE FROM person WHERE userID = {intdelete};
                '''

                query_results = self.sql_executor(self.cursor, query)

                #Formatting the results as a table using pandas
                query_df = pd.DataFrame(query_results)

                st.success("Deletion Complete")


        elif choice == "Update User":
            st.subheader("Update User")

            with st.form(key='delete'):
                update = st.text_input("Enter ID to update")
                # delete = int(delete)
                update_submit = st.form_submit_button("Submit")


        elif choice == "Export":
            st.subheader("Export")
            query = "SELECT * FROM person"
            query_results = self.sql_executor(self.cursor, query)

            #Formatting the results as a table using pandas
            query_df = pd.DataFrame(query_results)

            with st.form(key='export'):
                # delete = int(delete)
                export_submit = st.form_submit_button("Submit")

            if export_submit:
                query_df.to_csv("export.csv")
                st.write("Export Successful!")


        #------ VIEW POINT FROM THE USER --------
        elif choice == "User View":
            st.subheader("Find Friends")
            
            option = st.selectbox("Select Filter",(
                "Age","Language","Height","Sex","Relationship","Ethnicity","Religion","Social"))


            # SELECTING AGE
            if option == "Age":
                with st.form(key='age_pref'):
                    height_pref_max = st.slider("Age Preference MIN", min_value=18, max_value=70, value=20, step=1)
                    heigh_pref_min = st.slider("Age Preference MAX", min_value=18, max_value=70, value=25, step=1)
                    submit_code = st.form_submit_button("Search")

                
                if submit_code:
                    if heigh_pref_min < height_pref_max:
                        st.error("Min age is greater than max age")
                    else:
                        query = f'''
                        SELECT username, age FROM person
                        WHERE Age BETWEEN {height_pref_max} AND {heigh_pref_min}
                        ORDER BY RAND()
                        LIMIT 3;
                        '''
                        ages = self.sql_executor(self.cursor, query)
                        
                        query_df = pd.DataFrame(ages)

                        st.success(f"Showing Top 3 Matches with Ages Between {height_pref_max} and {heigh_pref_min}")

                        st.dataframe(query_df)

            
            # SELECTING LANGUAGE
            if option == "Language":
                with st.form(key="langauge_pref"):
                    lang_pref = st.radio("Choose Language Preference", ["English", "Spanish", "French", "Other"])
                    submit_code = st.form_submit_button("Search")
    

                if submit_code:               
                    query = f'''
                    SELECT per.userID, per.userName
                    from person per
                    inner join profile p on p.profileID = per.profileID
                    inner join traits t on p.traitID = t.traitID
                    inner join languages L on t.languageID = L.languageID
                    where L.{lang_pref.lower()} = 1
                    ORDER BY RAND()
                    LIMIT 3;
                    '''
                    ages = self.sql_executor(self.cursor, query)
                    query_df = pd.DataFrame(ages)
            
                    st.success(f"Showing Top 3 Matches That Speak {lang_pref}")
                    st.dataframe(query_df)


            # SELECTING HEIGHT
            if option == "Height":
                with st.form(key="height_pref"):
                    height_pref_min = st.slider("Height Preference MIN (in inches)", min_value=50, max_value=80, value=60, step=1)
                    height_pref_max = st.slider("Height Preference MAX (in inches)", min_value=50, max_value=80, value=70, step=1)
                    submit_code = st.form_submit_button("Search")

                if submit_code: 
                    if height_pref_max < height_pref_min:
                        st.error("Min age is greater than max age")
                    else:
                        query = f'''
                        SELECT per.userID, per.userName, t.height
                        FROM person per
                        INNER JOIN profile p ON p.profileID = per.profileID
                        INNER JOIN traits t ON p.traitID = t.traitID
                        WHERE t.height BETWEEN {height_pref_min} AND {height_pref_max}
                        ORDER BY RAND()
                        LIMIT 3;
                        '''
                        ages = self.sql_executor(self.cursor, query)
                        
                        query_df = pd.DataFrame(ages)

                        st.success(f"Showing Top 3 Matches with Ages Between {height_pref_max} and {height_pref_min}")

                        st.dataframe(query_df)              



            # RELATIONSHIP
            if option == "Relationship":
                with st.form(key="relationship_pref"):
                    relation_pref = st.radio("Choose Relationship Preference", ["Single", "Taken", "Other"])
                    submit_code = st.form_submit_button("Search")
            
                if submit_code:
                    query = f'''
                    SELECT per.userID, per.userName
                    from person per
                    inner join profile p on p.profileID = per.profileID
                    inner join traits t on p.traitID = t.traitID
                    where t.status = "{relation_pref.lower()}"
                    ORDER BY RAND()
                    LIMIT 3;
                    '''

                    st.success(f"Showing Top 3 Matches That Are {relation_pref}")
                    ages = self.sql_executor(self.cursor, query)
                    query_df = pd.DataFrame(ages)
            
                    st.dataframe(query_df)
                    
            
            # ETHNICITY
            if option == "Ethnicity":
                with st.form(key="ethnicity_pref"):
                    ethnicity_pref = st.radio("Choose Ethnicity Preference", ["White", "Middle Eastern", "Black", "Asian", "Indian","Hispanic", "Other"])
                    submit_code = st.form_submit_button("Search")


                if submit_code:
                    query = f'''
                    SELECT per.userID, per.userName
                    from person per
                    inner join profile p on p.profileID = per.profileID
                    inner join demographics d on p.demographicsID = d.demographicsID
                    where d.ethnicity = "{ethnicity_pref.lower()}"
                    ORDER BY RAND()
                    LIMIT 3;
                    '''

                    st.success(f"Showing Top 3 Matches That Are {ethnicity_pref}")
                    ages = self.sql_executor(self.cursor, query)
                    query_df = pd.DataFrame(ages)
            
                    st.dataframe(query_df)

            # SEX
            if option == "Sex":
                with st.form(key="sex_pref"):
                    sex_pref = st.radio("Choose Sex Preference", ["Male", "Female"])
                    submit_code = st.form_submit_button("Search")

                if sex_pref == "Male": sex_pref = "m"
                else: sex_pref = "f"

                if submit_code:
                    query = f'''
                    SELECT per.userID, per.userName
                    from person per
                    inner join profile p on p.profileID = per.profileID
                    inner join traits t on p.traitID = t.traitID
                    where t.sex = "{sex_pref}"
                    ORDER BY RAND()
                    LIMIT 3;
                    '''

                    st.success(f"Showing Top 3 Matches That Are {sex_pref}")
                    sexes = self.sql_executor(self.cursor, query)
                        
                    query_df = pd.DataFrame(sexes)

                    st.dataframe(query_df)   

            # RELIGION
            if option == "Religion":
                with st.form(key="religion_pref"):
                    religion_pref = st.radio("Choose Religion Preference", ["Christianity", "Hindu", "Muslim", "Other"])
                    submit_code = st.form_submit_button("Search")
            
                if submit_code:
                    query = f'''
                    SELECT per.userID, per.userName
                    from person per
                    inner join profile p on p.profileID = per.profileID
                    inner join demographics d on p.demographicsID = d.demographicsID
                    where d.religion = "{religion_pref.lower()}"
                    ORDER BY RAND()
                    LIMIT 3;
                    '''
                
                    religions = self.sql_executor(self.cursor, query)  
                    query_df = pd.DataFrame(religions)
                    st.dataframe(query_df)  
                    st.success(f"Showing Top 3 Matches That Are {religion_pref}")

            if option == "Social":
                col5,col6 = st.columns(2)

                with st.form(key="social_pref"):
                    with col5:
                        diet = st.radio("Dietary Restrictions?: ", ["Yes","No"])
                        offspring = st.radio("Do you want offspring?: ", ["Yes","No"])
                        drugs = st.radio("Do you do drugs?: ", ["Yes", "No"])
                    with col6:
                        drinks = st.radio("Do you drink?: ", ["Yes", "No"])
                        pets = st.radio("Do you want pets?: ", ["Yes", "No"])
                    submit_code = st.form_submit_button("Search")
            
                if submit_code:

                    diet = 1 if diet == "Yes" else 0
                    drinks = 1 if drinks == "Yes" else 0
                    drugs = 1 if drugs == "Yes" else 0
                    offspring = 1 if offspring == "Yes" else 0
                    pets = 1 if pets == "Yes" else 0


                    query = f'''
                    SELECT per.userID, per.userName
                    FROM person per
                    INNER JOIN profile p on p.profileID = per.profileID
                    INNER JOIN preferences pref on p.preferenceID = pref.preferenceID
                    WHERE pref.diet = {diet}
                    AND pref.drinks =  {drinks}
                    AND pref.drugs = {drugs}
                    AND pref.offspring = {offspring}
                    AND pref.pets= {pets}
                    ORDER BY RAND()
                    LIMIT 3;
                    '''
                
                    religions = self.sql_executor(self.cursor, query)  
                    query_df = pd.DataFrame(religions)
                    st.dataframe(query_df)  
                    st.success(f"Showing Top 3 Matches")

                

        #----------- SQL COMMANDS ------------
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

                    # Results
                    query_results = self.sql_executor(self.cursor, raw_code)
                    with st.expander("Results"):
                        st.write(query_results)

                    #Formatting the results as a table using pandas
                    with st.expander("Table Format"):
                        query_df = pd.DataFrame(query_results)
                        st.dataframe(query_df)


        #-------- SIGN UP ADD PROFILE ---------
        elif choice == "Sign Up (Add profile)":

            #TO keep track of all the info
            personInfo = []
            traits = []
            demographics = []
            survey = []
            preferences = []

            st.subheader("Sign Up")

            col1,col2 = st.columns(2)
            st.markdown("#")
            st.write("Additional Info")
            col3, col4 = st.columns(2)
            st.markdown("#")
            st.write("Survey Info")
            col5, col6 = st.columns(2)

            bigcol1,bigcol2 = st.columns(2)
            
            
            with st.form(key='login_form'):
                with col1:
                    name = st.text_input("Name: ")
                    # email = st.text_input("Email: ")
                    username = st.text_input("Username: ")
                    password = st.text_input("Password: ")

                with col2:
                    age = st.text_input("Age: ")
                    location = st.text_input("Location: ")
                    sex = st.text_input("Sex: ")
                
                with col3:
                    income = st.text_input("Income: ", '0')
                    job = st.text_input("Job: ")
                    orientation = st.text_input("Orientation: ")
                    body_type = st.selectbox("Body Type",("Skinny", "Athletic", "Fit", "Thick","Prefer not to answer"))
                    height = st.number_input("Height in Inches: ", step=1, value=52)

                with col4:
                    ethnicity = st.text_input("Ethnicity: ")
                    education = st.text_input("Education: ")
                    religion = st.text_input("Religion: ")
                    lang_pref = st.multiselect("Spoken Languages",["English", "French", "Spanish", "Other"])
                    status = st.selectbox("Status",("Single", "Taken","Complicated"))
                
                with col5:
                    diet = st.radio("Dietary Restrictions?: ", ["Yes","No"])
                    offspring = st.radio("Do you want offspring?: ", ["Yes","No"])
                    drugs = st.radio("Do you do drugs?: ", ["Yes", "No"])
                with col6:
                    drinks = st.radio("Do you drink?: ", ["Yes", "No"])
                    pets = st.radio("Do you want pets?: ", ["Yes", "No"])


                submit_code = st.form_submit_button("Submit")
                rollback = st.form_submit_button("Rollback")

                #CHECK IF THE EMAIL DOES NOT EXIST

            if rollback:
                st.success("Rollback Succesful")

            #Adding the basic info and asks for income
            if submit_code: 

                #GETS THE HIGHEST USER ID AND ADDS 1
                query = "SELECT @id:=MAX(userID) + 1 FROM person"
                userID = self.sql_executor(self.cursor, query)

                # THIS IS ADDING THE USER SECTION
                personInfo.append(userID[0][0])
                personInfo.append(age) 
                personInfo.append(income)
                # personInfo.append(name)
                personInfo.append(username)
                personInfo.append(password)

                #TAKES THE LAST PROFILE ID AND ADDS TO IT
                query = "SELECT @id:=MAX(profileID) + 1 FROM profile"
                profileID = self.sql_executor(self.cursor, query)

                personInfo.append(profileID[0][0])

                #TAKES THE LAST survey ID AND ADDS TO IT
                #CHANGE IT FOR LATER
                query = "SELECT @id:=MAX(surveyID) + 1 FROM survey"
                surveyID = self.sql_executor(self.cursor, query)

                personInfo.append(surveyID[0][0])
                st.write(personInfo)

                # GETS THE TRAITS
                query = "SELECT @id:=MAX(traitID) + 1 FROM traits"
                traitsID = self.sql_executor(self.cursor, query)
                traits.append(traitsID[0][0])

                # GETS THE TRAITS
                demoID = "SELECT @id:=MAX(demographicsID) + 1 FROM demographics"
                demoID = self.sql_executor(self.cursor, query)
                demographics.append(demoID[0][0])



                # ------- LANGUAGE --------
                eng, span, fren, oth = 0, 0, 0, 0

                if "English" in lang_pref: eng = 1
                if "French" in lang_pref: fren = 1
                if "Spanish" in lang_pref: span = 1
                
                if "Other" in lang_pref:
                    eng, span, fren = 0
                    oth = 1
            

                # GRABS THE LANGAUGE ID FROM THE LANGUAGES TABLE
                query = f'''
                SELECT languageID FROM languages 
                WHERE english = {eng}
                AND spanish =  {span}
                AND french = {fren}
                AND other = {oth}
                '''

                langID = self.sql_executor(self.cursor, query)

                #IF THE LANGUAGE ID FOR SOME REASON IS NULL
                if not langID: 
                    langID = 0
                else:
                    langID = langID[0][0]


                # -----  BODY TYPE ------- 
                if body_type == "Skinny":
                    body_type = 0
                elif body_type == "Athletic":
                    body_type == 1
                elif body_type == "Fit":
                    body_type = 2
                elif body_type == "Thick":
                    body_type = 3
                else:
                    body_type = 4
                
                # ----  TRAITS ---- 
                
                traits.append(sex)
                traits.append(height)
                traits.append(body_type)
                traits.append(status)
                traits.append(langID) # <----- GET THE FOREIGN KEY
                st.write(traits)

                # --- DEMOGRAPHICS ---
                demographics.append(ethnicity)
                demographics.append(orientation)

                #CONVERTING INCOME TO INT
                income = str(income)
                income = income.strip(" ")
                income = income.strip(",")
                income = int(income)

                demographics.append(income)
                demographics.append(location)
                demographics.append(job)
                demographics.append(education)
                demographics.append(religion)
                st.write(demographics)

                #Ternary Operator for SURVEYS
                diet = 1 if diet == "Yes" else 0
                drinks = 1 if drinks == "Yes" else 0
                drugs = 1 if drugs == "Yes" else 0
                offspring = 1 if offspring == "Yes" else 0
                pets = 1 if pets == "Yes" else 0

                query = f'''
                SELECT preferenceID FROM preferences
                WHERE diet = {diet}
                AND drinks =  {drinks}
                AND drugs = {drugs}
                AND offspring = {offspring}
                AND pets= {pets}
                '''

                prefID = self.sql_executor(self.cursor, query)

                #IF THE PREF ID FOR SOME REASON IS NULL
                if not prefID: 
                    prefID = 0
                else:
                    prefID = prefID[0][0]

                # --- SURVEY ----
                survey.append(surveyID[0][0])
                survey.append(traitsID[0][0])
                survey.append(prefID)
                survey.append(demoID[0][0])
                

                st.write(survey)


                #insert person
                # try:
                #     query = "INSERT INTO person VALUES(%s,%s,%s,%s,%s,%s,%s)"
                #     result = self.cursor.executemany(query, tuple(personInfo))
                #     self.connection.commit()
                # except:
                #     st.error("User already exists")


                self.connection.start_transaction()
                query1 = "INSERT INTO traits VALUES(%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(query1, tuple(traits))
                # self.connection.commit()

                # self.connection.start_transaction()
                query2 = "INSERT INTO demographics VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(query2, tuple(demographics))
                # self.connection.commit()

                # self.connection.start_transaction()
                query3 = "INSERT INTO survey VALUES(%s,%s,%s,%s)"
                self.cursor.execute(query3, tuple(survey))
                # self.connection.commit()
                # query = "INSERT INTO traits VALUES(%s,%s,%s,%s,%s,%s)"
                # result = self.cursor.execute(query, tuple(traits))
                # self.connection.commit()

                
                profile = []
                profile.append(profileID[0][0])
                profile.append(traitsID[0][0])
                profile.append(prefID)
                profile.append(demoID[0][0])

                # self.connection.start_transaction()
                query4 = "INSERT INTO profile VALUES(%s,%s,%s,%s)"
                self.cursor.execute(query4, tuple(profile))
                # self.connection.commit()
                
                # self.connection.start_transaction()
                query5 = "INSERT INTO person VALUES(%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(query5, tuple(personInfo))
                self.connection.commit()


            

                #insert profile

                #insert demographics

                st.write(personInfo)
                st.write(profileID)

                #insert traits
                st.write(tuple(personInfo))
                st.success("Person Created")
            
            if rollback:
                try:
                    self.connection.rollback()
                    st.success("Successful Rollback")
                
                except:
                    st.error("Unsuccesful Rollback")


        else:
            st.subheader("About")
        

    # ---- ABLE TO RUN THE QUERIES ON THE WEB ----
    def sql_executor(self, cursor, raw_code):
        try:
            cursor.execute(raw_code)
            data = cursor.fetchall()
            return data
        except:
            st.write("Invalid Query")


f = frontend()

f.webInterface()
