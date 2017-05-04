from __future__ import division, print_function

import numpy as np
from . import utils


class SkyRandoms(object):
    """
    Base class for generating random points on the celestial sphere.
    """

    def __init__(self, ralim=[0,360], declim=[-90,90], random_state=None):
        self.ralim = np.asarray(ralim)
        self.declim = np.asarray(declim)
        self.rng = utils.check_random_state(random_state)
        self._area = None
    
    @property
    def area(self):
        if self._area is None:
            self._area = utils.solid_angle(self.ralim, self.declim)
        return self._area

    @property
    def ralim(self):
        return self._ralim

    @ralim.setter
    def ralim(self, lim):
        assert lim[0]>=0 and lim[1]<=360, 'ra must be in [0, 360]'
        self._ralim = lim

    @property
    def declim(self):
        return self._declim

    @declim.setter
    def declim(self, lim):
        assert lim[0]>=-90 and lim[1]<=90, 'dec must be in [-90, 90]'
        self._declim = lim

    def draw_randoms(self, npoints=1, density=None):
        if density is not None:
            npoints = round(density*self.area, 0)
        ra, dec = utils.random_radec(
            npoints, self.ralim, self.declim, random_state=self.rng)
        return ra, dec
