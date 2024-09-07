from django.core.management.base import BaseCommand
from matching_algo.create_teams import form_teams

class Command(BaseCommand):
    help = 'Calculate interest and goal similarity scores between user profiles'

    def handle(self, *args, **kwargs):
        # Run the imported function
        form_teams()
