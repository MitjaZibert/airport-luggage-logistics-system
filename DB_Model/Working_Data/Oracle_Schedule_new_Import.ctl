LOAD DATA
INFILE 'schedule_new.csv'
INTO TABLE schedules
FIELDS TERMINATED BY ','
(from_airport_iata,to_airport_iata,days_of_week,departure_time_old,arrival_time_old,flight,aircraft_iata,flight_duration_old,airline_iata)