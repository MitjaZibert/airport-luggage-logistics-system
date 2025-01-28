# ===========================================================================================
# Airport Luggage Logistics System - Flights Simulation
# ===========================================================================================


# System libraries imports
import names
import time
import random

# App imports
from db_util import DBUtil


# Win_Main class
class FlightsSimulation:
    
    def __init__(self):
        # Simulation parameters
        self.airport_iata = None # Airport that is being simulated (e,g, 'ORD' = Chicago O'Hare International Airport)
        self.max_delays_percentage  = None
        self.max_delay_minutes = None

        self.arriving_flight_location_id = None
        self.departing_flight_location_id = None

        self.initialize_settings()
        
    # ===========================================================================================
    def initialize_settings(self):
        from read_file import read_file

        settings_file = read_file(r'\settings.ini')

        # App settings (mainly for simulation purposes)
        self.airport_iata = settings_file['app_settings']['simulated_airport_iata']
        self.max_delays_percentage = settings_file['app_settings']['max_delays_percentage']
        self.max_delays_percentage = int(self.max_delays_percentage)
        self.max_delay_minutes = settings_file['app_settings']['max_delay_minutes']
        self.max_delay_minutes = int(self.max_delay_minutes)
        self.hour_lenght_in_seconds = settings_file['app_settings']['hour_lenght_in_seconds']
        self.hour_lenght_in_seconds = int(self.hour_lenght_in_seconds)
        
        # Default DB values
        self.arriving_flight_location_id = settings_file['default_db_values']['arriving_flight_location_id']
        self.departing_flight_location_id = settings_file['default_db_values']['departing_flight_location_id']
        
    
    # ===========================================================================================
    def start_flights_simulation(self):
        DBUtil.get_conn()

        DBUtil.db_truncate_table("db_trigger_log")
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!        
        # TESTING CODE
        DBUtil.db_truncate_table("luggage")
        DBUtil.db_truncate_table("arriving_flights")

        
        #self.process_arriving_flights(7, 7)
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # Check if AIRPORT_SIMULATION_DATA exists - if not, insert default data
        sql = "SELECT max(hour_length_in_seconds) FROM AIRPORT_SIMULATION_DATA"
        query_result = DBUtil.db_query(sql)
        data = query_result[0][0]
        if data is None:
            params = {'airport_iata': self.airport_iata, 'hour_lenght_in_seconds': self.hour_lenght_in_seconds}
            sql = "INSERT INTO AIRPORT_SIMULATION_DATA VALUES (:airport_iata, 0, 1, 0, :hour_lenght_in_seconds)"
            DBUtil.db_insert(sql, params)
            # COMMIT new db entries
            DBUtil.db_commit()
                

        # Start simulation of one week
        self.simulate_week_hours()

                
        DBUtil.close_conn()

    # ===========================================================================================
    # Simulate each hour of the week
    def simulate_week_hours(self):
        
        
        # get length of 1 hour in seconds
        sql = "SELECT max(week), max(hour_length_in_seconds) FROM AIRPORT_SIMULATION_DATA"
        query_result = DBUtil.db_query(sql)
        week = query_result[0][0]
        week += 1
        
        hour_in_seconds = query_result[0][1]
        

        # Process all 7 days
        for day in range(1, 2): #(1, 8) 
            # Process all 24 hours
            for hour_of_day in range(8): #range(24):
                print(str(day) + " - " + str(hour_of_day))
                
                params = {"week": week, "day": day, "hour": hour_of_day}
                sql = "UPDATE AIRPORT_SIMULATION_DATA SET week = :week, day_of_week = :day, hour_of_day = :hour"
                DBUtil.db_update(sql, params)
                
                DBUtil.db_commit() # COMMIT AIRPORT_SIMULATION_DATA update to make sure DB triggers and procedures were processed


                self.process_arriving_flights()
                #self.process_departing_flights(cursor, day, hour_of_day)

                self.generate_new_luggage()
                
                time.sleep(hour_in_seconds)  # Pause for x seconds (for simulation purpose only)
        

    
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
    def process_arriving_flights(self):

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
        
    # ===========================================================================================
    # Generate new luggage for currently arriving and departing flights
    def generate_new_luggage(self):


        # Simulate luggage for all arriving flights
        sql = """SELECT af.arriving_flight_id, ac.capacity
                        FROM arriving_flights af
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id
                        INNER JOIN aircrafts ac
                        ON ac.aircraft_iata = s.aircraft_iata
                        ORDER BY af.arriving_flight_id ASC"""
        
        
        arriving_flights = DBUtil.db_query(sql)
        
        luggage = []

        for flight in arriving_flights:
            random_name = names.get_full_name() # Generates a random full name as the owner of the luggage

            luggage.append([self.arriving_flight_location_id, flight[0], random_name])

        # SQL statement with bind variables
        sql = "INSERT INTO luggage (luggage_location_id, active_flight_id, owner_name) VALUES (:1, :2, :3)"

        # Execute INSERT statement for all items in luggage list
        DBUtil.db_insert_many(sql, luggage)

        

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
    
