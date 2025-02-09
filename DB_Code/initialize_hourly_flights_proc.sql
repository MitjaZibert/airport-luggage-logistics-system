-- ===========================================================================================
-- Airport Luggage Logistics System - Oracle Database PL/SQL Procedures
-- ===========================================================================================

-- Function to initialize arriving and departing flights for a given day and hour
CREATE OR REPLACE PROCEDURE initialize_hourly_flights_proc (
    p_airport_iata VARCHAR2, 
    p_day_of_week NUMBER, 
    p_hour_of_day NUMBER
    )
AS
    v_sql_error VARCHAR2(4000);
BEGIN
    INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
    VALUES ('initialize_hourly_flights_proc', 'to_airport_iata: ' || p_airport_iata || ', days_of_week: ' || p_day_of_week || ', hour_of_day: ' || p_hour_of_day);
    
    -- filter by to_airport_iata
    INSERT INTO arriving_flights (schedule_id, scheduled_arrival_time, actual_arrival_time, delay_minutes)
    SELECT schedule_id, scheduled_arrival_time, scheduled_arrival_time, 0
        FROM schedules
        WHERE to_airport_iata = p_airport_iata
        AND days_of_week LIKE '%'||p_day_of_week||'%'
        AND TO_NUMBER(REPLACE(SUBSTR(scheduled_departure_time, 1, 2), ':', '')) = p_hour_of_day;

    -- filter by from_airport_iata
    INSERT INTO departing_flights (schedule_id, scheduled_departure_time, actual_departure_time, delay_minutes)
    SELECT schedule_id, scheduled_departure_time, scheduled_departure_time, 0
        FROM schedules
        WHERE from_airport_iata = p_airport_iata
        AND days_of_week LIKE '%'||p_day_of_week||'%'
        AND TO_NUMBER(REPLACE(SUBSTR(scheduled_departure_time, 1, 2), ':', '')) = p_hour_of_day;

    
EXCEPTION
    -- Handle unexpected errors
    WHEN OTHERS THEN
        -- Log the error
        v_sql_error := SUBSTR('Error: ' || SQLERRM, 1, 4000);

        INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
        VALUES ('initialize_hourly_flights_proc', 'Error: ' || v_sql_error);

END;
