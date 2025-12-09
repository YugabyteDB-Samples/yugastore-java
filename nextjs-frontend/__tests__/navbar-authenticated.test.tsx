import { render, screen } from "@testing-library/react";
import { Navbar } from "@/components/navbar";

jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

jest.mock("@/context/AuthContext", () => ({
  useAuth: () => ({
    user: { username: "testuser" },
    logout: jest.fn(),
  }),
}));

describe("Navbar - Authenticated User", () => {
  it("shows username when user is authenticated", () => {
    render(<Navbar />);
    expect(screen.getByText("Hi, testuser")).toBeInTheDocument();
  });

  it("shows logout button when user is authenticated", () => {
    render(<Navbar />);
    expect(screen.getByRole("button", { name: /logout/i })).toBeInTheDocument();
  });
});
