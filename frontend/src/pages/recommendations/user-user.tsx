import { Header } from "@/components/Header"
import { UserUserRecommendations } from "@/components/movies/UserUserRecommendations"

export default function UserUserRecommendationsPage() {
    return (
        <div className="min-h-svh">
            <Header />
            <main className="container px-4 mx-auto">
                <UserUserRecommendations k={40} showViewAll={false} />
            </main>
        </div>
    )
} 