import datetime

import xlwt
from django.forms.forms import pretty_name
from django.core.exceptions import ObjectDoesNotExist

HEADER_STYLE = xlwt.easyxf('font: bold on')
DEFAULT_STYLE = xlwt.easyxf()
CELL_STYLE_MAP = (
    (datetime.date, xlwt.easyxf(num_format_str='DD/MM/YYYY')),
    (datetime.time, xlwt.easyxf(num_format_str='HH:MM')),
    (bool, xlwt.easyxf(num_format_str='BOOLEAN')),
)


def multi_getattr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj


def get_column_head(obj, name):
    name = name.rsplit('.', 1)[-1]
    return pretty_name(name)


def get_column_cell(obj, name):
    try:
        attr = multi_getattr(obj, name)
    except ObjectDoesNotExist:
        return None
    if hasattr(attr, '_meta'):
        # A Django Model (related object)                                                                                                                                                                          
        return unicode(attr).strip()
    elif hasattr(attr, 'all'):
        # A Django queryset (ManyRelatedManager)                                                                                                                                                                   
        return ', '.join(unicode(x).strip() for x in attr.all())
    return attr


def queryset_to_workbook(queryset, columns, header_style=None,
                         default_style=None, cell_style_map=None):
    workbook = xlwt.Workbook()
    report_date = datetime.date.today()
    sheet_name = 'Export {0}'.format(report_date.strftime('%Y-%m-%d'))
    sheet = workbook.add_sheet(sheet_name)

    if not header_style:
        header_style = HEADER_STYLE
    if not default_style:
        default_style = DEFAULT_STYLE
    if not cell_style_map:
        cell_style_map = CELL_STYLE_MAP

    obj = queryset.first()
    for y, column in enumerate(columns):
        value = get_column_head(obj, column)
        sheet.write(0, y, value, header_style)

    for x, obj in enumerate(queryset, start=1):
        for y, column in enumerate(columns):
            value = get_column_cell(obj, column)
            style = default_style
            for value_type, cell_style in cell_style_map:
                if isinstance(value, value_type):
                    style = cell_style
            sheet.write(x, y, value, style)

    return workbook
