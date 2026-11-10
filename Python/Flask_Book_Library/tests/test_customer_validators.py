import unittest

from project.customers.validators import validate_customer, validate_text, validate_age


class ValidCustomerTests(unittest.TestCase):
    def test_valid_customer(self):
        self.assertEqual(validate_customer('Jan Kowalski', 'Warszawa', '30'), ('Jan Kowalski', 'Warszawa', 30))

    def test_polish_characters_hyphen_apostrophe(self):
        self.assertEqual(validate_text('Łukasz Żółć-O\'Brien', 'name'), 'Łukasz Żółć-O\'Brien')

    def test_whitespace_is_stripped(self):
        self.assertEqual(validate_text('  Anna  ', 'name'), 'Anna')

    def test_age_boundaries(self):
        self.assertEqual(validate_age(0), 0)
        self.assertEqual(validate_age(150), 150)


class InvalidCustomerTests(unittest.TestCase):
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        '<img src=x onerror=alert(1)>',
        '"><svg onload=alert(1)>',
        "' onmouseover='alert(1)",
        'javascript:alert(1)',
        '<b>bold</b>',
    ]

    def test_xss_payloads_rejected_in_name(self):
        for payload in self.XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_customer(payload, 'Warszawa', 30)

    def test_xss_payloads_rejected_in_city(self):
        for payload in self.XSS_PAYLOADS:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    validate_customer('Jan', payload, 30)

    def test_empty_values_rejected(self):
        for value in ('', '   '):
            with self.assertRaises(ValueError):
                validate_text(value, 'name')

    def test_too_long_rejected(self):
        with self.assertRaises(ValueError):
            validate_text('a' * 65, 'name')

    def test_digits_rejected(self):
        with self.assertRaises(ValueError):
            validate_text('Jan123', 'name')

    def test_non_string_rejected(self):
        with self.assertRaises(ValueError):
            validate_text(None, 'name')

    def test_invalid_age_rejected(self):
        for value in ('abc', '', None, -1, 151, '<script>'):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_age(value)


if __name__ == '__main__':
    unittest.main()
