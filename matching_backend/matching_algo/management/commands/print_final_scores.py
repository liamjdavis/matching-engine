from django.core.management.base import BaseCommand
from matching_algo.calculate_final_scores import calculate_final_scores

class Command(BaseCommand):
    help = 'Calculate interest and goal similarity scores between user profiles'

    def handle(self, *args, **kwargs):
        # Run the imported function
        calculate_final_scores()
