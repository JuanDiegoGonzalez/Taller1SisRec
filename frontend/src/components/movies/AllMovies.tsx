import { useQuery } from "@tanstack/react-query"
import { MovieCard } from "./MovieCard"
import { Skeleton } from "../ui/skeleton"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { useState } from "react"

interface MovieListItem {
  movie_id: number
  movie_title: string
  imdb_url: string
  avg_rating: number
}

interface MovieListResponse {
  items: MovieListItem[]
  has_next: boolean
  has_previous: boolean
  current_page: number
  total_pages: number
}

export function AllMovies() {
  const [page, setPage] = useState(1)
  const backendUrl = import.meta.env.VITE_BACKEND_URL

  const { data, isLoading, error } = useQuery({
    queryKey: ["allMovies", page],
    queryFn: async (): Promise<MovieListResponse> => {
      const response = await fetch(`${backendUrl}/movies/list?page=${page}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      })
      
      if (!response.ok) {
        throw new Error("Error fetching movies")
      }
      
      return response.json()
    }
  })

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">Error al cargar las películas</p>
      </div>
    )
  }

  const handlePreviousPage = () => {
    if (data?.has_previous) {
      setPage(page - 1)
    }
  }

  const handleNextPage = () => {
    if (data?.has_next) {
      setPage(page + 1)
    }
  }

  return (
    <section className="py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-semibold">Explora todas las películas</h2>
          <p className="text-muted-foreground mt-2">Descubre nuestra colección completa de películas</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {isLoading ? (
          Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="h-[400px] w-full rounded-lg" />
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-4 w-1/2" />
            </div>
          ))
        ) : (
          data?.items.map((movie) => (
            <MovieCard
              key={movie.movie_id}
              id={movie.movie_id}
              title={movie.movie_title}
              image_url={movie.imdb_url}
              avg_rating={movie.avg_rating}
            />
          ))
        )}
      </div>
      
      {data && (
        <div className="flex justify-between items-center mt-8">
          <div className="text-sm text-muted-foreground">
            Página {data.current_page} de {data.total_pages}
          </div>
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={handlePreviousPage}
              disabled={!data.has_previous}
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Anterior
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleNextPage}
              disabled={!data.has_next}
            >
              Siguiente
              <ChevronRight className="h-4 w-4 ml-1" />
            </Button>
          </div>
        </div>
      )}
    </section>
  )
} 