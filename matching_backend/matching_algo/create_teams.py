import random
from matching_algo.calculate_final_scores import calculate_final_scores
from django.core.management import call_command

def form_teams():
    final_scores, user_profiles = calculate_final_scores()
    teams = []
    used_users = set()

    # Get lists of users by role
    business_users = [i for i, user in enumerate(user_profiles) if user.role_business and i not in used_users]
    engineer_users = [i for i, user in enumerate(user_profiles) if user.role_engineer and i not in used_users]
    finance_users = [i for i, user in enumerate(user_profiles) if user.role_finance and i not in used_users]

    # Form teams starting with business users
    for business_user in business_users:
        if business_user in used_users:
            continue

        team = [business_user]
        used_users.add(business_user)

        # Find best matching engineer
        if engineer_users:
            best_engineer = max(engineer_users, key=lambda x: final_scores[business_user][x])
            team.append(best_engineer)
            used_users.add(best_engineer)
            engineer_users.remove(best_engineer)

        # Find best matching finance person
        if finance_users:
            best_finance = max(finance_users, key=lambda x: final_scores[business_user][x])
            team.append(best_finance)
            used_users.add(best_finance)
            finance_users.remove(best_finance)

        teams.append(team)

    # Handle leftover users
    leftover_users = [i for i in range(len(user_profiles)) if i not in used_users]

    # Randomly shuffle leftover users before forming teams
    random.shuffle(leftover_users)

    # Form teams of 3 from leftover users
    while len(leftover_users) >= 3:
        team = leftover_users[:3]
        teams.append(team)
        leftover_users = leftover_users[3:]

    # If there are 1 or 2 users left, add them to the smallest existing teams
    if leftover_users:
        sorted_teams = sorted(teams, key=len)
        for user in leftover_users:
            smallest_team = sorted_teams[0]
            smallest_team.append(user)
            sorted_teams = sorted(sorted_teams, key=len)

    # Flush database
    try:
        call_command('flush', interactive=False)
        print('Database flushed')
    except Exception as e:
        print('Error flushing database')
        print(e)

    # Convert user indices to UserProfile objects
    return [[user_profiles[i] for i in team] for team in teams]