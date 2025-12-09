import { render, screen } from "@testing-library/react";
import { Badge, badgeVariants } from "@/components/ui/badge";

describe("Badge", () => {
  it("renders with default styling", () => {
    render(<Badge data-testid="badge">Default</Badge>);
    const badge = screen.getByTestId("badge");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveTextContent("Default");
    expect(badge).toHaveClass("bg-primary");
    expect(badge).toHaveClass("text-primary-foreground");
    expect(badge).toHaveClass("rounded-full");
  });

  it("renders with secondary variant", () => {
    render(<Badge variant="secondary" data-testid="badge">Secondary</Badge>);
    const badge = screen.getByTestId("badge");
    expect(badge).toHaveClass("bg-secondary");
    expect(badge).toHaveClass("text-secondary-foreground");
  });

  it("renders with destructive variant", () => {
    render(<Badge variant="destructive" data-testid="badge">Destructive</Badge>);
    const badge = screen.getByTestId("badge");
    expect(badge).toHaveClass("bg-destructive");
    expect(badge).toHaveClass("text-destructive-foreground");
  });

  it("renders with outline variant", () => {
    render(<Badge variant="outline" data-testid="badge">Outline</Badge>);
    const badge = screen.getByTestId("badge");
    expect(badge).toHaveClass("text-foreground");
    expect(badge).not.toHaveClass("bg-primary");
  });

  it("applies custom className", () => {
    render(<Badge className="custom-class" data-testid="badge">Custom</Badge>);
    const badge = screen.getByTestId("badge");
    expect(badge).toHaveClass("custom-class");
  });

  it("has correct base styles", () => {
    render(<Badge data-testid="badge">Base</Badge>);
    const badge = screen.getByTestId("badge");
    expect(badge).toHaveClass("inline-flex");
    expect(badge).toHaveClass("items-center");
    expect(badge).toHaveClass("border");
    expect(badge).toHaveClass("px-2.5");
    expect(badge).toHaveClass("py-0.5");
    expect(badge).toHaveClass("text-xs");
    expect(badge).toHaveClass("font-semibold");
  });
});

describe("badgeVariants", () => {
  it("generates correct default classes", () => {
    const classes = badgeVariants();
    expect(classes).toContain("bg-primary");
  });

  it("generates correct secondary classes", () => {
    const classes = badgeVariants({ variant: "secondary" });
    expect(classes).toContain("bg-secondary");
  });
});
