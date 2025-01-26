-- ===========================================================================================
-- Airport Luggage Logistics System - Oracle Database PL/SQL Functions
-- ===========================================================================================

-- Function to initialize arriving flights for a given day and hour
CREATE OR REPLACE PROCEDURE initialize_arraving_flights (
    p_airport_iata VARCHAR2, 
    p_day_of_week NUMBER, 
    p_hour_of_day NUMBER
    )
AS
BEGIN
    
    INSERT INTO arriving_flights (schedule_id, scheduled_arrival_time)
    SELECT schedule_id, arrival_time
        FROM schedules
        WHERE to_airport_iata = p_airport_iata
        AND days_of_week LIKE '%'||p_day_of_week||'%'
        AND REPLACE(SUBSTR(arrival_time, 1, 2), ':', '') = p_hour_of_day;

    
EXCEPTION
    -- Handle unexpected errors
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
