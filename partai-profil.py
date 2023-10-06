import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import pandas
from bs4 import BeautifulSoup

def scroll_to_end(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = '/usr/local/bin/chromedriver'

driver = webdriver.Chrome(options=chrome_options)

csv_path = 'raw_data/partai_list.csv'
df = pd.read_csv(csv_path)

profile_links = df['Profile Link'].tolist()
party_names = df['Party Name'].tolist()

scraped_df = pd.DataFrame()

for profile_link, party_name in zip(profile_links, party_names):
    if pd.isna(profile_link):
        print(f"Skipping empty profile link for {party_name}.")
        continue

    full_url = f"https://www.bijakmemilih.id/{profile_link}"

    driver.get(full_url)

    scroll_to_end(driver)

    collapsible_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-framer-name*="Closed"][tabindex="0"]')

    page_source = driver.page_source

    for element in collapsible_elements:
        try:
            ActionChains(driver).move_to_element(element).click(element).perform()
            time.sleep(1) 
        except Exception as e:
            print(f"Could not click element: {e}")

    try:
        korupsi_section = driver.find_element(By.CSS_SELECTOR, 'div[data-framer-name="Korupsi"]')
    except Exception as e:
        print(f"Could not find Korupsi section: {e}")
        korupsi_section = None

    data_framer_names = {
        "Profil Partai": "Data Profil Partai",
        "Pemungutan Suara": "Voting History",
        "Mantan Narapidana Yang Dicalonkan di 2024": "Partai List"
    }

    scraped_data = {}

    for section_name, framer_name in data_framer_names.items():
        if isinstance(framer_name, dict):
            scraped_data[section_name] = {}
            for sub_section, sub_framer in framer_name.items():
                try:
                    section_element = driver.find_element(By.CSS_SELECTOR, f'div[data-framer-name="{sub_framer}"]')
                    scraped_data[section_name][sub_section] = section_element.text
                except Exception as e:
                    print(f"Could not scrape data for {sub_section}: {e}")
                    scraped_data[section_name][sub_section] = "Not found"
        else:
            try:
                section_element = driver.find_element(By.CSS_SELECTOR, f'div[data-framer-name="{framer_name}"]')
                scraped_data[section_name] = section_element.text
            except Exception as e:
                print(f"Could not scrape data for {section_name}: {e}")
                scraped_data[section_name] = "Not found"

driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')

korupsi_section = soup.find('div', {'data-framer-name': 'Data Korupsi'})

if korupsi_section:
    suap_section = korupsi_section.find('div', {'data-framer-name': 'Suap & Gratifikasi'})
    kerugian_section = korupsi_section.find('div', {'data-framer-name': 'Kerugian Negara'})
    
    scraped_data['Suap & Gratifikasi'] = suap_section.text if suap_section else "Not found"
    scraped_data['Kerugian Keuangan Negara'] = kerugian_section.text if kerugian_section else "Not found"

# Print or process the scraped data
# for section, data in scraped_data.items():
#     print(f"{section} Data:")
#     print(data[:500])  # Print only the first 500 characters
#     print('-' * 40)
output_csv_path = 'raw_data/scraped_data.csv'
scraped_df.to_csv(output_csv_path, index=False)