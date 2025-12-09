"use client"

import React, { createContext, useContext, useState, useEffect } from "react"
import axios from "axios"
import { useRouter } from "next/navigation"

interface User {
    username: string
}

interface AuthContextType {
    user: User | null
    token: string | null
    login: (token: string, username: string) => void
    logout: () => void
    isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null)
    const [token, setToken] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(true)
    const router = useRouter()

    useEffect(() => {
        // Check for token in localStorage on mount
        const storedToken = localStorage.getItem("token")
        const storedUser = localStorage.getItem("username")

        if (storedToken && storedUser) {
            setToken(storedToken)
            setUser({ username: storedUser })
            // Unsafe: setting global axios header here
            axios.defaults.headers.common["Authorization"] = `Bearer ${storedToken}`
        }
        setIsLoading(false)
    }, [])

    const login = (newToken: string, newUsername: string) => {
        setToken(newToken)
        setUser({ username: newUsername })
        localStorage.setItem("token", newToken)
        localStorage.setItem("username", newUsername)
        axios.defaults.headers.common["Authorization"] = `Bearer ${newToken}`
        router.push("/")
    }

    const logout = () => {
        setToken(null)
        setUser(null)
        localStorage.removeItem("token")
        localStorage.removeItem("username")
        delete axios.defaults.headers.common["Authorization"]
        router.push("/login")
    }

    return (
        <AuthContext.Provider value={{ user, token, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider")
    }
    return context
}
