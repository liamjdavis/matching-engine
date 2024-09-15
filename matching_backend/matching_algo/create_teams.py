from matching_algo.calculate_final_scores import calculate_final_scores
from matching_algo.models import UserProfile
from django.core.management import call_command

user_profiles = UserProfile.objects.all()

def form_teams(user_profiles):
    print("calculating final scores")
    final_scores, user_profiles = calculate_final_scores(user_profiles)
    teams = []
    used_users = set()

    print("generating teams")

    # Get lists of users by role
    business_users = [i for i, user in enumerate(user_profiles) if user.role_business and i not in used_users]
    engineer_users = [i for i, user in enumerate(user_profiles) if user.role_engineer and i not in used_users]
    finance_users = [i for i, user in enumerate(user_profiles) if user.role_finance and i not in used_users]

    # Form initial teams
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

    # Distribute leftover users to teams with less than 3 members
    for team in teams:
        while len(team) < 3 and leftover_users:
            best_user = max(leftover_users, key=lambda x: sum(final_scores[x][member] for member in team) / len(team))
            team.append(best_user)
            leftover_users.remove(best_user)
            used_users.add(best_user)

    # Create new teams with leftover users
    while leftover_users:
        new_team = []
        for _ in range(3):
            if leftover_users:
                new_team.append(leftover_users.pop(0))
        teams.append(new_team)

    # Ensure teams have only 3 or 4 members by redistributing users
    small_teams = [team for team in teams if len(team) < 3]
    teams = [team for team in teams if len(team) >= 3]

    while small_teams:
        team = small_teams.pop(0)
        if len(team) == 2:
            if small_teams:
                next_team = small_teams.pop(0)
                team += next_team
            if len(team) == 4:
                teams.append(team)
            else:
                small_teams.append(team)
        elif len(team) == 1:
            if teams:
                # Add single user to a team of 3 to make it a team of 4
                teams.sort(key=len)
                smallest_team = teams[0]
                if len(smallest_team) == 3:
                    smallest_team.append(team[0])
                else:
                    small_teams.append(team)
            else:
                small_teams.append(team)

    # Combine remaining small teams to make sure only 3 or 4 member teams remain
    while len(small_teams) > 0:
        current_team = small_teams.pop(0)
        if small_teams:
            next_team = small_teams.pop(0)
            current_team += next_team
        if len(current_team) <= 4:
            teams.append(current_team)
        else:
            teams.append(current_team[:3])
            small_teams.append(current_team[3:])

    print("teams generated")

    # Flush database
    try:
        call_command('flush', interactive=False)
        print('Database flushed')
    except Exception as e:
        print('Error flushing database')
        print(e)

    # Convert user indices to UserProfile objects
    final_teams = [[user_profiles[i] for i in team] for team in teams]

    return final_teams
