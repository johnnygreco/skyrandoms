#!/tigress/HSC/LSST/stack_20160915/Linux64/miniconda2/3.19.0.lsst4/bin/python
from __future__ import division, print_function

import os
import numpy as np
from skyrandoms import SkyRandomsDatabase, SkyRandoms
from skyrandoms.footprints import hsc

randoms_density = 36000 # per deg^2
db_name = '/scratch/network/jgreco/hsc-hugs-randoms-safe.db'
db = SkyRandomsDatabase(db_fn=db_name)

print('generating', randoms_density, 'randoms per deg^2\n')
for fp in hsc.values():
    print('generating randoms for region ', fp.region)
    db.set_sky_limits(fp.ra_lim, fp.dec_lim)
    print('ra limits = {}, dec limit = {}'.format(db.ra_lim, db.dec_lim))
    print('solid angle =', db.area, 'deg^2')
    print('N randoms =', db.area*randoms_density, '\n')
    db.add_random_batch(density=randoms_density)
