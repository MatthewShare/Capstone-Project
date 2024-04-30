import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_URL = "https://forms.gle/ggXanF8UiZebdSnp6"

response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")
links = soup.select(selector="ul li div div article div div a")

list_of_links = [link.get("href") for link in links]
list_of_links = list_of_links[::2]

prices = soup.select(selector="ul li div div article div div div div")
list_of_prices = [price.text.strip().split("/")[0].split("+")[0] for price in prices]
list_of_prices = list_of_prices[::3]

addresses = soup.select(selector="ul li div div article div div a address")
list_of_addresses = [address.text.strip() for address in addresses]

list_of_all_data = [(list_of_addresses[number], list_of_prices[number], list_of_links[number]) for number in range(0, len(list_of_links))]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_URL)

for each_property in list_of_all_data:
    inputs = driver.find_elements(by=By.CSS_SELECTOR, value="input[type='text']")
    for number in range(0, 3):
        inputs[number].send_keys(each_property[number])
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="div[jsname='M2UYVd']")
    submit_button.click()
    record_another_response = driver.find_element(by=By.LINK_TEXT, value="Submit another response")
    record_another_response.click()

