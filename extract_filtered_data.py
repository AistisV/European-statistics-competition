import pandas as pd
import numpy as np
import re
import json
from io import StringIO

# ----------------------------
# LOAD CONFIGURATION FROM JSON FILE
# ----------------------------

def load_config(config_file='config.json'):
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load the configuration
CONFIG = load_config()

# ----------------------------
# FILTER EUROSTAT DATA FUNCTION
# ----------------------------

def filter_eurostat_data(input_file, output_file, age_groups=None, min_year=None):
    # Read the raw content
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # Fix "number b number" -> "number \t number" in memory
    fixed_content = re.sub(r'(\d+\.\d+)\s*b\s*(\d+\.\d+)', r'\1\t\2', raw_content)

    df = pd.read_csv(StringIO(fixed_content), sep='\t', na_values=':')  # NaN for ": "

    # Split the metadata column
    df_split = df[CONFIG['columns']['metadata']].str.split(',', expand=True)
    expected_columns = [CONFIG['columns']['freq'], CONFIG['columns']['indic_is'], CONFIG['columns']['unit'], 
                        CONFIG['columns']['ind_type'], CONFIG['columns']['geo']]
    
    if df_split.shape[1] == len(expected_columns):
        df[expected_columns] = df_split
        df = df.drop(columns=[CONFIG['columns']['metadata']])
    else:
        print("Unexpected number of columns after split!")
        return

    # Clean values in the dataframe (convert to numeric)
    def clean_value(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, str):
            # Check for ": " and return NaN
            if val.strip() == ": ":
                return np.nan
            # Check for valid numeric value
            match = re.match(r'^-?\d+(\.\d+)?', val.strip())
            if match:
                return float(match.group())
            else:
                return np.nan
        return val

    # Apply cleaning to year columns
    year_columns = [col for col in df.columns if col.isdigit()]
    for col in year_columns:
        df[col] = df[col].apply(clean_value)

    # Filter the data based on 'indic_is', 'unit', and 'geo'
    df_filtered = df[
        (df[CONFIG['columns']['indic_is']] == CONFIG['indic_is_value']) & 
        (df[CONFIG['columns']['unit']] == CONFIG['unit_value']) & 
        (df[CONFIG['columns']['geo']].str.startswith(CONFIG['countries']['EU27_2020']) | df[CONFIG['columns']['geo']].str.contains(CONFIG['countries']['LT']))
    ]

    # Apply age group filter
    if age_groups:
        pattern = '^(' + '|'.join(age_groups) + ')$'
        df_filtered = df_filtered[df_filtered[CONFIG['columns']['ind_type']].str.match(pattern)]

    # Clean up column names
    df_filtered.columns = df_filtered.columns.str.strip()

    # Remove year columns earlier than min_year
    if min_year:
        valid_year_columns = [col for col in df_filtered.columns if col.isdigit() and int(col) >= min_year]
        metadata_columns = [CONFIG['columns']['freq'], CONFIG['columns']['indic_is'], CONFIG['columns']['unit'], 
                            CONFIG['columns']['ind_type'], CONFIG['columns']['geo']]
        df_filtered = df_filtered[metadata_columns + valid_year_columns]

    # Reverse columns (most recent year first)
    df_filtered = df_filtered.iloc[:, ::-1]

    # NDrop columns after missing data

    valid_year_columns = []
    for col in df_filtered.columns:
        if col.isdigit():
            if df_filtered[col].eq(': ').any():  # Specifically detect ": "
                break
            else:
                valid_year_columns.append(col)

    # Add metadata columns
    final_columns = [CONFIG['columns']['freq'], CONFIG['columns']['indic_is'], CONFIG['columns']['unit'], 
                     CONFIG['columns']['ind_type'], CONFIG['columns']['geo']] + valid_year_columns
    df_filtered = df_filtered[final_columns]

    df_filtered.to_csv(output_file, sep='\t', index=False)

    # -------------------
    # Create readable tsv files for graph making
    # -------------------

    # Helper to make chart-friendly format
    def create_chart_friendly(df, country_code, output_name):
        country_df = df[df[CONFIG['columns']['geo']].str.contains(country_code)]

        if country_df.empty:
            print(f"No data found for {country_code}")
            return
        
        data = {}
        for age_group in age_groups:
            label = CONFIG['age_groups'][age_group]  # Use the age group labels from CONFIG
            age_df = country_df[country_df[CONFIG['columns']['ind_type']] == age_group]
            if not age_df.empty:
                years = [col for col in age_df.columns if col.isdigit()]
                years = sorted(years)  # Reverse for output (earliest ➔ latest)
                data[label] = age_df[years].values.flatten()

        if not data:
            print(f"No age group data found for {country_code}")
            return

        # Build final DataFrame
        years_sorted = sorted([int(col) for col in years])
        result_df = pd.DataFrame({'Year': years_sorted})
        for label, values in data.items():
            result_df[label] = values

        # Save to tsv
        result_df.to_csv(output_name, sep='\t', index=False)
        print(f"Saved readable file: {output_name}")

    # Create readable TSVs
    create_chart_friendly(df_filtered, CONFIG['countries']['EU27_2020'], CONFIG['output_folder'] + 'readable_EU.tsv')
    create_chart_friendly(df_filtered, CONFIG['countries']['LT'], CONFIG['output_folder'] + 'readable_LT.tsv')

input_file = CONFIG['input_folder'] + 'estat_isoc_ci_ac_i.tsv'
output_file = CONFIG['output_folder'] + 'filtered_data.tsv'
user_input_age_groups = ['Y16_24', 'Y25_64']
user_min_year = 2015

filter_eurostat_data(input_file, output_file, age_groups=user_input_age_groups, min_year=user_min_year)
