import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def validate_date_format(date_str):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        logger.warning(f"Date string '{date_str}' does not match YYYY-MM-DD pattern")
        return False
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError as e:
        logger.warning(f"Date validation failed for '{date_str}': {e}")
        return False


def validate_date_sequence(check_in, check_out):
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        return check_out_date > check_in_date
    except ValueError as e:
        logger.warning(f"Date sequence validation failed: {e}")
        return False


def validate_date_not_in_past(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return date >= today
    except ValueError as e:
        logger.warning(f"Date validation failed: {e}")
        return False
    
    
def validate_child_age(age):
    try:
        age_int = int(age)
        return 0 <= age_int <= 17
    except (ValueError, TypeError):
        logger.warning(f"Child age validation failed for '{age}'")
        return False