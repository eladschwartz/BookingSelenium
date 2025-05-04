import logging
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import booking.constants as const

logger = logging.getLogger(__name__)


class DatePicker:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, const.CONFIG["WAIT_TIMEOUT"])
        
    def select_dates(self, check_in_date: str, check_out_date: str):
        logger.info(f"Selecting dates: {check_in_date} to {check_out_date}")
        
        try:
            # Open the date picker
            dates_element = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, const.SELECTORS["DATE_CONTAINER"])
            ))
            dates_element.click()
            
            # Navigate to and select check-in date
            self._navigate_to_date_month(check_in_date)
            check_in_selector = const.SELECTORS["DATE_CELL"].format(date=check_in_date)
            check_in_element = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, check_in_selector)
            ))
            check_in_element.click()
            logger.info(f"Check-in date {check_in_date} selected")
            
            # Navigate to and select check-out date
            self._navigate_to_date_month(check_out_date)
            check_out_selector = const.SELECTORS["DATE_CELL"].format(date=check_out_date)
            check_out_element = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, check_out_selector)
            ))
            check_out_element.click()
            logger.info(f"Check-out date {check_out_date} selected")
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to select dates: {e}")
            raise
    
    def _navigate_to_date_month(self, date_str: str) -> bool:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month_name = date_obj.strftime('%B').capitalize()
        year = date_obj.strftime('%Y')
        month_year = f"{month_name} {year}"
        
        logger.info(f"Navigating to {month_year}")
        
        try:
            # Find the calendar element
            calendar = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, const.SELECTORS["CALENDAR"])
            ))
            
            # Check if the target month is already visible
            for _ in range(const.CONFIG["MAX_MONTH_NAVIGATION"]):
                try:
                    month_xpath = const.SELECTORS["MONTH_HEADER"].format(month_year=month_year)
                    calendar.find_element(By.XPATH, month_xpath)
                    logger.info(f"Found {month_year} in the calendar")
                    return True
                except NoSuchElementException:
                    # Click next month if target month is not found
                    next_button = calendar.find_element(
                        By.CSS_SELECTOR, const.SELECTORS["NEXT_MONTH_BUTTON"]
                    )
                    next_button.click()
                    logger.debug(f"Clicked next month, looking for {month_year}")
            
            logger.warning(f"Could not find {month_year} after {const.CONFIG['MAX_MONTH_NAVIGATION']} attempts")
            return False
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Error navigating to month {month_year}: {e}")
            raise