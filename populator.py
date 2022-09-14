#module contains functions to populate our lists with data read from another
#variable.
import csv
import mysql
from helper import helper
from db_operations import db_operations
from mysql.connector.errors import Error

class populator():

    #Method pops tuples from list and calls ofther load function to select
    #specified elements from the tuple into new 2D array and returns this array
    @staticmethod
    def load(data, indexList):
        emptyList = []
        for x in range(0, len(data)-1, 1):
            if (len(data) % 10000 == 0):
                print ("processed another 10,000 records at count ")
                print (len(data))
            tuple = data.pop()
            element =populator.loadTuple(tuple, indexList)
            #Checks to see if the element is a duplicate
            try:
                emptyList.index(element)

            except ValueError:
                emptyList.append(element)
        return(emptyList)



    #Method takes tuples and the specific elements we want from the tuple and
    #returns a list of filtered elemets from the given tuple
    @staticmethod
    def loadTuple(tuple, indexList):
        element = []
        i=0
        while(i< len(tuple)):
            for j in tuple:
                if i in indexList:
                    element.append(j)
                i += 1
        return (element)

    @staticmethod
    def export(filename, data):
        file = open(filename, "w+", newline = "")
        with file:
            write = csv.writer(file)
            write.writerows(data)


    # function inserts data into table if it is empty
    @staticmethod
    def insert_list(list, cursor, connection, number):
        if number == 1:
            query = "INSERT INTO languages VALUES(%s, %s, %s, %s, %s)"
        elif number == 2:
            # For traits we need to set up the INSERT with the languageID
            query = "INSERT INTO traits(relationship_status,sex,body_type,height,languageID) VALUES(%s, %s, %s, %s,%s)"
        elif number == 3:
            query = "INSERT INTO preferences VALUES(%s, %s, %s, %s, %s, %s)"
        elif number == 4:
            query = "INSERT INTO demographics VALUES(%s, %s, %s, %s, %s, %s, %s)"
        elif number == 5:
            query = "INSERT INTO profile VALUES(default, %s,%s,%s)"
        elif number == 6:
            query = "INSERT INTO survey VALUES(%s, default, default, default)"
        elif number == 7:
            query = "INSERT INTO person VALUES(default,%s,%s,%s,%s,%s,%s)"
        elif number == 8:
            query = "INSERT INTO staging VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s," \
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
        else:
            print("Error inserting list into unknown table")
        result = cursor.executemany(query,list)
        connection.commit()
        return

    # function inserts a record into table if it is not there
    @staticmethod
    def insert_trait(tuple, cursor, connection):
        query = "INSERT INTO traits(sex,height,body_type,relationship_status,languageID) VALUES(%s, %s, %s, %s,%s)"
        result = cursor.execute(query,tuple)
        connection.commit()
        return

    # Returns a list from the query sent in
    @staticmethod
    def load_table(query, cursor):
        cursor.execute(query)
        result = cursor.fetchall()
        return(result)

    @staticmethod
    def langAssociator(tuple, cursor):

        query = ("SELECT languageID FROM languages WHERE english = "
        + str(tuple[0])
        +" AND spanish = "
        + str(tuple[1])
        + " AND french = "
        + str(tuple[2])
        + " AND other = "
        + str(tuple[3]))

        cursor.execute(query)
        result = cursor.fetchall()

        if len(result):
            tempid = result[0][0]
            return(result[0])
        else:
            print ("No language record found")
            return 0

    @staticmethod
    def find_trait_id(tuple, cursor):
        #print(tuple)
        query = ("SELECT traitID FROM traits WHERE sex LIKE '"
                 + tuple[6]
                 + "' AND height = "
                 + str(tuple[14])
                 + " AND body_type = "
                 + str(tuple[8])
                 + " AND status LIKE '"
                 + tuple[5]
                 + "' AND languageID = "
                 + str(tuple[29]))

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result):
            return(result[0])
        else:
            print ("No trait record found")
            return 0

    @staticmethod
    def find_demographics_id(tuple, cursor):

        query = ("SELECT demographicsID FROM demographics WHERE ethnicity LIKE '"
                 + tuple[13]
                 + "' AND orientation LIKE '"
                 + tuple[7]
                 + "' AND income = "
                 + str(tuple[15])
                 + " AND location LIKE '"
                 + tuple[17]
                 + "' AND job LIKE '"
                 + tuple[16]
                 + "' AND education LIKE '"
                 + tuple[12]
                 + "' AND religion LIKE '"
                 + tuple[20] + "'"
                 )

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result):
            return(result[0])
        else:
            print ("No demographics record found")
            return 0

    @staticmethod
    def find_profile_id(tuple, cursor):

        query = ("SELECT profileID FROM profile WHERE traitID = "
                 + str(tuple[0])
                 + " AND preferenceID = "
                 + str(tuple[1])
                 + " AND demographicsID = "
                 + str(tuple[2])
                 )

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result):
            return(result[0])
        else:
            print ("No profile record found")
            return 0

    @staticmethod
    def find_survey_id(tuple, cursor):

        query = ("SELECT surveyID FROM survey WHERE traitID = "
                 + str(tuple[0])
                 + " AND preferenceID = "
                 + str(tuple[1])
                 + " AND demographicsID = "
                 + str(tuple[2])
                 )

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result):
            return(result[0])
        else:
            print ("No survey record found")
            return 0

    @staticmethod
    def find_preference_id(tuple, cursor):

        query = ("SELECT preferenceID FROM preferences WHERE diet = "
                 + str(tuple[9])
                 + " AND drinks = "
                 + str(tuple[10])
                 + " AND drugs = "
                 + str(tuple[11])
                 + " AND offspring = "
                 + str(tuple[18])
                 + " AND pets = "
                 + str(tuple[19])
                 )

        cursor.execute(query)
        result = cursor.fetchall()
        if len(result):
            return(result[0])
        else:
            print ("No record found diet = "+ x[9]
                   + " drinks = " + x[10]
                   + " drugs = " + x[11]
                   + " offspring = " + x[18]
                   + " pets = " + x[19])
            return 0

    @staticmethod
    # function outputs a csv from a sql query
    # fname = the csv you want to output to
    # query is the sql query you want to execute
    # conn is the connection to the mysqldb
    # pd is the pandas dataframe

    def exportReportCSV(fname, query, conn,pd):
        sql_query = pd.read_sql_query(query,conn)
        rp = pd.DataFrame(sql_query)
        rp.to_csv(fname, index= False)
        print("Outputted to file")
