import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu

data = pd.read_csv("Output.csv")

bidirectional_mmE_cost = pd.to_numeric(data.iloc[:, -8], errors='coerce')  # Assuming last 4th column is "Bi-directional Euclidean Heuristic" cost
bidirectional_mmE_score = pd.to_numeric(data.iloc[:, -5], errors='coerce')  # Assuming last column is "Bi-directional Euclidean Heuristic" score
bidirectional_mmE_nodes = pd.to_numeric(data.iloc[:, -7], errors='coerce')  # Assuming last 3rd column is "Bi-directional Euclidean Heuristic" nodes

bidirectional_mmM_cost = pd.to_numeric(data.iloc[:, -12], errors='coerce')  # Assuming last 4th column is "Bi-directional Manhattan Heuristic" cost
bidirectional_mmM_score = pd.to_numeric(data.iloc[:, -9], errors='coerce')  # Assuming last column is "Bi-directional Manhattan Heuristic" score
bidirectional_mmM_nodes = pd.to_numeric(data.iloc[:, -11], errors='coerce')  # Assuming last 3rd column is "Bi-directional Manhattan Heuristic" nodes

algorithm_columns = {
    'BFS': (1, 4, 2),
    'DFS': (5, 8, 6),
    'UCS': (9, 12, 10),
    'A*': (13, 16, 14),
    'BDS with Euclidean Heuristic': (17, 20, 18),
    'BDS with Manhattan Heuristic': (21, 24, 22),
    'BDS with Null Heuristic': (25, 28, 26),
}

comparison_results_mmE = []
comparison_results_mmM = []

alpha = 0.05   # significance level

for algorithm, (cost_col, score_col, nodes_col) in algorithm_columns.items():
    algorithm_cost = pd.to_numeric(data.iloc[:, cost_col], errors='coerce')
    algorithm_score = pd.to_numeric(data.iloc[:, score_col], errors='coerce')
    algorithm_nodes = pd.to_numeric(data.iloc[:, nodes_col], errors='coerce')
    
    cost_ttest = ttest_ind(bidirectional_mmM_cost.dropna(), algorithm_cost.dropna(), equal_var=False)
    score_ttest = ttest_ind(bidirectional_mmM_score.dropna(), algorithm_score.dropna(), equal_var=False)
    nodes_ttest = ttest_ind(bidirectional_mmM_nodes.dropna(), algorithm_nodes.dropna(), equal_var=False)

    # Perform Mann-Whitney U-test for normality
    cost_mwu = mannwhitneyu(bidirectional_mmM_cost.dropna(), algorithm_cost.dropna())
    score_mwu = mannwhitneyu(bidirectional_mmM_score.dropna(), algorithm_score.dropna())
    nodes_mwu = mannwhitneyu(bidirectional_mmM_nodes.dropna(), algorithm_nodes.dropna())

    comparison_results_mmM.append({ 
        'Algorithm': algorithm,

        'Cost p-value': cost_ttest.pvalue,
        'Cost t-stat': cost_ttest.statistic,
        'Cost p-value (Mann-Whitney U)': cost_mwu.pvalue,
        'Cost t-stat (Mann-Whitney U)': cost_mwu.statistic,

        'Score p-value': score_ttest.pvalue,
        'Score t-stat': score_ttest.statistic,
        'Score p-value (Mann-Whitney U)': score_mwu.pvalue,
        'Score t-stat (Mann-Whitney U)': score_mwu.statistic,

        'Nodes p-value': nodes_ttest.pvalue,
        'Nodes t-stat': nodes_ttest.statistic,
        'Nodes p-value (Mann-Whitney U)': nodes_mwu.pvalue,
        'Nodes t-stat (Mann-Whitney U)': nodes_mwu.statistic
    })

for algorithm, (cost_col, score_col, nodes_col) in algorithm_columns.items():
    algorithm_cost = pd.to_numeric(data.iloc[:, cost_col], errors='coerce')
    algorithm_score = pd.to_numeric(data.iloc[:, score_col], errors='coerce')
    algorithm_nodes = pd.to_numeric(data.iloc[:, nodes_col], errors='coerce')
    
    cost_ttest = ttest_ind(bidirectional_mmE_cost.dropna(), algorithm_cost.dropna(), equal_var=False)
    score_ttest = ttest_ind(bidirectional_mmE_score.dropna(), algorithm_score.dropna(), equal_var=False)
    nodes_ttest = ttest_ind(bidirectional_mmE_nodes.dropna(), algorithm_nodes.dropna(), equal_var=False)

    # Perform Mann-Whitney U-test for normality
    cost_mwu = mannwhitneyu(bidirectional_mmE_cost.dropna(), algorithm_cost.dropna())
    score_mwu = mannwhitneyu(bidirectional_mmE_score.dropna(), algorithm_score.dropna())
    nodes_mwu = mannwhitneyu(bidirectional_mmE_nodes.dropna(), algorithm_nodes.dropna())

    comparison_results_mmE.append({
        'Algorithm': algorithm,

        'Cost p-value': cost_ttest.pvalue,
        'Cost t-stat': cost_ttest.statistic,
        'Cost p-value (Mann-Whitney U)': cost_mwu.pvalue,
        'Cost t-stat (Mann-Whitney U)': cost_mwu.statistic,

        'Score p-value': score_ttest.pvalue,
        'Score t-stat': score_ttest.statistic,
        'Score p-value (Mann-Whitney U)': score_mwu.pvalue,
        'Score t-stat (Mann-Whitney U)': score_mwu.statistic,

        'Nodes p-value': nodes_ttest.pvalue,
        'Nodes t-stat': nodes_ttest.statistic,
        'Nodes p-value (Mann-Whitney U)': nodes_mwu.pvalue,
        'Nodes t-stat (Mann-Whitney U)': nodes_mwu.statistic
    })

comparison_results_mmM_df = pd.DataFrame(comparison_results_mmM)
comparison_results_mmE_df = pd.DataFrame(comparison_results_mmE)
print('t-Test for BDS mmM vs other Algorithms:\n', comparison_results_mmM_df)
print('t-Test for BDS mmE vs other Algorithms:\n', comparison_results_mmE_df)

# if p_value < alpha:
#            print("Reject the null hypothesis; m1 != m2.")
# else:
# print("Fail to reject the null hypothesis; m1 = m2.")
