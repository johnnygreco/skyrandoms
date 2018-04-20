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
        self.rng = utils.check_random_state(random_state)
        self.set_sky_limits(ra_lim, dec_lim)
    
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

    def set_sky_limits(self, ra_lim, dec_lim):
        self.ra_lim = np.asarray(ra_lim)
        self.dec_lim = np.asarray(dec_lim)
        self._area = None

    def draw(self, npoints=1, density=None, as_df=True):
        if density is not None:
            npoints = round(density*self.area, 0)
        points = utils.random_radec(
            npoints, self.ra_lim, self.dec_lim, 
            random_state=self.rng, as_df=as_df)
        return points


class SkyRandoms(Base):
    """
    Database Table.
    """

    __tablename__ = 'skyrandoms'
    id = sq.Column(sq.Integer, primary_key=True)
    ra = sq.Column(sq.Float, nullable=False)
    dec = sq.Column(sq.Float, nullable=False)
    detected = sq.Column(sq.Integer, nullable=False)

    def __repr__(self):
        return '<SkyRandoms(id={}, ra={}, dec={}, detected={})>'.format(
            self.id, self.ra, self.dec, self.detected)


class SkyRandomsDatabase(SkyRandomsFactory):
    """
    Sky randoms database manager.
    """

    def __init__(self, db_fn='skyrandoms.db', overwrite=False, ra_lim=[0,360], 
                 dec_lim=[-90,90], random_state=None):

        super(SkyRandomsDatabase, self).__init__(ra_lim, dec_lim, random_state)
        self.db_fn = db_fn
        self.total_area = 0
        self.overwrite = overwrite

        if overwrite and os.path.isfile(db_fn):
            assert 'safe' not in db_fn, 'cannot delete safe file'
            os.remove(db_fn)

        # create engine 
        self.engine = sq.create_engine('sqlite:///'+db_fn)

        # create schema 
        Base.metadata.create_all(self.engine)

        # start session
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_last_id(self):
        last_id = self.session.query(func.max(SkyRandoms.id)).first()[0]
        return last_id if last_id else 0

    def add_single(self):
        id = self.get_last_id() + 1
        ra, dec = self.draw(npoints=1, as_df=False)[0]
        self.session.add(SkyRandoms(id=id, ra=ra, dec=dec, detected=0))
        self.session.commit()

    def add_batch(self, npoints=1, density=None, chunk_size=1e6):
        if density is not None:
            npoints = round(density*self.area, 0)
        num_chunks, remainder = _get_chunks(chunk_size, npoints)
        for n in range(num_chunks):
            randoms = self.draw(int(chunk_size), as_df=True)
            randoms['id'] = np.arange(len(randoms)) + 1 + self.get_last_id()
            randoms['detected'] = 0
            randoms.to_sql(
                'skyrandoms', self.engine, if_exists='append', index=False)
        if remainder>0:
            randoms = self.draw(remainder, as_df=True)
            randoms['id'] = np.arange(len(randoms)) + 1 + self.get_last_id()
            randoms['detected'] = 0
            randoms.to_sql(
                'skyrandoms', self.engine, if_exists='append', index=False)

    def update_total_area(self):
        self.total_area += self.area

    def query_region(self, ra_lim, dec_lim):
        cut = (SkyRandoms.ra>ra_lim[0]) & (SkyRandoms.ra<ra_lim[1])
        cut &= (SkyRandoms.dec>dec_lim[0]) & (SkyRandoms.dec<dec_lim[1])
        query_statment = self.session.query(SkyRandoms).filter(cut).statement
        return pd.read_sql(query_statment, self.engine)

    def get_randoms(self, ids):
        if type(ids)==int:
            ids = [ids]
        filter_statement =  SkyRandoms.id.in_(ids)
        query = self.session.query(SkyRandoms).filter(filter_statement)
        return pd.read_sql_query(query.selectable, self.engine)

    def set_detected(self, ids):
        if type(ids)==int:
            ids = [ids]
        for _id in ids:
            self.session.query(SkyRandoms).filter(SkyRandoms.id==_id).update(
                {SkyRandoms.detected: 1})
        self.session.commit()

    def set_all_undetected(self):
        self.session.query(SkyRandoms).update({SkyRandoms.detected: 0})
        self.session.commit()

    def __reduce__(self):
        """Return state information for pickling"""
        state = (self.db_fn, self.overwrite, self.ra_lim, 
                 self.dec_lim, self.rng)
        return self.__class__, state


def _get_chunks(chunk_size, total_size):
    remainder = int(total_size % chunk_size)
    num_chunks = int(total_size // chunk_size)
    return num_chunks, remainder
