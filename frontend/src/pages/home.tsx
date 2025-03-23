import { Header } from "../components/Header"
import { UserUserRecommendations } from "@/components/movies/UserUserRecommendations"
import { ItemItemRecommendations } from "@/components/movies/ItemItemRecommendations"
import { Button } from "@/components/ui/button"
import { Star } from "lucide-react"
import { useNavigate } from "react-router"

export default function Home() {
  const navigate = useNavigate()
  
  return (
    <div className="min-h-svh">
      <Header />
      <main className="container px-4 mx-auto">
        <section className="pt-8">
          <div className="bg-secondary/30 rounded-lg p-6">
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
        </section>
        
        <UserUserRecommendations showViewAll={true} />
        <ItemItemRecommendations showViewAll={true} />
      </main>
    </div>
  )
}