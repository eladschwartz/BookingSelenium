"""
Service for handling occupancy selection (adults and children) on Booking.com.
"""

import logging
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import booking.constants as const

logger = logging.getLogger(__name__)


class OccupancySelector:
    """
    Handles occupancy selection operations on Booking.com.
    Responsible for setting the number of adults and children.
    """
    
    def __init__(self, driver: WebDriver):
        """
        Initialize the occupancy selector with a WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, const.CONFIG["WAIT_TIMEOUT"])
    
    def open_occupancy_menu(self):
        """Open the occupancy configuration menu."""
        try:
            occupancy_element = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, const.SELECTORS["OCCUPANCY_CONFIG"])
            ))
            occupancy_element.click()
            logger.info("Occupancy menu opened")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to open occupancy menu: {e}")
            raise
    
    def set_adults(self, num_adults: int):
        """
        Set the number of adults.
        
        Args:
            num_adults: Number of adults (must be at least 1)
        """
        if num_adults < 1:
            logger.warning("Number of adults must be at least 1, setting to 1")
            num_adults = 1
            
        logger.info(f"Setting number of adults to {num_adults}")
        
        try:
            # Open the occupancy menu
            self.open_occupancy_menu()
            
            # Get the input and buttons
            adult_input_id = const.SELECTORS["ADULTS_INPUT"]
            buttons = self._get_counter_buttons(adult_input_id)
            
            # Reset to 1 adult first
            self._reset_counter(buttons["minus"], adult_input_id, 1)
            
            # Increase to desired number
            for _ in range(num_adults - 1):
                buttons["plus"].click()
                
            logger.info(f"Set adults to {num_adults}")
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to set number of adults: {e}")
            raise
    
    def set_children(self, num_children: int, ages: List[int]):
        """
        Set the number of children and their ages.
        
        Args:
            num_children: Number of children
            ages: List of ages for each child
        """
        if num_children != len(ages):
            raise ValueError(f"Number of children ({num_children}) doesn't match ages provided ({len(ages)})")
            
        logger.info(f"Setting {num_children} children with ages {ages}")
        
        try:
            # Occupancy menu should already be open from set_adults
            # but ensure it's open
            try:
                # Check if occupancy menu is already open
                self.driver.find_element(By.ID, const.SELECTORS["ADULTS_INPUT"])
            except NoSuchElementException:
                self.open_occupancy_menu()
                
            # Get the input and buttons for children
            children_input_id = const.SELECTORS["CHILDREN_INPUT"]
            buttons = self._get_counter_buttons(children_input_id)
            
            # Reset to 0 children first
            self._reset_counter(buttons["minus"], children_input_id, 0)
            
            # Add children
            for _ in range(num_children):
                buttons["plus"].click()
                
            # Set ages for each child
            for i in range(num_children):
                self._set_child_age(i, ages[i])
                
            logger.info(f"Successfully set {num_children} children with ages {ages}")
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to set children: {e}")
            raise
    
    def _get_counter_buttons(self, input_id: str) -> dict:
        """
        Get the plus and minus buttons for a counter input.
        
        Args:
            input_id: ID of the counter input element
            
        Returns:
            dict: Dictionary with 'minus' and 'plus' buttons
        """
        root_div = self.driver.find_element(
            By.XPATH, f'//input[@id="{input_id}"]/parent::div'
        )
        buttons = root_div.find_elements(By.TAG_NAME, 'button')
        return {
            'minus': buttons[0],
            'plus': buttons[1]
        }
    
    def _reset_counter(self, minus_button, counter_id: str, target_value: int):
        """
        Reset a counter to the target value by clicking the minus button.
        
        Args:
            minus_button: The button element to click
            counter_id: ID of the counter input
            target_value: Target value to reset to
        """
        while True:
            value_element = self.driver.find_element(By.ID, counter_id)
            current_value = int(value_element.get_attribute('value'))
            
            if current_value == target_value:
                break
                
            if current_value < target_value:
                logger.warning(f"Current value {current_value} is less than target {target_value}")
                break
                
            minus_button.click()
    
    def _set_child_age(self, index: int, age: int):
        """
        Set the age for a child.
        
        Args:
            index: Index of the child (0-based)
            age: Age of the child (0-17)
        """
        if not 0 <= age <= 17:
            logger.warning(f"Child age {age} is outside valid range (0-17), clamping to valid range")
            age = max(0, min(age, 17))
            
        try:
            # Find the age selector for this child
            age_selectors = self.driver.find_elements(
                By.CSS_SELECTOR, const.SELECTORS["KIDS_AGE_SELECT"]
            )
            
            if index >= len(age_selectors):
                raise IndexError(f"Child index {index} is out of range")
                
            child_age_element = age_selectors[index]
            select_element = child_age_element.find_element(By.CSS_SELECTOR, "select")
            
            # Use JavaScript to set the value and trigger change event
            self.driver.execute_script(
                f"arguments[0].value = '{age}';", select_element
            )
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", 
                select_element
            )
            
            logger.info(f"Set age for child {index + 1} to {age}")
            
        except (NoSuchElementException, IndexError) as e:
            logger.error(f"Failed to set age for child {index + 1}: {e}")
            raise