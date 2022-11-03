"""initial commit

Revision ID: 0cee523da336
Revises: 
Create Date: 2022-11-02 23:03:49.291432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cee523da336'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('about', sa.Text(length=100), nullable=False),
    sa.Column('socials', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('password')
    )
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('content', sa.Text(length=5000), nullable=False),
    sa.Column('date_posted', sa.DateTime(timezone=True), nullable=True),
    sa.Column('tag', sa.String(length=80), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_blog_tag'), 'blog', ['tag'], unique=False)
    op.create_index(op.f('ix_blog_title'), 'blog', ['title'], unique=True)
    op.create_index(op.f('ix_blog_user_id'), 'blog', ['user_id'], unique=False)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(length=800), nullable=False),
    sa.Column('blog', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('guest_user', sa.String(), nullable=True),
    sa.Column('date_posted', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['blog'], ['blog.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_comment_blog'), 'comment', ['blog'], unique=False)
    op.create_index(op.f('ix_comment_user'), 'comment', ['user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_user'), table_name='comment')
    op.drop_index(op.f('ix_comment_blog'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_blog_user_id'), table_name='blog')
    op.drop_index(op.f('ix_blog_title'), table_name='blog')
    op.drop_index(op.f('ix_blog_tag'), table_name='blog')
    op.drop_table('blog')
    op.drop_table('user')
    # ### end Alembic commands ###
