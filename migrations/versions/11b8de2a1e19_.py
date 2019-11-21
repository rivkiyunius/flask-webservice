"""empty message

Revision ID: 11b8de2a1e19
Revises: d68b0a1811e5
Create Date: 2019-11-21 22:39:54.145772

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '11b8de2a1e19'
down_revision = 'd68b0a1811e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=False),
                    sa.Column('password', sa.String(length=128), nullable=True),
                    sa.Column('create_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_table('blogposts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=128), nullable=False),
                    sa.Column('contents', sa.String(), nullable=False),
                    sa.Column('create_at', sa.DateTime(), nullable=True),
                    sa.Column('modified_at', sa.DateTime(), nullable=True),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('dataset',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('number_of_pregnancy', sa.Integer, nullable=False),
                    sa.Column('plasma_glucose_concentration', sa.Integer(), nullable=False),
                    sa.Column('diastolic_blood_pressure', sa.Integer(), nullable=True),
                    sa.Column('triceps_skin_thickness', sa.Integer(), nullable=True),
                    sa.Column('serum_insulin', sa.Float(), nullable=False),
                    sa.Column('bmi', sa.Float(), nullable=False),
                    sa.Column('diabetes_pedigree_function', sa.Float(), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=False),
                    sa.Column('test_result', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    pass
