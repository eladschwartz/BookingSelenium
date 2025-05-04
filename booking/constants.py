# Base URLs and endpoints
BASE_URL = "https://www.booking.com"

# CSS and XPath Selectors
SELECTORS = {
    # Navigation
    "CURRENCY_BUTTON": '[data-testid="header-currency-picker-trigger"]',
    "CURRENCY_ITEM": "//div[contains(@class, 'CurrencyPicker_currency') and text()='{currency}']/ancestor::button",
    "SEARCH_INPUT": 'input[name="ss"]',
    "SEARCH_BOX": '[data-testid="searchbox-layout-wide"]',
    "SEARCH_BUTTON": "button[type='submit']",
    
    # Date picker
    "DATE_CONTAINER": '[data-testid="searchbox-dates-container"]',
    "CALENDAR": '[data-testid="searchbox-datepicker-calendar"]',
    "NEXT_MONTH_BUTTON": '[aria-label="Next month"]',
    "DATE_CELL": 'span[data-date="{date}"]',
    "MONTH_HEADER": ".//h3[contains(text(),'{month_year}')]",
    
    # Occupancy
    "OCCUPANCY_CONFIG": '[data-testid="occupancy-config"]',
    "ADULTS_INPUT": "group_adults",
    "CHILDREN_INPUT": "group_children",
    "KIDS_AGE_SELECT": '[data-testid="kids-ages-select"]',
}

# Configuration
CONFIG = {
    "MAX_MONTH_NAVIGATION": 24,  # Maximum number of months to navigate
    "RETRY_ATTEMPTS": 3,         # Number of retry attempts for flaky operations
    "WAIT_TIMEOUT": 10,          # Default wait timeout in seconds
    "DEFAULT_ADULTS": 1,         # Default number of adults
    "DEFAULT_CHILDREN": 0,       # Default number of children
}