LOAD DATA
INFILE 'schedule.csv'
INTO TABLE schedules
FIELDS TERMINATED BY ','
(from_airport_iata,to_airport_iata,days_of_week,departure_time,arrival_time,flight_duration,flight,airline_iata,aircraft_iata)