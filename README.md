# Airport Luggage Logistics System
## Project to explore combination of Python + Oracle DB
## Project currently on hold due to focus on other projects and because key part of exploratin was achieved.

## Overview

The **Airport Luggage Logistics System** is a database project designed to manage the logistics of luggage handling at airports. It tracks flights (incoming and outgoing), luggage details (origin, destination, type, priority, status, etc.), and misplaced luggage (when and where it was reported misplaced, recovered, and delivered). 

This project is meant to showcase SQL database design, relationships between entities, usage of stored procedures and triggers, and implementing practical queries to manage data efficiently. 
Project will include both Oracle and MS SQL Server databases, to experiment with the database differences. The connecting point for both databases is a Python script, which handles flights and luggage traffic as well as produce basic data analysis. 

---

## Features

- **Flight Management**: Tracks flight details, including flight numbers, schedules, delays, and status.
- **Luggage Tracking**: Manages luggage details such as type, priority, weight, current location, and owner information.
- **Misplaced Luggage**: Maintains records of misplaced luggage, its recovery status, and location.
- **Data Relationships**: Implements relationships between flights, luggage, and misplaced luggage.
- **Stored Procedures and Triggers**: Uses stored procedures (PL/SQL and T-SQL) to manage all the airport and luggage logistics simulation.
- **Practical Queries**: Provides common SQL queries for managing and analyzing the system.

## Roadmap
[ ] - To-do
[x] - Done
[a] - Active: Curently working on it
[p] - Partially complete, the rest to be done later. Missing part, marked with {m}
[?] - Not yet confirmed for implementation
[!] - Problem (BUG) in the simulation / code


=======================================================================
APP Enhancements
=======================================================================

[ ] Add PyQt6 UI 
    - add buttons to manipulate simulation and data settings
    - display with all simulation data


=======================================================================
Code Optimization
=======================================================================

[ ] Remove magic numbers, but concisely use ENUMS and Oracle Type for LUGGAGE_LOCATION registry IDs
[ ] Optimise luggage creation ... right now it is extremely slow!!

=======================================================================
SIMULATION STEPS - Simulate each hour in a day
=======================================================================

1. arriving flights: luggage number = aircraft capacity
2. departing flights: luggage number = aircraft capacity + returning luggage + delayed luggage



--> [x] [DB] Uptick one hour

--> [x] [DB] Generate all flights for current hour
    - incoming flights
    - departing flights

--> [x] [Python] Generate luggage for all arriving flights for current hour
    - incoming flights luggage:
        - each flight gets same number of luggage as airplane's capacity
        - each luggage is assigned a random owner name
        - each luggage is designated a final destination (final destination / continuing on the same flight / connecting flight)

--> [x] [Python] Simulate delays for all flights for current hour
    - incoming delays
    - departing delays

--> [ ] [Python] Generate luggage for all departing flights for current hour*
    - departing flights luggage:
        - each flight gets transfer luggage, checked-in luggage and returning luggage
        - each checked-in luggage is assigned a random owner name
        - departing flights carry luggage of four types (1. checked in luggage, 2. continuing same flight, 3. from connecting flight, 4. forwarding delayed luggage-this is done in step two on DB)

* if luggage is traveling on a connected flight count it luggage for the connecting flight's capacity as well


--> [a] [DB] Process all luggage for current hour
    - process all the luggage in the system (for that hour)
        - to connecting flight (+ luggage that missed previous flight)
        - to Baggage Claim Area
        - Unclaimed Baggage Department (if it was returned)


  

--> [ ] [DB] End of each day
    - process all luggage that needs to be transfered to a different department

=========
[!] Flights that are delayed to another day are not processed by simulation!!


=========
[?] Add additional luggage pick up and check in for connecting flights on anoter airline
[?] Simulate cabin classes - higher class, less missandeling of luggage

===================================

- simulate status of each luggage
    - luggage misshandeling
    - missed connecting flight (goes to Baggage Service Office until next flight)
    - not claimed (+ check for luggage from up to past 3 hours) (goes or remains in Unclaimed Baggage Department)
 



=======================================================================
Luggage Lifecycle:
=======================================================================
In Flight 0
Baggage Claim Area 3
With Owner (Picked Up) 0
Lost & Found Department 720
Baggage Service Office 168
Unclaimed Baggage Department 1992
Disposed Luggage Area 0

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
                a. (95%) Claimed by a passenger within 60 days
                b. (5%) Not claimed for 83 days --> Disposed Luggage Area
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
 
=======================================================================
Possible luggage problems
=======================================================================

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

============================================================================

Statistics on Lost Luggage
- Delayed Bags: Around 85% of "lost" luggage is simply delayed and is usually returned to the passenger within a few days 
- Permanently Lost Bags: Only about 3% of luggage is permanently lost or stolen 
- Recovery Rate: Approximately 97% of lost luggage is eventually returned to its owner 


=======================================================================
Flight Delays
=======================================================================
- Average number of delayed flights per day: 25%
- Average delays:
    - Minor Delays  (15-59 minutes): ~80% of all delays.
    - Severe Delays (60+ minutes): ~20% of all delays.
