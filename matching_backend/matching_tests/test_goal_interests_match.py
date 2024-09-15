from matching_algo.models import UserProfile
import pytest
from django.contrib.auth.models import User
import pandas as pd
from matching_algo.goal_interests_match import calculate_interests_goals_scores


@pytest.mark.django_db
def test_identical_user_profiles_similar_interests():
    # Step 1: Create two identical UserProfile instances with matching interests and goals
    user1 = UserProfile.objects.create(
        name="John Doe",
        interest_arts=True,
        interest_education=True,
        interest_finance=True,
        interest_healthcare=True,
        interest_sustainability=True,
        interest_social_impact=True,
        interest_technology=True,
        goal_learn=True,
        goal_relations=True,
        goal_idea=True,
        goal_problems=True,
        goal_win_support=True
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Doe",
        interest_arts=True,
        interest_education=True,
        interest_finance=True,
        interest_healthcare=True,
        interest_sustainability=True,
        interest_social_impact=True,
        interest_technology=True,
        goal_learn=True,
        goal_relations=True,
        goal_idea=True,
        goal_problems=True,
        goal_win_support=True
    )

    # Step 2: Put the two identical profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate interest and goal similarity scores
    similarity_scores = calculate_interests_goals_scores(user_profiles)

    # Step 4: Assert the similarity should be at its maximum
    # Since both profiles are identical, similarity should be high
    max_score = float(5/5) + (0.5 * 1.0)  # Full goal score (5) + weighted interest score
    assert similarity_scores[0][1] == max_score
    assert similarity_scores[1][0] == max_score


@pytest.mark.django_db
def test_completely_different_user_profiles_similar_interests():
    # Step 1: Create two completely different UserProfile instances with no matching interests or goals
    user1 = UserProfile.objects.create(
        name="John Doe",
        interest_arts=True,
        interest_education=False,
        interest_finance=True,
        interest_healthcare=False,
        interest_sustainability=True,
        interest_social_impact=False,
        interest_technology=True,
        goal_learn=True,
        goal_relations=False,
        goal_idea=True,
        goal_problems=False,
        goal_win_support=True
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Smith",
        interest_arts=False,
        interest_education=True,
        interest_finance=False,
        interest_healthcare=True,
        interest_sustainability=False,
        interest_social_impact=True,
        interest_technology=False,
        goal_learn=False,
        goal_relations=True,
        goal_idea=False,
        goal_problems=True,
        goal_win_support=False
    )

    # Step 2: Put the two completely different profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate interest and goal similarity scores
    similarity_scores = calculate_interests_goals_scores(user_profiles)

    # Step 4: Assert the similarity should be very low (zero or near zero)
    assert similarity_scores[0][1] == 0, f"The similarity score should be 0 but is {similarity_scores[0][1]}"
    assert similarity_scores[1][0] == 0, f"The similarity score should be 0 but is {similarity_scores[0][1]}"



@pytest.mark.django_db
def test_partially_matching_user_profiles_similar_interests():
    # Step 1: Create two UserProfile instances with some matching interests and goals
    user1 = UserProfile.objects.create(
        name="John Doe",
        interest_arts=True,
        interest_education=True,
        interest_finance=False,
        interest_healthcare=False,
        interest_sustainability=False,
        interest_social_impact=True,
        interest_technology=True,
        goal_learn=True,
        goal_relations=False,
        goal_idea=True,
        goal_problems=False,
        goal_win_support=False
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Smith",
        interest_arts=False,
        interest_education=False,
        interest_finance=False,
        interest_healthcare=True,
        interest_sustainability=True,
        interest_social_impact=True,
        interest_technology=True,
        goal_learn=False,
        goal_relations=False,
        goal_idea=False,
        goal_problems=False,
        goal_win_support=True
    )

    # Step 2: Put the two partially similar profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate interest and goal similarity scores
    similarity_scores = calculate_interests_goals_scores(user_profiles)

    # Step 4: Assert the similarity should be greater than zero but less than the maximum score
    partial_score = float(3 / 7)  # Interests: 3 out of 7 match
    goal_score = float(2 / 5)  # Goals: 2 out of 5 match
    expected_similarity = goal_score + (0.5 * partial_score)
    
    assert abs(similarity_scores[0][1] - expected_similarity) < 0.01  # Allow small rounding errors
    assert abs(similarity_scores[1][0] - expected_similarity) < 0.01

