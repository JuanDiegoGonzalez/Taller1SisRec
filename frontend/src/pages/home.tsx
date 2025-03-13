import { Header } from "../components/Header"
import { RecommendedMovies } from "@/components/movies/RecommendedMovies"

export default function Home() {
  return (
    <div className="min-h-svh">
      <Header />
      <main className="container px-4 mx-auto">
        <RecommendedMovies />
      </main>
    </div>
  )
}