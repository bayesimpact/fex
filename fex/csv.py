"""Helper functions for fex."""

from __future__ import absolute_import
import csv


def dump_dict(features, dataset_path):
    """Write a dict of dict to disk as a CSV file.

    Input is expected in the shape of:
    `{'row_id': {'col_1': value1, 'col_2': value2}, ...}`.
    This function flattens this nested structure and writes it to disk as CSV.
    """
    col_names = set()
    for row_id, values in features.items():
        col_names.update(values.keys())
        values['id'] = row_id

    col_names_with_id = ['id'] + sorted(list(col_names))
    with open(dataset_path, 'w') as f:
        w = csv.DictWriter(f, col_names_with_id)
        w.writeheader()
        for _, values in sorted(features.items()):
            w.writerow(values)
