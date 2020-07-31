"""empty message

Revision ID: d6acfd32cb48
Revises: 
Create Date: 2020-07-28 15:29:31.194778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6acfd32cb48'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('industrys',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(length=31), nullable=True),
    sa.Column('updated_by', sa.String(length=31), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=31), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(length=31), nullable=True),
    sa.Column('updated_by', sa.String(length=31), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('job_offers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_name', sa.String(length=31), nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=True),
    sa.Column('occupation', sa.String(length=60), nullable=False),
    sa.Column('max_appicants', sa.Integer(), nullable=True),
    sa.Column('starting_salary', sa.Integer(), nullable=True),
    sa.Column('image_url_text', sa.Text(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(length=31), nullable=True),
    sa.Column('updated_by', sa.String(length=31), nullable=True),
    sa.ForeignKeyConstraint(['industry_id'], ['industrys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('google_id', sa.String(length=30), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('class_number', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(length=31), nullable=True),
    sa.Column('updated_by', sa.String(length=31), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.PrimaryKeyConstraint('google_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('job_offers')
    op.drop_table('subjects')
    op.drop_table('industrys')
    # ### end Alembic commands ###