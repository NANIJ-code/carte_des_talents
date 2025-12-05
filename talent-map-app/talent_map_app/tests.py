from django.test import TestCase
from .models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create(
            username='testuser',
            skills='Python, Django',
            talents='Web Development',
            languages='English, French',
            verified=True
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.username, 'testuser')
        self.assertEqual(self.user_profile.skills, 'Python, Django')
        self.assertEqual(self.user_profile.talents, 'Web Development')
        self.assertEqual(self.user_profile.languages, 'English, French')
        self.assertTrue(self.user_profile.verified)

    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile), 'testuser')

class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create(
            username='testuser',
            skills='Python, Django',
            talents='Web Development',
            languages='English, French',
            verified=True
        )

    def test_profile_detail_view(self):
        response = self.client.get(f'/profile/{self.user_profile.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Python, Django')

    def test_profile_create_view(self):
        response = self.client.post('/profile/create/', {
            'username': 'newuser',
            'skills': 'JavaScript',
            'talents': 'Frontend Development',
            'languages': 'English',
            'verified': False
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(UserProfile.objects.filter(username='newuser').exists())

    def test_profile_edit_view(self):
        response = self.client.post(f'/profile/edit/{self.user_profile.id}/', {
            'username': 'updateduser',
            'skills': 'Python, Django, React',
            'talents': 'Full Stack Development',
            'languages': 'English, Spanish',
            'verified': True
        })
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.username, 'updateduser')
        self.assertEqual(self.user_profile.skills, 'Python, Django, React')
        self.assertTrue(self.user_profile.verified)