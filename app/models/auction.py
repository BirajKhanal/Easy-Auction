from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float, DateTime, Table
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


auction_bid = Table('auction_bid', Base.metadata, Column('auction_session_id', Integer, ForeignKey('auctionsession.id')),
                    Column('bid_id', Integer, ForeignKey('bid.id')))


class Bid(Base):
    id = Column(Integer, primary_key=True, index=True)
    bid_amount = Column(Float)
    usr_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime)

    owner = relationship('User')
    auction_session = relationship(
        'AuctionSession', secondary=auction_bid, back_populates='bids')


class AuctionSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    minimum_bid_amount = Column(Float)
    winning_bid = Column(Integer, ForeignKey('bid.id'))
    auction_state = Column(String)
    last_bid_at = Column(DateTime)

    auction = relationship('Auction', back_populates='auction_session')
    # TODO: auction bids will have a timestamp and a remark
    bids = relationship('Bid', secondary=auction_bid,
                        back_populates='auction_session')


class Auction(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ending_at = Column(DateTime)
    created_at = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('user.id'))
    auction_winner_id = Column(Integer, ForeignKey('user.id'))
    auctionable_id = Column(Integer, ForeignKey('auctionable.id'))
    auction_session_id = Column(Integer, ForeignKey('auctionsession.id'))

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
