import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Link, useNavigate } from "react-router"
import { useState } from "react"
import { useMutation } from "@tanstack/react-query"

interface LoginResponse {
  message: string
  username: string
}

interface LoginData {
  username: string
  password: string
}

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const [formData, setFormData] = useState<LoginData>({
    username: "",
    password: "",
  })
  const [error, setError] = useState<string>("")
  const navigate = useNavigate()

  const loginMutation = useMutation({
    mutationFn: async (data: LoginData) => {
      console.log('Backend URL:', import.meta.env.VITE_BACKEND_URL); // Debug log
      const url = 
      `${import.meta.env.VITE_BACKEND_URL}/login/`;
      console.log('Full URL:', url); // Debug log
      
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        const errorData = await response.text();
        console.error('Login error:', errorData); // Debug log
        throw new Error(`Error al iniciar sesión: ${errorData}`);
      }

      return response.json() as Promise<LoginResponse>
    },
    onSuccess: (data) => {
      console.log('Login successful:', data); // Debug log
      localStorage.setItem("username", data.username)
      navigate("/")
    },
    onError: (error: Error) => {
      console.error('Login mutation error:', error); // Debug log
      setError(error.message)
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    loginMutation.mutate(formData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    })
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle>Iniciar sesión</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="flex flex-col gap-6">
              <div className="grid gap-3">
                <Label htmlFor="username">Usuario</Label>
                <Input
                  id="username"
                  type="text"
                  required
                  value={formData.username}
                  onChange={handleChange}
                />
              </div>
              <div className="grid gap-3">
                <div className="flex items-center">
                  <Label htmlFor="password">Contraseña</Label>
                </div>
                <Input 
                  id="password" 
                  type="password" 
                  required 
                  value={formData.password}
                  onChange={handleChange}
                />
              </div>
              {error && (
                <div className="text-sm text-red-500">
                  {error}
                </div>
              )}
              <div className="flex flex-col gap-3">
                <Button 
                  type="submit" 
                  className="w-full"
                  disabled={loginMutation.isPending}
                >
                  {loginMutation.isPending ? "Iniciando sesión..." : "Iniciar sesión"}
                </Button>
              </div>
            </div>
            <div className="mt-4 text-center text-sm">
              No tienes una cuenta?{" "}
              <Link to="/register" className="underline underline-offset-4">
                Registrarse
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
