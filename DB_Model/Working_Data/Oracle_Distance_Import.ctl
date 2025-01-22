LOAD DATA
INFILE 'distance.csv'
INTO TABLE distances
FIELDS TERMINATED BY ','
(from_airport_iata,to_airport_iata,distance_km)