from matching_algo.models import UserProfile
import pytest
from django.contrib.auth.models import User
import pandas as pd
from matching_algo.calculate_final_scores import calculate_final_scores



@pytest.mark.django_db
def test_identical_user_profiles_final_scores():
    # Step 1: Create two identical UserProfile instances
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform",
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
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform",
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

    # Step 3: Calculate final scores
    final_scores, _ = calculate_final_scores(user_profiles)

    # Step 4: Assert that the final score is high for identical profiles
    assert final_scores[0][1] > 0.9, f"Expected high final score, but got {final_scores[0][1]}"
    assert final_scores[1][0] > 0.9, f"Expected high final score, but got {final_scores[1][0]}"


@pytest.mark.django_db
def test_completely_different_user_profiles_final_scores():
    # Step 1: Create two completely different UserProfile instances
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform",
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
        majors="History",
        add_info="Interested in ancient civilizations",
        idea="A historical archive",
        interest_arts=False,
        interest_education=False,
        interest_finance=True,
        interest_healthcare=True,
        interest_sustainability=True,
        interest_social_impact=False,
        interest_technology=False,
        goal_learn=False,
        goal_relations=True,
        goal_idea=False,
        goal_problems=True,
        goal_win_support=True
    )

    # Step 2: Put the two completely different profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate final scores
    final_scores, _ = calculate_final_scores(user_profiles)

    # Step 4: Assert that the final score is low for completely different profiles
    assert final_scores[0][1] < 0.5, f"Expected low final score, but got {final_scores[0][1]}"
    assert final_scores[1][0] < 0.5, f"Expected low final score, but got {final_scores[1][0]}"


@pytest.mark.django_db
def test_partially_matching_user_profiles_final_scores():
    # Step 1: Create two partially similar UserProfile instances
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform",
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
        majors="Computer Science",
        add_info="Interested in AI but with a business focus",
        idea="An AI-based startup",
        interest_arts=True,
        interest_education=False,
        interest_finance=False,
        interest_healthcare=False,
        interest_sustainability=False,
        interest_social_impact=True,
        interest_technology=True,
        goal_learn=True,
        goal_relations=False,
        goal_idea=False,
        goal_problems=False,
        goal_win_support=True
    )

    # Step 2: Put the two partially similar profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate final scores
    final_scores, _ = calculate_final_scores(user_profiles)

    # Step 4: Assert that the final score is moderate for partially matching profiles
    assert 0.6 < final_scores[0][1] < 1.6, f"Expected moderate final score, but got {final_scores[0][1]}"
    assert 0.6 < final_scores[1][0] < 1.6, f"Expected moderate final score, but got {final_scores[1][0]}"


@pytest.mark.django_db
def test_empty_fields_user_profiles_final_scores():
    # Step 1: Create two UserProfile instances with missing or empty fields
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="",
        idea="",
        interest_arts=True,
        interest_education=False,
        interest_finance=False,
        interest_healthcare=False,
        interest_sustainability=False,
        interest_social_impact=False,
        interest_technology=True,
        goal_learn=False,
        goal_relations=False,
        goal_idea=False,
        goal_problems=False,
        goal_win_support=False
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Smith",
        majors="History",
        add_info="",
        idea="",
        interest_arts=False,
        interest_education=True,
        interest_finance=False,
        interest_healthcare=True,
        interest_sustainability=False,
        interest_social_impact=False,
        interest_technology=False,
        goal_learn=True,
        goal_relations=True,
        goal_idea=True,
        goal_problems=True,
        goal_win_support=True
    )

    # Step 2: Put the two profiles with empty fields in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate final scores
    final_scores, _ = calculate_final_scores(user_profiles)

    # Step 4: Assert that the final score is low due to missing or empty fields
    assert final_scores[0][1] < 0.8, f"Expected low final score, but got {final_scores[0][1]}"
    assert final_scores[1][0] < 0.8, f"Expected low final score, but got {final_scores[1][0]}"
