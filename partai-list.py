import requests
from bs4 import BeautifulSoup
import csv

# Fetch the HTML content from the website
response = requests.get("https://www.bijakmemilih.id/partai")
page_content = response.text

# Initialize BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

# Find the container that holds all parties; you'll need to adjust this based on the actual HTML
party_containers = soup.find_all('div', {'class': 'framer-fvxdms'})

# Initialize an empty list to hold party details
party_details = []

# Loop through each party container to extract information
for container in party_containers:
    party_info = {}
    
    party_number_element = container.find('h3', {'class': 'framer-text'})
    if party_number_element:
        party_info['Party Number'] = party_number_element.text.strip()
    
    party_name_element = container.find_all('h3', {'class': 'framer-text'})
    if party_name_element and len(party_name_element) > 1:
        party_info['Party Name'] = party_name_element[1].text.strip()
    
    profile_link_element = container.find('a', {'data-highlight': 'true'})
    if profile_link_element:
        party_info['Profile Link'] = profile_link_element.get('href').strip()
    
    image_link_element = container.find('img')
    if image_link_element:
        party_info['Image Link'] = image_link_element.get('src')
    
    if party_info:  # Check if the dictionary is not empty
        party_details.append(party_info)

# Open a CSV file for writing
with open('raw_data/party_details.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Party Number', 'Party Name', 'Profile Link', 'Image Link']  # CSV column headers
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    csv_writer.writeheader()  # Write the headers
    
    # Write the data
    for details in party_details:
        csv_writer.writerow(details)
        
# Print the extracted details (optional)
for details in party_details:
    print(f"Party Number: {details.get('Party Number', 'N/A')}")
    print(f"Party Name: {details.get('Party Name', 'N/A')}")
    print(f"Profile Link: {details.get('Profile Link', 'N/A')}")
    print(f"Image Link: {details.get('Image Link', 'N/A')}")
    print('-' * 40)