LOAD DATA
INFILE 'schedule_tmp.csv'
INTO TABLE schedules_tmp
FIELDS TERMINATED BY ','
(from_airport_iata,to_airport_iata,valid_from,valid_until,days_of_week,departure_time,scheduled_arrival_time,flight,aircraft_iata,flight_duration)