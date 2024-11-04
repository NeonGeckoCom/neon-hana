from unittest import TestCase

from neon_hana.schema.user_profile import UserProfile

from neon_data_models.models.user import User


class TestUserProfile(TestCase):
    def test_user_profile(self):
        # Test default
        profile = UserProfile()
        self.assertIsInstance(profile, UserProfile)

        # Test from User
        default_user = User(username="test_user")
        profile = UserProfile.from_user_object(default_user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(default_user.username, profile.user.username)
