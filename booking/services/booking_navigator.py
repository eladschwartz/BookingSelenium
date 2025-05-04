import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import booking.constants as const

logger = logging.getLogger(__name__)


class BookingNavigator:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, const.CONFIG["WAIT_TIMEOUT"])
        
    def go_to_home_page(self):
        logger.info(f"Navigating to {const.BASE_URL}")
        self.driver.get(const.BASE_URL)
        
        # Wait for the page to load
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, const.SELECTORS["SEARCH_INPUT"])
            ))
            logger.info("Homepage loaded successfully")
        except TimeoutException:
            logger.error("Timeout waiting for homepage to load")
            raise
    
    def change_currency(self, currency: str):
        logger.info(f"Changing currency to {currency}")
        
        try:
            # Click on currency button
            currency_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, const.SELECTORS["CURRENCY_BUTTON"])
            ))
            currency_button.click()
            
            # Select the desired currency
            currency_xpath = const.SELECTORS["CURRENCY_ITEM"].format(currency=currency)
            currency_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, currency_xpath)
            ))
            currency_option.click()
            
            logger.info(f"Currency changed to {currency}")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to change currency: {e}")
            raise
    
    def search_city(self, city: str):
        logger.info(f"Entering city: {city}")
        
        try:
            search_input = self.wait.until(EC.element_to_be_clickable(
                (By.NAME, "ss")
            ))
            search_input.clear()
            search_input.send_keys(city)
            logger.info(f"City '{city}' entered successfully")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to enter city name: {e}")
            raise
    
    def submit_search(self):
        logger.info("Submitting search")
        
        try:
            search_box = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, const.SELECTORS["SEARCH_BOX"])
            ))
            search_button = search_box.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            )
            search_button.click()
            
            # Wait for results page to start loading
            self.wait.until(
                lambda driver: driver.execute_script(
                    "return document.readyState"
                ) != "complete" or True
            )
            
            logger.info("Search submitted successfully")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to submit search: {e}")
            raise