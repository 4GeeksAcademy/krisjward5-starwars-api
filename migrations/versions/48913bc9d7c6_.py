"""empty message

Revision ID: 48913bc9d7c6
Revises: d448cfcfa9dc
Create Date: 2024-08-31 00:19:21.246665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48913bc9d7c6'
down_revision = 'd448cfcfa9dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person_favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.Text(),
               existing_nullable=False)
        batch_op.drop_column('hair_color')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('person', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hair_color', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=False)

    op.drop_table('person_favorite')
    # ### end Alembic commands ###
