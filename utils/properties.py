import requests
from bs4 import BeautifulSoup as bs
from threading import RLock, Thread

class PropertyScraper:
    def __init__(self):
        self.list_of_lists = []
        self.rlock = RLock()
        self.processed_count = 0

    def get_further_info(self, title_url):
        try:
            headers = {"User-agent": "alper", "Authorization": "alper1"}
            with requests.Session() as session:
                r = session.get(title_url, headers=headers)
                soup = bs(r.text, "html.parser")

                locality, type_of_property = self.extract_basic_info(title_url)
                price = self.extract_price(soup)
                rooms_text = self.extract_rooms(soup)
                living_text = self.extract_living_area(soup)
                plotm2 = self.extract_plot_surface(soup)
                kitchen_type = self.extract_kitchen_type(soup)
                furnished_type = self.extract_furnished(soup)
                open_fire_type = self.extract_open_fire(soup)
                terrace_type, terrace_surface_m2 = self.extract_terrace(soup)
                garden_type, garden_surface_m2 = self.extract_garden(soup)
                facades = self.extract_facades(soup)
                pool_type = self.extract_swimming_pool(soup)
                building_state_text = self.extract_building_state(soup)
                construction_year_text = self.extract_construction_year(soup)
                energy_text = self.extract_energy(soup)

                with self.rlock:
                    self.list_of_lists.append([
                        locality, type_of_property, price, rooms_text, living_text,
                        plotm2, kitchen_type, furnished_type, open_fire_type, terrace_type,
                        terrace_surface_m2, garden_type, garden_surface_m2, facades, pool_type,
                        building_state_text, construction_year_text, energy_text
                    ])
                    self.processed_count += 1
                    print(f"Urls Processed: {self.processed_count}")

        except Exception as e:
            print(f"Error: {title_url}: {e}")

    def extract_basic_info(self, title_url):
        basic_info = title_url.split("/")
        locality = basic_info[-3].capitalize() if len(basic_info) > 2 else None
        type_of_property = basic_info[5].capitalize() if len(basic_info) > 5 else None
        return locality, type_of_property

    def extract_price(self, soup):
        price_p = soup.find("p", attrs={"class": "classified__price"})
        return price_p.find("span", class_="sr-only").get_text() if price_p else None

    def extract_rooms(self, soup):
        rooms = soup.find("th", string=lambda text: text and 'Bedrooms' in text)
        return rooms.find_next('td').contents[0].strip() if rooms else None

    def extract_living_area(self, soup):
        living = soup.find("th", string=lambda text: text and 'Living area' in text)
        return living.find_next('td').contents[0].strip() if living else None

    def extract_plot_surface(self, soup):
        plot_surface = soup.find("th", text="Surface of the plot")
        return plot_surface.find_next("td").contents[0].strip() if plot_surface else None

    def extract_kitchen_type(self, soup):
        kitchen = soup.find('th', string=lambda text: text and 'Kitchen type' in text)
        if kitchen:
            kitchen_text = kitchen.find_next('td').contents[0].strip()
            return 1 if kitchen_text == "Installed" else 0
        return None

    def extract_furnished(self, soup):
        furnished = soup.find('th', string=lambda text: text and 'Furnished' in text)
        if furnished:
            furnished_text = furnished.find_next('td').contents[0].strip()
            return 1 if furnished_text == 'Yes' else 0
        return None

    def extract_open_fire(self, soup):
        open_fire = soup.find('th', string=lambda text: text and 'How many fireplaces?' in text)
        if open_fire:
            open_fire_text = open_fire.find_next('td').contents[0].strip()
            return 1 if int(open_fire_text) >= 1 else 0
        return None

    def extract_terrace(self, soup):
        terrace = soup.find('th', string=lambda text: text and 'Terrace' in text)
        terrace_surface = soup.find('th', string=lambda text: text and 'Terrace surface' in text)
        if terrace_surface:
            return 1, terrace_surface.find_next('td').contents[0].strip()
        elif terrace:
            terrace_text = terrace.find_next('td').contents[0].strip()
            return (1, None) if terrace_text == "Yes" else (0, 0)
        return None, None

    def extract_garden(self, soup):
        garden = soup.find('th', string=lambda text: text and 'Garden' in text)
        garden_surface = soup.find('th', string=lambda text: text and 'Garden surface' in text)
        if garden_surface:
            return 1, garden_surface.find_next('td').contents[0].strip()
        elif garden:
            garden_text = garden.find_next('td').contents[0].strip()
            return (1, None) if garden_text == 'Yes' else (0, 0)
        return None, None

    def extract_facades(self, soup):
        facades = soup.find('th', string=lambda text: text and 'Number of frontages' in text)
        return int(facades.find_next('td').contents[0].strip()) if facades else None

    def extract_swimming_pool(self, soup):
        swimming_pool = soup.find('th', string=lambda text: text and 'Furnished' in text)
        if swimming_pool:
            pool_text = swimming_pool.find_next('td').contents[0].strip()
            return 1 if pool_text == 'Yes' else 0
        return None

    def extract_building_state(self, soup):
        building_state = soup.find('th', string=lambda text: text and 'Building condition' in text)
        return building_state.find_next('td').contents[0].strip() if building_state else None

    def extract_construction_year(self, soup):
        construction_year = soup.find('th', string=lambda text: text and 'Construction year' in text)
        return int(construction_year.find_next('td').contents[0].strip()) if construction_year else None

    def extract_energy(self, soup):
        energy = soup.find('th', string=lambda text: text and 'Energy class' in text)
        return energy.find_next('td').contents[0].strip() if energy else None
    
    def get_faster_info(self, list_of_urls):
        threads = []
        for url in list_of_urls:
            thread = Thread(target=self.get_further_info, args=(url,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
