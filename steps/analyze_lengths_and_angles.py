import plotly.graph_objs as go
import numpy as np

from cauldron import plotting
from cauldron import project

import measurement_stats as mstats

df = project.shared.measurements

normalized_lengths = []
length_traces = []

normalized_angles = []
angle_traces = []

for key_data in project.shared.measurement_keys:
    if key_data['type'] == 'length':
        combined_normalized = normalized_lengths
        combined_traces = length_traces
    else:
        combined_normalized = normalized_angles
        combined_traces = angle_traces

    d = mstats.create_distribution(
        measurements=df[key_data['keys'][0]].tolist(),
        uncertainties=df[key_data['keys'][1]].tolist()
    )

    median = mstats.distributions.percentile(d)
    normalized = [100.0 * (v / median - 1.0) for v in d.measurements]
    combined_normalized += normalized

    x_values = list(np.arange(1, len(normalized), 1))
    y_values, y_uncertainties = mstats.values.unzip(normalized)

    combined_traces.append(go.Bar(
        x=x_values,
        y=y_values,
        error_y=dict(
            type='data',
            array=y_uncertainties,
            visible=True
        ),
        name=key_data['label'],
        marker=dict(
            color=plotting.get_color(len(combined_traces), 0.5)
        )
    ))

d = mstats.create_distribution(normalized_lengths)
mad = mstats.distributions.weighted_median_average_deviation(d, count=2048)
result = mstats.ValueUncertainty(0, mad)

project.display.text(
    """
    The plot below shows the three digit measurements
    (Left, Center, &amp; Right) for each sample drawing as a deviation from
    the median of each measurement collection with uncertainty. While there is
    obviously differences between samples, the combined distribution of
    measurements has only a &#177;3% deviation from the median, which is well
    within the expected bounds of measurement uncertainty for the sample.
    """
)

project.display.plotly(
    data=length_traces,
    layout=plotting.create_layout(
        title='Digit Length Measurements Deviations ({}%)'.format(
            result.html_label.split(' ', 1)[-1]
        ),
        x_label='Drawing Index (#)',
        y_label='Fractional Value (%)'
    )
)

d = mstats.create_distribution(normalized_angles)
mad = mstats.distributions.weighted_median_average_deviation(d, count=2048)
result = mstats.ValueUncertainty(0, mad)

project.display.text(
    """
    Then the splay angles (Left + Center &amp; Right + Center) were plotted
    in the same fashion as the above digit length plot. The overall deviations
    were larger with a &#177;6% deviation, but angular measurements are
    more susceptible to measurement error and still well within tolerance.
    It is interesting that the angular field measurements in the A16 field work
    typically exhibit around two times more measurement uncertainty than their
    length measurements, which strengthens the case for expecting higher angular
    uncertainties.
    """
)

project.display.plotly(
    data=angle_traces,
    layout=plotting.create_layout(
        title='Splay Angle Measurements Deviations ({}%)'.format(
            result.html_label.split(' ', 1)[-1]
        ),
        x_label='Drawing Index (#)',
        y_label='Fractional Value (%)'
    )
)

project.shared.normalized_values += normalized_lengths + normalized_angles
