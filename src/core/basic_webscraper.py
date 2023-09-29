# The Book of Web Scrapping: A Guide to Collecting Stories from FirstPeople.us

# The Magic Ingredients: Importing Libraries
# Import the necessary modules for web scraping and data storage.
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
from queue import Queue

# The Scroll of Constants: Define Global Variables
# Constants that shall not change during the script's execution are defined here.
BASE_URL = 'https://www.firstpeople.us/FP-Html-Legends/'
BASE_FOLDER_PATH = '/Users/francinasimone/Desktop/DreamApp1/Starlight/Test/'

# Elixir of Cleanliness: A String Cleaning Potion
# Function to remove unwanted characters from a string, making it URL and filesystem friendly.
def clean_string(s):
    return s.replace(" ", "_").replace("'", "")

# Summoning the Magic Mirror: Scanning URLs
# Function to fetch all story URLs on a given webpage.
def scan_url_for_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    return [
        urljoin(url, link.get('href'))
        for link in soup.find_all('a')
        if link.get('href') and link.get('href').endswith('.html')
    ]

# The Lore Keeper: Fetching Page Data
# Function to scrape the title, tribe, and content of a story from a URL.
def fetch_page_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1').text if soup.find('h1') else 'Unknown'
    tribe = soup.find('h2').text if soup.find('h2') else 'Unknown'
    content = soup.find('div', class_="content").text if soup.find('div', class_="content") else 'Content Missing'
    
    return title, tribe, content

# Scribing the Tome: Saving to CSV
# Function to save the scraped data to a CSV file.
def save_to_csv(title, tribe, content):
    folder_path = os.path.join(BASE_FOLDER_PATH, clean_string(tribe))
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, f"{clean_string(title)}.csv")
    
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, tribe])
        writer.writerow([content])

# The Hero's Journey: Main Function
# The main function where our scraping adventure begins.
def main():
    # Quest Log: Initialize Queue for BFS
    link_queue = Queue()
    
    # The Gathering: Add Links to Queue
    for link in scan_url_for_links(BASE_URL):
        link_queue.put(link)
        
    # The Trials: Process Each Link in the Queue
    while not link_queue.empty():
        current_link = link_queue.get()
        
        print(f"Scraping: {current_link}")
        title, tribe, content = fetch_page_data(current_link)
        
        print(f"Title: {title}\nTribe: {tribe}\nContent Length: {len(content)}")
        
        # The Reward: Save Data
        save_to_csv(title, tribe, content)

# The Portal: Where the Program Starts
if __name__ == "__main__":
    main()