import measurement_stats as mstats
from cauldron import project
from cauldron import plotting

import plotly.graph_objs as go

d = mstats.create_distribution(project.shared.normalized_values)

x_values = mstats.distributions.adaptive_range(d, 3.0, max_delta=0.1)
y_values = d.probabilities_at(x_values)


data = go.Scatter(
    x=x_values,
    y=y_values,
    fill='tozeroy'
)

layout = plotting.create_layout(
    title='Combined Measurement Deviations Cumulative Distribution',
    x_label='Median Deviation (%)',
    y_label='Expectation Value (au)'
)

project.display.markdown(
    """
    Cumulative Distribution
    -----------------------

    In this final plot, the median-deviation values for every previous
    measurement were combined into a single weighted distribution and plotted
    to inspect the structure of the variance. An important conclusion to take
    away from this distribution is that the small humps, particularly in the
    lower half of the graph, are the result of singular or small numbers of
    measurements. This indicates that the measurement distribution is not
    robustly sampled and that more samples should be added for additional
    statistical validation of the result.
    """
)

project.display.plotly(
    data=[data],
    layout=layout
)
