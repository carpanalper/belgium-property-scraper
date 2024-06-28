import pandas as pd
from utils.properties import PropertyScraper
from utils.immo_urls import belgium_property_url_finder

def main():
    # Instantiate the URL finder
    url_finder = belgium_property_url_finder()
    
    # Get a list of property URLs
    number_of_pages = 2  # Adjust the number of pages as needed
    list_of_urls = url_finder.get_all_urls(number_of_pages)

    # Instantiate the PropertyScraper
    scraper = PropertyScraper()

    # Scrape property details from the URLs
    scraper.get_faster_info(list_of_urls)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(scraper.list_of_lists, columns=['Locality', 'Type', 'Price', 'Rooms', 'Living area(m2)',
                                                      'Plot(m2)', 'Installed Kitchen', 'Furnished', 'Fireplace',
                                                      'Terrace', 'Terrace Surface(m2)', 'Garden', 'Garden Surface(m2)',
                                                      'No.Facades', 'Swimming Pool', 'Condition', 'Construction Year',
                                                      'Energy Label'])

    # Print the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    df.to_csv('belgium_property_database.csv', index=False, float_format='%.0f')

if __name__ == "__main__":
    main()