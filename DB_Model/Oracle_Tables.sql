-- Oracle DB
--
-- Data source: http://www.lsv.fr/~sirangel/teaching/dataset/
--
-- sqlldr user/pass@localhost:1521/XEPDB1 control=Oracle_Airlines_Import.ctl
--
-- ===========================================================================================


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
    airline_iata VARCHAR2(2),
    aircraft_iata VARCHAR2(3),
    CONSTRAINT pk_schedules PRIMARY KEY (schedule_id)
);




--DROP TABLE LUGGAGE;

CREATE TABLE LUGGAGE (
    luggage_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    luggage_location_id NUMBER,
    flight_id NUMBER,
    cabin_class_id NUMBER,
    owner_name VARCHAR2(100),
    CONSTRAINT pk_luggage PRIMARY KEY (luggage_id)
);


--DROP TABLE LUGGAGE_;

CREATE TABLE LUGGAGE_LOCATION (
    luggage_location_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    location_name VARCHAR2(100),
    location_hours_limit NUMBER,
    CONSTRAINT pk_luggage_location PRIMARY KEY (luggage_location_id)
);


--DROP TABLE LUGGAGE_STATUS;

CREATE TABLE LUGGAGE_STATUS (
    luggage_status_id NUMBER GENERATED ALWAYS AS IDENTITY, 
    luggage_id NUMBER,
    luggage_location_id NUMBER,
    CONSTRAINT pk_luggage_status PRIMARY KEY (luggage_status_id)
);


/*

LUGGAGE LOCATION

Luggage Lifecycle:
1. Check-In Process - handeled by baggage handling system
    a. (99.2%) Successful load - Loaded to the right flight
    b. (0.3%) Late Check-In --> Rebooked For The Next Flight
    c. (0.5%) Unsuccessful load - Loaded to the wrong flight - Rebooked For The Next Flight Back (go to point 2)
   
2. Flight transit
    
3. Arrival at airport
    a. Sent to Baggage Claim Area - handeled by baggage handling system
        a. (99.9%) Picked Up by a passenger
        b. (0.1%) Not picked up - after 3 hours remmoved and stored at Baggage Service Office
            a. (90%) Claimed by a passenger within 7 days
            b. (10%) Not claimed for 7 days --> moved to Unclaimed Baggage Department 
                a. (95%) Claimed by a passenger within 83 days
                b. (5%) Not claimed for 83 days --> disposed
    b. If connecting flight sent to next flight - handeled by baggage handling system
        a. (99.2%) Successful load - Loaded to the right flight
        b. (0.5%) Missed connecting flight due to delay - Rebooked For The Next Flight
        c. (0.3%) Unsuccessful load - Loaded to the wrong flight - Rebooked For The Next Flight Back (go to point 2)

4. (cca 2 / hour) Found at airport or aircraft
    Sent to Lost & Found Department
        a. Claimed by a passenger within 30 days
        b. Not claimed for 30 days --> moved to Unclaimed Baggage Department 
            a. Claimed by a passenger within 60 days
            b. Not claimed for 90 days --> disposed
 



1. Check-In
- Incorrect tagging (e.g., wrong destination or flight).
- Late check-in, which may not allow enough time for the bag to be loaded onto the plane.

2. Baggage Handling and Sorting
- Bags may be misrouted due to scanner errors or human mistakes.
- Mishandling during sorting can lead to damage or delays

3. Loading onto the Aircraft
- Tight connection times between flights can result in bags being left behind.
- Weather delays or operational issues may disrupt the loading process.

4. Transit (Connecting Flights)
- Short layover times increase the risk of bags missing the connecting flight.
- Bags may be sent to the wrong connecting flight, especially if multiple flights are departing to similar destinations

5. Arrival and Claim
- Bags may be delayed if they are unloaded last or if there are issues with the baggage claim system.
- Theft or accidental pickup by another passenger can occur at the baggage claim area.



Statistics on Lost Luggage
- Delayed Bags: Around 85% of "lost" luggage is simply delayed and is usually returned to the passenger within a few days 
- Permanently Lost Bags: Only about 3% of luggage is permanently lost or stolen 
- Recovery Rate: Approximately 97% of lost luggage is eventually returned to its owner 
