from dataclasses import dataclass

from numpy import floating
from typing import Union


@dataclass
class D:
    d2: Union[float, floating]
    d3: Union[float, floating]


# Source: https://www.qimacros.com/control-chart/control-chart-constants/
# Checked with: Introduction to Statistical Quality Control, Douglas C. Montgomery
#               ISBN: 978-1-118-14681-1
_D_TABLE = {
    2: D(d2=1.128, d3=0.853),
    3: D(d2=1.693, d3=0.888),
    4: D(d2=2.059, d3=0.880),
    5: D(d2=2.326, d3=0.864),
    6: D(d2=2.534, d3=0.848),
    7: D(d2=2.704, d3=0.833),
    8: D(d2=2.847, d3=0.820),
    9: D(d2=2.970, d3=0.808),
    10: D(d2=3.078, d3=0.797),
    15: D(d2=3.472, d3=0.756),
    25: D(d2=3.931, d3=0.708),
}
