import Link from "next/link"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Star } from "lucide-react"

export interface Product {
    id: string | { asin: string }
    title: string
    price: number
    imUrl: string
    category: string
}

export function ProductCard({ product }: { product: Product }) {
    const asin = typeof product.id === 'string' ? product.id : product.id.asin

    return (
        <Card className="flex flex-col h-full overflow-hidden transition-all hover:border-primary/50 rounded-xl">
            <Link href={`/product/${asin}`} className="flex-1">
                <div className="aspect-[3/4] overflow-hidden relative group bg-secondary">
                    <img
                        src={product.imUrl}
                        alt={product.title}
                        className="object-cover w-full h-full transition-transform group-hover:scale-105"
                    />
                </div>
            </Link>
            <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                    <Badge variant="secondary" className="text-xs">{product.category}</Badge>
                    <div className="flex items-center text-primary">
                        <Star className="w-3 h-3 fill-current" />
                        <span className="text-xs ml-1 font-semibold">4.5</span>
                    </div>
                </div>
                <Link href={`/product/${asin}`}>
                    <h3 className="font-bold text-base leading-tight line-clamp-2 hover:text-primary transition-colors">{product.title}</h3>
                </Link>
                <div className="mt-2 font-extrabold text-xl text-primary">${product.price.toFixed(2)}</div>
            </CardContent>
            <CardFooter className="p-4 pt-0 mt-auto">
                <Button className="w-full font-bold">Add to Cart</Button>
            </CardFooter>
        </Card>
    )
}
