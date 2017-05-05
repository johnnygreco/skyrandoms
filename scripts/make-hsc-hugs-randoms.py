#!/tigress/HSC/LSST/stack_20160915/Linux64/miniconda2/3.19.0.lsst4/bin/python
from __future__ import division, print_function

from argparse import ArgumentParser
import numpy as np
from skyrandoms import SkyRandomsDatabase, SkyRandoms
from skyrandoms.footprints import hsc
dbdir = '/scratch/network/jgreco/'

parser = ArgumentParser()
parser.add_argument('density', type=int, help='# of randoms per square degree')
parser.add_argument(
    '-p', '--prefix',  default='randoms-safe', help='db file name prefix')
args = parser.parse_args()

randoms_density =  args.density # per deg^2
prefix = args.prefix
db_name = dbdir+prefix+'-{}.db'.format(randoms_density)
db = SkyRandomsDatabase(db_fn=db_name)

print('generating', randoms_density, 'randoms per deg^2\n')
for fp in hsc.values():
    print('generating randoms for region ', fp.region)
    db.set_sky_limits(fp.ra_lim, fp.dec_lim)
    print('ra limits = {}, dec limit = {}'.format(db.ra_lim, db.dec_lim))
    print('solid angle = {:.2f} deg^2'.format(db.area))
    print('N randoms =', int(db.area*randoms_density), '\n')
    db.add_random_batch(density=randoms_density)
    db.update_total_area()
print('total area covered by randoms = {:.2f} deg^2'.format(db.total_area))
