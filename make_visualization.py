import numpy as np
from numpy import pi

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, CDSView, BooleanFilter,HoverTool
from bokeh.models import Select
from bokeh.layouts import column, widgetbox

from make_datasets import hourly_all_winters, daily_all_winters


# Convert dataset to a column data source
source = ColumnDataSource(data={
    'date': hourly_all_winters['date'],
    'max': hourly_all_winters['max'],
    'min': hourly_all_winters['min'],
    'first': hourly_all_winters['first'],
    'last': hourly_all_winters['last'],
    'average': hourly_all_winters['mean'],
    'winter': hourly_all_winters['winter'],
})

source2 = ColumnDataSource(data={
    'date': daily_all_winters['Date/Time'],
    'month': daily_all_winters['Month'],
    'winter': daily_all_winters['winter'],
    'average': daily_all_winters['Mean Temp (°C)'],
    'rain': daily_all_winters['Total Rain (mm)'],
    'snow': daily_all_winters['Total Snow (cm)'],
    'snow on ground': daily_all_winters['Snow on Grnd (cm)'],
})

# Create first plot and select only the box_zoom and reset tools
y_range = (-30, 30)
p1 = figure(y_range=y_range, x_axis_type="datetime", plot_width=950, plot_height=400,
            title="Daily temperature variations",
            x_axis_label='Months', y_axis_label='Temperature in °C',
            tools="box_zoom,reset")
p1.xaxis.formatter = DatetimeTickFormatter(months=['%B'])

# Create the range line glyph
p1.segment('date', 'max', 'date', 'min', source=source, color="black")

# Create the ascending bars glyph - we need to create a view of our data with a boolean mask to only plot the data
# we want
booleans_inc = [True if last > first else False for last, first in zip(source.data['last'], source.data['first'])]
view_inc = CDSView(source=source, filters=[BooleanFilter(booleans_inc)])

booleans_dec = [True if last < first else False for last, first in zip(source.data['last'], source.data['first'])]
view_dec = CDSView(source=source, filters=[BooleanFilter(booleans_dec)])

w = 365 * 60 * 2000

p1.vbar('date', w, 'first', 'last', source=source, view=view_inc, fill_color="#2c8cd1", line_color="#2c8cd1")
p1.vbar('date', w, 'first', 'last', source=source, view=view_dec, fill_color="#F2583E", line_color="#F2583E")

# Create a hover tool so that we can see min, max, first and last values for each record
# over the plot
hover = HoverTool(tooltips=[("First", "@first{first.1f}"),
                            ("Last", "@last{last.1f}"),
                            ("Min", "@min{min.1f}"),
                            ("Max", "@max{max.1f}"), ], mode='vline')

p1.add_tools(hover)

# Make second plot to see distribution
y_range = (0, 70)
p2 = figure(y_range=y_range, x_axis_type="datetime", plot_width=950, plot_height=200,
            title="Daily snow precipitations",
            x_axis_label='Months', y_axis_label='Total Snow (cm)',
            tools="box_zoom,reset")
p2.xaxis.formatter = DatetimeTickFormatter(months=['%B'])
p2.vbar(x='date', top='snow', bottom=0, width=w, color="firebrick", source=source2)
# p2.line('date', 'snow on ground', line_width=2, source=source2)
p2.varea('date', y1=0, y2='snow on ground', source=source2, alpha=0.5)

# Link the x_range of p2 to p1: p2.x_range
p2.x_range = p1.x_range


# Make a slider object
slider = Select(options=['', '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019'],
                value='', title='Winter')

def update_plot(attr, old, new):
    if new == '':
        source.data = ColumnDataSource(data={'date': hourly_all_winters['date'],
                                             'max': hourly_all_winters['max'],
                                             'min': hourly_all_winters['min'],
                                             'first': hourly_all_winters['first'],
                                             'last': hourly_all_winters['last'],
                                             'average': hourly_all_winters['mean'],
                                             'winter': hourly_all_winters['winter'],}).data
        source2.data = ColumnDataSource(data={'date': daily_all_winters['Date/Time'],
                                              'month': daily_all_winters['Month'],
                                              'winter': daily_all_winters['winter'],
                                              'average': daily_all_winters['Mean Temp (°C)'],
                                              'rain': daily_all_winters['Total Rain (mm)'],
                                              'snow': daily_all_winters['Total Snow (cm)'],
                                              'snow on ground': daily_all_winters['Snow on Grnd (cm)'],
                                              }).data
    else:
        new_source = {'date': hourly_all_winters[hourly_all_winters.winter == new]['date'],
                      'max': hourly_all_winters[hourly_all_winters.winter == new]['max'],
                      'min': hourly_all_winters[hourly_all_winters.winter == new]['min'],
                      'first': hourly_all_winters[hourly_all_winters.winter == new]['first'],
                      'last': hourly_all_winters[hourly_all_winters.winter == new]['last'],
                      'average': hourly_all_winters[hourly_all_winters.winter == new]['mean'],
                      'winter': hourly_all_winters[hourly_all_winters.winter == new]['winter'],
                      }
        source.data = new_source
        new_source2 = {'date': daily_all_winters[daily_all_winters.winter == new]['Date/Time'],
                       'month': daily_all_winters[daily_all_winters.winter == new]['Month'],
                       'winter': daily_all_winters[daily_all_winters.winter == new]['winter'],
                       'average': daily_all_winters[daily_all_winters.winter == new]['Mean Temp (°C)'],
                       'rain': daily_all_winters[daily_all_winters.winter == new]['Total Rain (mm)'],
                       'snow': daily_all_winters[daily_all_winters.winter == new]['Total Snow (cm)'],
                       'snow on ground': daily_all_winters[daily_all_winters.winter == new]['Snow on Grnd (cm)'],
                       }
        source2.data = new_source2

# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)
print(slider.value)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(widgetbox(slider), p1, p2))

