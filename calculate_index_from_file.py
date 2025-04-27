import pandas as pd
import json

# ----------------------------
# Load configuration from file
# ----------------------------

def load_config(config_file='config.json'):
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load the configuration
CONFIG = load_config()

# ----------------------------
# Influence Index Calculation
# ----------------------------

def calculate_slope(values):
    return (values[-1] - values[0]) / (len(values) - 1) if len(values) > 1 else 0

def influence_index(gen_z, older):
    m_g = calculate_slope(gen_z)
    m_o = calculate_slope(older)

    if m_o == 0:
        return 0.0
    if m_g == 0:
        return m_o
    if (m_g > 0 and m_o > 0) or (m_g < 0 and m_o < 0):
        return round(m_o / m_g, 1)  # Round to 1 decimal place
    else:
        return round(-abs(m_o / m_g), 1)  # Round to 1 decimal place

def calculate_influence_from_file(filtered_file):
    df_filtered = pd.read_csv(filtered_file, sep='\t')

    for country_code in CONFIG['countries'].values():
        if country_code == CONFIG['countries']['EU27_2020']:
            region_name = CONFIG['countries']['EU27_2020']
            region_data = df_filtered[df_filtered[CONFIG['columns']['geo']] == CONFIG['countries']['EU27_2020']]
        else:
            region_name = CONFIG['countries']['LT']
            region_data = df_filtered[df_filtered[CONFIG['columns']['geo']].str.contains('LT')]

        gen_z_row = region_data[region_data[CONFIG['columns']['ind_type']] == 'Y16_24']
        older_row = region_data[region_data[CONFIG['columns']['ind_type']] == 'Y25_64']

        if gen_z_row.empty or older_row.empty:
            print(f"\n⚠️ Warning: Missing data for {region_name}. Skipping...")
            continue

        # Select year columns (starting from column index 5)
        gen_z = gen_z_row.iloc[:, 5:].values.flatten()
        older = older_row.iloc[:, 5:].values.flatten()

        # Reverse to make it earliest -> latest
        gen_z = gen_z[::-1]
        older = older[::-1]

        if len(gen_z) == 0 or len(older) == 0:
            print(f"\n⚠️ Warning: No valid values for {region_name}. Skipping...")
            continue

        if len(gen_z) != len(older):
            print(f"\n⚠️ Warning: Data length mismatch for {region_name}. Skipping...")
            continue

        # Print first and last datapoints
        print(f"\n{region_name} statistics:")
        print(f"Gen Z first year value: {gen_z[0]}")
        print(f"Gen Z last year value: {gen_z[-1]}")
        print(f"Older generations first year value: {older[0]}")
        print(f"Older generations last year value: {older[-1]}")

        # Calculate and print influence index
        index = influence_index(gen_z, older)
        print(f"Influence Index for {region_name}: {index}")

# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":
    calculate_influence_from_file(CONFIG['filtered_file'])
