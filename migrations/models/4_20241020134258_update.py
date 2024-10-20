from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "permission_groups_permissions";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "permission_groups_permissions" (
    "permission_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE,
    "permission_groups_id" INT NOT NULL REFERENCES "permission_groups" ("id") ON DELETE CASCADE
);"""
