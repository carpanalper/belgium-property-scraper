# Belgium Property Scraper

## Description
This Python project scrapes real estate property listings from Immoweb for various provinces in Belgium. It collects property URLs based on population-weighted page requests per province and extracts detailed information about each property using multithreading.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/carpanalper/belgium-property-scraper.git
   ```
2. Navigate into the project directory:
   ```
   cd belgium-property-scraper
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Modify `main.py` to customize the number of pages to scrape per province and other parameters as needed. The default is 80 and it scraps between 12.000-14.000 titles.
2. Run the main script to start scraping:
   ```
   python main.py
   ```
3. Scraped data will be saved to `belgium_property_dataset.csv` in the current working directory.


## Contributors
- John Doe (@johndoe): Project lead
- Jane Smith (@janesmith): Data analysis