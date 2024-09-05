from django.db import models

class UserProfile(models.Model):
    # Add name field
    name = models.CharField(max_length=255, default='Dhyey Mavani')
    
    # Combine all majors into one string
    majors = models.CharField(max_length=255)
    
    # Domains of Interest
    interest_arts = models.BooleanField(default=False)
    interest_education = models.BooleanField(default=False)
    interest_finance = models.BooleanField(default=False)
    interest_healthcare = models.BooleanField(default=False)
    interest_sustainability = models.BooleanField(default=False)
    interest_social_impact = models.BooleanField(default=False)
    interest_technology = models.BooleanField(default=False)
    
    # Goals for the Lab
    goal_learn = models.BooleanField(default=False)
    goal_relations = models.BooleanField(default=False)
    goal_idea = models.BooleanField(default=False)
    goal_problems = models.BooleanField(default=False)
    goal_win_support = models.BooleanField(default=False)
    
    # Roles interested in
    role_business = models.BooleanField(default=False)
    role_engineer = models.BooleanField(default=False)
    role_finance = models.BooleanField(default=False)
    
    # Additional information
    add_info = models.TextField(blank=True, null=True)
    idea = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name