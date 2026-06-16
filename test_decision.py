import json
import unittest
from decision import decide_application_method

class TestDecision(unittest.TestCase):
    
    def test_json_schema(self):
        # We mock the content and check if it parses and returns the expected keys.
        # Note: This requires GROQ_API_KEY in the .env to actually run against the API,
        # but serves as a basic integration test.
        url = "http://example.com/contact"
        content = "Please send your application and CV to jobs@example.com."
        
        result = decide_application_method(url, content)
        if result is None:
            self.skipTest("GROQ_API_KEY is not set or API failed. Skipping test.")
            
        self.assertIn("method", result)
        self.assertIn(result["method"], ["email", "form"])
        self.assertIn("email", result)
        self.assertIn("form_action", result)
        self.assertIn("fields", result)
        self.assertIn("submit_hint", result)
        
        # In this specific test case, we expect it to detect an email
        self.assertEqual(result["method"], "email")
        self.assertEqual(result["email"], "jobs@example.com")

if __name__ == '__main__':
    unittest.main()
