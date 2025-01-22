LOAD DATA
INFILE 'countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ','
(country_iso,country_name)