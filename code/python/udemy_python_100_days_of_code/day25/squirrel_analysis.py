#!/opt/homebrew/bin/python3
"""
source: https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw
downloaded csv file: 2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20231219.csv
"""
import pandas

def load_dataframe():
    datafname = '2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20231219.csv'
    dataframe = pandas.read_csv(datafname)
    return dataframe

def count_colors():
    """
chatgpt: To count the number of rows with a specific value in a DataFrame using pandas in Python, you can use the `sum()` function along with a boolean condition. Here's an example:

```python
import pandas as pd

# Create a sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 25, 35],
        'City': ['New York', 'San Francisco', 'New York', 'Los Angeles']}

df = pd.DataFrame(data)

# Count the number of rows where the 'City' column has a specific value, e.g., 'New York'
specific_value = 'New York'
count_rows = (df['City'] == specific_value).sum()

print(f"Number of rows with '{specific_value}' in the 'City' column: {count_rows}")
```

In this example, `df['City'] == specific_value` creates a boolean Series where each element is `True` if the corresponding row has the specified value in the 'City' column and `False` otherwise. The `.sum()` function then counts the number of `True` values, which corresponds to the number of rows with the specific value.

Adjust the column name and specific value according to your DataFrame and requirements.
    """
    pass

def main():
    data = load_dataframe()
    color_column_key = 'Primary Fur Color'
    fur_colors = data[color_column_key].unique().tolist()
    del fur_colors[0]
    fur_colors_count =[]
    for color in fur_colors:
        fur_colors_count.append( (data[color_column_key] == color).sum() )
    print(f"Extract these unique fur colors from DataFrame: {fur_colors} and their counts {fur_colors_count}")
    output_df = pandas.DataFrame( { 'Fur Color': fur_colors,
                 'Count': fur_colors_count,
            })
    print(output_df)
    ##get a series of booleans where the condition result is True/False
    #print((data[color_column_key] == color))
    ##get the rows in which for this column there's a specific value (like select in sql)
    #print(data[data[color_column_key] == color])




if __name__ == "__main__":
    main()

