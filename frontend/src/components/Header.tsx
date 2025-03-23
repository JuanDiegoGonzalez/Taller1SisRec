import { Button } from "./ui/button"
import { ModeToggle } from "./mode-toggle"
import { useNavigate, useLocation } from "react-router"
import { ChevronLeft, Home, Star } from "lucide-react"

export function Header() {
    const navigate = useNavigate()
    const location = useLocation()
    const username = localStorage.getItem("username")
    
    const handleLogout = () => {
        localStorage.removeItem("username")
        navigate("/login")
    }

    const showBackButton = location.pathname !== "/"
    
    return (
        <header className="w-full border-b">
            <div className="container flex h-16 items-center justify-between px-4 mx-auto">
                <div className="flex items-center gap-4">
                    {showBackButton && (
                        <Button 
                            variant="ghost" 
                            size="icon"
                            onClick={() => navigate(-1)}
                        >
                            <ChevronLeft className="h-5 w-5" />
                        </Button>
                    )}
                    {showBackButton && (
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => navigate("/")}
                        >
                            <Home className="h-5 w-5" />
                        </Button>
                    )}
                    <h1 className="text-2xl font-bold">Bienvenido, {username}!</h1>
                </div>
                <div className="flex items-center gap-4">
                    <Button 
                        variant="ghost" 
                        className="flex items-center gap-2"
                        onClick={() => navigate("/user-ratings")}
                    >
                        <Star className="h-4 w-4" />
                        <span>Mis Calificaciones</span>
                    </Button>
                    <Button variant="outline" onClick={handleLogout}>
                        Cerrar sesión
                    </Button>
                    <ModeToggle />
                </div>
            </div>
        </header>
    )
} 