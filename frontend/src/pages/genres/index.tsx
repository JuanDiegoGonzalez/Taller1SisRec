import { useQuery } from "@tanstack/react-query"
import { Header } from "@/components/Header"
import { Button } from "@/components/ui/button"
import { useNavigate } from "react-router"
import { Skeleton } from "@/components/ui/skeleton"

interface Genre {
  id: number
  name: string
}

export default function GenreExplorer() {
  const navigate = useNavigate()
  const backendUrl = import.meta.env.VITE_BACKEND_URL

  const { data: genres, isLoading, error } = useQuery({
    queryKey: ["allGenres"],
    queryFn: async (): Promise<Genre[]> => {
      const response = await fetch(`${backendUrl}/genre/all`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      })
      
      if (!response.ok) {
        throw new Error("Error fetching genres")
      }
      
      return response.json()
    }
  })

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Explorar por Género</h1>
        <p className="text-muted-foreground mb-8">
          Descubre películas organizadas por género para encontrar exactamente lo que buscas.
        </p>

        {error ? (
          <div className="text-center py-8">
            <p className="text-red-500">Error al cargar los géneros</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {isLoading
              ? Array.from({ length: 19 }).map((_, i) => (
                  <Skeleton key={i} className="h-24 rounded-lg" />
                ))
              : genres?.map((genre) => (
                  <Button
                    key={genre.id}
                    variant="outline"
                    className="h-24 text-lg font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
                    onClick={() => navigate(`/genres/${genre.id}`)}
                  >
                    {genre.name}
                  </Button>
                ))}
          </div>
        )}
      </main>
    </div>
  )
}