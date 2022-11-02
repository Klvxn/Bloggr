"""added tag field for blog model

Revision ID: debfe167a3c0
Revises: 
Create Date: 2022-10-27 22:23:06.253233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'debfe167a3c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('tag', sa.String(length=80), nullable=True))
    op.create_index(op.f('ix_blog_tag'), 'blog', ['tag'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_blog_tag'), table_name='blog')
    op.drop_column('blog', 'tag')
    # ### end Alembic commands ###
