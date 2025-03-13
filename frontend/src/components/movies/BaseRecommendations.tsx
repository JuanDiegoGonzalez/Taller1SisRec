import { useQuery } from "@tanstack/react-query"
import { MovieCard } from "./MovieCard"
import { Skeleton } from "../ui/skeleton"
import { Button } from "../ui/button"
import { useNavigate } from "react-router"

interface Movie {
    id: number
    title: string
    image_url: string
    avg_rating: number
    estimation: number
}

type PredictionResponse = Movie[]

interface BaseRecommendationsProps {
    title: string
    description: string
    queryKey: string
    tipo: "Usuario-Usuario" | "Item-Item"
    k: number
    showViewAll?: boolean
    viewAllPath?: string
}

export function BaseRecommendations({ 
    title, 
    description, 
    queryKey, 
    tipo, 
    k,
    showViewAll = false,
    viewAllPath
}: BaseRecommendationsProps) {
    const userId = localStorage.getItem("username")
    const backendUrl = import.meta.env.VITE_BACKEND_URL
    const navigate = useNavigate()

    const { data, isLoading, error } = useQuery({
        queryKey: [queryKey, userId, k],
        queryFn: async (): Promise<PredictionResponse> => {
            const response = await fetch(`${backendUrl}/model/predict`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    modelo: "Pearson",
                    tipo,
                    k,
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
        <section className="py-8">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-semibold">{title}</h2>
                    <p className="text-muted-foreground mt-2">{description}</p>
                </div>
                {showViewAll && viewAllPath && (
                    <Button 
                        variant="secondary" 
                        onClick={() => navigate(viewAllPath)}
                    >
                        Ver todas las recomendaciones
                    </Button>
                )}
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {isLoading ? (
                    Array.from({ length: k }).map((_, i) => (
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