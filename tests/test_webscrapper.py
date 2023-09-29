# Need to create Unitest (MockTesting) and CI/CD Pipeline

import unittest 
from src.core.advanced_webscraper import WebScraper

class TestWebScraper(unittest.TestCase):
    def test_scan_url_for_links(self):
        scraper = WebScraper('https://www.firstpeople.us/FP-Html-Legends/')
        links = scraper.scan_url_for_links()
        
        # Check that it returns a list (replace this with more specific tests)
        self.assertIsInstance(links, list)


