LOAD DATA
INFILE 'airports.csv'
INTO TABLE airports
FIELDS TERMINATED BY ','
(airport_iata,name,city,country)