"""Helper functions for fex."""

import csv


def write_csv_from_dict(features, dataset_path):
    """Write the internal fex datastore to disc as CSV.

    Fex records the combined results of all feature extractors in a dictionary
    with the shape: `{'row_id': {'col_1': value1, 'col_2': value2}, ...}`.
    This function flattens this nested structure and writes it to disc as CSV.
    """
    col_names = set()
    for row_id, values in features.items():
        col_names.update(values.keys())
        values['id'] = row_id

    col_names_with_id = ['id'] + list(col_names)
    with open(dataset_path, 'w') as f:
        w = csv.DictWriter(f, col_names_with_id)
        w.writeheader()
        w.writerows(features.values())
