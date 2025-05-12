"""
Generate dummy data for the patients table based on DATA_CONFIG
Data is saved to a SQLite database in the root directory of this repo

Execute from the root directory of this repo:
    python scripts/generate_data.py
"""
import random
from datetime import datetime, timedelta
import sqlite3
import pandas as pd

# Configuration dictionary for columns and their possible values/ranges
DATABASE_NAME = 'sample.sqlite'
TABLE_NAME = 'patients'
DATA_CONFIG = {
    'PATIENT_ID': 1000,       # Starting sequence number
    'AGE': [12, 89],   
    'GENDER': ['M', 'F'],
    'RACE': ['White', 'Black', 'Asian', 'Other'],
    'ETHNICITY': ['Hispanic', 'Non-Hispanic'],
    'HOSPITAL_DATE': [datetime(2022, 1, 1), datetime(2025, 1, 1)], 
    'HOSPITALIZATION_COUNT': [1, 10],  
    'IS_SMOKER': bool
}

def generate_value(column_name, config):
    """Generate a single value based on column configuration"""
    value_config = config[column_name]

    if isinstance(value_config, int):  # Sequence
        return None
    
    elif isinstance(value_config, list):
        if isinstance(value_config[0], datetime):  # Date range
            days_between = (value_config[1] - value_config[0]).days
            random_days = random.randint(0, days_between)
            random_date = value_config[0] + timedelta(days=random_days)
            return random_date.date()
        elif isinstance(value_config[0], (int, float)):  # Numeric range
            return random.randint(value_config[0], value_config[1])
        else:  # String list
            return random.choice(value_config)
    
    elif value_config == bool:
        return random.choice([True, False])
    
    else:
        raise ValueError(f"Invalid configuration for column: {column_name}")
        
def generate_dataset(n_rows: int, config: dict) -> pd.DataFrame:
    """Generate a dataset based on configuration"""
    data = {}
    
    for column, col_config in config.items():
        if isinstance(col_config, int):  # Sequence
            data[column] = list(range(col_config, col_config + n_rows))

        elif isinstance(col_config, list) or col_config == bool:
            data[column] = [generate_value(column, config) for _ in range(n_rows)]
    
    return pd.DataFrame(data)

def save_to_sqlite(df, database_name, table_name):
    """Save the generated dataset to SQLite database"""
    conn = sqlite3.connect(database_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def main():
    # Generate the dataset
    n_rows = 100
    df = generate_dataset(n_rows, DATA_CONFIG)
    
    # Save to SQLite
    save_to_sqlite(df, DATABASE_NAME, TABLE_NAME)
    
    print(f"Generated {n_rows} rows of data and saved to {DATABASE_NAME}")
    print("\nFirst few rows of generated data:")
    print(df.head())

if __name__ == "__main__":
    main()
