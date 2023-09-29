import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import re
import os
from queue import Queue

class WebScraper:
    # Constructor of the Alchemical Circle
    def __init__(self, base_url):
        self.base_url = base_url

    # The Astral Projector: Scans a URL for Usable Links
    def scan_url_for_links(self):
        response = requests.get(self.base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.html') and 'cookie' not in href.lower() and 'privacy' not in href.lower():
                full_url = urljoin(self.base_url, href)
                links.append(full_url)
        return links

    # The Lore Master: Extracts the Essence of a Single Page
    def scrape_page_data(self, current_link):
        page = requests.get(current_link)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extracting the Sacred Title
        story_title_tag = soup.find('h1')
        story_title = story_title_tag.text if story_title_tag else "Unknown Title"

        # Unveiling the Tribe of Origin
        h2_tag = soup.find('h2')
        text = h2_tag.text if h2_tag else "Unknown Tribe"
        words = text.split()
        words_to_strip = ["An", "Legend"]
        tribe = " ".join([word for word in words if word not in words_to_strip])

        # Scribing the Lore
        story_content_tag = soup.find('div', class_="content")
        story_text = story_content_tag.text if story_content_tag else "Content Missing"

        self.save_csv_to_drive(story_text, tribe, story_title)

        return story_title, tribe, story_text

    # The Time Traveler: Scrapes Links with Breadth-First Search
    def scrape_links_bfs(self, link_list):
        queue = Queue()
        
        for link in link_list:
            queue.put(link)
            
        while not queue.empty():
            current_link = queue.get()
            
            print(f"Processing link: {current_link}")
            story_title, tribe, story_text = self.scrape_page_data(current_link)
            
            print(story_title)
            print(tribe)
            print(story_text)

    # The Scribe: Stores Extracted Lore as CSV Files
    def save_csv_to_drive(self, story_text, tribe, story_title):
        cleaned_tribe = re.sub(r'\W+', '_', tribe)
        cleaned_title = re.sub(r'\W+', '_', story_title)
        
        folder_path = '/Users/francinasimone/Desktop/DreamApp1/Starlight/Test2/' + cleaned_tribe + '/'
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = folder_path + cleaned_title + '.csv'
        
        csv_data = [[story_text]]
        
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_data)

# Example usage
scraper = WebScraper('https://www.firstpeople.us/FP-Html-Legends/')
link_list = scraper.scan_url_for_links()
scraper.scrape_links_bfs(link_list)