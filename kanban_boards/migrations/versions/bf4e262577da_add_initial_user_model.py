"""Add initial user model.

Revision ID: bf4e262577da
Revises: 
Create Date: 2021-01-13 00:15:21.550082

"""
from alembic import op
import sqlalchemy as sa
from lib.util_sqlalchemy import AwareDateTime


# revision identifiers, used by Alembic.
revision = "bf4e262577da"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("created_on", AwareDateTime(), nullable=True),
        sa.Column("update_on", AwareDateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=24), nullable=False),
        sa.Column("email", sa.String(length=255), server_default="", nullable=False),
        sa.Column("password", sa.String(length=128), server_default="", nullable=False),
        sa.Column(
            "role",
            sa.Enum("member", "admin", name="role_types", native_enum=False),
            server_default="member",
            nullable=False,
        ),
        sa.Column("active", sa.Boolean(), server_default="1", nullable=False),
        sa.Column("confirmed", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("confirmed_on", AwareDateTime(), nullable=True),
        sa.Column("sign_in_count", sa.Integer(), nullable=False),
        sa.Column("current_sign_in_on", AwareDateTime(), nullable=True),
        sa.Column("current_sign_in_ip", sa.String(length=45), nullable=True),
        sa.Column("last_sign_in_on", AwareDateTime(), nullable=True),
        sa.Column("last_sign_in_ip", sa.String(length=45), nullable=True),
        sa.Column("locale", sa.String(length=5), server_default="en", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###