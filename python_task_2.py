
import pandas as pd

def calculate_distance_matrix(df):
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    distance_pivot = df.pivot_table(index='start_location', columns='end_location', values='distance', aggfunc='sum')
    distance_pivot = distance_pivot.fillna(0)
    distance_matrix = pd.DataFrame(distance_pivot)
    distance_matrix = distance_matrix + distance_matrix.T
    
    for idx in distance_matrix.index:
        distance_matrix.loc[idx, idx] = 0
    
    return distance_matrix

dataset_3_df = pd.read_csv('dataset-3.csv')
result_distance_matrix = calculate_distance_matrix(dataset_3_df)
print(result_distance_matrix)



def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    df = df.reset_index()
    unrolled_df = pd.melt(df, id_vars='index', var_name='id_end', value_name='distance')
    unrolled_df = unrolled_df.rename(columns={'index': 'id_start'})
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]
    unrolled_df = unrolled_df.sort_values(by=['id_start', 'id_end']).reset_index(drop=True)
    
    return unrolled_df

result_distance_matrix = pd.DataFrame()
unrolled_df = unroll_distance_matrix(result_distance_matrix)
print(unrolled_df)



def find_ids_within_ten_percentage_threshold(df, reference_id):
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold_min = reference_avg_distance * 0.9
    threshold_max = reference_avg_distance * 1.1
    ids_within_threshold = df.groupby('id_start')['distance'].mean()
    ids_within_threshold = ids_within_threshold[(ids_within_threshold >= threshold_min) & (ids_within_threshold <= threshold_max)]
    result_df = pd.DataFrame(ids_within_threshold).reset_index().sort_values(by='id_start')
    
    return result_df

unrolled_df = pd.DataFrame()
reference_id = 123
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(result_within_threshold)



def calculate_toll_rate(df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle_type, rate in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate
    
    return df

unrolled_df = pd.DataFrame()
result_with_toll_rates = calculate_toll_rate(unrolled_df)
print(result_with_toll_rates)

import datetime

def calculate_time_based_toll_rates(df):
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    weekday_discount_factors = {
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0)): 0.8,
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0)): 1.2,
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59)): 0.8
    }
    
    weekend_discount_factor = 0.7
    for index, row in df.iterrows():
        if row['start_time'].weekday() < 5:
            for time_range, discount_factor in weekday_discount_factors.items():
                if time_range[0] <= row['start_time'].time() <= time_range[1]:
                    for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
                        df.at[index, vehicle_type] *= discount_factor
        else:
            for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
                df.at[index, vehicle_type] *= weekend_discount_factor
    
    return df

time_based_df = pd.DataFrame(...)
result_with_time_based_rates = calculate_time_based_toll_rates(time_based_df)
print(result_with_time_based_rates)
