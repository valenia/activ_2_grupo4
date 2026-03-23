-- upgrade --
CREATE TABLE IF NOT EXISTS "userdb" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(30) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "address" VARCHAR(255),
    "hashed_password" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "stored_files" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "owner_external_id" INT NOT NULL,
    "filename" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "mime_type" VARCHAR(100),
    "content" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
