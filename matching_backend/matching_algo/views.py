from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from matching_algo.clean_data import clean_and_create_users
from matching_algo.create_teams import form_teams
from matching_algo.models import UserProfile

import os

# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        file_path = fs.save(csv_file.name, csv_file)
        file_url = fs.url(file_path)
        
        # Assuming clean_and_create_users accepts a file path
        clean_and_create_users(file_path)
        
        # Now form teams after the users are created
        teams = form_teams()
        
        # Collect the team information
        team_output = []
        for team in teams:
            team_output.append([user_profile.name for user_profile in team])
        
        # Clean up the uploaded file
        os.remove(file_path)
        
        return render(request, 'matching_algo/index.html', {'teams': team_output})

    return render(request, 'matching_algo/index.html')