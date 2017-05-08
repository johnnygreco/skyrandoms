from __future__ import division, print_function

import numpy as np
from ..core import SkyRandomsFactory, SkyRandomsDatabase

def test_SkyRandomsFactory():
    srf = SkyRandomsFactory([0, 360], [-90, 90])
    points = srf.draw(density=1)
    assert len(points)==41253

def test_SkyRandomsDatabase():
    db = SkyRandomsDatabase(db_fn='')
    
    db.add_batch(density=2)
    assert np.allclose(db.get_last_id()/db.area, 2)

    df = db.query_region([330, 331], [8, 10])
    assert df['ra'].min()>330 and df['ra'].max()<331
    assert df['dec'].min()>8 and df['dec'].max()<10

    df = db.get_randoms([1, 100, 1000])
    assert len(df)==3
    assert df['skyrandoms_detected'].sum()==0

    db.set_detected([1, 100, 1000])
    df = db.get_randoms([1, 100, 1000])
    assert df['skyrandoms_detected'].sum()==3
