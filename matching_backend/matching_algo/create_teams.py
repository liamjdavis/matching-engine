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

    # Create teams of 3 from leftover users
    while len(leftover_users) >= 3:
        new_team = leftover_users[:3]
        teams.append(new_team)
        leftover_users = leftover_users[3:]

    # Handle remaining users
    if leftover_users:
        if len(leftover_users) == 1:
            # If only one user is left, add them to the last team
            teams[-1].append(leftover_users[0])
        else:  # len(leftover_users) == 2
            # If two users are left, create a new team
            teams.append(leftover_users)

    # Ensure all teams have at least 2 members
    single_member_teams = [team for team in teams if len(team) == 1]
    multi_member_teams = [team for team in teams if len(team) > 1]

    while single_member_teams:
        if len(single_member_teams) >= 2:
            # Combine two single-member teams
            new_team = single_member_teams.pop(0) + single_member_teams.pop(0)
            multi_member_teams.append(new_team)
        else:
            # Add the last single member to a team of 2 if possible, otherwise to a team of 3
            single_member = single_member_teams.pop(0)[0]
            two_member_teams = [team for team in multi_member_teams if len(team) == 2]
            if two_member_teams:
                two_member_teams[0].append(single_member)
            else:
                multi_member_teams[0].append(single_member)

    teams = multi_member_teams

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