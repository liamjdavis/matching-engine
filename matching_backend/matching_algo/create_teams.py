from matching_algo.calculate_final_scores import calculate_final_scores
from django.core.management import call_command

def form_teams():
    print("calculating final scores")
    final_scores, user_profiles = calculate_final_scores()
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

    # Distribute leftover users to existing teams or create new teams
    while leftover_users:
        if len(leftover_users) >= 3:
            new_team = leftover_users[:3]
            teams.append(new_team)
            leftover_users = leftover_users[3:]
        else:
            # Add remaining users to existing teams based on highest average similarity
            for user in leftover_users:
                best_team = max(teams, key=lambda team: sum(final_scores[user][member] for member in team) / len(team))
                best_team.append(user)
            leftover_users = []

    # Ensure each team has at least 3 members
    while any(len(team) < 3 for team in teams):
        teams.sort(key=len)  # Sort teams by size, smallest first
        small_team = teams[0]
        large_teams = [team for team in teams if len(team) > 3]
        
        if not large_teams:
            # If no team has more than 3 members, we can't redistribute
            break
        
        # Find the best user to move from a large team to the small team
        best_user = None
        best_score = float('-inf')
        best_source_team = None
        
        for large_team in large_teams:
            for user in large_team:
                score = sum(final_scores[user][member] for member in small_team) / len(small_team)
                if score > best_score:
                    best_score = score
                    best_user = user
                    best_source_team = large_team
        
        # Move the best user to the small team
        best_source_team.remove(best_user)
        small_team.append(best_user)

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

    # Print teams by user name
    print("\nGenerated Teams:")
    for i, team in enumerate(final_teams, 1):
        print(f"Team {i}:")
        for user in team:
            print(f"  - {user.name}")
        print()  # Add a blank line between teams for better readability

    return final_teams