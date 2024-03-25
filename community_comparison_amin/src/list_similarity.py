#Developed by chatGPT, modified by Amin
from scipy.spatial.distance import euclidean, cosine
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import jaccard_score
import numpy as np

def pad_lists(list1, list2):
    """
    Pads the shorter list with zeroes to ensure both lists are of equal length.
    Written by ChatGPT
    """
    len1, len2 = len(list1), len(list2)
    if len1 > len2:
        list2.extend([0] * (len1 - len2))
    elif len2 > len1:
        list1.extend([0] * (len2 - len1))
    return list1, list2

def calculate_list_similarity_measures(list1, list2):
    """
    Calculates various similarity and distance measures for two lists of numbers.
    Assumes lists are of the same length or can be padded with zeroes.
    Written by ChatGPT
    """
    # Pad lists with zeroes if they are of different lengths
    list1, list2 = pad_lists(list1.copy(), list2.copy())

    # Convert lists to numpy arrays for computation
    arr1, arr2 = np.array(list1), np.array(list2)

    # Euclidean Distance
    euclidean_dist = euclidean(arr1, arr2)

    # Cosine Similarity
    cosine_sim = 1 - cosine(arr1, arr2)  # cosine function returns the distance, so we subtract from 1

    # Pearson Correlation Coefficient
    pearson_corr, _ = pearsonr(arr1, arr2)

    # Spearman's Rank Correlation Coefficient
    spearman_corr, _ = spearmanr(arr1, arr2)

    # Jaccard Similarity Score (treating the lists as binary for this example)
    # Convert lists to binary (1 if element is present, 0 if not)
    binary_arr1 = np.clip(arr1, 0, 1)
    binary_arr2 = np.clip(arr2, 0, 1)
    jaccard_sim = jaccard_score(binary_arr1, binary_arr2)

    # Overlap Coefficient
    overlap_coefficient = np.sum(np.minimum(arr1, arr2)) / np.minimum(np.sum(arr1), np.sum(arr2))

    # Root Mean Square Deviation
    rmsd = np.sqrt(np.mean((arr1 - arr2) ** 2))

    # Manhattan Distance
    manhattan_dist = np.sum(np.abs(arr1 - arr2))

    return {
        "euclidean_distance": euclidean_dist,
        "cosine_similarity": cosine_sim,
        "pearson_correlation": pearson_corr,
        "spearman_correlation": spearman_corr,
        "jaccard_similarity": jaccard_sim,
        "overlap_coefficient": overlap_coefficient,
        "rmsd": rmsd,
        "manhattan_distance": manhattan_dist
    }

