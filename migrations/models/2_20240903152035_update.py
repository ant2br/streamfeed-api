from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "indicators" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "differential" DECIMAL(10,2) NOT NULL,
    "symbol" VARCHAR(50) NOT NULL,
    "tenant" INT NOT NULL
);
        CREATE TABLE IF NOT EXISTS "symbols" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(50) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "tenant" INT NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "indicators";
        DROP TABLE IF EXISTS "symbols";"""
