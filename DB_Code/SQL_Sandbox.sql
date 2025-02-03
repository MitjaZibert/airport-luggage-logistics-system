
rollback;

commit;



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







WITH valid_flights AS (
                select af.aircraft_iata, 
                af.schedule_id AS schedule_id_from, af.from_airport_iata, TO_CHAR(af.scheduled_arrival_time, 'HH24:MI') AS scheduled_arrival_time,
                df.schedule_id AS schedule_id_to, df.to_airport_iata, TO_CHAR(df.scheduled_departure_time, 'HH24:MI') AS scheduled_departure_time
                FROM schedules af
                INNER JOIN schedules df
                ON df.aircraft_iata = af.aircraft_iata 
                WHERE df.from_airport_iata = 'ORD' AND af.to_airport_iata = 'ORD'
                AND af.days_of_week LIKE '%5%' AND df.days_of_week LIKE '%5%'
                AND ROUND((df.scheduled_departure_time - af.scheduled_arrival_time) * 24 * 60) > 60
),
random_departng_flights AS 
(
        SELECT *
        FROM 
        (
                SELECT vf.*, 
                ROW_NUMBER() OVER (PARTITION BY vf.schedule_id_from ORDER BY sys_guid()) AS rn
                FROM valid_flights vf
                WHERE NOT EXISTS (
                        SELECT 1
                        FROM schedules s2
                        WHERE s2.connecting_to_schedule = vf.schedule_id_to)
                        )
        WHERE rn = 1
)
SELECT * 
FROM random_departng_flights
order by schedule_id_to;



select * 
FROM schedules s1
WHERE NOT EXISTS (
        SELECT 1
        FROM schedules s2
        WHERE s2.connecting_to_schedule = s1.schedule_id);