"""Init first revision

Revision ID: 5706f9906ae2
Revises:
Create Date: 2015-05-28 13:42:07.364902

"""

# revision identifiers, used by Alembic.
revision = '5706f9906ae2'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from config.parser import prefix_table_name

user_table = prefix_table_name("user")
scan_table = prefix_table_name("scan")
job_table = prefix_table_name("job")


def upgrade():
    op.create_table(
        user_table,
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('rmqvhost', sa.String(), nullable=False),
        sa.Column('ftpuser', sa.String(), nullable=False),
        sa.Column('quota', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_{}_rmqvhost'.format(user_table)),
        user_table,
        ['rmqvhost'],
        unique=False
    )
    op.create_table(
        scan_table,
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scan_id', sa.String(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.Float(precision=2), nullable=False),
        sa.Column('nb_files', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['{}.id'.format(user_table)], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_{}_scan_id'.format(scan_table)),
        scan_table,
        ['scan_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_{}_user_id'.format(scan_table)),
        scan_table,
        ['user_id'],
        unique=False
    )
    op.create_table(
        job_table,
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('probename', sa.String(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('ts_start', sa.Integer(), nullable=False),
        sa.Column('ts_end', sa.Integer(), nullable=True),
        sa.Column('task_id', sa.String(), nullable=True),
        sa.Column('scan_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['scan_id'], ['{}.id'.format(scan_table)], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_{}_filename'.format(job_table)),
        job_table,
        ['filename'],
        unique=False
    )
    op.create_index(
        op.f('ix_{}_probename'.format(job_table)),
        job_table,
        ['probename'],
        unique=False)
    op.create_index(
        op.f('ix_{}_scan_id'.format(job_table)),
        job_table,
        ['scan_id'],
        unique=False)


def downgrade():
    op.drop_index(op.f('ix_{}_scan_id'.format(job_table)), table_name=job_table)
    op.drop_index(op.f('ix_{}_probename'.format(job_table)), table_name=job_table)
    op.drop_index(op.f('ix_{}_filename'.format(job_table)), table_name=job_table)
    op.drop_table(job_table)
    op.drop_index(op.f('ix_{}_user_id'.format(scan_table)), table_name=scan_table)
    op.drop_index(op.f('ix_{}_scan_id'.format(scan_table)), table_name=scan_table)
    op.drop_table(scan_table)
    op.drop_index(op.f('ix_{}_rmqvhost'.format(user_table)), table_name=user_table)
    op.drop_table(user_table)
