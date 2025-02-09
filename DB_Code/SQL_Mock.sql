MERGE INTO schedules s
USING (
WITH valid_flights AS (
                select af.aircraft_iata, 
                af.schedule_id AS schedule_id_from, af.from_airport_iata, TO_CHAR(af.scheduled_arrival_time, 'HH24:MI') AS scheduled_arrival_time,
                df.schedule_id AS schedule_id_to, df.to_airport_iata, TO_CHAR(df.scheduled_departure_time, 'HH24:MI') AS scheduled_departure_time,
                ROW_NUMBER() OVER (PARTITION BY af.schedule_id ORDER BY sys_guid()) AS rn
                FROM schedules af
                INNER JOIN schedules df
                ON df.aircraft_iata = af.aircraft_iata 
                WHERE df.from_airport_iata = 'ORD' AND af.to_airport_iata = 'ORD'
                AND af.days_of_week LIKE '%5%' AND df.days_of_week LIKE '%5%'
                --AND af.aircraft_iata = '757'
                AND ROUND((df.scheduled_departure_time - af.scheduled_arrival_time) * 24 * 60) > 60
)
-- ,
-- random_departng_flights AS (
--         SELECT *
--         FROM (
--                 SELECT vf.*, 
--                 ROW_NUMBER() OVER (PARTITION BY vf.schedule_id_from ORDER BY sys_guid()) AS rn
--                 FROM valid_flights vf   )
--         WHERE rn = 1
-- )
SELECT 
        schedule_id_from, 
        schedule_id_to
    FROM valid_flights
    WHERE rn = 1
)  flights
ON (s.schedule_id = flights.schedule_id_from)
WHEN MATCHED THEN 
    UPDATE SET s.connecting_to_schedule = flights.schedule_id_to;


rollback;

commit;

--=================================================================================================================
--=================================================================================================================
--=================================================================================================================

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
        )
        WHERE rn = 1
)
SELECT * 
FROM random_departng_flights
order by schedule_id_to;



SELECT * FROM SCHEDULES
WHERE connecting_to_schedule IS NOT NULL
ORDER BY connecting_to_schedule;


SELECT connecting_to_schedule, count(*) AS cnt, 1 FROM SCHEDULES
WHERE connecting_to_schedule IS NOT NULL
GROUP BY connecting_to_schedule
--HAVING COUNT(*) > 1
ORDER BY cnt desc;


