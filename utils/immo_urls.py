import requests
from bs4 import BeautifulSoup as bs
from requests import Session
from threading import Thread, RLock
from time import perf_counter
from typing import List

class belgium_property_url_finder:

    '''
    The class 'belgium_property_url_finder' includes functions to list requested amount of urls of properties for sale 
    from all around Belguim for further processing.

        Attributes
            list_of_provinces (List): This is a list that contains all provinces in Belgium and the coefficients proportional to each province's population.
            list_of_urls(List): All the urls collected from the web will be stored in this list.
            rlock is a reentrant lock (RLock) used to ensure thread-safe operations within the class. 
                It allows a thread to acquire the lock multiple times before releasing it.
    '''

    def __init__(self):
        self.list_of_provinces: List[tuple] = [('brussels', 0.6), ('west-flanders', 0.6), ('east-flanders', 0.75),
                                               ('antwerp', 0.9), ('flemish-brabant', 0.55), ('limburg', 0.4),
                                               ('hainaut', 0.65), ('namur', 0.25), ('walloon-brabant', 0.2),
                                               ('liege', 0.55), ('luxembourg', 0.15)
                                               ]
        self.list_of_urls: List[str] = []
        self.rlock = RLock()

    def __str__(self):
        return f"Collected URLs: {len(self.list_of_urls)}"
    
    def get_province_urls(self, no: int, session: Session, elem: tuple):
        
        """
        this function takes 2 arguments
        elem: is an element from the list_of_provinces, which contains the name of the province and a coefficient proportional (1:2.000.000) to its population.
        no: the number of search pages where the properties listed.

        # it lists the first 30 elements on each page, because the page also include property recommendations. Listing recommended properties on each page could
        lead repetitions on the list. 
        # it excludes new real estate projects since they contain ambiguous information on more than one property.
        """
        url = f"https://www.immoweb.be/en/search/house/for-sale/{elem[0]}/province?countries=BE&page={no}&orderBy=relevance"
        headers = {"User-agent": "eliza", "Authorization": "eliza1"}  
        r = session.get(url, headers=headers)
        soup = bs(r.text, "html.parser")
        urls = []
        for i, link in enumerate(soup.find_all("a", attrs={"class": "card__title-link"})):
            #getting only the first 30 links
            if i >= 30:
                break
            href = link.get("href")
            #excluing new real estate projects
            if "project" in href:
                continue
            urls.append(href)

        with self.rlock:
            self.list_of_urls.extend(urls)

        print(f"{elem[0]} province: {len(urls)} URLs collected.")  #URL count for each province

    
    def get_all_urls(self,no:int) -> List[str]:
       
        """
        #This function takes an argument "no" which defines the range of pages that the program would gather links from.

        #It multiplies and round the given "no" with the population coefficient of each province, c
        collects at least 1 page of property listings from each province.

        #It returns list of urls from all around Belgium.
        """

        with Session() as session:
            threads = []
            for elem in self.list_of_provinces:
                no_pages = round(no * elem[1]) if round(no * elem[1]) > 0 else 1
                #making it faster by starting each loop at the same time with threads
                for i in range(1, no_pages + 1):
                    thread = Thread(target=self.get_province_urls, args=(i, session, elem))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
                no_pages = no   
        
        with self.rlock:
            self.list_of_urls = list(set(self.list_of_urls))  # Ensure unique URLs

        return self.list_of_urls