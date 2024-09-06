from django.core.management.base import BaseCommand
from matching_algo.cosine_similarity import calculate_cosine_similarity

class Command(BaseCommand):
    help = 'Calculate interest and goal similarity scores between user profiles'

    def handle(self, *args, **kwargs):
        # Run the imported function
        calculate_cosine_similarity()
