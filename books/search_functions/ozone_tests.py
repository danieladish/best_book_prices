import unittest

from ozone_search_query import (search_ozone)

class TestSearchOzone(unittest.TestCase):
    def test_full_title_and_author(self):
        """Test case to check the search result for full title and author."""
        title_promt, author_promt = "Змей побратим", "Симона Панова"
        expected_output = {'title': 'Змей побратим (Змей закрилник 2)', 'author': 'Симона Панова', 'price': '24.00', 'link': 'https://www.ozone.bg/product/zmey-pobratim-zmey-zakrilnik2'}
        actual_output = search_ozone(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_missing_author(self):
        """Test case to check handling of a missing author in the search result."""
        title_promt, author_promt = "BEYOND THE STORY", ""
        expected_output = {'title': 'BEYOND THE STORY : Десет години от историята на BTS', 'author': '', 'price': '49.90', 'link': 'https://www.ozone.bg/product/beyond-the-story-deset-godini-ot-istoriyata-na-bts'}
        actual_output = search_ozone(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_incomplete_title(self):
        """Test case to check the search result for incomplete title."""
        title_promt, author_promt = "Змей", "Симона Панова"
        expected_output = {'title': 'Змей закрилник (Змей закрилник 1)', 'author': 'Симона Панова', 'price': '20.00', 'link': 'https://www.ozone.bg/product/zmey-zakrilnik'}
        actual_output = search_ozone(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)
    
    def test_promt_with_similar_title(self):
        """Test case to check the search result for title that is not in this store but they have added it in the next days so"""
        title_promt, author_promt = "Изкуство да не ти пука", "Марк Менсън"
        expected_output = {'title': 'Тънкото изкуство да не ти пука', 'author': 'Марк Менсън', 'price': '17.95', 'link': 'https://www.ozone.bg/product/t-nkoto-izkustvo-da-ne-ti-puka'} 
        actual_output = search_ozone(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_promt_with_wrong_author(self):
        """Test case to check the search result for wrong author"""
        title_promt, author_promt = "pride and prejudice", 'Симона Панова'
        expected_output = {}
        actual_output = search_ozone(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

# Run the tests
if __name__ == "__main__":
    unittest.main()
