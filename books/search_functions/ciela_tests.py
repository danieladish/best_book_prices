import unittest

from ciela_search_query import (search_ciela)

class TestSearchCiela(unittest.TestCase):
    def test_missing_author(self):
        """Test case to check handling of a missing author in the search result."""
        title_promt, author_promt = "BEYOND THE STORY", ""
        expected_output = {'title': 'BEYOND THE STORY : Десет години от историята на BTS',  'author': '', 'publisher': 'Сиела', 'price': '49.9', 'link': 'https://www.ciela.com/bts-beyond-the-story.html'}
        actual_output = search_ciela(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_incomplete_title(self):
        """Test case to check the search result for incomplete title."""
        title_promt, author_promt = "Змей", "Симона Панова"
        #added a new e-book that precedes the regular book. Could change in time 
        #expected_output = {'title': 'Змей побратим', 'author': 'Симона Панова', 'publisher': 'Сиела', 'price': '24', 'link': 'https://www.ciela.com/zmej-pobratim.html'}
        expected_output = {'title': 'Е-книга Змей закрилник', 'author': 'Симона Панова', 'publisher': 'Сиела', 'price': '17', 'link': 'https://www.ciela.com/e-kniga-zmej-zakrilnik.html'}
        actual_output = search_ciela(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)
    
    def test_promt_with_similar_titles(self):
        """Test case to check the search result for title that results in more than one of the authors books."""
        title_promt, author_promt = "Изкуство да не ти пука", "Марк Менсън"
        expected_output = {'title': 'Тънкото изкуство да не ти пука', 'author': 'Марк Менсън', 'publisher': 'Хермес', 'price': '17.95', 'link': 'https://www.ciela.com/tankoto-izkustvo-da-ne-ti-puka.html'}
        actual_output = search_ciela(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

    def test_promt_with_wrong_author(self):
        """Test case to check the search result for wrong author"""
        title_promt, author_promt = "pride and prejudice", 'Симона Панова'
        expected_output = {}
        actual_output = search_ciela(title_promt, author_promt)
        self.assertEqual(actual_output, expected_output)

# Run the tests
if __name__ == "__main__":
    unittest.main()
