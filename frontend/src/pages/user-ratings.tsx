import { useQuery } from "@tanstack/react-query"
import { Header } from "@/components/Header"
import { Skeleton } from "@/components/ui/skeleton"
import { UserRatedMovieCard } from "@/components/movies/UserRatedMovieCard"

interface Movie {
  id: number
  title: string
  image_url: string
  user_rating: number
}

interface UserRatingsResponse {
  user_id: number
  movies: Movie[]
}

export default function UserRatings() {
  const userId = localStorage.getItem("username")
  const backendUrl = import.meta.env.VITE_BACKEND_URL

  const { data, isLoading, error } = useQuery({
    queryKey: ["userRatings", userId],
    queryFn: async (): Promise<UserRatingsResponse> => {
      const response = await fetch(`${backendUrl}/movies/user_rating/${userId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      })
      console.log(response)
      if (!response.ok) {
        throw new Error("Error fetching user ratings")
      }
      
      return response.json()
    },
    enabled: !!userId,
  })

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Mis Calificaciones</h1>
        <p className="text-muted-foreground mb-8">
          Aquí puedes ver y modificar todas las películas que has calificado.
        </p>

        {error ? (
          <div className="text-center py-8">
            <p className="text-red-500">Error al cargar tus calificaciones</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {isLoading
              ? Array.from({ length: 8 }).map((_, i) => (
                  <div key={i} className="space-y-3">
                    <Skeleton className="h-[400px] w-full rounded-lg" />
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-1/2" />
                  </div>
                ))
              : data?.movies.map((movie) => (
                  <UserRatedMovieCard
                    key={movie.id}
                    id={movie.id}
                    title={movie.title}
                    image_url={movie.image_url}
                    user_rating={movie.user_rating}
                  />
                ))}
          </div>
        )}
      </main>
    </div>
  )
} 