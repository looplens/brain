-- AlterTable
ALTER TABLE "Post" ALTER COLUMN "attachments" DROP NOT NULL,
ALTER COLUMN "attachments" SET DATA TYPE TEXT;
