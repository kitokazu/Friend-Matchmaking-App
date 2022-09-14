use finalproj408;

select count(*)
from person;

select *
from demographics;

SELECT *
FROM languages
WHERE English = 1
LIMIT 3;



#will attempt to create a stored procedure
#if french, show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join traits t on p.traitID = t.traitID
inner join languages L on t.languageID = L.languageID
where L.french = 1
ORDER BY RAND()
LIMIT 3;

#will attempt to create a stored procedure
#if english, show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join traits t on p.traitID = t.traitID
inner join languages L on t.languageID = L.languageID
where L.english = 1
ORDER BY RAND()
LIMIT 3;

#will attempt to create a stored procedure
#if spanish, show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join traits t on p.traitID = t.traitID
inner join languages L on t.languageID = L.languageID
where L.spanish = 1
ORDER BY RAND()
LIMIT 3;

#will attempt to create a stored procedure
#if other, show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join traits t on p.traitID = t.traitID
inner join languages L on t.languageID = L.languageID
where L.other = 1
ORDER BY RAND()
LIMIT 3;

#sex query
#show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join traits t on p.traitID = t.traitID
where t.sex = "m"
ORDER BY RAND()
LIMIT 3;

#relationship query
#show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join traits t on p.traitID = t.traitID
where t.status = "single"
ORDER BY RAND()
LIMIT 3;

#drinks query
#show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join preferences pref on p.preferenceID = pref.preferenceID
where pref.drinks= 1
ORDER BY RAND()
LIMIT 3;

#drugs query
#show top 3 matches
SELECT per.userID
from person per
inner join profile p on p.profileID = per.profileID
inner join preferences pref on p.preferenceID = pref.preferenceID
where pref.drugs= 1
ORDER BY RAND()
LIMIT 3;


select *
from preferences;

#using a groupby: showing count of users by orientation?
SELECT orientation, COUNT(*)
FROM demographics
GROUP BY orientation;

SELECT orientation, COUNT(*) as NumOfUsers_in_CA
from demographics
WHERE location = "california"
group by orientation;


SELECT ethnicity, count(per.userID) as Num_of_users_in_CA
from person per
inner join profile p on p.profileID = per.profileID
inner join demographics d on p.demographicsID = d.demographicsID
where d.location = "california"
group by ethnicity;

#group by
SELECT location, count(per.userID) as Num_of_users_in_area
from person per
inner join profile p on p.profileID = per.profileID
inner join demographics d on p.demographicsID = d.demographicsID
group by location;

#subquery
SELECT COUNT(*) allCount, (
    SELECT COUNT(*)
    from person
    WHERE age > 30
    ) AS above30Count
FROM person;


#doesnt work ignore
SELECT *
FROM person
WHERE profileID = (
    SELECT profileID
    FROM profile
    WHERE demographicsID = (
        SELECT demographicsID
        from demographics
        WHERE orientation = "gay"
    )
);


select *
from demographics;

select demographicsID
from profile;



#database view for admin
create view admin_view as
select per.userID, per.age, d.ethnicity, d.orientation, d.income, d.location, d.job, d.education, d.religion
from person per
inner join profile p on p.profileID = per.profileID
inner join demographics d on p.demographicsID = d.demographicsID;

select * from admin_view;


select count(*)
from survey;

select count(*)
from traits;




#from admin view
#view profile table
#view demographics
