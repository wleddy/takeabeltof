from takeabeltof.date_utils import date_to_string

# some custom filters for templates
def iso_date_string(value):
    format = '%Y-%m-%d'
    return date_to_string(value,format)
        
        
def short_date_string(value):
    format='%m/%d/%y'
    return date_to_string(value,format)
    
def long_date_string(value):
    format='%B %-d, %Y'
    return date_to_string(value,format)
    
def two_decimal_string(value):
    try:
        if type(value) is str:
            value = value.strip()
        if value == None or value == '':
            value = '0'
        value = float(value)
        value = (str(value) + "00")
        pos = value.find(".")
        if pos > 0:
            value = value[:pos+3]
    except ValueError as e:
        pass
        
    return value
    

def register_jinja_filters(app):
    # register the filters
    app.jinja_env.filters['short_date_string'] = short_date_string
    app.jinja_env.filters['long_date_string'] = long_date_string
    app.jinja_env.filters['two_decimal_string'] = two_decimal_string
    app.jinja_env.filters['money'] = two_decimal_string
    app.jinja_env.filters['iso_date_string'] = iso_date_string
