"use client"

import { useEffect, useState } from "react"
import { useAuth } from "@/context/AuthContext"
import { Navbar } from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Trash2 } from "lucide-react"
import Link from "next/link"
import axios from "axios"
import { useRouter } from "next/navigation"

interface CartItem {
    asin: string
    quantity: number
    title: string
    price: number
    imUrl: string
}

export default function CartPage() {
    const { user, token, isLoading } = useAuth()
    const [cartItems, setCartItems] = useState<CartItem[]>([])
    const [loadingCart, setLoadingCart] = useState(true)
    const [checkoutStatus, setCheckoutStatus] = useState("")
    const router = useRouter()

    useEffect(() => {
        if (!isLoading && !user) {
            router.push("/login")
        } else if (user) {
            fetchCart()
        }
    }, [user, isLoading, router])

    const fetchCart = async () => {
        setLoadingCart(true)
        try {
            // 1. Get items (asin -> qty)
            const res = await axios.get(`http://localhost:8081/cart-microservice/shoppingCart/productsInCart?userid=${user?.username}`)
            const itemsMap = res.data

            // 2. Hydrate with product details
            const hydratedItems: CartItem[] = []
            for (const [asin, qty] of Object.entries(itemsMap)) {
                try {
                    const prodRes = await axios.get(`http://localhost:8081/products-microservice/product/${asin}`)
                    const prod = prodRes.data
                    hydratedItems.push({
                        asin: asin,
                        quantity: qty as number,
                        title: prod.title,
                        price: prod.price,
                        imUrl: prod.imUrl
                    })
                } catch (e) {
                    // If product not found, maybe just skip or show minimal
                    console.error("Failed to fetch product", asin)
                }
            }
            setCartItems(hydratedItems)
        } catch (error) {
            console.error("Failed to fetch cart", error)
        } finally {
            setLoadingCart(false)
        }
    }

    const removeItem = async (asin: string) => {
        try {
            await axios.get(`http://localhost:8081/cart-microservice/shoppingCart/removeProduct?userid=${user?.username}&asin=${asin}`)
            fetchCart() // Refresh
        } catch (error) {
            console.error("Failed to remove item", error)
        }
    }

    const checkout = async () => {
        try {
            setCheckoutStatus("processing")
            const res = await axios.post(`http://localhost:8081/checkout-microservice/shoppingCart/checkout?userid=${user?.username}`)
            if (res.data.status === "SUCCESS") {
                setCheckoutStatus("success")
                setCartItems([]) // Clear local cart
            } else {
                setCheckoutStatus("failed")
                alert(res.data.orderDetails)
            }
        } catch (error) {
            console.error("Checkout failed", error)
            setCheckoutStatus("failed")
        }
    }

    if (isLoading || (loadingCart && user)) {
        return (
            <div className="flex min-h-screen flex-col">
                <Navbar />
                <div className="flex-1 flex items-center justify-center">
                    <Loader2 className="h-8 w-8 animate-spin" />
                </div>
            </div>
        )
    }

    const total = cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0)

    return (
        <div className="flex min-h-screen flex-col">
            <Navbar />
            <main className="container py-8 flex-1">
                <h1 className="text-3xl font-bold tracking-tight mb-8">Shopping Cart</h1>

                {checkoutStatus === "success" ? (
                    <Card className="max-w-md mx-auto text-center p-8">
                        <CardTitle className="mb-4 text-green-600">Order Placed Successfully!</CardTitle>
                        <p className="text-muted-foreground mb-6">Thank you for your purchase.</p>
                        <Link href="/">
                            <Button>Continue Shopping</Button>
                        </Link>
                    </Card>
                ) : cartItems.length === 0 ? (
                    <div className="text-center py-20">
                        <p className="text-muted-foreground mb-4">Your cart is empty.</p>
                        <Link href="/">
                            <Button>Start Shopping</Button>
                        </Link>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 space-y-4">
                            {cartItems.map((item) => (
                                <Card key={item.asin} className="flex flex-row p-4 items-center gap-4">
                                    <div className="w-20 h-20 relative overflow-hidden rounded border shrink-0">
                                        <img src={item.imUrl} alt={item.title} className="object-cover w-full h-full" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="font-semibold line-clamp-1">{item.title}</h3>
                                        <div className="text-sm text-muted-foreground">Qty: {item.quantity}</div>
                                        <div className="font-bold">${item.price.toFixed(2)}</div>
                                    </div>
                                    <Button variant="ghost" size="icon" className="text-destructive" onClick={() => removeItem(item.asin)}>
                                        <Trash2 className="h-5 w-5" />
                                    </Button>
                                </Card>
                            ))}
                        </div>
                        <div>
                            <Card>
                                <CardHeader>
                                    <CardTitle>Order Summary</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-2">
                                    <div className="flex justify-between">
                                        <span>Subtotal</span>
                                        <span>${total.toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between font-bold text-lg pt-4 border-t">
                                        <span>Total</span>
                                        <span>${total.toFixed(2)}</span>
                                    </div>
                                </CardContent>
                                <CardFooter>
                                    <Button className="w-full" size="lg" onClick={checkout} disabled={checkoutStatus === "processing"}>
                                        {checkoutStatus === "processing" ? "Processing..." : "Checkout"}
                                    </Button>
                                </CardFooter>
                            </Card>
                        </div>
                    </div>
                )}
            </main>
        </div>
    )
}
