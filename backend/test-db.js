import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

const adapter = new PrismaPg({
  connectionString:
    "postgresql://postgres.gjjtacehnudeeqjuftge:oeIrRaTtnZqtPQBV@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres",
});

const prisma = new PrismaClient({ adapter });

async function testConnection() {
  try {
    await prisma.$connect();
    console.log("✅ Database connected successfully");

    // Test basic query
    const result = await prisma.$queryRaw`SELECT version()`;
    console.log("✅ Database query successful:", result);

    await prisma.$disconnect();
  } catch (err) {
    console.error("❌ Database connection failed:", err.message);
    process.exit(1);
  }
}

testConnection();
