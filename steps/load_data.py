import pandas as pd

import measurement_stats as mstats

from cauldron import project

df = pd.read_csv('../Measurements.csv')

measurements = []

measurement_keys = []

for toe in ['Left', 'Center', 'Right']:
    measurement_keys.append({
        'label': '{} Digit Length'.format(toe),
        'type': 'length',
        'keys': [
            '{}-Length'.format(toe),
            '{}-Length-Unc'.format(toe)
        ],
        'sources': [
            'Length-Small-{}'.format(toe),
            'Length-Large-{}'.format(toe)
        ]
    })

for side in ['Left', 'Right']:
    measurement_keys.append({
        'label': '{} Angle'.format(side),
        'type': 'angle',
        'keys': [
            '{}-Angle'.format(side),
            '{}-Angle-Unc'.format(side)
        ],
        'sources': [
            'Angle-Small-{}'.format(side),
            'Angle-Large-{}'.format(side)
        ]
    })

for index, row in df.iterrows():
    entry = {'drawing': index}

    for key_data in measurement_keys:
        small = row[key_data['sources'][0]]
        large = row[key_data['sources'][1]]

        value = mstats.ValueUncertainty(
            0.5 * (small + large),
            max(0.5, 0.5 * abs(large - small))
        )

        entry[key_data['keys'][0]] = value.raw
        entry[key_data['keys'][1]] = value.raw_uncertainty

    entry['Width-Box'] = row['W-Box']
    entry['Height-Box'] = row['H-Box']
    measurements.append(entry)

df = pd.DataFrame(measurements)
project.shared.measurement_keys = measurement_keys
project.shared.measurements = df
project.shared.normalized_values = []
# project.display.table(df, scale=0.5)
