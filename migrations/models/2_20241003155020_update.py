from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "permissions" ADD "tenant" INT NOT NULL;
        ALTER TABLE "permission_groups" ADD "tenant" INT NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "permissions" DROP COLUMN "tenant";
        ALTER TABLE "permission_groups" DROP COLUMN "tenant";"""
