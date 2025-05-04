import logging
from booking.utils.browser_factory import BrowserFactory
from booking.utils.input_collector import UserInputCollector
from booking.services.booking import Booking
from selenium.common.exceptions import WebDriverException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("booking_automation.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    try:
        # Get user input for search parameters
        collector = UserInputCollector()
        search_params = collector.collect_search_parameters()
        
        # Setup browser using the factory
        browser_factory = BrowserFactory()
        browser_service, browser_options = browser_factory.prepare_browser("chrome")
        
        logger.info(f"Starting search for accommodations in {search_params.city}")
        
        # Initialize the booking automation and perform search
        with Booking(browser_service, browser_options) as booking:
            booking.search_accommodation(search_params)
            
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
        print("\nBrowser automation failed. Please try again.")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\nInput validation failed: {e}")
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nProcess interrupted. Exiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()