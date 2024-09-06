from django.core.management.base import BaseCommand
from matching_algo.goal_interests_match import calculate_interests_goals_scores

class Command(BaseCommand):
    help = 'Calculate interest and goal similarity scores between user profiles'

    def handle(self, *args, **kwargs):
        # Run the imported function
        calculate_interests_goals_scores()
