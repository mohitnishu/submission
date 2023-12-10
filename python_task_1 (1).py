import pandas as pd

def generate_car_matrix(df):
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    matrix_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    for i in range(min(matrix_df.shape)):
        matrix_df.iat[i, i] = 0
    
    return matrix_df

dataset_df = pd.read_csv('dataset-1.csv')
result_df = generate_car_matrix(dataset_df)
print(result_df)





def get_type_count(df):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_type_counts = {k: type_counts[k] for k in sorted(type_counts)}
    return sorted_type_counts


dataset_df = pd.read_csv('dataset-1.csv')
result_dict = get_type_count(dataset_df)
print(result_dict)



def get_bus_indexes(df):
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    bus_mean = df['bus'].mean()
    indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    indexes.sort()
    return indexes


dataset_df = pd.read_csv('dataset-1.csv')
result_indexes = get_bus_indexes(dataset_df)
print(result_indexes)


def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    avg_truck_per_route = df.groupby('route')['truck'].mean()
    filtered_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()    
    filtered_routes.sort()
    return filtered_routes


dataset_df = pd.read_csv('dataset-1.csv')
result_routes = filter_routes(dataset_df)
print(result_routes)


def multiply_matrix(matrix):
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame): Input DataFrame

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)    
    modified_matrix = modified_matrix.round(1)
    
    return modified_matrix


result_df = pd.DataFrame(...)
modified_result_df = multiply_matrix(result_df)
print(modified_result_df)



def time_check(df):
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: Return a boolean series indicating if each (id, id_2) pair has incorrect timestamps
    """
    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = df['end'] - df['start']
    completeness_check = df.groupby(['id', 'id_2']).apply(lambda x: 
        (x['duration'].min() >= pd.Timedelta(days=7)) and 
        (x['start'].min().time() == pd.Timestamp('00:00:00').time()) and 
        (x['end'].max().time() == pd.Timestamp('23:59:59').time())
    )
    
    return completeness_check

dataset_2_df = pd.read_csv('dataset-2.csv')
result_series = time_check(dataset_2_df)
print(result_series)
