select from_airport_iata, count(*) as count, 1
from SCHEDULES
GROUP by from_airport_iata
order by 2 desc;

-- from DFW (858), MAD (593), ORD (539), LHR (443)
-- to DFW (838), MAD (577), ORD (535), LHR (456)


SELECT Count(*)
FROM schedules s
INNER JOIN aircrafts ac 
ON ac.aircraft_iata = s.aircraft_iata
INNER JOIN CABIN_CLASSES
WHERE s.to_airport_iata = 'ORD';



INSERT INTO arriving_flights (schedule_id, actual_arrival_time)
    SELECT schedule_id, arrival_time
        FROM schedules
        WHERE to_airport_iata = 'ORD'
        and days_of_week LIKE '%7%'
        AND REPLACE(SUBSTR(arrival_time, 1, 2), ':', '') = 7
        ORDER BY arrival_time ASC;


SELECT af.active_flight_id, af.actual_arrival_time, ac.capacity
                        FROM active_flights af
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id
                        INNER JOIN aircrafts ac
                        ON ac.aircraft_iata = s.aircraft_iata;


INSERT INTO arriving_flights (schedule_id, actual_arrival_time) SELECT schedule_id, arrival_time FROM schedules WHERE to_airport_iata = 'ORD' AND days_of_week LIKE '%7%' AND REPLACE(SUBSTR(arrival_time, 1, 2), ':' , '') = 7;



commit;


truncate table luggage;
truncate table arriving_flights;
rollback;

