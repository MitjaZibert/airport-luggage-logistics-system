-- ===========================================================================================
-- Airport Luggage Logistics System - Oracle Database PL/SQL Triggers
-- ===========================================================================================

-- Trigger to initialize arriving flights for a current day and hour
CREATE OR REPLACE TRIGGER airport_simulation_data_after_upd_trg
AFTER UPDATE ON AIRPORT_SIMULATION_DATA
DECLARE
    airport_iata VARCHAR2(3);
    week NUMBER;
    day_of_week NUMBER;
    hour_of_day NUMBER;

    sql_error VARCHAR2(4000);
BEGIN
    -- Log trigger execution
    INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
    VALUES ('airport_simulation_data_after_upd_trg', 
            'Executed by user: ' || SYS_CONTEXT('USERENV', 'SESSION_USER') || 
            ', at: ' || TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS'));

    -- Retrieve data
    SELECT MAX(airport_iata), MAX(week), MAX(day_of_week), MAX(hour_of_day)
    INTO airport_iata, week, day_of_week, hour_of_day
    FROM AIRPORT_SIMULATION_DATA;


    -- Call the procedure
    IF week > 0 THEN
        initialize_hourly_flights_proc(
            p_airport_iata => airport_iata, 
            p_day_of_week => day_of_week, 
            p_hour_of_day => hour_of_day
        );
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        -- Log the error
        sql_error := SUBSTR('Error: ' || SQLERRM, 1, 4000);

        INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
        VALUES ('airport_simulation_data_after_upd_trg', 'Error: ' || sql_error);

END;
