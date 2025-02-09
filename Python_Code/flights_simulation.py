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
        self.simulation_week = 0
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

        

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        # Check if AIRPORT_SIMULATION_DATA exists - if not, insert default data
        sql = "SELECT max(hour_length_in_seconds) FROM AIRPORT_SIMULATION_DATA"
        query_result = DBUtil.db_query(sql)
        data = query_result[0][0]
        if data is None:
            params = {'airport_iata': self.airport_iata, 
                      'week': self.simulation_week,
                      'hour_lenght_in_seconds': self.hour_lenght_in_seconds, 
                      'max_hours_connecting_flight': self.max_hours_connecting_flight}

            sql = """INSERT INTO AIRPORT_SIMULATION_DATA (airport_iata, week, day_of_week, hour_of_day, hour_length_in_seconds, max_hours_connecting_flight)
                    VALUES (:airport_iata, :week, 1, 0, :hour_lenght_in_seconds, :max_hours_connecting_flight)"""
            
            DBUtil.db_insert(sql, params)

            DBUtil.db_commit() # COMMIT new db entries
                
        # ====== START SIMULATION PROCESS
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
        self.simulation_week = week + 1
        
        hour_in_seconds = query_result[0][1]
        

        # Process all 7 days
        for day in range(1, 2): # range(1, 8)
            # Process all 24 hours
            for hour_of_day in range(10, 16): # range(24)
                
                params = {"week": self.simulation_week, 
                          "day": day, 
                          "hour": hour_of_day}

                sql = "UPDATE AIRPORT_SIMULATION_DATA SET week = :week, day_of_week = :day, hour_of_day = :hour"

                DBUtil.db_update(sql, params)
                
                DBUtil.db_commit() # COMMIT AIRPORT_SIMULATION_DATA update to make sure DB triggers and procedures were processed

                
                #
                # ====== START SIMULATION STEPS
                #
                
                print("Simulation for day - hour: " + str(day) + " - " + str(hour_of_day))
                

                # Step 1: Generate luggage for arriving flights
                self.generate_arriving_flights_luggage(day, hour_of_day)
                
                # Step 2: Simulate flight delays
                self.simulate_active_flights_delays(day, hour_of_day)

                # Step 3: 

                #
                # ===============================
                #

                time.sleep(hour_in_seconds)  # Pause for x seconds (for simulation purpose only)

    
    # ===========================================================================================
    # Generate new luggage for currently arriving flights
    def generate_arriving_flights_luggage(self, day, hour_of_day):
        
        # Simulate / generate new luggage for arriving flights within current hour
        arriving_flights = []

        params = {'day_of_week': f'%{day}%', 
                  'hour_of_day': hour_of_day}
                
        sql = """SELECT af.schedule_id, af.arriving_flight_id, s.connecting_to_schedule, ac.capacity
                        FROM arriving_flights af
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id
                        INNER JOIN aircrafts ac
                        ON ac.aircraft_iata = s.aircraft_iata
                        WHERE s.days_of_week LIKE (:day_of_week)
                        AND TO_NUMBER(REPLACE(SUBSTR(s.scheduled_arrival_time, 1, 2), ':', ''))  = :hour_of_day
                        ORDER BY TO_NUMBER(SUBSTR(s.scheduled_arrival_time, -2)) ASC"""
        
        arriving_flights = DBUtil.db_query(sql, params)
        
        
        # x% current flight's next destination (IF current flight actually continues) - self.continuing_flight_luggage_percentage
        # x% to other flights' next destinations - self.connecting_flight_luggage_percentage
        # All remaining luggage to current airport (self.airport_iata)

        luggage = []
        
        for flight in arriving_flights:
            schedule_id = flight[0]
            arriving_flight_id = flight[1]
            capacity = flight[3]
            
            for i in range(capacity): # flight capacity
                
                # if None, luggage reached its final destination
                destination_schedule_id = None
                
                # see if luggage continues on the same flight (continuing flight)
                if flight[2]:
                    if random.randint(1, 100) <= self.continuing_flight_luggage_percentage: 
                        destination_schedule_id = flight[2]
                    
                # see if luggage continues on another flight (connecting flight)
                if not destination_schedule_id:
                 
                    if random.randint(1, 100) <= self.connecting_flight_luggage_percentage:
                        params = {'airport_iata': self.airport_iata, 
                                'schedule_id': schedule_id,
                                'day_of_week': f'%{day}%'}
                        
                        sql = """WITH arriving_flight AS (
                                            SELECT arriving_flight_id, scheduled_arrival_time
                                            FROM arriving_flights
                                            WHERE schedule_id = :schedule_id
                                            ),
                                    valid_flights AS (
                                            SELECT s.schedule_id, 
                                            ROW_NUMBER() OVER (PARTITION BY af.arriving_flight_id ORDER BY sys_guid()) AS rn_r
                                            FROM schedules s
                                            CROSS JOIN arriving_flight af
                                            WHERE s.from_airport_iata = :airport_iata
                                            AND s.days_of_week LIKE (:day_of_week)
                                            AND ROUND((TO_DATE(s.scheduled_departure_time, 'HH24:MI') - TO_DATE(af.scheduled_arrival_time, 'HH24:MI')) * 24 * 60) > 60
                                    )
                                    SELECT schedule_id
                                    FROM valid_flights
                                    WHERE rn_r = 1"""
                        
                        destination_schedule_id = DBUtil.db_query(sql, params)[0][0]

                
                
                random_name = names.get_full_name() # Generates a random full name as the owner of the luggage
                
                luggage.append([schedule_id, 
                                destination_schedule_id, 
                                self.arriving_flight_location_id, 
                                arriving_flight_id, 
                                random_name, 
                                self.simulation_week, 
                                day, 
                                hour_of_day])

                      
        # INSERT luggage from luggage list
        if luggage:
            sql = """INSERT INTO luggage (origin_schedule_id, 
                                            destination_schedule_id, 
                                            luggage_location_id, 
                                            arriving_flight_id, 
                                            owner_name,
                                            entry_week,
                                            entry_day,
                                            entry_hour) 
                                            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)"""
            
            DBUtil.db_insert_many(sql, luggage) 
            
    
    # ===========================================================================================
    # Simulate delays on all flights arriving and departing at self.airport_iata on the simulated day and hour and simulate delays
    def simulate_active_flights_delays(self, day, hour_of_day):

        # calculate delayed time, making sure it doesn't pass midnight
        def delayed_time (scheduled_arrival_time, delay_minutes):
            hour_org = scheduled_arrival_time[:2]
            hour_org = int(hour_org.replace(":", ""))

            minutes_org = scheduled_arrival_time[2:]
            minutes_org = int(minutes_org.replace(":", ""))

            hour_new = hour_org + ((delay_minutes + minutes_org) // 60)

            minutes_new = (delay_minutes + minutes_org) % 60
            minutes_new = str(minutes_new)
            minutes_new = minutes_new.zfill(2)

            time_new = str(hour_new) + ":" + minutes_new

            if hour_new > 23:
                time_new = "23:55"

            return time_new


        # =================
        # ARRIVING FLIHTS
        # =================
        
        # Simulate arriving flight delays - get a % of randomly selected arriving flights
        sql = f"""SELECT af.arriving_flight_id, s.scheduled_arrival_time
                        FROM arriving_flights SAMPLE({self.max_delays_percentage}) af 
                        INNER JOIN schedules s
                        ON af.schedule_id = s.schedule_id 
                        WHERE s.days_of_week LIKE '%{day}%'
                        AND TO_NUMBER(REPLACE(SUBSTR(s.scheduled_arrival_time, 1, 2), ':', '')) = {hour_of_day}"""
        
 
        
        arriving_flights = DBUtil.db_query(sql)

        
        for flight in arriving_flights:
            scheduled_arrival_time = flight[1]
            delay_minutes = random.randint(10, self.max_delay_minutes)
            actual_arrival_time = delayed_time(scheduled_arrival_time, delay_minutes)
            
            
            params = {"arriving_flight_id": flight[0], 
                      "actual_arrival_time":  actual_arrival_time,
                      "delay_minutes": delay_minutes}
            
            sql = """UPDATE arriving_flights
                        SET actual_arrival_time = :actual_arrival_time, 
                            delay_minutes = :delay_minutes
                        WHERE arriving_flight_id = :arriving_flight_id """
                    
            DBUtil.db_update(sql, params)
        
        # =================
        # DEPARTING FLIGHTS
        # =================
        
        # Simulate departing flight delays - get a % of randomly selected departing flights
        sql = f"""SELECT df.departing_flight_id, s.scheduled_departure_time
                        FROM departing_flights SAMPLE({self.max_delays_percentage}) df 
                        INNER JOIN schedules s
                        ON df.schedule_id = s.schedule_id 
                        WHERE s.days_of_week LIKE '%{day}%'
                        AND TO_NUMBER(REPLACE(SUBSTR(s.scheduled_departure_time, 1, 2), ':', '')) = {hour_of_day}"""
        
 
        
        departing_flights = DBUtil.db_query(sql)

        
        for flight in departing_flights:
            scheduled_departure_time = flight[1]
            delay_minutes = random.randint(10, self.max_delay_minutes)
            actual_departure_time = delayed_time(scheduled_departure_time, delay_minutes)
            
            params = {"departing_flight_id": flight[0], 
                      "actual_departure_time": actual_departure_time,
                      "delay_minutes": delay_minutes}
            
            sql = """UPDATE departing_flights
                        SET actual_departure_time = :actual_departure_time, 
                            delay_minutes = :delay_minutes
                        WHERE departing_flight_id = :departing_flight_id """
                    
            DBUtil.db_update(sql, params)