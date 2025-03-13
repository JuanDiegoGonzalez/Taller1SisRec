import { ThemeProvider } from "@/components/theme-provider"
import { Route, Routes, BrowserRouter } from "react-router"
import { ProtectedRoute } from "./components/protected-route"
import Home from "./pages/home"
import Login from "./pages/login"
function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
