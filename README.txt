Description
You are in a network analytics project where communities have been detected. However, there are five
competing ways to detect communities – and they have all been shown to give valuable insights. Before
making any future decision on the implementation of the project, the differences in the detected
communities need to be analyzed further. You pick up this task for the upcoming week.

Objectives
Perform an exploratory data analysis and report your most interesting findings:
1. Determine which two community detection methods are the most similar.
2. For those two methods, align the communities and sort based on their similarities.
3. Keep in mind - this does not necessarily have to be a difficult assignment. We also want to see how
you write good quality code and how you organize it.


Execution plan:
1. Place the paraquet or csv files in a folder, e.g., "data"
2. In main.py, set path_data_folder, path_report_folder and extension.
3. Run main.py.
4. Check the reports in the given report folder. 
4.1. general_info.csv (general description of the communities created by each methods)
4.2. similarity_shape_based.csv (shaped (topological) based similarities of the communities created by methods regardless of the nodes they share)
4.3. similarity_shared_nodes_based.csv (shared-nodes-based similarities of the communities created by methods)
4.4. methodX-methodY.csv (align the communities and sort based on their similarities (prcntg2))

Future plans:
5.Using Topological Data Analysis (gudhi.wasserstein_distance) to compare network similarity

Future check plans:
1.test_community_comparison.py>test_data_quality>ghost nodes
2.same community aligns with multiple communities and contributes to the score (is that an issue?)
