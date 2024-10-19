import numpy as np
import scipy.stats as st
from scipy.special import gamma


def d(m, sim_size=100000):
    X = st.norm.rvs(size=(sim_size, m))
    R_i = X.max(axis=1) - X.min(axis=1)
    d2 = np.mean(R_i)
    d3 = np.std(R_i, ddof=1)
    return d2, d3


def c4(m):
    return gamma(m / 2) / gamma((m - 1) / 2) * np.sqrt(2 / (m - 1))