"""Some date utilities"""

from datetime import datetime
from pytz import timezone

def local_datetime_now(time_zone=None):
    """Return a datetime object for now at the time zone specified.
    
    If tz is None, use the tz name in app.config else use the local time per the server"""
    if time_zone == None:
        time_zone = get_time_zone_setting()
        if time_zone == None:
            return datetime.now()
        
    try:
        #import pdb;pdb.set_trace()
        utc = timezone("UTC")
        local_tz = timezone(time_zone)
        now = utc.localize(datetime.utcnow())
        return now.astimezone(local_tz)
        
    except:
        return datetime.now()
            
def make_tz_aware(the_datetime,time_zone=None):
    """Return the time zone aware version of the datetime 
    This function will not convert an aware datetime to a new time zone"""
    if the_datetime.tzinfo != None:
        return the_datetime # not needed
        
    if time_zone == None:
        time_zone = get_time_zone_setting()
        if time_zone == None:
            time_zone = 'UTC'
            
    tz = timezone(time_zone)
    return tz.localize(the_datetime)
    
    
def get_time_zone_setting():
    """Return the TIME_ZONE config setting if it exists else None"""
    try:
        from app import app
        time_zone = app.config['TIME_ZONE']
    except:
        time_zone = None
        
    return time_zone
    
    
def nowString():
    """Return the timestamp string in the normal format"""
    return datetime_as_string(local_datetime_now())
    
    
def date_to_string(value,format):
    """Attempt to return a date string in the format specified
    value may be a datetime or a 'date like' string"""
        
    if value and format:
        if type(value) is datetime:
            return value.strftime(format)
        if type(value) is str:
            # convert the string to a date first then back.
            temp_date = getDatetimeFromString(value)
            if temp_date:
                return temp_date.strftime(format)
    
    #default - return unchanged
    return value

    
def datetime_as_string(the_datetime=None):
    """Return a string version of the datetime provided or for now"""
    if the_datetime == None:
        the_datetime = local_datetime_now()
        
    return the_datetime.isoformat(sep=" ")[:19]
    

def getDatetimeFromString(dateString):
    """Try to create a datetime object based on the string provided
    or else None.
    The  datetime object returned is time zone aware
    """
    if type(dateString) is str: # or type(dateString) is unicode:
        pass
    else:
        return None

    dateString = dateString[:19]
    timeDelimiter = " "
    if "T" in dateString:
        timeDelimiter = "T"

    formats = [
        '%m/%d/%y',
        '%m/%d/%Y',
        '%m-%d-%y',
        '%m-%d-%Y',
        '%y-%m-%d',
        '%Y-%m-%d',
        '%Y-%m-%d{}%H:%M:%S'.format(timeDelimiter),
        '%y-%m-%d{}%H:%M:%S'.format(timeDelimiter),
        '%Y-%m-%d{}%H:%M'.format(timeDelimiter),
        '%y-%m-%d{}%H:%M'.format(timeDelimiter),
        ]

    theDate = None
    for fmt in formats:
        try:
            theDate = datetime.strptime(dateString,fmt)
            break
        except Exception as e:
            theDate = None
            
    if theDate == None:
        return None
        
    # Make datetime aware
    theDate = timezone(get_time_zone_setting()).localize(theDate)
        
    return theDate.replace(microsecond=0)