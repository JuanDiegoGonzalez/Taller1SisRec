import { Button } from "./ui/button"
import { ModeToggle } from "./mode-toggle"
import { useNavigate } from "react-router"

export function Header() {
    const navigate = useNavigate()
    const username = localStorage.getItem("username")
    
    const handleLogout = () => {
        localStorage.removeItem("username")
        navigate("/login")
    }

    return (
        <header className="w-full border-b">
            <div className="container flex h-16 items-center justify-between px-4 mx-auto">
                <h1 className="text-2xl font-bold">Bienvenido, {username}!</h1>
                <div className="flex items-center gap-4">
                    <Button variant="outline" onClick={handleLogout}>
                        Cerrar sesión
                    </Button>
                    <ModeToggle />
                </div>
            </div>
        </header>
    )
} 