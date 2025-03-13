import { MovieCard } from "@/components/movies/MovieCard"
import { ModeToggle } from "../components/mode-toggle"
import { Button } from "../components/ui/button"
import { useNavigate } from "react-router"


export default function Home() {
    const navigate = useNavigate()
    const username = localStorage.getItem("username")
    const handleLogout = () => {
        localStorage.removeItem("username")
        navigate("/login")
    }
  return (
    <div className="flex flex-col items-center justify-center min-h-svh">
    <div className="flex items-center gap-4 mb-8">
      <h1 className="text-2xl font-bold">Bienvenido, {username}!</h1>
      <Button variant="outline" onClick={handleLogout}>
        Cerrar sesión
      </Button>
      <ModeToggle />
    <MovieCard id={1} estimation={5} title="The Dark Knight" image_url="https://image.tmdb.org/t/p/w500/tgNjemQPG96uIezpiUiXFcer5ga.jpg" avg_rating={4.5} />
      </div>
    </div>
  )
}