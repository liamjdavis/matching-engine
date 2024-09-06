from matching_algo.cosine_similarity import calculate_cosine_similarity
from matching_algo.goal_interests_match import calculate_interests_goals_scores
from matching_algo.models import UserProfile

def calculate_final_scores():
    user_profiles = UserProfile.objects.all()
    final_scores = [[0 for _ in range(len(user_profiles))] for _ in range(len(user_profiles))]
    
    # Calculate cosine similarity scores
    cosine_similarities = calculate_cosine_similarity()
    matching_similarities = calculate_interests_goals_scores()
    
    # combine matching similarities with cosine similarities
    for i in range(len(cosine_similarities)):
        for j in range(len(cosine_similarities[i])):
            final_scores[i][j] = cosine_similarities[i][j] + matching_similarities[i][j]
            print(final_scores[i][j])
    
    return final_scores