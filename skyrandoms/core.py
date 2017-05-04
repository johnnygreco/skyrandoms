from __future__ import division, print_function

import os
import numpy as np
import pandas as pd

import sqlalchemy as sq
import sqlalchemy.ext.declarative 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from . import utils

Base = sq.ext.declarative.declarative_base()

__all__ = ['SkyRandomsFactory', 'SkyRandomsDatabase', 'SkyRandoms']


class SkyRandomsFactory(object):
    """
    Base class for generating random points on the celestial sphere.
    """

    def __init__(self, ra_lim=[0,360], dec_lim=[-90,90], random_state=None):
        self.ra_lim = np.asarray(ra_lim)
        self.dec_lim = np.asarray(dec_lim)
        self.rng = utils.check_random_state(random_state)
        self._area = None
    
    @property
    def area(self):
        if self._area is None:
            self._area = utils.solid_angle(self.ra_lim, self.dec_lim)
        return self._area

    @property
    def ra_lim(self):
        return self._ra_lim

    @ra_lim.setter
    def ra_lim(self, lim):
        assert lim[0]>=0 and lim[1]<=360, 'ra must be in [0, 360]'
        self._ra_lim = lim

    @property
    def dec_lim(self):
        return self._dec_lim

    @dec_lim.setter
    def dec_lim(self, lim):
        assert lim[0]>=-90 and lim[1]<=90, 'dec must be in [-90, 90]'
        self._dec_lim = lim

    def draw_randoms(self, npoints=1, density=None, as_df=False):
        if density is not None:
            npoints = round(density*self.area, 0)
        ra, dec = utils.random_radec(
            npoints, self.ra_lim, self.dec_lim, random_state=self.rng)
        if as_df:
            df = pd.DataFrame(
                data=np.array([ra, dec]).T, columns=['ra', 'dec'])
            return df
        else:
            return ra, dec


class SkyRandoms(Base):
    """
    Database Table.
    """

    __tablename__ = 'skyrandoms'
    id = sq.Column(sq.Integer, primary_key=True)
    ra = sq.Column(sq.Float, index=True)
    dec = sq.Column(sq.Float, nullable=False)
    detected = sq.Column(sq.Integer, nullable=False)

    def __repr__(self):
        return '<SkyRandoms(id={}, ra={}, dec={}, detected={})>'.format(
            self.id, self.ra, self.dec, self.detected)


class SkyRandomsDatabase(SkyRandomsFactory):
    """
    Sky randoms database manager.
    """

    def __init__(self, db_fn='skyrandoms.db', overwrite=False, **kwargs):

        super(SkyRandomsDatabase, self).__init__(**kwargs)
        self.db_fn = db_fn

        if overwrite and os.path.isfile(db_fn):
            os.remove(db_fn)

        # create engine 
        self.engine = sq.create_engine('sqlite:///'+db_fn)

        # create schema 
        Base.metadata.create_all(self.engine)

        # start session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_last_id(self):
        return self.session.query(func.max(SkyRandoms.id)).first()[0]

    def add_single(self, id, ra, dec):
        self.session.add(SkyRandoms(id=id, ra=ra, dec=dec, detected=0))
        self.session.commit()

    def add_random_single(self):
        id = self.get_last_id() + 1
        ra, dec = self.draw_randoms(npoints=1)
        self.add_single(id, ra, dec)

    def add_random_batch(self, npoints=1, density=None):
        if density is not None:
            npoints = round(density*self.area, 0)
        randoms = self.draw_randoms(npoints, as_df=True)
        last_id = self.get_last_id()
        last_id = last_id if last_id else 0
        randoms['id'] = np.arange(len(randoms)) + 1 + last_id
        randoms['detected'] = 0
        randoms.to_sql(
            'skyrandoms', self.engine, if_exists='append', index=False)
