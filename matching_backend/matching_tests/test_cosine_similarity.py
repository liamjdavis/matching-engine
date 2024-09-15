from matching_algo.models import UserProfile
import pytest
from django.contrib.auth.models import User
import pandas as pd
from matching_algo.cosine_similarity import calculate_cosine_similarity

@pytest.mark.django_db
def test_identical_user_profiles_cosine_similarity():
    # Step 1: Create two identical UserProfile instances
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform"
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform"
    )

    # Step 2: Put the two identical profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate cosine similarity
    similarities = calculate_cosine_similarity(user_profiles)

    # Step 4: Assert the similarity should be very high (close to 1)
    assert similarities[0][1] > 0.9, f"Expected similarity > 0.9 but got {similarities[0][1]}"
    assert similarities[1][0] > 0.9, f"Expected similarity > 0.9 but got {similarities[1][0]}"


@pytest.mark.django_db
def test_completely_different_user_profiles_cosine_similarity():
    # Step 1: Create two completely different UserProfile instances
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform"
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Smith",
        majors="History",
        add_info="Passionate about ancient civilizations",
        idea="A historical archive website"
    )

    # Step 2: Put the two completely different profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate cosine similarity
    similarities = calculate_cosine_similarity(user_profiles)

    # Step 4: Assert the similarity should be very low (close to 0)
    assert similarities[0][1] < 0.2, f"Expected similarity < 0.2 but got {similarities[0][1]}"
    assert similarities[1][0] < 0.2, f"Expected similarity < 0.2 but got {similarities[1][0]}"


@pytest.mark.django_db
def test_partially_similar_user_profiles_cosine_similarity():
    # Step 1: Create two UserProfile instances with some common fields
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="Loves programming and AI",
        idea="An AI-driven platform"
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Doe",
        majors="Computer Science",
        add_info="Interested in AI but focuses on business strategies",
        idea="An AI startup"
    )

    # Step 2: Put the two partially similar profiles in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate cosine similarity
    similarities = calculate_cosine_similarity(user_profiles)

    # Step 4: Assert the similarity should be somewhere between 0 and 1
    assert 0.3 < similarities[0][1] < 0.8, f"Expected similarity between 0.3 and 0.8 but got {similarities[0][1]}"
    assert 0.3 < similarities[1][0] < 0.8, f"Expected similarity between 0.3 and 0.8 but got {similarities[1][0]}"


@pytest.mark.django_db
def test_empty_or_missing_fields_cosine_similarity():
    # Step 1: Create two UserProfile instances with missing/empty fields
    user1 = UserProfile.objects.create(
        name="John Doe",
        majors="Computer Science",
        add_info="",
        idea=""
    )
    
    user2 = UserProfile.objects.create(
        name="Jane Smith",
        majors="",
        add_info="Interested in technology",
        idea=""
    )

    # Step 2: Put the profiles with empty/missing fields in a list
    user_profiles = [user1, user2]

    # Step 3: Calculate cosine similarity
    similarities = calculate_cosine_similarity(user_profiles)

    # Step 4: Assert the similarity should be low since most fields are missing
    assert similarities[0][1] < 0.4, f"Expected similarity < 0.4 but got {similarities[0][1]}"
    assert similarities[1][0] < 0.4, f"Expected similarity < 0.4 but got {similarities[1][0]}"