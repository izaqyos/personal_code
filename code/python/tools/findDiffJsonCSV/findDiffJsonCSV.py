import pandas as pd
import json

def find_entity_diff(csv_path, json_path, id_col='entity_id', type_col='entity_type'):
    """
    Compares a CSV result set with a JSON array of objects, identifying differences in entity IDs and types.

    Args:
        csv_path: Path to the CSV file.
        json_path: Path to the JSON file.
        id_col: Column name for entity ID in the CSV (default: 'entity_id').
        type_col: Column name for entity type in the CSV (default: 'entity_type').

    Returns:
        A dictionary containing:
            - "csv_only": Entities present only in the CSV.
            - "json_only": Entities present only in the JSON.
            - "type_mismatch": Entities with matching IDs but different types.
    """

    # Load CSV into DataFrame
    df_csv = pd.read_csv(csv_path, usecols=[id_col, type_col])

    # Load JSON array
    with open(json_path, 'r') as f:
        data_json = json.load(f)
    df_json = pd.DataFrame(data_json)

    # Merge and identify differences
    merged = df_csv.merge(df_json, on=id_col, how='outer', suffixes=('_csv', '_json'), indicator=True)

    results = {
        'csv_only': merged[merged['_merge'] == 'left_only'][[id_col, type_col + '_csv']].to_dict(orient='records'),
        'json_only': merged[merged['_merge'] == 'right_only'][[id_col, type_col + '_json']].to_dict(orient='records'),
        'type_mismatch': merged[(merged['_merge'] == 'both') & (merged[type_col + '_csv'] != merged[type_col + '_json'])]
                                    [[id_col, type_col + '_csv', type_col + '_json']].to_dict(orient='records')
    }

    return results

# Example usage
csv_file = 'your_result_set.csv'
json_file = 'your_entity_data.json'
results = find_entity_diff(csv_file, json_file)
print(results)
