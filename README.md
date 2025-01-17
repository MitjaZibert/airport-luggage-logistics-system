# Airport Luggage Logistics System

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
