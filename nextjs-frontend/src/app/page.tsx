import { Navbar } from "@/components/navbar";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

async function getProducts(category: string) {
  // SSR Fetch
  try {
    // Use Docker internal URL if running in Docker, else localhost
    // Since specific instructions said "Run services locally (Docker)", we might be outside docker now calling localhost
    const res = await fetch(`http://localhost:8081/products-microservice/products/category/${category}?page=0&size=4`, { cache: 'no-store' });
    if (!res.ok) return [];
    const data = await res.json();
    return data.content || [];
  } catch (e) {
    console.error(e);
    return [];
  }
}

export default async function Home() {
  const books = await getProducts("Books");
  const music = await getProducts("Music");
  const electronics = await getProducts("Electronics");

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        {/* Hero Section - X.com inspired */}
        <section className="py-16 md:py-24 lg:py-32 border-b border-border">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-6 text-center">
              <div className="space-y-4">
                <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
                  Your Favorite Bookstore, <span className="text-primary">Reimagined.</span>
                </h1>
                <p className="mx-auto max-w-[700px] text-muted-foreground text-lg md:text-xl">
                  Discover the best books, music, and electronics. Secure, fast, and built for you.
                </p>
              </div>
              <div className="flex gap-4">
                <Link href="/products/Books">
                  <Button size="lg" className="font-bold px-8">Shop Books</Button>
                </Link>
                <Link href="/register">
                  <Button variant="outline" size="lg" className="font-bold px-8 border-primary text-primary hover:bg-primary hover:text-primary-foreground">Join Now</Button>
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Bestsellers Section */}
        <section className="container py-12 space-y-16">
          {books.length > 0 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-border pb-4">
                <h2 className="text-xl font-extrabold tracking-tight">Best Sellers in Books</h2>
                <Link href="/products/Books" className="flex items-center text-primary font-semibold hover:underline">
                  View all <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {books.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
              </div>
            </div>
          )}

          {music.length > 0 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-border pb-4">
                <h2 className="text-xl font-extrabold tracking-tight">Top Music</h2>
                <Link href="/products/Music" className="flex items-center text-primary font-semibold hover:underline">
                  View all <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {music.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
              </div>
            </div>
          )}

          {electronics.length > 0 && (
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-border pb-4">
                <h2 className="text-xl font-extrabold tracking-tight">Electronics & Gadgets</h2>
                <Link href="/products/Electronics" className="flex items-center text-primary font-semibold hover:underline">
                  View all <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {electronics.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
              </div>
            </div>
          )}
        </section>
      </main>
      <footer className="border-t border-border py-8 md:px-8">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
          <p className="text-sm text-muted-foreground">
            Built by Antigravity. Source code available on GitHub.
          </p>
        </div>
      </footer>
    </div>
  );
}
