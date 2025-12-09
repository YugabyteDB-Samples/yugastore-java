import { render, screen } from "@testing-library/react";
import { Navbar } from "@/components/navbar";

jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

const mockUser = { username: "testuser" };

jest.mock("@/context/AuthContext", () => ({
  useAuth: () => ({
    user: null,
    logout: jest.fn(),
  }),
}));

describe("Navbar", () => {
  it("renders the navbar with brand name", () => {
    render(<Navbar />);
    expect(screen.getByText("Bookstore R Us")).toBeInTheDocument();
  });

  it("renders navigation links for categories", () => {
    render(<Navbar />);
    expect(screen.getByText("Books")).toBeInTheDocument();
    expect(screen.getByText("Music")).toBeInTheDocument();
    expect(screen.getByText("Beauty")).toBeInTheDocument();
    expect(screen.getByText("Electronics")).toBeInTheDocument();
  });

  it("renders cart button", () => {
    render(<Navbar />);
    expect(screen.getByRole("link", { name: /cart/i })).toBeInTheDocument();
  });

  it("renders login button when user is not authenticated", () => {
    render(<Navbar />);
    expect(screen.getByText("Login")).toBeInTheDocument();
  });

  it("has sticky positioning", () => {
    render(<Navbar />);
    // Get the main nav (first one) - there are nested navs in the component
    const navs = screen.getAllByRole("navigation");
    const mainNav = navs[0];
    expect(mainNav).toHaveClass("sticky");
    expect(mainNav).toHaveClass("top-0");
  });

  it("has dark-mode friendly background classes", () => {
    render(<Navbar />);
    const navs = screen.getAllByRole("navigation");
    const mainNav = navs[0];
    expect(mainNav).toHaveClass("bg-background/95");
  });
});
