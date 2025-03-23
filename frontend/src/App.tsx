import { ThemeProvider } from "@/components/theme-provider"
import { Route, Routes, BrowserRouter } from "react-router"
import { ProtectedRoute } from "./components/protected-route"
import Home from "./pages/home"
import Login from "./pages/login"
import Register from "./pages/register"
import UserRecommendations from "./pages/recommendations/user-user"
import MovieRecommendations from "./pages/recommendations/item-item"
import UserRatings from "./pages/user-ratings"
import GenreExplorer from "./pages/genres/index"
import GenreMovies from "./pages/genres/[id]"

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/recommendations/user-user"
            element={
              <ProtectedRoute>
                <UserRecommendations />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recommendations/item-item"
            element={
              <ProtectedRoute>
                <MovieRecommendations />
              </ProtectedRoute>
            }
          />
          <Route
            path="/user-ratings"
            element={
              <ProtectedRoute>
                <UserRatings />
              </ProtectedRoute>
            }
          />
          <Route path="/genres" element={<GenreExplorer />} />
          <Route path="/genres/:id" element={<GenreMovies />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
