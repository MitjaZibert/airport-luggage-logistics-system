truncate table luggage_tmp;

truncate table arriving_flights_tmp;

truncate table departing_flights_tmp;

insert into luggage_tmp (luggage_id,
    origin_schedule_id ,
    destination_schedule_id ,
    luggage_location_id ,
    arriving_flight_id ,
    departing_flight_id ,
    owner_name ,
    entry_week ,
    entry_day ,
    entry_hour ,
    update_week ,
    update_day ,
    update_hour)
    select luggage_id,
    origin_schedule_id ,
    destination_schedule_id ,
    luggage_location_id ,
    arriving_flight_id ,
    departing_flight_id ,
    owner_name ,
    entry_week ,
    entry_day ,
    entry_hour ,
    update_week ,
    update_day ,
    update_hour from luggage;

insert into ARRIVING_FLIGHTS_TMP
select * from ARRIVING_FLIGHTS;


insert into departing_FLIGHTS_TMP
select * from departing_FLIGHTS;