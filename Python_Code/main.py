# ===========================================================================================
# Airport Luggage Logistics System - MAIN
# ===========================================================================================


# System libraries imports
import pandas as pd
import numpy as np

# App imports
from flights_simulation import FlightsSimulation

# =================================================

def main():
    # Create an instance of StartSimulation
    flights_simulation = FlightsSimulation()
    flights_simulation.start_flights_simulation()
    

# =================================================
if __name__ == "__main__":
    try:
        main()
        
    except Exception as e:
        print(f"Error: {e}")  # Catch any exceptions

# *********************************************************************************************
# *********************************************************************************************
# NOTES
# *********************************************************************************************



