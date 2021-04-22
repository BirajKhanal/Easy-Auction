import enum
from datetime import datetime
from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float, DateTime, Table, Enum
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
    created_at = Column(DateTime)

    owner = relationship('User')
    auction_session = relationship(
        'AuctionSession', secondary=auction_bid, back_populates='bids')


class AuctionSession(Base):

    def __init__(self,
                 minimum_bid_amount,
                 auction_state,
                 ending_at,
                 winning_bid_id=None,
                 last_bid_at=None):
        self.minimum_bid_amount = minimum_bid_amount
        self.auction_state = auction_state
        self.last_bid_at = last_bid_at
        self.ending_at = ending_at
        self.winning_bid_id = winning_bid_id

        if self.ending_at and self.ending_at < datetime.now():
            self.auction_state = AuctionState.ENDED

    id = Column(Integer, primary_key=True, index=True)
    minimum_bid_amount = Column(Float)
    auction_state = Column(Enum(AuctionState))
    last_bid_at = Column(DateTime)
    ending_at = Column(DateTime)
    winning_bid_id = Column(Integer, ForeignKey('bid.id'))

    winning_bid = relationship('Bid', foreign_keys=[winning_bid_id])
    auction = relationship('Auction', back_populates='auction_session' )
    # TODO: auction bids will have a timestamp and a remark
    bids = relationship('Bid', secondary=auction_bid,
                        back_populates='auction_session')


class Auction(Base):

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('user.id'))
    auction_winner_id = Column(Integer, ForeignKey('user.id'))
    auctionable_id = Column(Integer, ForeignKey('auctionable.id'))
    auction_session_id = Column(Integer, ForeignKey('auctionsession.id'))

    owner = relationship("User", foreign_keys=[owner_id])
    auction_winner = relationship("User", foreign_keys=[auction_winner_id])
    auctionable = relationship("Auctionable")
    auction_session = relationship("AuctionSession", back_populates='auction' )


class Auctionable(Base):
    id = Column(Integer, primary_key=True, index=True)
    bid_cap = Column(Float)
    starting_bid = Column(Float)
    prod_id = Column(Integer, ForeignKey('product.id'))

    product = relationship("Product", back_populates='auctionable')
