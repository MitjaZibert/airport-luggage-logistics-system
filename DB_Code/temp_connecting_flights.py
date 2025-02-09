# ===========================================================================================
# Airport Luggage Logistics System - Flights Simulation
# ===========================================================================================

# App imports
from db_util import DBUtil

DBUtil.get_conn()


sql = 'UPDATE SCHEDULES SET connecting_to_schedule = null'
DBUtil.db_update(sql)


sql = "SELECT aircraft_iata FROM schedules GROUP BY aircraft_iata ORDER BY COUNT(*) ASC"
all_iata = DBUtil.db_query(sql)

for iata in all_iata:
    aircraft_iata = iata[0]

    sql = f"""SELECT DISTINCT af.schedule_id AS schedule_id_from
        FROM schedules af
        INNER JOIN schedules df
        ON df.aircraft_iata = af.aircraft_iata 
        WHERE df.from_airport_iata = 'ORD' AND af.to_airport_iata = 'ORD'
        AND af.days_of_week LIKE '%5%' AND df.days_of_week LIKE '%5%'
        AND af.aircraft_iata IN ('{aircraft_iata}')
        AND ROUND((df.scheduled_departure_time - af.scheduled_arrival_time) * 24 * 60) > 60"""

    schedule_ids = DBUtil.db_query(sql)

    for id in schedule_ids:
        schedule_id = id[0]
    
        sql = f"""MERGE INTO schedules s
        USING (
        WITH valid_flights AS (
                SELECT 
                ROW_NUMBER() OVER (PARTITION BY af.schedule_id ORDER BY sys_guid()) AS rn_r,
                af.schedule_id AS schedule_id_from,
                df.schedule_id AS schedule_id_to
                FROM schedules af
                INNER JOIN schedules df
                ON df.aircraft_iata = af.aircraft_iata 
                WHERE df.from_airport_iata = 'ORD' AND af.to_airport_iata = 'ORD'
                AND af.days_of_week LIKE '%5%' AND df.days_of_week LIKE '%5%'
                AND af.schedule_id = '{schedule_id}'
                AND ROUND((df.scheduled_departure_time - af.scheduled_arrival_time) * 24 * 60) > 60
                AND df.schedule_id NOT IN (SELECT DISTINCT connecting_to_schedule FROM SCHEDULES WHERE connecting_to_schedule IS NOT NULL)
        )
        SELECT schedule_id_from, schedule_id_to
            FROM valid_flights
            WHERE rn_r = 1
        )  flights
        ON (s.schedule_id = flights.schedule_id_from)
        WHEN MATCHED THEN 
            UPDATE SET s.connecting_to_schedule = flights.schedule_id_to"""


        DBUtil.db_update(sql)

        DBUtil.db_commit()




# MERGE INTO schedules s
#     USING (
#     WITH valid_flights AS (
#             SELECT 
#             ROW_NUMBER() OVER (PARTITION BY af.schedule_id ORDER BY sys_guid()) AS rn_r,
#             af.aircraft_iata,
#             af.schedule_id AS schedule_id_from, af.from_airport_iata, TO_CHAR(af.scheduled_arrival_time, 'HH24:MI') AS scheduled_arrival_time,
#             df.schedule_id AS schedule_id_to, df.to_airport_iata, TO_CHAR(df.scheduled_departure_time, 'HH24:MI') AS scheduled_departure_time
#             FROM schedules af
#             INNER JOIN schedules df
#             ON df.aircraft_iata = af.aircraft_iata 
#             WHERE df.from_airport_iata = 'ORD' AND af.to_airport_iata = 'ORD'
#             AND af.days_of_week LIKE '%5%' AND df.days_of_week LIKE '%5%'
#             AND ROUND((df.scheduled_departure_time - af.scheduled_arrival_time) * 24 * 60) > 60
#             AND df.schedule_id NOT IN (SELECT DISTINCT connecting_to_schedule FROM SCHEDULES WHERE connecting_to_schedule IS NOT NULL)
#     )
#     SELECT 
#             schedule_id_from, 
#             schedule_id_to
#         FROM valid_flights
#         WHERE rn_r = 1
#     )  flights
#     ON (s.schedule_id = flights.schedule_id_from)
#     WHEN MATCHED THEN 
#         UPDATE SET s.connecting_to_schedule = flights.schedule_id_to,
#                     s.connecting_from_schedule = flights.schedule_id_from