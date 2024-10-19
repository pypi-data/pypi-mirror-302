import numpy as np
import scipy.stats as st
from scipy.special import gamma

from ._d_table import _D_TABLE, D


def get_d(m: int, sim_size: int = 10_000) -> D:
    """Correction factors for the R and X control charts.

    Refer to
    [Shewhart charts](http://spc.pages.gitlab.ost.ch/statistische-qualitaetskontrolle/cc_variable_data.html#die-shewhart-kontrollkarte)
    for further reference.

    Args:
        m: Size of each sample.
        sim_size: Number of simulations performed to estimate d2 and d3 if no
                  predifined value is available.

    Returns:
        Dataclass with the corrisponding d2 and d3 value.

    Examples:
        >>> d = get_d(5)
        >>> d.d2
        2.326
        >>> d.d3
        0.864
    """
    if m < 2:
        raise ValueError("The sample size m has to be >= 2.")

    if m in _D_TABLE:
        return _D_TABLE[m]

    x = np.array(st.norm.rvs(size=(sim_size, m)))
    R_i = x.max(axis=1) - x.min(axis=1)
    d2 = np.mean(R_i)
    d3 = np.std(R_i, ddof=1)
    return D(d2=d2, d3=d3)


def get_c4(m: int) -> float:
    """Correction factor used for the s and corrisponding X control charts.

    Refer to
    http://spc.pages.gitlab.ost.ch/statistische-qualitaetskontrolle/cc_variable_data.html#s-karte
    for further reference.

    Args:
        m: Size of each sample.

    Returns:
        Calculated c4 value.

    Examples:
        >>> get_c4(5)
        np.float64(0.9399856029866253)
    """
    return gamma(m / 2) / gamma((m - 1) / 2) * np.sqrt(2 / (m - 1))
