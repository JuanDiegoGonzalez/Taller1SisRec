import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Link, useNavigate } from "react-router"
import { useState } from "react"
import { useMutation, useQuery } from "@tanstack/react-query"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { StarRating } from "@/components/movies/MovieCard"  
import { Search } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface RegisterResponse {
  message: string
  username: string
  id: number
}

interface RegisterData {
  username: string
  password: string
}

interface Movie {
  movie_id: number
  movie_title: string
  imdb_url: string
  avg_rating: number
}

interface MovieListResponse {
  items: Movie[]
  has_next: boolean
  has_previous: boolean
  current_page: number
  total_pages: number
}

interface RatedMovie extends Movie {
  user_rating: number
}

export function RegisterForm({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const [activeTab, setActiveTab] = useState("account")
  const [formData, setFormData] = useState<RegisterData>({
    username: "",
    password: "",
  })
  const [confirmPassword, setConfirmPassword] = useState("")
  const [error, setError] = useState<string>("")
  const [searchQuery, setSearchQuery] = useState("")
  const [page, setPage] = useState(1)
  const [ratedMovies, setRatedMovies] = useState<RatedMovie[]>([])
  const navigate = useNavigate()
  const backendUrl = import.meta.env.VITE_BACKEND_URL

  const MIN_RATED_MOVIES = 5
  const isReadyToRegister = formData.username && 
                          formData.password && 
                          formData.password === confirmPassword && 
                          ratedMovies.length >= MIN_RATED_MOVIES

  // Fetch movies for rating
  const { data: movieData, isLoading: isLoadingMovies } = useQuery({
    queryKey: ["registerMovies", page, searchQuery],
    queryFn: async (): Promise<MovieListResponse> => {
      const url = searchQuery 
        ? `${backendUrl}/movies/list?search=${encodeURIComponent(searchQuery)}&page=${page}`
        : `${backendUrl}/movies/list?page=${page}`
      
      const response = await fetch(url, {
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

  const registerMutation = useMutation({
    mutationFn: async (data: { user: RegisterData, ratings: { movie_id: number, rating: number }[] }) => {
      // First register the user
      const registerResponse = await fetch(`${backendUrl}/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data.user),
      })

      if (!registerResponse.ok) {
        const errorData = await registerResponse.text();
        throw new Error(`Error al registrarse: ${JSON.parse(errorData).error}`);
      }

      const userData = await registerResponse.json() as RegisterResponse;
      
      // Then submit all ratings
      if (data.ratings.length > 0) {
        const ratingPromises = data.ratings.map(rating => 
          fetch(`${backendUrl}/movies/rate_movie/${rating.movie_id}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
              user_id: Number(userData.id), 
              rating: rating.rating 
            }),
          })
        );
        
        await Promise.all(ratingPromises);
      }

      return userData;
    },
    onSuccess: (data) => {
      localStorage.setItem("username", data.id.toString())
      navigate("/")
    },
    onError: (error: Error) => {
      setError(error.message)
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    
    if (!isReadyToRegister) {
      setError(`Debes calificar al menos ${MIN_RATED_MOVIES} películas para continuar.`)
      return
    }
    
    const ratings = ratedMovies.map(movie => ({
      movie_id: movie.movie_id,
      rating: movie.user_rating
    }))
    
    registerMutation.mutate({ user: formData, ratings })
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target
    
    if (id === "confirm-password") {
      setConfirmPassword(value)
    } else {
      setFormData({
        ...formData,
        [id]: value,
      })
    }
  }
  
  const toggleMovieSelection = (movie: Movie) => {
    // Check if movie is already rated
    const existingIndex = ratedMovies.findIndex(m => m.movie_id === movie.movie_id)
    
    if (existingIndex >= 0) {
      // Remove movie from rated list
      setRatedMovies(prev => prev.filter(m => m.movie_id !== movie.movie_id))
    } else {
      // Add movie to rated list with 5 stars
      setRatedMovies(prev => [...prev, { ...movie, user_rating: 5 }])
    }
  }
  
  const isMovieSelected = (movieId: number) => {
    return ratedMovies.some(m => m.movie_id === movieId)
  }
  
  const handleNextPage = () => {
    if (movieData?.has_next) {
      setPage(p => p + 1)
    }
  }
  
  const handlePrevPage = () => {
    if (movieData?.has_previous) {
      setPage(p => p - 1)
    }
  }
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value)
    setPage(1) // Reset to first page when search changes
  }

  return (
    <div className={cn("flex flex-col gap-6", className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Registro</CardTitle>
          <CardDescription>
            Crea una cuenta y califica al menos {MIN_RATED_MOVIES} películas que te gusten para comenzar.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8">
              <TabsTrigger value="account">Cuenta</TabsTrigger>
              <TabsTrigger value="movies" disabled={!formData.username || !formData.password || formData.password !== confirmPassword}>
                Calificar Películas {ratedMovies.length > 0 && (
                  <Badge variant="secondary" className="ml-2">
                    {ratedMovies.length}/{MIN_RATED_MOVIES}
                  </Badge>
                )}
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="account">
              <form className="space-y-6">
                <div className="grid gap-3">
                  <Label htmlFor="username">Usuario</Label>
                  <Input
                    id="username"
                    type="text"
                    required
                    value={formData.username}
                    onChange={handleChange}
                  />
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="password">Contraseña</Label>
                  <Input 
                    id="password" 
                    type="password" 
                    required 
                    value={formData.password}
                    onChange={handleChange}
                  />
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="confirm-password">Confirmar Contraseña</Label>
                  <Input 
                    id="confirm-password" 
                    type="password" 
                    required 
                    value={confirmPassword}
                    onChange={handleChange}
                  />
                  {formData.password && confirmPassword && formData.password !== confirmPassword && (
                    <p className="text-sm text-red-500">Las contraseñas no coinciden</p>
                  )}
                </div>
                
                <Button 
                  type="button" 
                  onClick={() => setActiveTab("movies")}
                  disabled={!formData.username || !formData.password || formData.password !== confirmPassword}
                  className="w-full"
                >
                  Continuar
                </Button>
              </form>
            </TabsContent>
            
            <TabsContent value="movies" className="space-y-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Buscar películas..."
                  className="pl-10"
                  value={searchQuery}
                  onChange={handleSearchChange}
                />
              </div>
              
              {ratedMovies.length > 0 && (
                <div className="space-y-2">
                  <h3 className="text-lg font-medium">Películas Seleccionadas ({ratedMovies.length}/{MIN_RATED_MOVIES})</h3>
                  <div className="flex flex-wrap gap-2">
                    {ratedMovies.map(movie => (
                      <Badge key={movie.movie_id} variant="outline" className="px-3 py-1">
                        {movie.movie_title.length > 40 
                          ? movie.movie_title.substring(0, 37) + '...' 
                          : movie.movie_title}
                        <button 
                          className="ml-2 text-destructive hover:text-destructive/80"
                          onClick={() => toggleMovieSelection(movie)}
                        >
                          ×
                        </button>
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="border rounded-lg overflow-hidden">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
                  {isLoadingMovies ? (
                    Array.from({ length: 6 }).map((_, i) => (
                      <div key={i} className="p-4 border rounded-lg space-y-2">
                        <Skeleton className="h-[180px] w-full rounded-md" />
                        <Skeleton className="h-4 w-3/4" />
                        <Skeleton className="h-4 w-1/2" />
                      </div>
                    ))
                  ) : (
                    movieData?.items.map((movie) => (
                      <div 
                        key={movie.movie_id} 
                        className={cn(
                          "p-4 border rounded-lg space-y-3 cursor-pointer hover:bg-secondary/50 transition-colors",
                          isMovieSelected(movie.movie_id) && "bg-secondary border-primary"
                        )}
                        onClick={() => toggleMovieSelection(movie)}
                      >
                        <div className="flex gap-4">
                          <div className="h-[100px] w-[70px] overflow-hidden rounded">
                            <img 
                              src={movie.imdb_url} 
                              alt={movie.movie_title} 
                              className="h-full w-full object-cover"
                            />
                          </div>
                          <div className="flex-1">
                            <h3 className="font-medium line-clamp-2">{movie.movie_title}</h3>
                            <div className="flex items-center mt-1">
                              <StarRating rating={movie.avg_rating} />
                              <span className="text-xs text-muted-foreground ml-2">
                                {movie.avg_rating.toFixed(1)}
                              </span>
                            </div>
                          </div>
                        </div>
                        
                        {isMovieSelected(movie.movie_id) && (
                          <Badge className="bg-primary">Seleccionada</Badge>
                        )}
                      </div>
                    ))
                  )}
                </div>
                
                {movieData && (
                  <div className="flex items-center justify-between p-4 border-t">
                    <div className="text-sm text-muted-foreground">
                      Página {movieData.current_page} de {movieData.total_pages}
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handlePrevPage}
                        disabled={!movieData.has_previous}
                      >
                        Anterior
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleNextPage}
                        disabled={!movieData.has_next}
                      >
                        Siguiente
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
          
          {error && (
            <Alert variant="destructive" className="mt-6">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button 
            onClick={handleSubmit}
            className="w-full"
            disabled={!isReadyToRegister || registerMutation.isPending}
          >
            {registerMutation.isPending ? "Registrando..." : "Completar Registro"}
          </Button>
          
          <p className="text-center text-sm">
            ¿Ya tienes una cuenta?{" "}
            <Link to="/login" className="underline underline-offset-4">
              Iniciar sesión
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
} 