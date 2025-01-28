-- ===========================================================================================
-- Airport Luggage Logistics System - Oracle Database PL/SQL Procedures
-- ===========================================================================================

-- Function to initialize arriving flights for a given day and hour
CREATE OR REPLACE PROCEDURE initialize_arraving_flights_proc (
    p_airport_iata VARCHAR2, 
    p_day_of_week NUMBER, 
    p_hour_of_day NUMBER
    )
AS
    sql_error VARCHAR2(4000);
BEGIN
    INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
    VALUES ('initialize_arraving_flights_proc', 'to_airport_iata: ' || p_airport_iata || ', days_of_week: ' || p_day_of_week || ', arrival_time: ' || p_hour_of_day);
    
    INSERT INTO arriving_flights (schedule_id, scheduled_arrival_time)
    SELECT schedule_id, arrival_time
        FROM schedules
        WHERE to_airport_iata = p_airport_iata
        AND days_of_week LIKE '%'||p_day_of_week||'%'
        AND REPLACE(SUBSTR(arrival_time, 1, 2), ':', '') = p_hour_of_day;

    
EXCEPTION
    -- Handle unexpected errors
    WHEN OTHERS THEN
        -- Log the error
        sql_error := SUBSTR('Error: ' || SQLERRM, 1, 4000);

        INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
        VALUES ('initialize_arraving_flights_proc', 'Error: ' || sql_error);

END;
