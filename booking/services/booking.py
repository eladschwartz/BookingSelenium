import logging
from selenium import webdriver
from booking.models.search_parameters import SearchParameters
from booking.services.booking_navigator import BookingNavigator
from booking.services.date_picker import DatePicker
from booking.services.occupancy_selector import OccupancySelector

logger = logging.getLogger(__name__)


class Booking:
    def __init__(self, browser_service, options=None, teardown=False):
        self.driver = webdriver.Chrome(service=browser_service, options=options)
        self.teardown = teardown
        self.driver.maximize_window()
        self.navigator = BookingNavigator(self.driver)
        self.date_picker = DatePicker(self.driver)
        self.occupancy_selector = OccupancySelector(self.driver)
        
        logger.info("Booking service initialized")
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            logger.info("Closing browser")
            self.driver.quit()
    
    def search_accommodation(self, search_params: SearchParameters):
        logger.info(f"Searching accommodations in {search_params.city}")
        
        # Navigate to homepage
        self.navigator.go_to_home_page()
        
        # Set currency if specified
        if search_params.currency:
            self.navigator.change_currency(search_params.currency)
            
        # Enter destination city
        self.navigator.search_city(search_params.city)
        
        # Select dates
        self.date_picker.select_dates(
            search_params.check_in_date, 
            search_params.check_out_date
        )
        
        # Set occupancy (adults and children)
        self.occupancy_selector.set_adults(search_params.num_adults)
        
        if search_params.num_children > 0:
            self.occupancy_selector.set_children(
                search_params.num_children, 
                search_params.children_ages
            )
            
        # Submit search
        self.navigator.submit_search()
        
        logger.info("Search submitted successfully")