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
        self.max_hours_connecting_flight = None
        self.continuing_flight_luggage_percentage = None
        self.connecting_flight_luggage_percentage = None

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
        self.max_hours_connecting_flight = settings_file['app_settings']['max_hours_connecting_flight']
        self.max_hours_connecting_flight = int(self.max_hours_connecting_flight)
        self.continuing_flight_luggage_percentage = settings_file['app_settings']['continuing_flight_luggage_percentage']
        self.continuing_flight_luggage_percentage = int(self.continuing_flight_luggage_percentage)
        self.connecting_flight_luggage_percentage = settings_file['app_settings']['connecting_flight_luggage_percentage']
        self.connecting_flight_luggage_percentage = int(self.connecting_flight_luggage_percentage)
        
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
        DBUtil.db_truncate_table("departing_flights")

        
        #self.process_arriving_flights(7, 7)
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # Check if AIRPORT_SIMULATION_DATA exists - if not, insert default data
        sql = "SELECT max(hour_length_in_seconds) FROM AIRPORT_SIMULATION_DATA"
        query_result = DBUtil.db_query(sql)
        data = query_result[0][0]
        if data is None:
            params = {'airport_iata': self.airport_iata, 
                      'hour_lenght_in_seconds': self.hour_lenght_in_seconds, 
                      'max_hours_connecting_flight': self.max_hours_connecting_flight}
            
            sql = "INSERT INTO AIRPORT_SIMULATION_DATA VALUES (:airport_iata, 0, 1, 0, :hour_lenght_in_seconds, :max_hours_connecting_flight)"
            
            DBUtil.db_insert(sql, params)

            DBUtil.db_commit() # COMMIT new db entries
                
        
        self.simulate_week_hours() # Start simulation of one week
        
        DBUtil.db_commit() # COMMIT new db entries
                
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
                
                params = {"week": week, 
                          "day": day, 
                          "hour": hour_of_day}

                sql = "UPDATE AIRPORT_SIMULATION_DATA SET week = :week, day_of_week = :day, hour_of_day = :hour"

                DBUtil.db_update(sql, params)
                
                DBUtil.db_commit() # COMMIT AIRPORT_SIMULATION_DATA update to make sure DB triggers and procedures were processed

                print(str(day) + " - " + str(hour_of_day))
                
                self.generate_arriving_flights_luggage(day, hour_of_day)
                
                self.simulate_active_flights_delays(day, hour_of_day)

                
                time.sleep(hour_in_seconds)  # Pause for x seconds (for simulation purpose only)
        

    # ===========================================================================================
    # Calculculate delayed time
    # def _calculate_delayed_time(self, arrival_time, delay_minutes):
    #         arrival_hour =int(arrival_time[:2].replace(':', ''))
    #         arrival_minutes = int(arrival_time[-2:])

    #         temp_minutes = arrival_minutes + delay_minutes
    #         new_arrival_hour = str(arrival_hour + (temp_minutes // 60))

    #         new_arrival_minutes = str(temp_minutes % 60)
    #         new_arrival_minutes = new_arrival_minutes.zfill(2) # add leading zero if only one char
            
            
    #         actual_arrival_time = new_arrival_hour + ":" + new_arrival_minutes

    #         return actual_arrival_time


    # ===========================================================================================
    # Simulate delays on all flights arriving and departing at self.airport_iata on the simulated day and hour and simulate delays
    def simulate_active_flights_delays(self, day, hour_of_day):

        # ARRIVING FLIHTS
        # Simulate arriving flight delays - get a % of randomly selected arriving flights
        sql = f"""SELECT af.arriving_flight_id, s.scheduled_arrival_time
                        FROM arriving_flights SAMPLE({self.max_delays_percentage}) af 
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id 
                        WHERE s.days_of_week LIKE '%{day}%'
                        AND TO_NUMBER(TO_CHAR(s.scheduled_arrival_time, 'HH24')) = {hour_of_day}"""
        
 
        
        arriving_flights = DBUtil.db_query(sql)

        
        for flight in arriving_flights:
            delay_minutes = random.randint(10, self.max_delay_minutes)
            #scheduled_arrival_time = flight[1]
            #actual_arrival_time = self._calculate_delayed_time(arrival_time, delay_minutes)
            
            params = {"arriving_flight_id": flight[0], 
                      "scheduled_arrival_time":  flight[1],
                      "delay_minutes": delay_minutes}
            
            sql = """UPDATE arriving_flights
                        SET actual_arrival_time = :scheduled_arrival_time + NUMTODSINTERVAL(:delay_minutes,'MINUTE'), 
                            delay_minutes = :delay_minutes
                        WHERE arriving_flight_id = :arriving_flight_id """
                    
            DBUtil.db_update(sql, params)
        
        # DEPARTING FLIGHTS
        # Simulate departing flight delays - get a % of randomly selected departing flights
        sql = f"""SELECT df.departing_flight_id, s.scheduled_departure_time
                        FROM departing_flights SAMPLE({self.max_delays_percentage}) df 
                        INNER JOIN schedules s
                        ON df.schedule_id = s.schedule_id 
                        WHERE s.days_of_week LIKE '%{day}%'
                        AND TO_NUMBER(TO_CHAR(s.scheduled_departure_time, 'HH24')) = {hour_of_day}"""
        
 
        
        departing_flights = DBUtil.db_query(sql)

        
        for flight in departing_flights:
            delay_minutes = random.randint(10, self.max_delay_minutes)
            #scheduled_departure_time = flight[1]
            #actual_departure_time = self._calculate_delayed_time(scheduled_departure_time, delay_minutes)
            
            params = {"departing_flight_id": flight[0], 
                      "scheduled_departure_time": flight[1],
                      "delay_minutes": delay_minutes}
            
            sql = """UPDATE departing_flights
                        SET actual_departure_time = :scheduled_departure_time + NUMTODSINTERVAL(:delay_minutes,'MINUTE'), 
                            delay_minutes = :delay_minutes
                        WHERE departing_flight_id = :departing_flight_id """
                    
            DBUtil.db_update(sql, params)
        
    # ===========================================================================================
    # Generate new luggage for currently arriving flights
    def generate_arriving_flights_luggage(self, day, hour_of_day):

        # Simulate / generate new luggage for arriving flights within current hour
        params = {'day_of_week': f"%{day}%", 
                  'hour_of_day': hour_of_day}

        sql = """SELECT af.arriving_flight_id, s.from_airport_iata, ac.capacity
                        FROM arriving_flights af
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id
                        INNER JOIN aircrafts ac
                        ON ac.aircraft_iata = s.aircraft_iata
                        WHERE s.days_of_week LIKE :day_of_week
                        AND TO_NUMBER(TO_CHAR(s.scheduled_arrival_time, 'HH24')) = :hour_of_day
                        ORDER BY af.arriving_flight_id ASC"""
        
        arriving_flights = DBUtil.db_query(sql, params)
        
        luggage = []
        
        for flight in arriving_flights:
            for i in range(flight[2]):
                
                random_name = names.get_full_name() # Generates a random full name as the owner of the luggage

                luggage.append([self.arriving_flight_location_id, flight[0], flight[1], random_name])

        # INSERT luggage from luggage list
        if luggage:
            sql = "INSERT INTO luggage (luggage_location_id, active_flight_id, origin_airport_iata, owner_name) VALUES (:1, :2, :3, :4)"
            
            DBUtil.db_insert_many(sql, luggage) 

        # Simualate / determine luggage final destination
        # x% current flight's next (IF current flight actually continues) - self.continuing_flight_luggage_percentage
        # x% to other flights' next destinations - self.connecting_flight_luggage_percentage
        # All remaining luggage to current airport (self.airport_iata)


             
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
    
