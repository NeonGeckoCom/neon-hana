from unittest import TestCase

from neon_hana.hub_id import generate_hub_id, _ADJECTIVES, _NOUNS


class TestHubIdGenerator(TestCase):
    def test_words_from_lists(self):
        hub_id = generate_hub_id()
        adj1, adj2, noun = hub_id.split("-")
        self.assertIn(adj1, _ADJECTIVES, f"{adj1} not in adjectives")
        self.assertIn(adj2, _ADJECTIVES, f"{adj2} not in adjectives")
        self.assertIn(noun, _NOUNS, f"{noun} not in nouns")

    def test_adjectives_always_distinct(self):
        for _ in range(5):
            adj1, adj2, _ = generate_hub_id().split("-")
            self.assertNotEqual(adj1, adj2,
                                "Both adjective slots drew the same word")

    def test_no_duplicates_in_word_lists(self):
        self.assertEqual(len(_ADJECTIVES), len(set(_ADJECTIVES)),
                         "Duplicate adjectives found")
        self.assertEqual(len(_NOUNS), len(set(_NOUNS)),
                         "Duplicate nouns found")
