from matching_algo.cosine_similarity import calculate_cosine_similarity
from matching_algo.goal_interests_match import calculate_interests_goals_scores
from matching_algo.models import UserProfile

def calculate_final_scores():
    user_profiles = UserProfile.objects.all()
    final_scores = [[0 for _ in range(len(user_profiles))] for _ in range(len(user_profiles))]
    
    # Calculate matching similarity scores
    print("calculating matching similarities")
    matching_similarities = calculate_interests_goals_scores()
    
    # calculatie cosine similarity scores
    print("calculating cosine similarities")
    cosine_similarities = calculate_cosine_similarity()
    
    # combine matching similarities with cosine similarities
    for i in range(len(cosine_similarities)):
        for j in range(len(cosine_similarities[i])):
            final_scores[i][j] = cosine_similarities[i][j] + matching_similarities[i][j]
    
    return final_scores, user_profiles