import unittest

from orange_search_query import (search_orange)

class TestSearchOrange(unittest.TestCase):
    def test_missing_author(self):
        """Test case to check handling of a missing author in the search result."""
        title_promt, author_promt = "BEYOND THE STORY", ""
        expected_output = {'title': 'BEYOND THE STORY: Десет години от историята на BTS', 'author': '', 'price': '49.9', 'link': 'https://www.orangecenter.bg/beyond-the-story-deset-godini-ot-istoriyata-na-bts.html'}
        actual_output = search_orange(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_incomplete_title(self):
        """Test case to check the search result for incomplete title."""
        title_promt, author_promt = "Змей", "Симона Панова"
        expected_output = {'title': 'Змей побратим', 'author': 'Симона Панова', 'price': '24', 'link': 'https://www.orangecenter.bg/zmey-pobratim.html'}
        actual_output = search_orange(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)
    
    def test_promt_with_similar_titles(self):
        """Test case to check the search result for title that results in more than one of the authors books."""
        title_promt, author_promt = "Изкуство да не ти пука", "Марк Менсън"
        expected_output = {'title': 'Тънкото изкуство да не ти пука', 'author': 'Марк Менсън', 'price': '17.95', 'link': 'https://www.orangecenter.bg/tankoto-izkustvo-da-ne-ti-puka.html'}
        actual_output = search_orange(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_promt_with_wrong_author(self):
        """Test case to check the search result for wrong author"""
        title_promt, author_promt = "pride and prejudice", 'Симона Панова'
        expected_output = {}
        actual_output = search_orange(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

# Run the tests
if __name__ == "__main__":
    unittest.main()
