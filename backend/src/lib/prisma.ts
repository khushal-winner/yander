// Load environment variables from .env file
import { config } from "dotenv";
import bcrypt from "bcrypt";
config({ path: ".env" });

// Mock Prisma Client for development without database
class MockPrismaClient {
  private users: any[] = [];

  user = {
    create: async ({ data }: { data: any }) => {
      // Check for duplicate email
      const existingUser = this.users.find((u) => u.email === data.email);
      if (existingUser) {
        const error = new Error(
          "Unique constraint failed on the fields: (email)",
        );
        throw error;
      }

      // Simulate database failure if requested
      if (data.email === "db-failure@test.com") {
        throw new Error("Database connection failed");
      }

      const user = {
        id: Math.random().toString(36).substring(7),
        ...data,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      this.users.push(user);
      console.log("✅ Mock user created:", user);
      return user;
    },
    findMany: async () => this.users,
    findUnique: async ({ where }: { where: any }) => {
      const user = this.users.find(
        (u) => u.email === where.email || u.id === where.id,
      );

      // For authentication, we need to mock password comparison
      if (user && where.email) {
        // Create a user with a properly hashed password for login tests
        const hashedPassword = await bcrypt.hash("password123", 12);
        return {
          ...user,
          passwordHash: user.passwordHash || hashedPassword,
        };
      }

      return user;
    },
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
