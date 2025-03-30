import pandas as pd
from scipy import stats


def perform_ttest(group1: pd.Series, group2: pd.Series, equal_var: bool = False) -> dict:
    """
    Perform an independent T-test between two groups.

    Parameters:
        group1 (pd.Series): Data for the first group.
        group2 (pd.Series): Data for the second group.
        equal_var (bool): Assume equal variance or not.

    Returns:
        dict: T-statistic and p-value.
    """
    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=equal_var)
    return {'t_stat': t_stat, 'p_value': p_value}


def interpret_results(p_value: float, alpha: float = 0.05) -> str:
    """
    Interpret the hypothesis test results.

    Parameters:
        p_value (float): The p-value from the statistical test.
        alpha (float): Significance level.

    Returns:
        str: Interpretation of the test result.
    """
    if p_value < alpha:
        return "Reject the null hypothesis (H0). There is a significant difference."
    else:
        return "Fail to reject the null hypothesis (H0). No significant difference detected."
