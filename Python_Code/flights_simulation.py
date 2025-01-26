# ===========================================================================================
# Airport Luggage Logistics System - Flights Simulation
# ===========================================================================================


# System libraries imports
import oracledb
import names
import time
import random

# App imports
from db_util import DBUtil


# Win_Main class
class FlightsSimulation:
    
    def __init__(self):
        # Simulation parameters
        self.airport_iata = 'ORD' # Airport that is being simulated (e,g, 'ORD' = Chicago O'Hare International Airport)
        self.max_delays_percentage = 25
        self.max_delay_minutes = 150
        
    # ===========================================================================================
    def start_flights_simulation(self):
        DBUtil.get_conn()


        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
        # TESTING CODE
        #sql = "TRUNCATE TABLE luggage"
        DBUtil.db_truncate_table("luggage")
        #sql = "TRUNCATE TABLE arriving_flights"
        DBUtil.db_truncate_table("arriving_flights")

        
        self.process_arriving_flights(7, 7)
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Start simulation of one week
        #self.simulate_week_hours(cursor)

                
        
        DBUtil.close_conn()

    # ===========================================================================================
    # Simulate each hour of the week
    def simulate_week_hours(self, cursor):
        
        
        # get length of 1 hour in seconds
        sql = "SELECT max(hour_length_in_seconds) FROM AIRPORT_SIMULATION_DATA"
        hour_length_in_seconds = DBUtil.db_query(sql)
        hour_in_seconds = hour_length_in_seconds[0]
        
        # increase week number by 1
        sql = "UPDATE AIRPORT_SIMULATION_DATA SET week = week + 1"
        DBUtil.db_update(sql)

        # Process all 7 days
        for day in range(1, 8): 
            params = {"day": day}
            sql = "UPDATE AIRPORT_SIMULATION_DATA SET day_of_week = :day"
            DBUtil.db_update(sql, params)

            # Process all 24 hours
            for hour in range(24):
                hour_of_day = str(hour)+":00"

                params = {"hour": hour_of_day}
                sql = "UPDATE AIRPORT_SIMULATION_DATA SET hour_of_day = :hour"
                DBUtil.db_update(sql, params)
        
                print(str(day) + " - " + hour_of_day)
                
                self.process_arriving_flights(cursor, day, hour_of_day)
                #self.process_departing_flights(cursor, day, hour_of_day)
                
                time.sleep(hour_in_seconds)  # Pause for x seconds

    
    # ===========================================================================================
    # Calculculate delayed time
    def _calculate_delayed_time(self, arrival_time, delay_minutes):
            arrival_hour =int(arrival_time[:2].replace(':', ''))
            arrival_minutes = int(arrival_time[-2:])

            temp_minutes = arrival_minutes + delay_minutes
            new_arrival_hour = str(arrival_hour + (temp_minutes // 60))

            new_arrival_minutes = str(temp_minutes % 60)
            new_arrival_minutes = new_arrival_minutes.zfill(2) # add leading zero if only one char
            
            
            actual_arrival_time = new_arrival_hour + ":" + new_arrival_minutes

            return actual_arrival_time


    # ===========================================================================================
    # Process all flights arriving at self.airport_iata on the simulated day and hour and simulate delays
    def process_arriving_flights(self, day, hour):

        # Call initialize_arraving_flights DB procedure to save all relevant flights
        DBUtil.db_procedure_no_return (procedure_name="initialize_arraving_flights", 
                                      params_in=[self.airport_iata, day, hour])

       
        # Simulate arriving flight delays - get a % of randomly selected arriving flights
        sql = f"""SELECT arriving_flight_id, scheduled_arrival_time
                        FROM arriving_flights
                        SAMPLE ({self.max_delays_percentage})"""
                
        
        arriving_flights = DBUtil.db_query(sql)

        
        for flight in arriving_flights:
            delay_minutes = random.randint(10, self.max_delay_minutes)
            arrival_time = flight[1]
            actual_arrival_time = self._calculate_delayed_time(arrival_time, delay_minutes)
            
            params = {"arriving_flight_id": flight[0], 
                      "actual_arrival_time": actual_arrival_time,
                      "delay_minutes": delay_minutes}
            
            sql = """UPDATE arriving_flights
                        SET actual_arrival_time = :actual_arrival_time, 
                            delay_minutes = :delay_minutes
                        WHERE arriving_flight_id = :arriving_flight_id """
                    
            DBUtil.db_update(sql, params)
        
        

        # Simulate luggage for currently active flights
        sql = """SELECT af.arriving_flight_id, af.actual_arrival_time, ac.capacity
                        FROM arriving_flights af
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id
                        INNER JOIN aircrafts ac
                        ON ac.aircraft_iata = s.aircraft_iata
                        ORDER BY af.arriving_flight_id ASC"""
        
        
        arriving_flights = DBUtil.db_query(sql)
        
        luggage_location_id = 1
        luggage = []

        for flight in arriving_flights:
            # Generate a random full name
            random_name = names.get_full_name()

            luggage.append([luggage_location_id, flight[0], random_name])

        # SQL statement with bind variables
        #sql = "INSERT INTO luggage (luggage_location_id, active_flight_id, owner_name) VALUES (:1, :2, :3)"

       
        # Execute the statement for all rows
        #cursor.executemany(sql, luggage)

        

        # COMMIT new db entries
        DBUtil.db_commit()


    # ===========================================================================================
    # Process all flights departing from self.airport_iata on the simulated day and hour and simulate delays
    # def process_departing_flights(self, cursor, day, hour):
        
    #     # Find all relevant flights and simulate delays
    #     day_of_week = f"%{day}%"
    #     params = {"airport_iata": self.airport_iata, 
    #               "day_of_week": day_of_week, 
    #               "hour_of_day": hour}
        
    #     sql = """SELECT schedule_id, departure_time
    #                     FROM schedules
    #                     WHERE from_airport_iata = :airport_iata
    #                     and days_of_week LIKE :day_of_week
    #                     AND REPLACE(SUBSTR(departure_time, 1, 2), ':', '') = :hour_of_day"""
        
        
    #     cursor.execute(sql, params)
    
