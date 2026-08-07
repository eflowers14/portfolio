from django.core.management import call_command
from django.test import TestCase

from core.management.commands import seed as seed_command
from core.models import SocialLink


class SeedCommandTests(TestCase):
    def test_seed_replaces_previous_social_links(self):
        SocialLink.objects.create(
            label="Antiguo",
            url="https://example.com/old",
            icon="github",
        )

        call_command("seed")

        self.assertFalse(SocialLink.objects.filter(url="https://example.com/old").exists())
        self.assertTrue(SocialLink.objects.filter(url="https://x.com/eflowersssss").exists())
        self.assertEqual(SocialLink.objects.count(), len(seed_command.SOCIAL_LINKS_DATA))
