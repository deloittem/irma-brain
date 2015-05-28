"""Updating timestamp to datetime

Revision ID: 8f43066aacb
Revises: 5706f9906ae2
Create Date: 2015-05-28 15:45:56.315671

"""

# revision identifiers, used by Alembic.
revision = '8f43066aacb'
down_revision = '5706f9906ae2'
branch_labels = None
depends_on = None

from alembic import op

from config.parser import prefix_table_name

scan_table = prefix_table_name("scan")
job_table = prefix_table_name("job")


def upgrade():
    for column in ['ts_end', 'ts_start']:
        op.execute('ALTER TABLE {0} ALTER COLUMN {1} TYPE TIMESTAMP WITHOUT TIME ZONE USING to_timestamp({1})'.format(job_table, column))
    op.execute('ALTER TABLE "{0}" ALTER COLUMN {1} TYPE TIMESTAMP WITHOUT TIME ZONE USING to_timestamp({1})'.format(scan_table, "timestamp"))


def downgrade():
    for column in ['ts_end', 'ts_start']:
        op.execute('ALTER TABLE {0} ALTER COLUMN {1} TYPE REAL USING extract(epoch from {1})'.format(job_table, column))
    op.execute('ALTER TABLE "{0}" ALTER COLUMN {1} TYPE REAL USING extract(epoch from {1})'.format(scan_table, "timestamp"))
