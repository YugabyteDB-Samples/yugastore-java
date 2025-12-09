"use client"

import Link from "next/link"
import { useAuth } from "@/context/AuthContext"
import { Button } from "@/components/ui/button"
import { ShoppingCart, LogOut, LogIn, User } from "lucide-react"

export function Navbar() {
    const { user, logout } = useAuth()

    return (
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
            <div className="container flex h-14 items-center">
                <div className="mr-4 hidden md:flex">
                    <Link href="/" className="mr-6 flex items-center space-x-2">
                        <span className="hidden font-extrabold text-xl sm:inline-block tracking-tight">Bookstore R Us</span>
                    </Link>
                    <nav className="flex items-center space-x-6 text-sm font-medium">
                        <Link href="/products/Books" className="transition-colors hover:text-primary text-muted-foreground">Books</Link>
                        <Link href="/products/Music" className="transition-colors hover:text-primary text-muted-foreground">Music</Link>
                        <Link href="/products/Beauty" className="transition-colors hover:text-primary text-muted-foreground">Beauty</Link>
                        <Link href="/products/Electronics" className="transition-colors hover:text-primary text-muted-foreground">Electronics</Link>
                    </nav>
                </div>
                <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
                    <div className="w-full flex-1 md:w-auto md:flex-none">
                        {/* Search could go here */}
                    </div>
                    <nav className="flex items-center space-x-2">
                        <Link href="/cart">
                            <Button variant="ghost" size="icon" className="hover:bg-primary/10 hover:text-primary">
                                <ShoppingCart className="h-5 w-5" />
                                <span className="sr-only">Cart</span>
                            </Button>
                        </Link>

                        {user ? (
                            <>
                                <span className="text-sm text-muted-foreground hidden sm:inline-block">Hi, {user.username}</span>
                                <Button variant="ghost" size="icon" onClick={logout} className="hover:bg-destructive/10 hover:text-destructive">
                                    <LogOut className="h-5 w-5" />
                                    <span className="sr-only">Logout</span>
                                </Button>
                            </>
                        ) : (
                            <Link href="/login">
                                <Button variant="ghost" size="sm" className="hover:bg-primary/10 hover:text-primary">
                                    <LogIn className="mr-2 h-4 w-4" />
                                    Login
                                </Button>
                            </Link>
                        )}
                    </nav>
                </div>
            </div>
        </nav>
    )
}
