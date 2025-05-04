# Booking.com Automation Tool

A Python-based automation tool for searching accommodations on Booking.com using Selenium WebDriver.

## Project Overview

This tool automates the process of searching for accommodations on Booking.com by providing a command-line interface for inputting search parameters and automating the browser interactions. The automation includes:

- Navigating to Booking.com
- Setting currency preferences
- Entering destination city
- Selecting check-in and check-out dates
- Configuring the number of adults and children
- Submitting the search query

## Features

- **User-friendly CLI**: Interactive command-line interface for entering search parameters
- **Input Validation**: Robust validation of all input parameters using Pydantic
- **Browser Automation**: Selenium WebDriver-based automation for Chrome and Firefox
- **Modular Architecture**: Well-structured codebase with clear separation of concerns
- **Logging**: Comprehensive logging for debugging and monitoring
- **Cross-platform**: Compatible with Windows, macOS, and Linux

## Prerequisites

- Python 3.8+
- Chrome or Firefox browser
- Internet connection

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/booking-automation.git
   cd booking-automation
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the automation tool:

```
python run.py
```

Follow the prompts to enter:
- Destination city
- Check-in date (YYYY-MM-DD format)
- Check-out date (YYYY-MM-DD format)
- Number of adults
- Number of children and their ages (if applicable)
- Currency (optional)

## Project Structure

```
booking-automation/
├── booking/
│   ├── __init__.py
│   ├── constants.py
│   ├── models/
│   │   └── search_parameters.py
│   ├── services/
│   │   ├── booking.py
│   │   ├── booking_navigator.py
│   │   ├── date_picker.py
│   │   └── occupancy_selector.py
│   └── utils/
│       ├── browser_factory.py
│       ├── input_collector.py
│       └── validation.py
├── run.py
├── requirements.txt
└── README.md
```

## Key Components

- **run.py**: Main entry point that orchestrates the automation flow
- **models/search_parameters.py**: Data model with validation for search parameters
- **services/booking.py**: Core service that coordinates the search process
- **services/booking_navigator.py**: Handles navigation and search submission
- **services/date_picker.py**: Manages date selection in the calendar interface
- **services/occupancy_selector.py**: Configures adults and children settings
- **utils/browser_factory.py**: Creates and configures the WebDriver
- **utils/input_collector.py**: Collects and validates user input
- **constants.py**: Centralizes configuration settings and selectors

## Troubleshooting

If you encounter issues:

1. Ensure you have the latest version of Chrome or Firefox installed
2. Check that your Python environment has all dependencies installed
3. Verify your internet connection
4. Review the logs in `booking_automation.log` for detailed error information

## Dependencies

- selenium: Browser automation
- webdriver-manager: Automatic driver management
- pydantic: Data validation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Please ensure your use complies with Booking.com's Terms of Service.
