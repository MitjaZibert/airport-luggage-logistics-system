-- ===========================================================================================
-- Airport Luggage Logistics System - Oracle Database PL/SQL Triggers
-- ===========================================================================================

-- Trigger to initialize arriving flights for a current day and hour
CREATE OR REPLACE TRIGGER airport_simulation_data_after_upd_trg
AFTER UPDATE ON AIRPORT_SIMULATION_DATA
DECLARE
    v_airport_iata VARCHAR2(3);
    v_week NUMBER;
    v_day_of_week NUMBER;
    v_hour_of_day NUMBER;

    v_sql_error VARCHAR2(4000);
BEGIN
    -- Log trigger execution
    INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
    VALUES ('airport_simulation_data_after_upd_trg', 
            'Executed by user: ' || SYS_CONTEXT('USERENV', 'SESSION_USER') || 
            ', at: ' || TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS'));

    -- Retrieve data
    SELECT MAX(airport_iata), MAX(week), MAX(day_of_week), MAX(hour_of_day)
    INTO v_airport_iata, v_week, v_day_of_week, v_hour_of_day
    FROM AIRPORT_SIMULATION_DATA;


    IF v_week > 0 THEN
    
        -- Call the procedure to process arriving and departing fligths for current hour
        initialize_hourly_flights_proc(
            p_airport_iata => v_airport_iata, 
            p_day_of_week => v_day_of_week, 
            p_hour_of_day => v_hour_of_day
        );

        -- Call the procedure to process all luggage for current hour
        process_hourly_luggage_proc(
            p_airport_iata => v_airport_iata, 
            p_week => v_week,
            p_day_of_week => v_day_of_week, 
            p_hour_of_day => v_hour_of_day
        );


    END IF;

EXCEPTION
    WHEN OTHERS THEN
        -- Log the error
        v_sql_error := SUBSTR('Error: ' || SQLERRM, 1, 4000);

        INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
        VALUES ('airport_simulation_data_after_upd_trg', 'Error: ' || v_sql_error);

END;
