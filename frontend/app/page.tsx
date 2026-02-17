"use client";

import { useAuth } from "@/lib/context/auth.context";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function HomePage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user) {
      router.push("/dashboard");
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div>Loading...</div>
      </div>
    );
  }

  if (user) {
    return null; // Will redirect to dashboard
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Yander</h1>
        <p className="text-lg text-gray-600 mb-8">
          Modern Workspace Management Platform
        </p>

        <div className="bg-white p-8 rounded-lg shadow-sm border space-y-6">
          <h2 className="text-xl font-semibold">Get Started</h2>

          <div className="space-y-4">
            <a
              href="/login"
              className="block w-full bg-black text-white py-3 px-6 rounded-lg hover:bg-gray-800 transition-colors"
            >
              Login to Your Account
            </a>

            <a
              href="/register"
              className="block w-full border border-gray-300 py-3 px-6 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Create New Account
            </a>
          </div>

          <div className="text-left text-sm text-gray-600 space-y-2 pt-4 border-t">
            <p>✅ Next.js 16 with App Router</p>
            <p>✅ TypeScript configured</p>
            <p>✅ Tailwind CSS styling</p>
            <p>✅ Shadcn UI components</p>
            <p>✅ React Query for data fetching</p>
            <p>✅ Axios with interceptors</p>
            <p>✅ Authentication system</p>
          </div>
        </div>
      </div>
    </div>
  );
}
