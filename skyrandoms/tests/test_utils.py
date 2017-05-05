from __future__ import division, print_function

import numpy as np
from .. import utils


def test_solid_angle():
    area = utils.solid_angle([0, 360], [-90, 90])
    assert area == 4*np.pi*(180/np.pi)**2

    area = utils.solid_angle([0, 90], [0, 90])
    assert area == 4*np.pi*(180/np.pi)**2/8


def test_random_radec():
    p = utils.random_radec(1e4, [45, 80], [-45, 80])
    assert p['ra'].min()>45 and p['ra'].max()<80
    assert p['dec'].min()>-45 and p['dec'].max()<80
