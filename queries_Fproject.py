

# print("Welcome to your match preferences! Find platonic matches that are based on your settings ;)")
# print("\nPick which filter you would like to create. \n1: Filter by Age \n2:Language")

Age_query = '''
SELECT *
FROM person
WHERE Age <=:age1 and >=:age2
LIMIT 3;
'''
print("TOP 3 MATCHES")
#maybe change to single?
age_match = db_ops.multiple_attribute(query)

#english
if languagepref = "English"
    language_query = '''
    SELECT *
    FROM languages
    WHERE English = 1
    LIMIT 3;
    '''
elif languagepref = "Spanish":
    language_query = '''
    SELECT *
    FROM languages
    WHERE Spanish = 1
    LIMIT 3;
    '''
elif languagepref = "French":
    language_query = '''
    SELECT *
    FROM languages
    WHERE French = 1
    LIMIT 3;
    '''
elif languagepref = "Other":
    language_query = '''
    SELECT *
    FROM languages
    WHERE Other = 1
    LIMIT 3;
    '''

#sex query
input_sex = print("Enter sex preference")

sex_query = '''
SELECT *
from traits
WHERE Sex =: input_sex
LIMIT 3;
'''

#relationship query
input_status = print("select relationship status preference")
relationship_query = '''
SELECT *
from traits
WHERE Relationship =:input_status
'''

#ethnicity query
input_ethnicity = print("select ethnicity status preference")
ethnicity_query = '''
SELECT *
from traits
WHERE ethnicity LIKE '%input_ethnicity%'
LIMIT 3;
'''

#religion query
religion_input = print("select religion status preference")
religion_query = '''
SELECT *
from traits
WHERE religion LIKE 'religion_input%'
LIMIT 3;
'''
#social activities
user_pref = print("should equal either N or Y")
if selection = "Drinks":
    drink_query = '''
    SELECT *
    from preferences
    WHERE Drinks =:user_pref
    LIMIT 3;
    '''
elif selection = "Drugs":
    drugs_query = '''
    SELECT *
    from preferences
    WHERE Drugs =:user_pref
    LIMIT 3;
    '''
#count all users who are located in california
agre_query = '''
SELECT COUNT(*)
from Demographics
WHERE Location LIKE '%CA'
'''

#using a groupby: showing count of users by orientation?
#admin pov probably
groupby_query = '''
SELECT Orientation, COUNT(*)
FROM Demographics
GROUP BY Orientation;
'''
#count all users, and count all users who are above 30
sub_query2 = '''
SELECT COUNT(*) allCount, (
    SELECT COUNT(*)
    from Person
    WHERE Age > 30
    ) AS above30Count
FROM Person
'''
#subquery hard, displays userIDs that identify as gay
sub_query1 = '''
SELECT userID
FROM Person
WHERE Role = 'user'
AND profileID = (
    SELECT profileID
    FROM Profile
    WHERE DemographicsID = (
        SELECT DemographicsID
        from Demographics
        WHERE Orientation = "gay"
    )
)
'''

#inner join with at least three tables
#userID that are female
innerjoin_query1 = '''
select Person.userID
from Person
inner join Profile pro on Person.ProfileID on pro.ProfileID
inner join traits t on pro.TraitsID on t.TraitsID
where t.sex = "f";
'''


#inner join with at least three tables
innerjoin_query1 = '''
select Person.userID
from Person
inner join Profile pro on Person.ProfileID on pro.ProfileID
inner join traits t on pro.TraitsID on t.TraitsID
inner join languages L on t.TraitsID on L.TraitsID
where l.French = "Y";
'''
