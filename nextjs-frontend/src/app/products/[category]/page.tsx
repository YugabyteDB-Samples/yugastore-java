import { Navbar } from "@/components/navbar";
import { ProductCard } from "@/components/product-card";
import { Button } from "@/components/ui/button"; // For pagination if needed

async function getProducts(category: string) {
    try {
        const res = await fetch(`http://localhost:8081/products-microservice/products/category/${category}?page=0&size=20`, { cache: 'no-store' });
        if (!res.ok) return [];
        const data = await res.json();
        return data.content || [];
    } catch (e) {
        console.error(e);
        return [];
    }
}

export default async function CategoryPage({ params }: { params: { category: string } }) {
    const products = await getProducts(params.category);

    return (
        <div className="flex min-h-screen flex-col">
            <Navbar />
            <main className="container py-8 flex-1">
                <h1 className="text-3xl font-bold tracking-tight mb-8 capitalize">{params.category}</h1>

                {products.length === 0 ? (
                    <div className="text-center py-20 text-muted-foreground">
                        No products found in this category.
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        {products.map((p: any) => <ProductCard key={p.id.asin || p.id} product={p} />)}
                    </div>
                )}
            </main>
        </div>
    );
}
