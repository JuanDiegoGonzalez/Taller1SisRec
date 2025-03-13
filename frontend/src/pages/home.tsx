import { Header } from "../components/Header"
import { UserUserRecommendations } from "@/components/movies/UserUserRecommendations"
import { ItemItemRecommendations } from "@/components/movies/ItemItemRecommendations"

export default function Home() {
  return (
    <div className="min-h-svh">
      <Header />
      <main className="container px-4 mx-auto">
        <UserUserRecommendations showViewAll={true} />
        <ItemItemRecommendations showViewAll={true} />
      </main>
    </div>
  )
}