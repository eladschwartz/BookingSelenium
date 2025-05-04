import logging
from pydantic import ValidationError
from datetime import datetime, date
from booking.models.search_parameters import SearchParameters

logger = logging.getLogger(__name__)


class UserInputCollector:
    def collect_search_parameters(self):
        # Create a dictionary to store collected parameters
        params = {}
        
        # Collect city name
        params['city'] = self._get_city_name()
        
        # Collect dates
        params['check_in_date'] = self._get_check_in_date()
        params['check_out_date'] = self._get_check_out_date(params['check_in_date'])
        
        # Collect occupancy information
        params['num_adults'] = self._get_number_of_adults()
        params['num_children'] = self._get_number_of_children()
        
        if params['num_children'] > 0:
            params['children_ages'] = self._get_children_ages(params['num_children'])
            
        # Optionally collect currency
        currency = self._get_currency()
        if currency:
            params['currency'] = currency
        
        try:
            search_params = SearchParameters(**params)
            logger.info(f"Created validated search parameters: {search_params.model_dump()}")
            return search_params
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
    
    def _get_city_name(self):
        while True:
            city = input("Enter city name: ").strip()
            if city:
                logger.info(f"City name entered: {city}")
                return city
            print("City name cannot be empty. Please try again.")
    
    def _get_check_in_date(self):
        while True:
            check_in_date = input("Enter check-in date (YYYY-MM-DD): ").strip()
            
            try:
                # Basic format check
                datetime.strptime(check_in_date, '%Y-%m-%d')
                
                # Check if date is not in the past
                if datetime.strptime(check_in_date, '%Y-%m-%d').date() < date.today():
                    print("Check-in date cannot be in the past.")
                    continue
                
                logger.info(f"Check-in date entered: {check_in_date}")
                return check_in_date
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
    
    def _get_check_out_date(self, check_in_date):
        while True:
            check_out_date = input("Enter check-out date (YYYY-MM-DD): ").strip()
            
            try:
                # Basic format check
                check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
                check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
                
                # Simple check if check-out is after check-in
                if check_out <= check_in:
                    print("Check-out date must be after check-in date.")
                    continue
                
                logger.info(f"Check-out date entered: {check_out_date}")
                return check_out_date
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
    
    def _get_number_of_adults(self):
        while True:
            try:
                num_adults = int(input("Enter number of adults: ").strip())
                if num_adults > 0:
                    logger.info(f"Number of adults entered: {num_adults}")
                    return num_adults
                print("Number of adults must be greater than 0.")
            except ValueError:
                print("Please enter a valid number.")
    
    def _get_number_of_children(self):
        while True:
            try:
                num_children = int(input("Enter number of children (0-17 years old): ").strip())
                if num_children >= 0:
                    logger.info(f"Number of children entered: {num_children}")
                    return num_children
                print("Number of children cannot be negative.")
            except ValueError:
                print("Please enter a valid number.")
    
    def _get_children_ages(self, num_children):
        children_ages = []
        
        if num_children > 0:
            print(f"Enter the age of each child (0-17) - {num_children} children:")
            
            for i in range(num_children):
                while True:
                    try:
                        age = int(input(f"Child {i+1} age: ").strip())
                        if 0 <= age <= 17:
                            children_ages.append(age)
                            break
                        print("Age must be between 0 and 17.")
                    except ValueError:
                        print("Please enter a valid number.")
        
        logger.info(f"Children ages entered: {children_ages}")
        return children_ages
    
    def _get_currency(self):
        currency = input("Enter currency code (e.g., USD, EUR) or press Enter for default: ").strip().upper()
        
        if currency:
            logger.info(f"Currency entered: {currency}")
            return currency
            
        logger.info("Using default currency")
        return None