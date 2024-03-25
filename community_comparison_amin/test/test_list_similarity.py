from ..import calculate_list_similarity_measures

def test_calculate_list_similarity_measures():
    list_a = [56, 50, 37, 29, 27, 27, 26, 25, 25, 25]
    list_b = [50, 37, 29, 28, 27, 26, 25, 25, 24, 24]
    similarities = calculate_list_similarity_measures(list_a, list_b)

    result={'euclidean_distance': 16.55294535724685, 'cosine_similarity': 0.9943207312868381, 'pearson_correlation': 0.9526647008636797, 'spearman_correlation': 0.9783703741206881, 'jaccard_similarity': 1.0, 'overlap_coefficient': 1.0, 'rmsd': 5.2345009313209605, 'manhattan_distance': 32}
    for k,v in result.items():
        assert(similarities[k]==v)
