import string
import unittest
from copy import deepcopy

import password_generator as generator


class PasswordGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.original_settings = deepcopy(generator.settings)
        generator.history.clear()

    def tearDown(self):
        generator.settings.clear()
        generator.settings.update(self.original_settings)
        generator.history.clear()

    def test_generated_password_has_requested_length_and_required_groups(self):
        generator.settings.update(
            length=24,
            include_symbols=True,
            exclude_confusing=False,
        )

        password = generator.generate_password()

        self.assertEqual(len(password), 24)
        self.assertTrue(any(character in string.ascii_lowercase for character in password))
        self.assertTrue(any(character in string.ascii_uppercase for character in password))
        self.assertTrue(any(character in string.digits for character in password))
        self.assertTrue(any(character in generator.SYMBOLS for character in password))

    def test_confusing_characters_are_excluded(self):
        generator.settings.update(length=128, exclude_confusing=True)

        password = generator.generate_password()

        self.assertTrue(generator.CONFUSING_CHARACTERS.isdisjoint(password))

    def test_password_without_symbols_uses_only_alphanumeric_characters(self):
        generator.settings.update(length=64, include_symbols=False)

        password = generator.generate_password()

        self.assertTrue(password.isalnum())

    def test_entropy_classification_increases_with_length(self):
        short_strength, short_entropy = generator.calculate_strength("aB3!")
        long_strength, long_entropy = generator.calculate_strength("aB3!" * 8)

        self.assertEqual(short_strength, "Fraca")
        self.assertEqual(long_strength, "Muito forte")
        self.assertGreater(long_entropy, short_entropy)


if __name__ == "__main__":
    unittest.main()
