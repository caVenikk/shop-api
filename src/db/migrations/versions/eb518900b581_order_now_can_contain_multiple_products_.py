"""Order now can contain multiple products by many to many table

Revision ID: eb518900b581
Revises: d978178c2f10
Create Date: 2023-05-14 20:37:45.428362

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "eb518900b581"
down_revision = "d978178c2f10"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders_products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_constraint("orders_product_id_fkey", "orders", type_="foreignkey")
    op.drop_column("orders", "product_id")
    op.drop_index("product_price_index", table_name="products")
    op.drop_index("product_title_index", table_name="products")
    op.drop_index("user_username_index", table_name="users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("user_username_index", "users", ["username"], unique=False)
    op.create_index("product_title_index", "products", ["title"], unique=False)
    op.create_index("product_price_index", "products", ["price"], unique=False)
    op.add_column("orders", sa.Column("product_id", sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key("orders_product_id_fkey", "orders", "products", ["product_id"], ["id"])
    op.drop_table("orders_products")
    # ### end Alembic commands ###
