import logging
from dateutil import parser

logger = logging.getLogger(__name__)

def parse_date(date_string):
    """
    Parse a date string in various formats and return it in 'DD-MMM-YYYY' format.
    
    :param date_string: A string representing a date
    :return: A string representing the date in 'DD-MMM-YYYY' format
    """
    try:
        parsed_date = parser.parse(date_string)
        return parsed_date.strftime('%d-%b-%Y')
    except ValueError:
        logger.error(f"Unable to parse date: {date_string}")
        return None
