"""
This module contains methods to correct p-values in order to avoid the
`Multiple comparisons problem <https://en.wikipedia.org/wiki/Multiple_comparisons_problem>`_. The code is based on
`this codebase <https://github.com/rtmdrr/replicability-analysis-NLP>`_ corresponding to the
`Dror et al. (2017) <https://arxiv.org/abs/1709.09500>`_ publication.
"""

# EXT
import numpy as np
from scipy import stats

# PKD
from deepsig.conversion import p_value_conversion, ArrayLike


@p_value_conversion
def correct_p_values(p_values: ArrayLike, method: str = "bonferroni") -> np.array:
    """
    Correct p-values based on Bonferroni's or Fisher's method. Bonferroni's method is most appropriate when data sets
    that the p-values originated from are dependent, and Fisher's when they are independent.

    Parameters
    ----------
    p_values: ArrayLike
        p-values to be corrected.
    method: str
        Method used for correction. Has to be either "bonferroni" or "fisher".

    Returns
    -------
    np.array
        Corrected p-values.
    """
    assert method in ("bonferroni", "fisher")
    assert len(p_values) > 0, "List of p-values must not be empty."
    assert (0 <= p_values).all() and (
        p_values <= 1
    ).all(), "Input contains invalid p-values."

    N = len(p_values)
    p_values = p_values.copy()

    if N == 1:
        return p_values

    # In order to maintain order of p-values, remember which one was which after sorting
    indices = range(N)
    # Ugly one-liner (inside to outside): Zip p-values and indices to list of tuples and sort ascendingly by p-value.
    # Then unzip again with zip(* ...) into two separate lists.
    p_values, sorted_indices = zip(*sorted(zip(p_values, indices), key=lambda t: t[0]))
    p_values, sorted_indices = np.array(p_values), np.array(sorted_indices)
    corrected_p_values = np.ones(N)

    for u in range(N):
        corrected_p_values[u] = calculate_partial_conjunction(p_values, u + 1, method)

    # Make sure p-values never get correct above 1
    corrected_p_values = np.minimum(corrected_p_values, 1)

    # "Unsort" p-values again. This makes it easier to check which null hypotheses can be rejected.
    corrected_p_values = corrected_p_values[sorted_indices]

    return corrected_p_values


def calculate_partial_conjunction(
    sorted_p_values: np.array, u: int, method: str
) -> float:
    """
    Calculate the partial conjunction p-value for u out of N.

    Parameters
    ----------
    sorted_p_values: np.array
        Sorted p-values.
    u: int
        Number of null hypothesis.
    method: str
        Method used for correction. Has to be either "bonferroni" or "fisher".

    Returns
    -------
    float
        p-value for the partial conjunction hypothesis for u out of N.
    """
    N = len(sorted_p_values)
    p_value_selection = sorted_p_values[: (N - u + 1)]
    p_partial_u = 0

    if method == "bonferroni":
        p_partial_u = (N - u + 1) * sorted_p_values[u - 1]

    elif method == "fisher":
        p_partial_u = 1 - stats.chi2.cdf(
            -2 * np.sum(np.log(p_value_selection)), 2 * (N - u + 1)
        )

    return p_partial_u
