import sys
#print(sys.path)
sys.path.append('') ##get import to look in the working dir.
from datetime import datetime
import takeabeltof.jinja_filters as filters

def test_two_digit():
    """Test that it rounds to 2 digits"""
    assert filters.two_decimal_string(1234.0) == "1234.00"
    assert filters.two_decimal_string(1234) == "1234.00"
    assert filters.two_decimal_string(1234.001) == "1234.00"
    assert filters.two_decimal_string(1234) == "1234.00"
    assert filters.two_decimal_string("1234") == "1234.00"
    assert filters.two_decimal_string(1234.9999) == "1234.99"
    
def test_short_date_string():
    test_date = datetime(2018,5,9)
    assert filters.short_date_string(test_date) == "05/09/18"
    assert filters.short_date_string("2018-05-09") == "05/09/18"
    assert filters.short_date_string("05/09/18") == "05/09/18"
    
def test_iso_date_string():
    test_date = datetime(2018,5,9)
    assert filters.iso_date_string(test_date) == "2018-05-09"
    assert filters.iso_date_string("2018-05-09") == "2018-05-09"
    assert filters.iso_date_string("05/09/18") == "2018-05-09"
