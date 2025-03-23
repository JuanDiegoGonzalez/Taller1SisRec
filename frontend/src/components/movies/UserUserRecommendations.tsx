import { BaseRecommendations } from "./BaseRecommendations"

export function UserUserRecommendations({ k = 4, showViewAll = false, viewAllPath = "/recommendations/user-user" }) {
    return (
        <BaseRecommendations
            title="Películas recomendadas para ti"
            description="Basado en usuarios con gustos similares a los tuyos"
            queryKey="user-user-recommendations"
            tipo="Usuario-Usuario"
            k={k}
            showViewAll={showViewAll}
            viewAllPath={viewAllPath}
        />
    )
} 