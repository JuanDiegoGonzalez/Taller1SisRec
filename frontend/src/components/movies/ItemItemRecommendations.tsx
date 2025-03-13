import { BaseRecommendations } from "./BaseRecommendations"

export function ItemItemRecommendations({ k = 4, showViewAll = false }) {
    return (
        <BaseRecommendations
            title="Películas similares a tus favoritas"
            description="Basado en películas con características similares a las que te gustan"
            queryKey="item-item-recommendations"
            tipo="Item-Item"
            k={k}
            showViewAll={showViewAll}
            viewAllPath="/recommendations/item-item"
        />
    )
} 