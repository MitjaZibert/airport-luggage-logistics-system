LOAD DATA
INFILE 'aircrafts.csv'
INTO TABLE aircrafts
FIELDS TERMINATED BY ','
(aircraft_iata,aircraft_name,capacity,country_iso)