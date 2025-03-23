import { Header } from "../components/Header"
import { UserUserRecommendations } from "@/components/movies/UserUserRecommendations"
import { ItemItemRecommendations } from "@/components/movies/ItemItemRecommendations"
import { AllMovies } from "@/components/movies/AllMovies"
import { Button } from "@/components/ui/button"
import { Star, Film } from "lucide-react"
import { useNavigate } from "react-router"
import { useEffect, useState } from "react"

export default function Home() {
  const navigate = useNavigate()
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  
  useEffect(() => {
    const username = localStorage.getItem("username")
    setIsLoggedIn(!!username)
  }, [])
  
  return (
    <div className="min-h-svh">
      <Header />
      <main className="container px-4 mx-auto">
        <section className="py-8">
          {isLoggedIn && (
            <div className="bg-secondary/30 rounded-lg p-6 mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-semibold flex items-center gap-2">
                    <Star className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                    Mis Calificaciones
                  </h2>
                  <p className="text-muted-foreground mt-2">
                    Visualiza y modifica todas las películas que has calificado.
                  </p>
                </div>
                <Button onClick={() => navigate("/user-ratings")}>
                  Ver mis calificaciones
                </Button>
              </div>
            </div>
          )}
          
          <div className="bg-secondary/30 rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold flex items-center gap-2">
                  <Film className="h-5 w-5" />
                  Explorar por Género
                </h2>
                <p className="text-muted-foreground mt-2">
                  Descubre películas organizadas por género para encontrar exactamente lo que buscas.
                </p>
              </div>
              <Button onClick={() => navigate("/genres")}>
                Explorar géneros
              </Button>
            </div>
          </div>
        </section>
        
        {isLoggedIn ? (
          <>
            <UserUserRecommendations showViewAll={true} viewAllPath="/recommendations/user-user" />
            <ItemItemRecommendations showViewAll={true} viewAllPath="/recommendations/item-item" />
          </>
        ) : (
          <AllMovies />
        )}
      </main>
    </div>
  )
}