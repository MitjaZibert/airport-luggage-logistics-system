-- Each hour:
-- New arriving and departing flights are added
-- Arrived flights are removed from the table
-- Departed flights for previous hour are removed from the table
-- Luggage is processed

-- Each end of the day (hour 23):
-- Luggage location transitions are processed (after specific days)


CREATE OR REPLACE PROCEDURE process_hourly_luggage_proc (
    p_airport_iata VARCHAR2, 
    p_week NUMBER,
    p_day_of_week NUMBER, 
    p_hour_of_day NUMBER
)
AS
    v_sql_error VARCHAR2(4000);
    v_location_id NUMBER;
    
BEGIN
    INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
    VALUES ('process_hourly_luggage_proc', 'to_airport_iata: ' || p_airport_iata || ', days_of_week: ' || p_day_of_week || ', hour_of_day: ' || p_hour_of_day);
    
    -- In Flight - Departing ID = 2
    -- Remains on flight - continuing flight
    v_location_id := 2;

    UPDATE LUGGAGE_TMP 
    SET luggage_location_id = v_location_id,
        update_week = p_week,
        update_day = p_day_of_week,
        update_hour = p_hour_of_day
    WHERE luggage_location_id = 1
    AND destination_schedule_id IS NOT NULL
    AND arriving_flight_id IN (
        SELECT arriving_flight_id
        FROM arriving_flights 
        WHERE TO_NUMBER(REPLACE(SUBSTR(actual_arrival_time, 1, 2), ':', '')) = p_hour_of_day
        AND schedule_id IN (
                SELECT schedule_id
                FROM schedules
                WHERE connecting_to_schedule IS NOT NULL));


    -- Baggage Holding Area ID = 3
    -- Waits for a connecting flight Baggage Holding Area - connecting flight
    v_location_id := 3;

    UPDATE LUGGAGE_TMP 
    SET luggage_location_id = v_location_id,
        update_week = p_week,
        update_day = p_day_of_week,
        update_hour = p_hour_of_day
    WHERE luggage_location_id = 1
    AND destination_schedule_id IS NOT NULL
    AND arriving_flight_id IN (
            SELECT arriving_flight_id
            FROM arriving_flights 
            WHERE TO_NUMBER(REPLACE(SUBSTR(actual_arrival_time, 1, 2), ':', '')) = p_hour_of_day);


    -- Baggage Claim Area ID = 4
    -- Waits in Baggage Claim Area for passenger to claim it
    v_location_id := 4;

    UPDATE LUGGAGE_TMP 
    SET luggage_location_id = v_location_id,
        update_week = p_week,
        update_day = p_day_of_week,
        update_hour = p_hour_of_day
    WHERE luggage_location_id = 1
    AND destination_schedule_id IS NULL
    AND arriving_flight_id IN (
            SELECT arriving_flight_id
            FROM arriving_flights 
            WHERE TO_NUMBER(REPLACE(SUBSTR(actual_arrival_time, 1, 2), ':', '')) = p_hour_of_day);

    


EXCEPTION
    -- Handle unexpected errors
    WHEN OTHERS THEN
        -- Log the error
        v_sql_error := SUBSTR('Error: ' || SQLERRM, 1, 4000);

        INSERT INTO DB_TRIGGER_LOG (trigger_name, additional_info)
        VALUES ('process_hourly_luggage_proc', 'Error: ' || v_sql_error);

END;