LOAD DATA
INFILE 'schedule.csv'
INTO TABLE schedule
FIELDS TERMINATED BY ','
(from_iata,to_iata,days_of_week,departure_time,arrival_time,flight_iata,aircraft_iata,flight_duration)