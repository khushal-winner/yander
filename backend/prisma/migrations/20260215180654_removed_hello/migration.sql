/*
  Warnings:

  - You are about to drop the column `hello` on the `User` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "User_hello_key";

-- AlterTable
ALTER TABLE "User" DROP COLUMN "hello";
