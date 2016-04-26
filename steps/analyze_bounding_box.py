import plotly.graph_objs as go
import numpy as np

from cauldron import plotting
from cauldron import project

import measurement_stats as mstats

df = project.shared.measurements

normalized_values = []
traces = []

for key in ['Width-Box', 'Height-Box']:
    d = mstats.create_distribution(
        measurements=df[key].tolist(),
        uncertainties=5
    )
    median = mstats.distributions.percentile(d)

    normalized = [100.0 * (v / median - 1.0) for v in d.measurements]
    normalized_values += normalized

    x_values = list(np.arange(1, len(normalized), 1))
    y_values, y_uncertainties = mstats.values.unzip(normalized)
    traces.append(go.Bar(
        x=x_values,
        y=y_values,
        error_y=dict(
            type='data',
            array=y_uncertainties,
            visible=True
        ),
        name=key.split('-')[0],
        marker=dict(
            color=plotting.get_color(len(traces), 0.5)
        )
    ))

d = mstats.create_distribution(normalized_values)
mad = mstats.distributions.weighted_median_average_deviation(d, count=2048)
result = mstats.ValueUncertainty(0, mad)

project.display.text(
    """
    Finally, the overall width and height measurements were analyzed in the
    same fashion as the above results. The result is that they exhibit the same
    low and reasonable &#177;3% variance as the digit length measurements.
    """
)

project.display.plotly(
    data=traces,
    layout=plotting.create_layout(
        title='Size Measurements Deviations ({}%)'.format(
            result.html_label.split(' ', 1)[-1]
        ),
        x_label='Drawing Index (#)',
        y_label='Fractional Value (%)'
    )
)

project.shared.normalized_values += normalized_values
