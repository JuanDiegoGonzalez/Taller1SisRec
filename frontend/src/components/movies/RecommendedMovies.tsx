import { useQuery } from "@tanstack/react-query"
import { MovieCard } from "./MovieCard"
import { Skeleton } from "../ui/skeleton"

interface Movie {
    id: number
    title: string
    image_url: string
    avg_rating: number
    estimation: number
}

type PredictionResponse = Movie[]

export function RecommendedMovies() {
    const userId = localStorage.getItem("username")
    const backendUrl = import.meta.env.VITE_BACKEND_URL

    const { data, isLoading, error } = useQuery({
        queryKey: ["recommendations", userId],
        queryFn: async (): Promise<PredictionResponse> => {
            const response = await fetch(`${backendUrl}/model/predict`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    modelo: "Pearson",
                    tipo: "Usuario-Usuario",
                    k: 20,
                    userId: Number(userId)
                })
            })
            if (!response.ok) {
                throw new Error("Error fetching recommendations")
            }
            return response.json()
        },
        enabled: !!userId
    })

    if (error) {
        return (
            <div className="text-center py-8">
                <p className="text-red-500">Error al cargar las recomendaciones</p>
            </div>
        )
    }

    return (
        <section className="py-8 mx-auto">
            <h2 className="text-2xl font-semibold mb-6">Películas recomendadas para ti</h2>
            <p className="text-muted-foreground mb-6">Basado en usuarios con gustos similares a los tuyos</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {isLoading ? (
                    Array.from({ length: 8 }).map((_, i) => (
                        <div key={i} className="space-y-3">
                            <Skeleton className="h-[400px] w-full rounded-lg" />
                            <Skeleton className="h-4 w-3/4" />
                            <Skeleton className="h-4 w-1/2" />
                        </div>
                    ))
                ) : (
                    data?.map((movie) => (
                        <MovieCard
                            key={movie.id}
                            id={movie.id}
                            title={movie.title}
                            image_url={movie.image_url}
                            avg_rating={movie.avg_rating}
                            estimation={movie.estimation}
                        />
                    ))
                )}
            </div>
        </section>
    )
} 