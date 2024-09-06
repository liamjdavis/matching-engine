import os
from django.core.management.base import BaseCommand
from matching_algo.clean_data import clean_and_create_users

class Command(BaseCommand):
    help = 'Import users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['filepath']
        
        # Check if the file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('File does not exist'))
            return

        try:
            # Call the function to process the CSV file
            clean_and_create_users(file_path)
            self.stdout.write(self.style.SUCCESS('Users have been imported successfully'))
        except ValueError as e:
            # Handle specific exception for column mismatch or data issues
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
        except Exception as e:
            # Handle other potential exceptions
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
