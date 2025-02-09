
SELECT schedule_id, from_airport_iata, to_airport_iata, TO_CHAR(scheduled_arrival_time, 'HH24:MI'), TO_CHAR(scheduled_departure_time, 'HH24:MI'), aircraft_iata
        FROM schedules
        WHERE to_airport_iata = 'ORD'
        AND days_of_week LIKE '%6%'
        --AND TO_NUMBER(TO_CHAR(s.arrival_time, 'HH24')) = 7
        AND aircraft_iata = '757'
        order by aircraft_iata;

SELECT schedule_id, from_airport_iata, to_airport_iata, TO_CHAR(scheduled_arrival_time, 'HH24:MI'), TO_CHAR(scheduled_departure_time, 'HH24:MI'), aircraft_iata
        FROM schedules
        WHERE from_airport_iata = 'ORD'
        AND days_of_week LIKE '%6%'
        --AND TO_NUMBER(TO_CHAR(s.departure_time, 'HH24')) = 7
        AND aircraft_iata = '757'
        order by aircraft_iata;


--=================================================================================================================
--=================================================================================================================

rollback;

commit;

--=================================================================================================================
--=================================================================================================================


update luggage_tmp
set LUGGAGE_LOCATION_ID = 1;



select * from ARRIVING_FLIGHTS;

select * from luggage_tmp
WHERE LUGGAGE_LOCATION_ID = 2;
--WHERE ORIGIN_SCHEDULE_ID = DESTINATION_SCHEDULE_ID;




SELECT * 
FROM schedules
WHERE connecting_to_schedule IS NOT NULL;


select * from luggage_tmp
WHERE destination_schedule_id IS NOT NULL
AND LUGGAGE_LOCATION_ID not in (1, 2)
    AND arriving_flight_id IN (
        SELECT arriving_flight_id
        FROM arriving_flights 
        WHERE schedule_id IN (
                SELECT schedule_id
                FROM schedules
                WHERE connecting_to_schedule IS NOT NULL));

