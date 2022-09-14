#Process Raw Data
# This will clean the raw data and place the outputs in a clean csv file
# since we only do this one time it is placed in this seperate python file
import pandas as pd
from helper import helper
from populator import populator




#List of indexes for each table for the load to our list
#initial file
# userID,friendmatch,userRole,userAdmin,passcode,age,status,sex,orient,body,diet,drinks,drugs,
# education,ethnicity,hieght,income,job,lastonline,location,offspring, pets,religion,sign,smokes,
# speaks,survey1,survey2,survey3

stagingIndex = [0,1,2,3,4,5,6,7,10,11,12,13,14,15,16,17,19,20,21,22,23,24,26,27,28,29,30,31]

#Languages - languageID, english, spanish, french, other
languagesIndex = [0,1,2,3,4]

#Traits - traitID, sex, height, body_type, relationship_status, english, spanish, french, other
traitsIndex = [5, 15, 7, 4, 26, 27, 28, 29]

#Preferences - preferenceID, diet, drugs, offspring, pets
preferencesIndex = [0,1,2,3,4,5]

#Demographics - demographicsID, ethnicity, orientation, income_range, location, job, education, religion
demographicsIndex = [14, 6, 16, 19, 17, 13, 22]

#Profile - profileID
profileIndex = []

#Survey - surveyID
surveyIndex = []

#Person - userID, name, age, income, username, password
personIndex = []

# Set Up dataframes
origDf = pd.DataFrame()
df = origDf
fd = pd.DataFrame()

def fixUpDiet():
    df['diet'] = df['diet'].replace({'anything':'0'})
    df['diet'] = df['diet'].replace({'mostly anything':'0'})
    df['diet'] = df['diet'].replace({'strictly anything':'0'})
    df['diet'] = df['diet'].replace({'other':'0'})
    df['diet'] = df['diet'].replace({'mostly other':'0'})
    df['diet'] = df['diet'].replace({'strictly other':'0'})
    df['diet'] = df['diet'].replace({'halal':'0'})
    df['diet'] = df['diet'].replace({'mostly halal':'0'})
    df['diet'] = df['diet'].replace({'strictly halal':'0'})
    df['diet'] = df['diet'].replace({'kosher':'0'})
    df['diet'] = df['diet'].replace({'mostly kosher':'0'})
    df['diet'] = df['diet'].replace({'strictly kosher':'0'})
    df['diet'] = df['diet'].fillna("JAY")
    df['diet'] = df['diet'].replace({'JAY':'0'})

    df['diet'] = df['diet'].replace({'vegetarian':'1'})
    df['diet'] = df['diet'].replace({'mostly vegetarian':'1'})
    df['diet'] = df['diet'].replace({'strictly vegetarian':'1'})
    df['diet'] = df['diet'].replace({'vegan':'1'})
    df['diet'] = df['diet'].replace({'mostly vegan':'1'})
    df['diet'] = df['diet'].replace({'strictly vegan':'1'})

    df['diet'] = df['diet'].replace({'never':'0'})
    df['diet'] = df['diet'].replace({'':'0'})

def fixUpDrinks():
    df['drinks'] = df['drinks'].replace({'not at all':'0'})
    df['drinks'] = df['drinks'].replace({'rarely':'0'})

    df['drinks'] = df['drinks'].fillna("JEEVAN")
    df['drinks'] = df['drinks'].replace({'JEEVAN':'0'})

    df['drinks'] = df['drinks'].replace({'socially':'1'})
    df['drinks'] = df['drinks'].replace({'often':'1'})
    df['drinks'] = df['drinks'].replace({'desperately':'1'})
    df['drinks'] = df['drinks'].replace({'very often':'1'})


def fixUpDrugs():
    df['drugs'] = df['drugs'].replace({'never':'0'})
    df['drugs'] = df['drugs'].fillna("JEEVAN")
    df['drugs'] = df['drugs'].replace({'JEEVAN':'0'})

    df['drugs'] = df['drugs'].replace({'sometimes':'1'})
    df['drugs'] = df['drugs'].replace({'often':'1'})

def fixUpPets():
    df['pets'] = df['pets'].replace({'dislikes cats':'0'})
    df['pets'] = df['pets'].replace({'dislikes dogs':'0'})
    df['pets'] = df['pets'].replace({'dislikes dogs and dislikes cats':'0'})
    df['pets'] = df['pets'].replace({'likes dogs and dislikes cats':'0'})
    df['pets'] = df['pets'].replace({'likes dogs and likes cats':'0'})
    df['pets'] = df['pets'].replace({'has cats':'1'})
    df['pets'] = df['pets'].replace({'has dogs':'1'})
    df['pets'] = df['pets'].replace({'has dogs and dislike cats':'1'})
    df['pets'] = df['pets'].replace({'dislikes dogs and likes cats':'1'})
    df['pets'] = df['pets'].replace({'dislikes dogs and has cats':'1'})
    df['pets'] = df['pets'].replace({'likes cats':'0'})
    df['pets'] = df['pets'].replace({'likes dogs':'0'})
    df['pets'] = df['pets'].replace({'likes dogs and has cats':'1'})
    df['pets'] = df['pets'].replace({'has dogs and has cats':'1'})
    df['pets'] = df['pets'].replace({'has dogs and likes cats':'1'})
    df['pets'] = df['pets'].replace({'has dogs and dislikes cats':'1'})

    df['pets'] = df['pets'].fillna("JEEVAN")
    df['pets'] = df['pets'].replace({'JEEVAN':'0'})

def fixUpOffspring():
    df['offspring'] = df['offspring'].replace({"doesn't have kids":'0'})
    df['offspring'] = df['offspring'].replace({"doesn't want any":'0'})
    df['offspring'] = df['offspring'].replace({"doesn't want kids":'0'})
    df['offspring'] = df['offspring'].replace({"doesn't have kids  but wants them":'0'})
    df['offspring'] = df['offspring'].replace({'doesnt have kids':'0'})
    df['offspring'] = df['offspring'].replace({"doesn't have kids  and doesn't want any":'0'})
    df['offspring'] = df['offspring'].replace({"doesn't have kids  but might want them":'0'})
    df['offspring'] = df['offspring'].replace({"doesn't have kids  but wants them":'0'})
    df['offspring'] = df['offspring'].replace({"might want kids":'0'})
    df['offspring'] = df['offspring'].replace({"wants kids":'0'})

    df['offspring'] = df['offspring'].replace({"has a kid":'1'})
    df['offspring'] = df['offspring'].replace({"has a kid  and might want more":'1'})
    df['offspring'] = df['offspring'].replace({"has a kid  and wants more":'1'})
    df['offspring'] = df['offspring'].replace({"has a kid  but doesn't want more":'1'})
    df['offspring'] = df['offspring'].replace({"has kids":'1'})
    df['offspring'] = df['offspring'].replace({"has kids  and might want more":'1'})
    df['offspring'] = df['offspring'].replace({"has kids  and wants more":'1'})
    df['offspring'] = df['offspring'].replace({"has kids  but doesn't want more":'1'})

def fixUpSmokes():
    df['smokes'] = df['smokes'].replace({'no':'0'})

    df['smokes'] = df['smokes'].fillna("JEEVAN")
    df['smokes'] = df['smokes'].replace({'JEEVAN':'0'})

    df['smokes'] = df['smokes'].replace({'sometimes':'1'})
    df['smokes'] = df['smokes'].replace({'when drinking':'1'})
    df['smokes'] = df['smokes'].replace({'yes':'1'})
    df['smokes'] = df['smokes'].replace({'trying to quit':'1'})

def fixUpJob():
    df['job'] = df['job'].replace({'artistic / musical / writer':'artist'})
    df['job'] = df['job'].replace({'banking / financial / real estate':'finance'})
    df['job'] = df['job'].replace({'clerical / administrative':'administrative'})
    df['job'] = df['job'].replace({'computer / hardware / software':'tech'})
    df['job'] = df['job'].replace({'construction / craftsmanship':'contruction'})
    df['job'] = df['job'].replace({'ethnicity / academia':'ethnicity'})
    df['job'] = df['job'].replace({'entertainment / media':'artist'})
    df['job'] = df['job'].replace({'executive / management':'management'})
    df['job'] = df['job'].replace({'hospitality / travel':'hospitality'})
    df['job'] = df['job'].replace({'law / legal services':'law'})
    df['job'] = df['job'].replace({'medicine / health':'health'})
    df['job'] = df['job'].replace({'military':'military'})
    df['job'] = df['job'].replace({'other':'other'})
    df['job'] = df['job'].replace({'political / government':'political'})
    df['job'] = df['job'].replace({'rather not say':'other'})
    df['job'] = df['job'].replace({'retired':'retired'})
    df['job'] = df['job'].replace({'sales / marketing / biz dev':'other'})
    df['job'] = df['job'].replace({'science / tech / engineering':'tech'})
    df['job'] = df['job'].replace({'student':'student'})
    df['job'] = df['job'].replace({'transportation':'hospitality'})
    df['job'] = df['job'].replace({'unemployed':'other'})


def fixUpEducation():
    df['education'] = df['education'].replace({'college/university':'undergrad'})
    df['education'] = df['education'].replace({'dropped out of college/university':'high school'})
    df['education'] = df['education'].replace({'dropped out of high school':'high school'})
    df['education'] = df['education'].replace({'dropped out of med school':'undergrad'})
    df['education'] = df['education'].replace({'dropped out of masters program':'undergrad'})
    df['education'] = df['education'].replace({'dropped out of law school':'undergrad'})
    df['education'] = df['education'].replace({'dropped out of ph.d program':'graduated'})
    df['education'] = df['education'].replace({'dropped out of space camp':'high school'})
    df['education'] = df['education'].replace({'dropped out of two-year college':'high school'})
    df['education'] = df['education'].replace({'graduated from college/university':'graduated'})
    df['education'] = df['education'].replace({'graduated from high school':'high school'})
    df['education'] = df['education'].replace({'graduated from law school':'graduated'})
    df['education'] = df['education'].replace({'graduated from masters program':'graduated'})
    df['education'] = df['education'].replace({'graduated from med school':'graduated'})
    df['education'] = df['education'].replace({'graduated from ph.d program':'graduated'})
    df['education'] = df['education'].replace({'graduated from space camp':'undergrad'})
    df['education'] = df['education'].replace({'graduated from two-year college':'undergrad'})
    df['education'] = df['education'].replace({'graduated high school':'undergrad'})
    df['education'] = df['education'].replace({'high school':'high school'})

    df['education'] = df['education'].replace({'law school':'undergrad'})
    df['education'] = df['education'].replace({'masters program':'undergrad'})
    df['education'] = df['education'].replace({'med school':'high school'})
    df['education'] = df['education'].replace({'ph.d program':'graduated'})
    df['education'] = df['education'].replace({'space camp':'undergrad'})
    df['education'] = df['education'].replace({'two-year college':'undergrad'})

    df['education'] = df['education'].replace({'working on college/university':'undergrad'})
    df['education'] = df['education'].replace({'working on high school':'high school'})
    df['education'] = df['education'].replace({'working on law school':'undergrad'})
    df['education'] = df['education'].replace({'working on masters program':'undergrad'})
    df['education'] = df['education'].replace({'working on med school':'graduated'})
    df['education'] = df['education'].replace({'working on ph.d program':'graduated'})
    df['education'] = df['education'].replace({'working on space camp':'undergrad'})
    df['education'] = df['education'].replace({'working on two-year college':'undergrad'})

def fixUpEthnicity():
    df['ethnicity'] = df['ethnicity'].replace({'asian.*':'asian'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({'black.*':'black'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({'white.*':'white'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({'hispanic.*':'hispanic'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({' hispanic':'hispanic'})
    df['ethnicity'] = df['ethnicity'].replace({'pacific islander.*':'asian'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({'indian.*':'asian'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({'middle eastern.*':'middle eastern'},regex=True)
    df['ethnicity'] = df['ethnicity'].replace({'native american.*':'native american'},regex=True)

    df['ethnicity'] = df['ethnicity'].fillna("JEEVAN")
    df['ethnicity'] = df['ethnicity'].replace({'JEEVAN':'other'})

def fixUpLocation():
    df['location'] = df['location'].replace({'.* california':'california'},regex=True)
    df['location'] = df['location'].replace({'.* new york':'new york'},regex=True)
    df['location'] = df['location'].replace({'.* gerogia':'gerogia'},regex=True)
    df['location'] = df['location'].replace({'.* new jersey':'new jersey'},regex=True)
    df['location'] = df['location'].replace({'.* illinois':'illinois'},regex=True)
    df['location'] = df['location'].replace({'.* district of columbia':'dc'},regex=True)
    df['location'] = df['location'].replace({'.* washington':'washington'},regex=True)
    df['location'] = df['location'].replace({'.* united kingdom':'uk'},regex=True)
    df['location'] = df['location'].replace({'.* spain':'spain'},regex=True)
    df['location'] = df['location'].replace({'.* ireland':'ireland'},regex=True)
    df['location'] = df['location'].replace({'.* vietnam':'veitnam'},regex=True)
    df['location'] = df['location'].replace({'.* texas':'texas'},regex=True)
    df['location'] = df['location'].replace({'.* colorado':'colorado'},regex=True)
    df['location'] = df['location'].replace({'.* oregon':'oregon'},regex=True)
    df['location'] = df['location'].replace({'.* montana':'montana'},regex=True)

    df['location'] = df['location'].replace({'.* west virgina':'west virgina'},regex=True)
    df['location'] = df['location'].replace({'.* virgina':'virginia'},regex=True)
    df['location'] = df['location'].replace({'.* virginia':'virginia'},regex=True)
    df['location'] = df['location'].replace({'.* tennessee':'tennessee'},regex=True)
    df['location'] = df['location'].replace({'.* nevada':'nevada'},regex=True)
    df['location'] = df['location'].replace({'.* idaho':'idaho'},regex=True)
    df['location'] = df['location'].replace({'.* mississippi':'mississippi'},regex=True)
    df['location'] = df['location'].replace({'.* florida':'florida'},regex=True)
    df['location'] = df['location'].replace({'.* utah':'utah'},regex=True)

    df['location'] = df['location'].replace({'.* massachusetts':'massachusetts'},regex=True)
    df['location'] = df['location'].replace({'.* rhode island':'rhode island'},regex=True)
    df['location'] = df['location'].replace({'.* canada':'canada'},regex=True)
    df['location'] = df['location'].replace({'.* germany':'germany'},regex=True)
    df['location'] = df['location'].replace({'.* pennsylvania':'pennsylvania'},regex=True)
    df['location'] = df['location'].replace({'.* switzerland':'switzerland'},regex=True)
    df['location'] = df['location'].replace({'.* mexico':'mexico'},regex=True)
    df['location'] = df['location'].replace({'.* ohio':'ohio'},regex=True)
    df['location'] = df['location'].replace({'.* arizona':'arizona'},regex=True)

    df['location'] = df['location'].replace({'.* hawaii':'hawaii'},regex=True)
    df['location'] = df['location'].replace({'.* wisconsin':'wisconsin'},regex=True)
    df['location'] = df['location'].replace({'.* north carolina':'north carolina'},regex=True)
    df['location'] = df['location'].replace({'.* georgia':'georgia'},regex=True)
    df['location'] = df['location'].replace({'.* netherlands':'netherlands'},regex=True)
    df['location'] = df['location'].replace({'.* michigan':'michigan'},regex=True)
    df['location'] = df['location'].replace({'.* connecticut':'connecticut'},regex=True)

    df['location'] = df['location'].replace({'.* louisiana':'louisiana'},regex=True)
    df['location'] = df['location'].replace({'.* minnesota':'minnesota'},regex=True)
    df['location'] = df['location'].replace({'.* missouri':'missouri'},regex=True)

    df['location'] = df['location'].fillna("JEEVAN")
    df['location'] = df['location'].replace({'JEEVAN':'california'})

def fixUpBodyType():

    df['body_type'] = df['body_type'].replace({'a little extra':'chubby'})
    df['body_type'] = df['body_type'].replace({'athletic':'fit'})
    df['body_type'] = df['body_type'].replace({'full figured':'chubby'})
    df['body_type'] = df['body_type'].replace({'jacked':'fit'})
    df['body_type'] = df['body_type'].replace({'rather not say':'n/a'})
    df['body_type'] = df['body_type'].replace({'skinny':'thin'})
    df['body_type'] = df['body_type'].replace({'used up':'thin'})
    df['body_type'] = df['body_type'].fillna("JEEVAN")
    df['body_type'] = df['body_type'].replace({'JEEVAN':'n/a'})

    # Add a new column at the end called bodytypeClean
    df['bodytypeClean'] = df['body_type']
    df['bodytypeClean'] = df['bodytypeClean'].replace({'n/a':'0'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'thin':'1'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'fit':'2'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'average':'3'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'chubby':'4'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'curvy':'5'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'full figured':'6'})
    df['bodytypeClean'] = df['bodytypeClean'].replace({'overweight':'7'})

    print(df.head(4))

def fixUpEnglish():

    # Add a new column at the end called english
    df['english'] = df['speaks']

    # This will find and row with english and set the value to 1
    df['english'] = df['english'].replace({'.*english.*':'1'},regex = True)

    # This will leave the value which been set ti 1 alone an set the other value to 0
    df['english'].where(df['english'].isin(['1']), '0', inplace=True)

def fixUpReligion():
    df['religion'] = df['religion'].replace({'agnosticism.*':'agnosticism'},regex=True)
    df['religion'] = df['religion'].replace({'atheism.*':'atheism'},regex=True)
    df['religion'] = df['religion'].replace({'buddhism.*':'buddhism'},regex=True)
    df['religion'] = df['religion'].replace({'catholicism.*':'catholicism'},regex=True)
    df['religion'] = df['religion'].replace({'christianity.*':'christianity'},regex=True)
    df['religion'] = df['religion'].replace({'hinduism.*':'hinduism'},regex=True)
    df['religion'] = df['religion'].replace({'islam.*':'islam'},regex=True)
    df['religion'] = df['religion'].replace({'judaism.*':'judaism'},regex=True)
    df['religion'] = df['religion'].replace({'other.*':'other'},regex=True)

    df['religion'] = df['religion'].fillna("JEEVAN")
    df['religion'] = df['religion'].replace({'JEEVAN':'other'})



def fixUpSpanish():

    # Add a new column at the end called spanish
    df['spanish'] = df['speaks']

    # This will find and row with spanish and set the value to 1
    df['spanish'] = df['spanish'].replace({'.*spanish.*':'1'},regex = True)

    # This will leave the value which been set ti 1 alone an set the other value to 0
    df['spanish'].where(df['spanish'].isin(['1']), '0', inplace=True)

def fixUpFrench():

    # Add a new column at the end called french
    df['french'] = df['speaks']

    # This will find and row with french and set the value to 1
    df['french'] = df['french'].replace({'.*french.*':'1'},regex = True)

    # This will leave the value which been set ti 1 alone an set the other value to 0
    df['french'].where(df['french'].isin(['1']), '0', inplace=True)

def isOther(languages):
    # list all the other languages
    lang = ['c++',
            'afrikaans',
            'dutch',
            'basque',
            'arabic',
            'hawaiian'
            'german',
            'chinese',
            'sign',
            'italian',
            'slovak',
            'other',
            'turkish',
            'greek',
            'hebrew',
            'cebuano',
            'latin',
            'chechen',
            'icelandic',
            'tagalog',
            'japanese',
            'lisp',
            'indonesian',
            'swedish',
            'portuguese',
            'belarusan',
            'gujarati',
            'russian',
            'farsi',
            'serbian',
            'korean',
            'hindi',
            'vietnamese',
            'esperanto',
            'swahili',
            'norwegian']
    for x in lang:
        if x in languages:
            return 1
        else:
            return 0

def fixUpOther():

    # Add a new column at the end called other
    df['other'] = df['speaks']

    # This will find and row with frnch and set the value to 0
#    df['other'] = df['other'].replace({'.*french.*':'0'},regex = True)

    # This will leave the value which been set ti 1 alone an set the other value to 0
    #df['other'].where(df['other'].isin(lang), '9999', inplace=True)
    df['other'] = df['other'].apply(isOther)

def configureModifiedTable():

    fd['userRole'] = df['userRole']
    fd['username'] = df['username']
    fd['passcode'] = df['passcode']
    fd['age'] = df['age']
    fd['status'] = df['status']
    fd['sex'] = df['sex']
    fd['orientation'] = df['orientation']
    fd['bodytypeClean'] = df['bodytypeClean']
    fd['body_type'] = df['body_type']
    fd['diet type'] = origDf['diet']
    fd['diet'] = df['diet']
    fd['drinks'] = df['drinks']
    fd['drugs'] = df['drugs']
    fd['education'] = df['education']
    fd['ethnicity'] = df['ethnicity']
    fd['height'] = df['height']
    fd['income'] = df['income']
    fd['job'] = df['job']
    fd['last_online'] = df['last_online']
    fd['location'] = df['location']
    fd['offspring'] = df['offspring']
    fd['pets'] = df['pets']
    fd['religion'] = df['religion']
    fd['sign']  = df['sign']
    fd['smokes'] = df['smokes']
    fd['orid lang'] = df['speaks']
    fd['english'] = df['english']
    fd['spanish'] = df['spanish']
    fd['french'] = df['french']
    fd['other'] = df['other']
    fd['friendMatch'] = df['friendMatch']
    fd['userID'] = df['userID']

def fixUpData():
    fixUpDiet()
    fixUpDrinks()
    fixUpDrugs()
    fixUpPets()
    fixUpOffspring()
    fixUpSmokes()
    fixUpJob()
    fixUpReligion()
    fixUpEducation()
    fixUpEthnicity()
    fixUpLocation()
    fixUpBodyType()
    fixUpEnglish()
    fixUpSpanish()
    fixUpFrench()
    fixUpOther()
    configureModifiedTable()

def get_amount_of_records():
    choice = input("Enter amount of records to process: ")
    while choice.isdigit() == False:
        print("Incorrect value. Try again")
        choice = input("Enter a number: ")
    return int(choice)

# main

print("\n\nInitating the processing of the raw data in rawdata.csv.\n")
amount_of_records = get_amount_of_records()

# Read in onlythe number of rows requested (this speeds up the processing
origDf = pd.read_csv("rawdata.csv", nrows = amount_of_records)
df = origDf
fixUpData()
print(df)
fd.head(amount_of_records).to_csv("newdata1.csv", index=False)


#Reads raw data csv
data_original = helper.data_cleaner("newdata1.csv")

#Creates 2D array from filtration given of list of tuples
# No need to export languages as those values will be
# loaded directly by main

data = list(data_original)
staging = populator.load(data, stagingIndex)
populator.export("staging.csv", staging)
print ("Exported staging.csv clean data")
del staging


# Final output
print("\n\nFinished clean up raw data to csv file.")
