"""enable row level security on stem_images

stem_images was added after the RLS migration (0002), so on Supabase it was readable and writable
through the public REST API with the anon key. The backend connects with the database owner role,
which bypasses RLS, and the frontend never queries tables directly, so no policy is needed: with RLS
on and no policies, the public API sees nothing. No-op on non-Supabase databases.

Revision ID: 0007
Revises: b7d2e4f19a60
Create Date: 2026-10-18

"""
from alembic import op
import sqlalchemy as sa


revision = "0007"
down_revision = "b7d2e4f19a60"
branch_labels = None
depends_on = None


def _is_supabase(bind) -> bool:
    if bind.dialect.name != "postgresql":
        return False
    return bool(
        bind.execute(
            sa.text("select 1 from information_schema.schemata where schema_name = 'auth'")
        ).scalar()
    )


def upgrade():
    if _is_supabase(op.get_bind()):
        op.execute("alter table stem_images enable row level security")


def downgrade():
    if _is_supabase(op.get_bind()):
        op.execute("alter table stem_images disable row level security")
