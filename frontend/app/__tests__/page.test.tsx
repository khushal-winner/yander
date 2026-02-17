import { render, screen } from "@testing-library/react";
import { useRouter } from "next/navigation";
import HomePage from "../page";
import { useAuth } from "@/lib/context/auth.context";

// Mock the useRouter hook
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

// Mock the auth context
jest.mock("@/lib/context/auth.context", () => ({
  useAuth: jest.fn(),
}));

describe("HomePage", () => {
  const mockPush = jest.fn();
  const mockUseAuth = useAuth as jest.MockedFunction<typeof useAuth>;

  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    });
  });

  it("shows loading state when auth is loading", () => {
    mockUseAuth.mockReturnValue({
      user: null,
      isLoading: true,
    } as any);

    render(<HomePage />);

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows landing page when user is not authenticated", () => {
    mockUseAuth.mockReturnValue({
      user: null,
      isLoading: false,
    } as any);

    render(<HomePage />);

    expect(screen.getByText("Yander")).toBeInTheDocument();
    expect(
      screen.getByText("Modern Workspace Management Platform"),
    ).toBeInTheDocument();
    expect(screen.getByText("Login to Your Account")).toBeInTheDocument();
    expect(screen.getByText("Create New Account")).toBeInTheDocument();
  });

  it("redirects to dashboard when user is authenticated", () => {
    mockUseAuth.mockReturnValue({
      user: { id: "1", email: "test@example.com", name: "Test User" },
      isLoading: false,
    } as any);

    render(<HomePage />);

    expect(mockPush).toHaveBeenCalledWith("/dashboard");
  });

  it("contains correct technology stack information", () => {
    mockUseAuth.mockReturnValue({
      user: null,
      isLoading: false,
    } as any);

    render(<HomePage />);

    expect(
      screen.getByText("✅ Next.js 16 with App Router"),
    ).toBeInTheDocument();
    expect(screen.getByText("✅ TypeScript configured")).toBeInTheDocument();
    expect(screen.getByText("✅ Tailwind CSS styling")).toBeInTheDocument();
    expect(screen.getByText("✅ Shadcn UI components")).toBeInTheDocument();
    expect(
      screen.getByText("✅ React Query for data fetching"),
    ).toBeInTheDocument();
    expect(screen.getByText("✅ Axios with interceptors")).toBeInTheDocument();
    expect(screen.getByText("✅ Authentication system")).toBeInTheDocument();
  });
});
