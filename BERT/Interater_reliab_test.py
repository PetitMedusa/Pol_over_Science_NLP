import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
import statsmodels.stats.inter_rater as ir

# Example data format: rows are items, columns are raters
# For 2 raters
rater1 = [1, 2, 3, 1, 2]  # ratings from rater 1
rater2 = [1, 2, 2, 1, 3]  # ratings from rater 2

# Cohen's Kappa (for 2 raters)
kappa = cohen_kappa_score(rater1, rater2)
print(f"Cohen's Kappa: {kappa:.4f}")

# For 3+ raters (example with 3 raters)
data = np.array([
    [1, 1, 1],  # item 1 ratings from 3 raters
    [2, 2, 2],  # item 2 ratings 
    [3, 2, 3],  # item 3 ratings
    [1, 1, 2],  # etc.
    [2, 2, 3]
])

# Fleiss' Kappa
fleiss = ir.fleiss_kappa(ir.aggregate_raters(data))
print(f"Fleiss' Kappa: {fleiss:.4f}")

# Krippendorff's Alpha (requires additional package)
# pip install krippendorff
import krippendorff
alpha = krippendorff.alpha(reliability_data=data.T)
print(f"Krippendorff's Alpha: {alpha:.4f}")