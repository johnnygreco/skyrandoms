from __future__ import division, print_function

import numpy as np
from astropy import units as u

__all__ = ['solid_angle', 'random_radec', 'check_random_state']


def solid_angle(ralim, declim):
    """
    Calculate solid angle with given ra & dec range.
    All angles in degrees.
    
    Parameters
    ----------
    ralim : list-like, optional
        ra limits.
    declim : list-like, optional
        dec limits.

    Returns
    -------
    area : float
        Solid angle in square degrees.
    """
    ralim = np.deg2rad(np.asarray(ralim))
    declim = np.deg2rad(np.asarray(declim))
    dsin_dec = np.sin(declim[1]) - np.sin(declim[0])
    area = ralim.ptp() * dsin_dec * (180.0/np.pi)**2
    return area


def random_radec(npoints, ralim=[0, 360], 
                 declim=[-90, 90], random_state=None):
    """
    Generate random ra and dec points within a specified range.
    All angles in degrees.

    Parameters
    ----------
    npoints : int
        Number of random points to generate.
    ralim : list-like, optional
        ra limits.
    declim : list-like, optional
        dec limits.
    random_state : `None`, int, list of ints, or `numpy.random.RandomState`
        If ``seed`` is `None`, return the `~numpy.random.RandomState`
        singleton used by ``numpy.random``.  If ``seed`` is an `int`,
        return a new `~numpy.random.RandomState` instance seeded with
        ``seed``.  If ``seed`` is already a `~numpy.random.RandomState`,
        return it.  Otherwise raise ``ValueError``.
    Returns
    -------
    points : 2d ndarray
        Random ra and dec points in degrees.
    """
    rng = check_random_state(random_state)
    ralim = np.deg2rad(np.asarray(ralim))
    declim = np.deg2rad(np.asarray(declim))

    zlim = np.sin(declim)
    z = zlim[0] + zlim.ptp() * rng.uniform(size=int(npoints))
    ra = ralim[0] + ralim.ptp() * rng.uniform(size=int(npoints))
    dec = np.arcsin(z)
    return np.rad2deg(ra), np.rad2deg(dec)


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

