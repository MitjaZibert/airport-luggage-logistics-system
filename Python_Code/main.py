# ===========================================================================================
# Airport Luggage Logistics System
# ===========================================================================================


# System libraries imports
import pandas as pd
import numpy as np


# Win_Main class
class StartSimulation():
    
    def __init__(self):
        None

    countries = pd.read_csv('DB_Model/countries_temp.csv')
    unique_names = countries.drop_duplicates()
    print(unique_names) 
    unique_names_df = pd.DataFrame(unique_names, columns=['country'])
    unique_names_df.to_csv('countries_unique.csv', index=False)
    print(unique_names_df) 
    
# =================================================

def main():
    # Create an instance of StartSimulation
    simulation = StartSimulation()
    

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



