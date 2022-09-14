#Main
import mysql.connector
#import streamlit as st
import pandas as pd

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


# Reconnect to the database just created
# We do this to connect to the database, not just the ip address
# We set the use_unicode to true as some python environments return bytearrays not strs, this should fix that
connection = mysql.connector.connect(
    #host = "35.188.156.95",
    #host = "34.136.157.91",
    #host = "104.155.181.7",
    host = sql_host,
    user = "root",
    password = "GoRao1!",
    database = sql_database,
    charset = "utf8",
    use_unicode = True,
    autocommit=False
)

cursor = connection.cursor()

# Set Up dataframes
input_df = pd.DataFrame()


def get_choice(lst):
    choice = input("Enter choice number: ")
    while choice.isdigit() == False:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ")

    while int(choice) not in lst:
        print("Incorrect option. Try again")
        choice = input("Enter choice number: ")
    return int(choice)

def addDemographics():
    ethnicity = input("Enter the ethnicity ")
    orientation = input("Enter the orientation ")
    income = input("Enter the income ")
    location = input("What state / country ")
    job = input("What job ")
    education = input ("Highest education (high school, undergrad, graduated) ")
    religion = input ("Whats the religion ")

    connection.start_transaction()

    query = "SELECT * FROM demographics WHERE ethnicity = '" + ethnicity + \
            "'AND orientation = '" + orientation + \
            "'AND income = '" + income + \
            "'AND location = '" + location + \
            "'AND job = '" + job + \
            "'AND education = '" + education + \
            "'AND religion = '" + religion + \
            "';"
    cursor.execute(query)
    demorec = cursor.fetchall()

    df = pd.DataFrame.from_records(demorec,
                                   columns = ["demoID",
                                              "ethnicity",
                                              "orientation",
                                              "income",
                                              "location",
                                              "job",
                                              "education",
                                              "religion"])

    if (len(demorec) == 0):
        print("OK will add it")

        val = (ethnicity,orientation,int(income),location,job,education,religion)
        query = ("INSERT INTO demographics VALUES(default,"
                 "'" + ethnicity +
                 "','" +  orientation +
                 "'," +  income +
                 ",'" +  location +
                 "','" +  job +
                 "','" +  education +
                 "','" +  religion + "');")
        print(query)

        try:
            cursor.execute(query)
            #connection.commit()
        except connection.Error as e:
            print(" * SQL QURY: {0}".format(query))
            print(" * SQL RES: {0}".format(e) )
        else:
            print ("Duplicate record")
           # connection.rollback()
        print(cursor.fetchall())
        print(cursor.rowcount)
        print(query)
        confirm = input("rollback this record to db ? 1= yes")
        if  confirm == "1":
            print("do a rollback")
            connection.rollback()
        else:
            print("committing teh change")
            connection.commit()

    else:
        print(demorec)
        print("Already have a record with an ID of " + str(demorec[0][0]))

def getDemographics():
    choice = input("What id do you want to see: ")
    query = "SELECT * FROM demographics WHERE demographicsID = '" + str(choice) +"'"
    cursor.execute(query)
    demorec = cursor.fetchall()

    df = pd.DataFrame.from_records(demorec,
                                   columns = ["demoID",
                                              "ethnicity",
                                              "orientation",
                                              "income",
                                              "location",
                                              "job",
                                              "education",
                                              "religion"])

    print(df.to_string(index=False))

def getUserInput():
    print("reading in the values from the input.csv ")

    #input_df = pd.read_csv("input.csv")
    input_df = pd.read_csv("input.csv", nrows=1)
    print(input_df.to_string())





# main
print ("CONNECTED TO " + sql_database + " on instance " + sql_host)
print ("This program will allow you to test the main db.")
print ("\n\n")

print(" Select one of the following:")
print(" 1 - Add a demographics")
print(" 2 - View demographics")
print(" 3 - delete demographics")
print(" 4 - commit change")
print(" 5 - rollback changes")
print(" 6 - print report to csv")
print(" 7 - test input from user")
print()
print(" 0 - exit")
lst = [0,1,2,3,4,5,6,7]


selectedChoice = 9999
while selectedChoice != 0:
    selectedChoice = get_choice(lst)
    if selectedChoice == 1:
        addDemographics()

    elif selectedChoice == 2:
        getDemographics()
    elif selectedChoice == 6:
        myquery = input("Enter the sql statement: ")
        populator.exportReportCSV("jeevansreport.csv",myquery,connection,pd)
    elif selectedChoice == 7:
        getUserInput()
        addTestRecord()

