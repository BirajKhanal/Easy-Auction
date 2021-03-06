"""Initial tables

Revision ID: f0719705af34
Revises: 40fed8c8f962
Create Date: 2021-04-23 12:11:46.720156

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f0719705af34'
down_revision = '40fed8c8f962'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cartlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cartitem_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cartitem_id'], ['cartitem.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cartlog_id'), 'cartlog', ['id'], unique=False)
    op.add_column('auction', sa.Column('auction_winner_id', sa.Integer(), nullable=True))
    op.add_column('auction', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('auction', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_foreign_key(None, 'auction', 'user', ['owner_id'], ['id'])
    op.create_foreign_key(None, 'auction', 'user', ['auction_winner_id'], ['id'])
    op.drop_column('auction', 'duration')
    op.drop_column('auctionable', 'auction_state')
    op.add_column('auctionsession', sa.Column('ending_at', sa.DateTime(), nullable=True))
    op.add_column('auctionsession', sa.Column('winning_bid_id', sa.Integer(), nullable=True))
    op.drop_constraint('auctionsession_winning_bid_fkey', 'auctionsession', type_='foreignkey')
    op.create_foreign_key(None, 'auctionsession', 'bid', ['winning_bid_id'], ['id'])
    op.drop_column('auctionsession', 'winning_bid')
    op.add_column('bid', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.drop_index('ix_product_product_type', table_name='product')
    op.drop_column('product', 'product_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('product_type', postgresql.ENUM('AUCTIONABLE', 'SELLABLE', 'BOTH', name='producttype'), autoincrement=False, nullable=False))
    op.create_index('ix_product_product_type', 'product', ['product_type'], unique=False)
    op.drop_column('bid', 'updated_at')
    op.add_column('auctionsession', sa.Column('winning_bid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'auctionsession', type_='foreignkey')
    op.create_foreign_key('auctionsession_winning_bid_fkey', 'auctionsession', 'bid', ['winning_bid'], ['id'])
    op.drop_column('auctionsession', 'winning_bid_id')
    op.drop_column('auctionsession', 'ending_at')
    op.add_column('auctionable', sa.Column('auction_state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('auction', sa.Column('duration', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'auction', type_='foreignkey')
    op.drop_constraint(None, 'auction', type_='foreignkey')
    op.drop_column('auction', 'updated_at')
    op.drop_column('auction', 'owner_id')
    op.drop_column('auction', 'auction_winner_id')
    op.drop_index(op.f('ix_cartlog_id'), table_name='cartlog')
    op.drop_table('cartlog')
    # ### end Alembic commands ###
