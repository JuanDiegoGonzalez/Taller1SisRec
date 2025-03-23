import { useQuery } from "@tanstack/react-query"
import { Header } from "@/components/Header"
import { useParams } from "react-router"
import { Skeleton } from "@/components/ui/skeleton"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { MovieCard } from "@/components/movies/MovieCard"

interface Genre {
  id: number
  name: string
}

interface Movie {
  id: number
  title: string
  image_url: string
  avg_rating: number
}

interface GenreMoviesResponse {
  genre: Genre
  items: Movie[]
  has_next: boolean
  has_previous: boolean
  current_page: number
  total_pages: number
}

export default function GenreMovies() {
  const { id } = useParams<{ id: string }>()
  const [page, setPage] = useState(1)
  const backendUrl = import.meta.env.VITE_BACKEND_URL

  const { data, isLoading, error } = useQuery({
    queryKey: ["genreMovies", id, page],
    queryFn: async (): Promise<GenreMoviesResponse> => {
      // Add page parameter for pagination
      const url = new URL(`${backendUrl}/genre/movies/${id}`)
      url.searchParams.append("page", page.toString())
      
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      })
      
      if (!response.ok) {
        throw new Error("Error fetching genre movies")
      }
      
      return response.json()
    },
    enabled: !!id,
  })

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-8">
        {isLoading ? (
          <Skeleton className="h-10 w-64 mb-6" />
        ) : (
          <h1 className="text-3xl font-bold mb-6">
            Películas de Género: {data?.genre.name}
          </h1>
        )}

        {error ? (
          <div className="text-center py-8">
            <p className="text-red-500">Error al cargar las películas</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
              {isLoading
                ? Array.from({ length: 12 }).map((_, i) => (
                        <div key={i} className="space-y-3">
                            <Skeleton className="h-[400px] w-full rounded-lg" />
                            <Skeleton className="h-4 w-3/4" />
                            <Skeleton className="h-4 w-1/2" />
                        </div>
                    ))
                : data?.items.map((movie) => (
                    <MovieCard key={movie.id} id={movie.id} title={movie.title} image_url={movie.image_url} avg_rating={movie.avg_rating} />
                  ))}
            </div>

            {/* Pagination */}
            {data && (
              <div className="flex justify-between items-center pt-4 border-t">
                <div className="text-sm text-muted-foreground">
                  Página {data.current_page} de {data.total_pages}
                </div>
                
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="icon"
                    disabled={!data.has_previous}
                    onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  
                  <Button
                    variant="outline"
                    size="icon"
                    disabled={!data.has_next}
                    onClick={() => setPage((prev) => prev + 1)}
                  >
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
} 