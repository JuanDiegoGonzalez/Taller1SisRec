import { Header } from "@/components/Header"
import { ItemItemRecommendations } from "@/components/movies/ItemItemRecommendations"

export default function ItemItemRecommendationsPage() {
    return (
        <div className="min-h-svh">
            <Header />
            <main className="container px-4 mx-auto">
                <ItemItemRecommendations k={40} showViewAll={false} />
            </main>
        </div>
    )
} 