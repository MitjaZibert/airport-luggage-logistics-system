LOAD DATA
INFILE 'airlines.csv'
INTO TABLE airlines
FIELDS TERMINATED BY ','
(airline_iata,airline_name,callsign,country)