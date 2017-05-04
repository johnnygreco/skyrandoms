from __future__ import division, print_function

import numpy as np
from ..core import SkyRandomsFactory

def test_SkyRandomsFactory():
    sr = SkyRandomsFactory([0, 360], [-90, 90])
    ra, dec = sr.draw_randoms(density=1)
    assert len(ra)==41253
