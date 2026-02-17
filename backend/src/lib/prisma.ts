// Load environment variables from .env file
import { config } from "dotenv";
config({ path: ".env" });

// Mock Prisma Client for development without database
class MockPrismaClient {
  private users: any[] = [];

  user = {
    create: async ({ data }: { data: any }) => {
      const user = {
        id: Math.random().toString(36).substring(7),
        ...data,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      this.users.push(user);
      console.log("✅ Mock user created:", user);
      return user;
    },
    findMany: async () => this.users,
    findUnique: async ({ where }: { where: any }) =>
      this.users.find((u) => u.email === where.email || u.id === where.id),
    delete: async ({ where }: { where: any }) => {
      const index = this.users.findIndex((u) => u.id === where.id);
      if (index > -1) {
        return this.users.splice(index, 1)[0];
      }
      return null;
    },
  };

  $connect = async () => {
    console.log("🔗 Mock database connected");
  };

  $disconnect = async () => {
    console.log("🔌 Mock database disconnected");
  };
}

export const prisma = new MockPrismaClient() as any;
