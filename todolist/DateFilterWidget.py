__author__ = 'Dylan'

from datetime import date
from django.forms import widgets


class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # create choices for days, months, years
        # example below, the rest snipped for brevity.
        years = [(year, year) for year in range(2014, 2050)]
        months = [(month, month) for month in range(1, 12)]
        week = [(week, week) for week in range(1, 4)]

        _widgets = (
            widgets.Select(attrs=attrs, choices=week),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            d = date(month=int(datelist[1]),
                     year=int(datelist[2]))
        except ValueError:
            return ''
        else:
            return str(d)
