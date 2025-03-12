import { Button } from "@/components/ui/button"
import { ThemeProvider } from "@/components/theme-provider"
import { ModeToggle } from "@/components/mode-toggle"
import { useNavigate } from "react-router"

function App() {
  const navigate = useNavigate()
  const username = localStorage.getItem("username")

  const handleLogout = () => {
    localStorage.removeItem("username")
    navigate("/login")
  }

  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <div className="flex flex-col items-center justify-center min-h-svh">
        <div className="flex items-center gap-4 mb-8">
          <h1 className="text-2xl font-bold">Bienvenido, {username}!</h1>
          <Button variant="outline" onClick={handleLogout}>
            Cerrar sesión
          </Button>
          <ModeToggle />
        </div>
      </div>
    </ThemeProvider>
  )
}

export default App
