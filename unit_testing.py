import unittest
import os
import json
from voting_cli import (
    register_user, authenticate_user,
    generate_token, cast_vote, get_results,
    USERS_FILE, VOTES_FILE, TOKENS_FILE,
    CANDIDATES
)

# Override file paths for testing
TEST_USERS = "test_users.json"
TEST_VOTES = "test_votes.json"
TEST_TOKENS = "test_tokens.json"

# Patch the module variables
import voting_cli
voting_cli.USERS_FILE = TEST_USERS
voting_cli.VOTES_FILE = TEST_VOTES
voting_cli.TOKENS_FILE = TEST_TOKENS


class TestVotingSystem(unittest.TestCase):
    def setUp(self):
        # Clean up any test files
        for f in [TEST_USERS, TEST_VOTES, TEST_TOKENS]:
            if os.path.exists(f):
                os.remove(f)

    def test_registration_and_authentication(self):
        success, msg = register_user("testuser", "password123")
        self.assertTrue(success)
        self.assertEqual(msg, "Registration successful.")

        success, msg = authenticate_user("testuser", "password123")
        self.assertTrue(success)
        self.assertEqual(msg, "Login successful.")

        success, msg = authenticate_user("testuser", "wrongpass")
        self.assertFalse(success)

    def test_token_generation(self):
        register_user("voter1", "pass")
        token = generate_token("voter1")
        self.assertTrue(len(token) > 0)

    def test_vote_casting_and_result(self):
        register_user("voter2", "pass")
        token = generate_token("voter2")
        candidate = CANDIDATES[0]
        success, msg = cast_vote("voter2", token, candidate)
        self.assertTrue(success)
        self.assertEqual(msg, "Vote cast successfully!")

        results = get_results()
        self.assertIn(candidate, results)
        self.assertEqual(results[candidate], 1)

        # Voting again with same user should fail
        token2 = generate_token("voter2")
        success, msg = cast_vote("voter2", token2, candidate)
        self.assertFalse(success)
        self.assertEqual(msg, "You have already voted.")

    def test_invalid_token_or_candidate(self):
        register_user("voter3", "pass")
        token = generate_token("voter3")
        success, msg = cast_vote("voter3", "wrong-token", CANDIDATES[0])
        self.assertFalse(success)
        self.assertEqual(msg, "Invalid or expired token.")

        token = generate_token("voter3")
        success, msg = cast_vote("voter3", token, "Invalid Group")
        self.assertFalse(success)
        self.assertIn("Invalid candidate", msg)

    def tearDown(self):
        # Clean up test files after each test
        for f in [TEST_USERS, TEST_VOTES, TEST_TOKENS]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == '__main__':
    unittest.main()
