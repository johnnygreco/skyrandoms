from __future__ import division, print_function

import numpy as np
import pandas as pd
from astropy import units as u

__all__ = ['solid_angle', 'random_radec', 'check_random_state']


def solid_angle(ra_lim, dec_lim):
    """
    Calculate solid angle with given ra & dec range.
    All angles in degrees.
    
    Parameters
    ----------
    ra_lim : list-like, optional
        ra limits.
    dec_lim : list-like, optional
        dec limits.

    Returns
    -------
    area : float
        Solid angle in square degrees.
    """
    ra_lim = np.deg2rad(np.asarray(ra_lim))
    dec_lim = np.deg2rad(np.asarray(dec_lim))
    dsin_dec = np.sin(dec_lim[1]) - np.sin(dec_lim[0])
    area = ra_lim.ptp() * dsin_dec * (180.0/np.pi)**2
    return area


def random_radec(npoints, ra_lim=[0, 360], dec_lim=[-90, 90], 
                 random_state=None, as_df=True):
    """
    Generate random ra and dec points within a specified range.
    All angles in degrees.

    Parameters
    ----------
    npoints : int
        Number of random points to generate.
    ra_lim : list-like, optional
        ra limits.
    dec_lim : list-like, optional
        dec limits.
    random_state : `None`, int, list of ints, or `numpy.random.RandomState`
        If ``seed`` is `None`, return the `~numpy.random.RandomState`
        singleton used by ``numpy.random``.  If ``seed`` is an `int`,
        return a new `~numpy.random.RandomState` instance seeded with
        ``seed``.  If ``seed`` is already a `~numpy.random.RandomState`,
        return it.  Otherwise raise ``ValueError``.
    as_df : bool
        If True, return as pandas DataFrame.

    Returns
    -------
    points : 2d ndarray of pandas DataFrame
        Random ra and dec points in degrees.
    """
    rng = check_random_state(random_state)
    ra_lim = np.deg2rad(np.asarray(ra_lim))
    dec_lim = np.deg2rad(np.asarray(dec_lim))

    zlim = np.sin(dec_lim)
    z = zlim[0] + zlim.ptp() * rng.uniform(size=int(npoints))
    ra = ra_lim[0] + ra_lim.ptp() * rng.uniform(size=int(npoints))
    dec = np.arcsin(z)
    ra, dec = np.rad2deg(ra), np.rad2deg(dec)
    points = np.array([ra, dec]).T

    if as_df:
        df = pd.DataFrame(data=points, columns=['ra', 'dec'])
        return df
    else:
        return points


def check_random_state(seed):
    """
    Turn seed into a `numpy.random.RandomState` instance.
    Parameters
    ----------
    seed : `None`, int, list of ints, or `numpy.random.RandomState`
        If ``seed`` is `None`, return the `~numpy.random.RandomState`
        singleton used by ``numpy.random``.  If ``seed`` is an `int`,
        return a new `~numpy.random.RandomState` instance seeded with
        ``seed``.  If ``seed`` is already a `~numpy.random.RandomState`,
        return it.  Otherwise raise ``ValueError``.
    Returns
    -------
    random_state : `numpy.random.RandomState`
        RandomState object.
    Notes
    -----
    This routine is adapted from scikit-learn.  See
    http://scikit-learn.org/stable/developers/utilities.html#validation-tools.
    """
    import numbers

    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    if type(seed)==list:
        if type(seed[0])==int:
            return np.random.RandomState(seed)

    raise ValueError('{0!r} cannot be used to seed a numpy.random.RandomState'
                     ' instance'.format(seed))

