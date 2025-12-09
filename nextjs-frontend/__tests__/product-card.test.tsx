import { render, screen } from "@testing-library/react";
import { ProductCard, Product } from "@/components/product-card";

const mockProduct: Product = {
  id: "test-asin-123",
  title: "Test Product Title",
  price: 29.99,
  imUrl: "https://example.com/image.jpg",
  category: "Books",
};

const mockProductWithObjectId: Product = {
  id: { asin: "asin-object-456" },
  title: "Object ID Product",
  price: 49.99,
  imUrl: "https://example.com/image2.jpg",
  category: "Electronics",
};

describe("ProductCard", () => {
  it("renders product title", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText("Test Product Title")).toBeInTheDocument();
  });

  it("renders product price formatted correctly", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText("$29.99")).toBeInTheDocument();
  });

  it("renders product category as a badge", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText("Books")).toBeInTheDocument();
  });

  it("renders product image with alt text", () => {
    render(<ProductCard product={mockProduct} />);
    const img = screen.getByAltText("Test Product Title");
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute("src", "https://example.com/image.jpg");
  });

  it("renders Add to Cart button", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByRole("button", { name: /add to cart/i })).toBeInTheDocument();
  });

  it("links to product page with string id", () => {
    render(<ProductCard product={mockProduct} />);
    const links = screen.getAllByRole("link");
    const productLinks = links.filter(link =>
      link.getAttribute("href")?.includes("/product/test-asin-123")
    );
    expect(productLinks.length).toBeGreaterThan(0);
  });

  it("links to product page with object id", () => {
    render(<ProductCard product={mockProductWithObjectId} />);
    const links = screen.getAllByRole("link");
    const productLinks = links.filter(link =>
      link.getAttribute("href")?.includes("/product/asin-object-456")
    );
    expect(productLinks.length).toBeGreaterThan(0);
  });

  it("renders with X.com-inspired styling", () => {
    const { container } = render(<ProductCard product={mockProduct} />);
    const card = container.firstChild as HTMLElement;
    expect(card).toHaveClass("rounded-xl");
    expect(card).toHaveClass("hover:border-primary/50");
  });

  it("displays star rating", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText("4.5")).toBeInTheDocument();
  });

  it("price is styled with primary color", () => {
    render(<ProductCard product={mockProduct} />);
    const priceElement = screen.getByText("$29.99");
    expect(priceElement).toHaveClass("text-primary");
    expect(priceElement).toHaveClass("font-extrabold");
  });
});
