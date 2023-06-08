from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wb2
import time, re
from functions import error, procces, success, get_a_proxy
from place import Place
import settings

search_timeout = settings.search_timeout
place_timeout = settings.place_timeout
SCROLL_PAUSE_TIME = settings.SCROLL_PAUSE_TIME


class Scraper:

    def __init__(self, search_query=''):
        self.search_query = search_query
        self.driver = None
        success('new scrapper created')

    def setup_driver(self):
        global place_timeout
        global search_timeout

        try:
            procces("trying to start a web driver")
            proxy = get_a_proxy()
            seleniumwire_options = None
            if proxy:
                if 'http' in proxy['proxy']:
                    host = re.search(r'[a-z:]+\/\/([\d.]+):(\d+)', proxy['proxy'])
                    if host:
                        if proxy['username'] == '' or proxy['password'] == '':
                            seleniumwire_options = {
                                'proxy': {
                                    'http': f'http://{host[1]}:{host[2]}',
                                    'https': f'http://{host[1]}:{host[2]}'
                                }
                            }
                        else:
                            seleniumwire_options = {
                                'proxy': {
                                    'http': f'http://{proxy["username"]}:{proxy["password"]}@{host[1]}:{host[2]}',
                                    'https': f'https://{proxy["username"]}:{proxy["password"]}@{host[1]}:{host[2]}'
                                }
                            }
                    else:
                        error('please check your proxies again')
                        seleniumwire_options = None

                elif 'socks' in proxy['proxy']:
                    host = re.search(r'[a-z:]+\/\/([\d.]+):(\d+)', proxy['proxy'])
                    if host:
                        if proxy['username'] == '' or proxy['password'] == '':
                            error('please check your proxies again')
                            seleniumwire_options = None
                        else:
                            seleniumwire_options = {
                                'proxy': {
                                    'http': f'socks5://{proxy["username"]}:{proxy["password"]}@{host[1]}:{host[2]}',
                                    'https': f'socks5://{proxy["username"]}:{proxy["password"]}@{host[1]}:{host[2]}'
                                }
                            }
                    else:
                        error('please check your proxies again')
                        seleniumwire_options = None

            options = Options()
            # options.add_argument("--window-size=1920,1200")
            options.add_argument('--headless')
            options.headless = True
            if not seleniumwire_options:
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            else:
                print('using proxy')
                print(seleniumwire_options)
                self.driver = wb2.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options,
                                         seleniumwire_options=seleniumwire_options)
        except Exception as e:
            error(f'setup_driver - {e}')

        else:
            success("web driver started")

    def download_webpage(self, url):
        procces(f"downloading webpage => {url}")
        self.driver.get(url)
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.fontHeadlineLarge'))
            WebDriverWait(self.driver, place_timeout).until(element_present)
        except TimeoutException:
            error("Timed out waiting for page to load")
        else:
            success("Page loaded")

    # if cannot extract title return None
    def extract_details(self):
        place_ = {'Name': None, 'Website': '', 'Address': '', 'Phone number': '', 'Categories': '', 'Rating': '',
                  'Services offered': []}

        # extracing the name
        try:
            place_['Name'] = self.driver.find_elements(By.CSS_SELECTOR, 'h1.fontHeadlineLarge')[0].text
        except IndexError as e:
            error(f'extract_details - {e}')

        if place_['Name'] == None:
            return None

        # extracking the place's website
        try:
            # place_['Website'] = self.driver.find_elements(By.XPATH,
            #                                              '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[9]/a/div/div[3]/div[1]')[0].text
            place_['Website'] = self.driver.find_elements(By.CSS_SELECTOR, 'div.rogA2c.ITvuef')[0].get_attribute(
                "textContent")
        except IndexError as e:
            error(f'extract_details - {e}')

        # extracking the place's Address
        '''
        try:
            place_['Address'] = self.driver.find_elements(By.XPATH,
                                                          '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[3]/button/div/div[3]/div[1]')[0].text
        except IndexError as e:
            error(f'extract_details - {e}')
            '''
        tags = self.driver.find_elements(By.CSS_SELECTOR, 'div.Io6YTe')

        if ',' in tags[0].get_attribute("innerHTML"):
            place_['Address'] = tags[0].get_attribute("innerHTML")

        # extracking the place's Phone number
        '''
        try:
            place_['Phone number'] = self.driver.find_elements(By.XPATH,
                                                          '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[10]/button/div/div[3]/div[1]')[0].text
        except IndexError as e:
            error(f'extract_details - {e}')
        '''
        for tag in tags:
            number = tag.get_attribute("innerHTML").replace('+', '')
            number = number.replace(' ', '')
            number = number.replace('-', '')
            number = number.replace('(', '')
            number = number.replace(')', '')
            if number.isnumeric():
                place_['Phone number'] = tag.get_attribute("innerHTML")

        # extracking the place's Rating
        try:
            place_['Rating'] = \
                self.driver.find_elements(By.CSS_SELECTOR, 'div.F7nice')[0].find_elements(By.CSS_SELECTOR, 'span')[
                    0].text
        except IndexError as e:
            error(f'extract_details - {e}')

        # extracking the place's Categories
        try:
            place_['Categories'] = self.driver.find_elements(By.XPATH,
                                                             '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button')[
                0].text
        except IndexError as e:
            error(f'extract_details - {e}')

        bt = self.driver.find_elements(By.XPATH,
                                       '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]')
        if bt:
            bt[0].click()
            time.sleep(SCROLL_PAUSE_TIME / 2)
            divs = self.driver.find_elements(By.CSS_SELECTOR, 'div.iP2t7d.fontBodyMedium')
            for div in divs:
                h = div.find_element(By.TAG_NAME, 'h2').get_attribute("innerHTML")
                if 'Offerings' == h:
                    lis = div.find_elements(By.TAG_NAME, 'li')
                    if lis:
                        for li in lis:
                            place_['Services offered'].append(li.text)
        # shuld convert place_['Services offered'] list in to a string
        Place(place_['Name'], place_['Website'], place_['Address'], place_['Phone number'], place_['Categories'],
              place_['Rating'], ', '.join(place_['Services offered']), Scraper.search_query)

    def search(self):
        url = 'https://www.google.com/maps/search/' + '+'.join(self.search_query.split(' '))
        procces(f"downloading webpage => {url}")
        self.driver.get(url)
        procces(f'fletching search result. this may take up to {search_timeout} seconds....')
        global SCROLL_PAUSE_TIME
        start_t = time.time()
        while True:
            # Scroll down to bottom
            try:
                ele = self.driver.find_element(By.XPATH,
                                               '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]')
                self.driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
            except:
                try:
                    self.driver.find_element(By.XPATH,
                                             '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
                except:
                    error('"Accept All" button canot find')
            # Calculate new scroll height and compare with last scroll height
            cheke = self.driver.find_elements(By.XPATH, '//*[contains(text(), "reached the end of the list.")]')
            if cheke or time.time() - start_t > search_timeout:
                break
        links_for_places = []
        for li in self.driver.find_elements(By.CSS_SELECTOR, 'a'):
            if li.get_attribute('href'):
                if '/www.google.com/maps' in li.get_attribute('href'):
                    links_for_places.append(li.get_attribute('href'))
        success('fletching search result  completed')
        return links_for_places

    def shutdown(self):
        try:
            self.driver.quit()
        except KeyboardInterrupt as e:
            raise e
        except :
            pass
        success("scrapper quited")
