import enum
from datetime import datetime
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float, DateTime, Table, Enum, func
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base

BID_INCREASE_AMOUNT = 0.5


class AuctionState(str, enum.Enum):
    CREATED = 'created'
    ENDED = 'ended'
    CANCELED = 'canceled'
    ONGOING = 'ongoing'


auction_bid = Table(
    'auction_bid', Base.metadata, Column(
        'auction_session_id', Integer, ForeignKey('auctionsession.id')), Column(
            'bid_id', Integer, ForeignKey('bid.id')))


class Bid(Base):
    id = Column(Integer, primary_key=True, index=True)
    bid_amount = Column(Float)
    usr_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    owner = relationship('User')
    auction_session = relationship(
        'AuctionSession', secondary=auction_bid, back_populates='bids')


class AuctionSession(Base):

    id = Column(Integer, primary_key=True, index=True)
    minimum_bid_amount = Column(Float)
    auction_state = Column(Enum(AuctionState))
    last_bid_at = Column(DateTime)
    ending_at = Column(DateTime)
    winning_bid_id = Column(Integer, ForeignKey('bid.id'))

    winning_bid = relationship('Bid', foreign_keys=[winning_bid_id])
    auction = relationship('Auction', back_populates='auction_session')
    # TODO: auction bids will have a timestamp and a remark
    bids = relationship('Bid', secondary=auction_bid,
                        back_populates='auction_session')


class Auction(Base):

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('user.id'))
    auction_winner_id = Column(Integer, ForeignKey('user.id'))
    auctionable_id = Column(Integer, ForeignKey('auctionable.id'))
    auction_session_id = Column(Integer, ForeignKey('auctionsession.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())

    owner = relationship("User", foreign_keys=[owner_id])
    auction_winner = relationship("User", foreign_keys=[auction_winner_id])
    auctionable = relationship("Auctionable")
    auction_session = relationship("AuctionSession", back_populates='auction')


class Auctionable(Base):
    id = Column(Integer, primary_key=True, index=True)
    bid_cap = Column(Float)
    starting_bid = Column(Float)
    prod_id = Column(Integer, ForeignKey('product.id'))

    product = relationship("Product", back_populates='auctionable')
