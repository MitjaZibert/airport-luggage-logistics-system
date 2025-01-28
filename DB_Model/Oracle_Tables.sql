-- Oracle DB
--
-- Data source: http://www.lsv.fr/~sirangel/teaching/dataset/
--
-- sqlldr user/pass@localhost:1521/XEPDB1 control=Oracle_Airlines_Import.ctl
--
-- ===========================================================================================

DROP TABLE DB_TRIGGER_LOG;

CREATE TABLE DB_TRIGGER_LOG (
    trigger_name VARCHAR2(200),
    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_info VARCHAR2(4000)
);

DROP TABLE AIRPORT_SIMULATION_DATA;

CREATE TABLE AIRPORT_SIMULATION_DATA (
    airport_iata VARCHAR2(3),
    week NUMBER,
    day_of_week NUMBER,
    hour_of_day NUMBER,
    hour_length_in_seconds NUMBER
);



--DROP TABLE COUNTRIES;

CREATE TABLE COUNTRIES (
    country_iso VARCHAR2(3),
    country_name VARCHAR2(100),
    CONSTRAINT pk_countries PRIMARY KEY (country_iso)
);


--DROP TABLE AIRPORTS;

CREATE TABLE AIRPORTS (
    airport_iata VARCHAR2(3),
    name VARCHAR2(100),
    city VARCHAR2(100),
    country VARCHAR2(100),
    country_iso VARCHAR2(3),
    CONSTRAINT pk_airports PRIMARY KEY (airport_iata)
);


--DROP TABLE DISTANCES;

CREATE TABLE DISTANCES (
    from_airport_iata VARCHAR2(3),
    to_airport_iata VARCHAR2(3),
    distance_km NUMBER(8, 3),
    CONSTRAINT pk_distances PRIMARY KEY (from_airport_iata, to_airport_iata)
);


--DROP TABLE AIRLINES;

CREATE TABLE AIRLINES (
    airline_iata VARCHAR2(2),
    airline_name VARCHAR2(100),
    callsign VARCHAR2(35),
    country_iso VARCHAR2(3),
    CONSTRAINT pk_airlines PRIMARY KEY (airline_iata)
);


--DROP TABLE AIRCRAFTS;

CREATE TABLE AIRCRAFTS (
    aircraft_iata VARCHAR2(3),
    aircraft_name VARCHAR2(100),
    capacity NUMBER,
    country_iso VARCHAR2(3),
    CONSTRAINT pk_aircrafts PRIMARY KEY (aircraft_iata)
);


--DROP TABLE CABIN_CLASSES;

CREATE TABLE CABIN_CLASSES (
    cabin_class_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    cabin_class VARCHAR2(50),
    CONSTRAINT pk_cabin_classes PRIMARY KEY (cabin_class_id),
    CONSTRAINT uniq_cabin_class unique (cabin_class)
);


--DROP TABLE SCHEDULES;

CREATE TABLE SCHEDULES (
    schedule_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    from_airport_iata VARCHAR2(3),
    to_airport_iata VARCHAR2(3),
    days_of_week VARCHAR2(7),
    departure_time VARCHAR2(5),
    arrival_time VARCHAR2(5),
    flight_duration VARCHAR2(5),
    flight VARCHAR2(10),
    airline_iata VARCHAR2(2),
    aircraft_iata VARCHAR2(3),
    CONSTRAINT pk_schedules PRIMARY KEY (schedule_id)
);


--DROP TABLE LUGGAGE_LOCATION;

CREATE TABLE LUGGAGE_LOCATION (
    luggage_location_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    location_name VARCHAR2(100),
    location_hours_limit NUMBER,
    CONSTRAINT pk_luggage_location PRIMARY KEY (luggage_location_id)
);

DROP TABLE ARRIVING_FLIGHTS;

CREATE TABLE ARRIVING_FLIGHTS (
    arriving_flight_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    schedule_id NUMBER,
    day_of_week NUMBER,
    scheduled_arrival_time VARCHAR2(5),
    actual_arrival_time VARCHAR2(5),
    delay_minutes NUMBER,
    CONSTRAINT pk_arriving_flights PRIMARY KEY (arriving_flight_id)
);



DROP TABLE LUGGAGE;

CREATE TABLE LUGGAGE (
    luggage_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    luggage_location_id NUMBER,
    active_flight_id NUMBER,
    owner_name VARCHAR2(100),
    entry_time DATE DEFAULT SYSDATE,
    update_time DATE,
    CONSTRAINT pk_luggage PRIMARY KEY (luggage_id)
);

-- CREATE TABLE LUGGAGE (
--     luggage_id NUMBER GENERATED ALWAYS AS IDENTITY, 
--     luggage_location_id NUMBER,
--     flight_id NUMBER,
--     cabin_class_id NUMBER,
--     owner_name VARCHAR2(100),
--     CONSTRAINT pk_luggage PRIMARY KEY (luggage_id)
-- );


--DROP TABLE LUGGAGE_STATUS;

CREATE TABLE LUGGAGE_STATUS (
    luggage_status_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    luggage_id NUMBER,
    luggage_location_id NUMBER,
    CONSTRAINT pk_luggage_status PRIMARY KEY (luggage_status_id)
);