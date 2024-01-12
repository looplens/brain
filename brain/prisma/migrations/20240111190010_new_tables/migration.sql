/*
  Warnings:

  - Added the required column `post_id` to the `Comments` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "NotificationType" AS ENUM ('REPLY', 'COMMENT', 'LIKE_COMMENT', 'LIKE_POST', 'NEW_POST', 'MENTION', 'QUOTE');

-- CreateEnum
CREATE TYPE "SubscriptionType" AS ENUM ('ALL', 'ONLY_POSTS', 'NEVER');

-- CreateEnum
CREATE TYPE "DangerEventType" AS ENUM ('RESET_PASSWORD', 'DELETE_ACCOUNT');

-- CreateEnum
CREATE TYPE "CommentType" AS ENUM ('COMMENT', 'REPLY');

-- CreateEnum
CREATE TYPE "LikeType" AS ENUM ('POST', 'COMMENT');

-- AlterTable
ALTER TABLE "Comments" ADD COLUMN     "post_id" TEXT NOT NULL,
ADD COLUMN     "replied_to" TEXT,
ADD COLUMN     "type" "CommentType" DEFAULT 'COMMENT';

-- AlterTable
ALTER TABLE "Like" ADD COLUMN     "type" "LikeType" DEFAULT 'POST';

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "banner" TEXT,
ADD COLUMN     "points" INTEGER,
ADD COLUMN     "privacy_flags" INTEGER,
ADD COLUMN     "totp_secret" TEXT,
ADD COLUMN     "two_fa_enabled" BOOLEAN DEFAULT false;

-- CreateTable
CREATE TABLE "Notification" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "item_id" TEXT,
    "type" "NotificationType" NOT NULL,
    "mark_as_read" BOOLEAN DEFAULT false,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Notification_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Subscriptions" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "profile_id" TEXT NOT NULL,
    "type" "SubscriptionType" NOT NULL DEFAULT 'ALL',
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Subscriptions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "DangerEvent" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "token" TEXT NOT NULL,
    "type" "DangerEventType" NOT NULL,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "DangerEvent_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "HiddenPost" (
    "id" TEXT NOT NULL,
    "client_id" TEXT NOT NULL,
    "hide" BOOLEAN DEFAULT true,
    "post_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "HiddenPost_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Hashtags" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "count" INTEGER NOT NULL,
    "language" "Language" NOT NULL,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Hashtags_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Notification_id_key" ON "Notification"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Subscriptions_id_key" ON "Subscriptions"("id");

-- CreateIndex
CREATE UNIQUE INDEX "DangerEvent_id_key" ON "DangerEvent"("id");

-- CreateIndex
CREATE UNIQUE INDEX "HiddenPost_id_key" ON "HiddenPost"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Hashtags_id_key" ON "Hashtags"("id");
