from __future__ import division, print_function

import numpy as np
from ..core import SkyRandomsFactory, SkyRandomsDatabase

def test_SkyRandomsFactory():
    sr = SkyRandomsFactory([0, 360], [-90, 90])
    ra, dec = sr.draw_randoms(density=1)
    assert len(ra)==41253

def test_SkyRandomsDatabase():
    db = SkyRandomsDatabase(db_fn='')
    db.add_random_batch(density=2)
    assert np.allclose(db.get_last_id()/db.area, 2)



