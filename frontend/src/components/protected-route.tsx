import { Navigate } from "react-router"

interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const username = localStorage.getItem("username")

  if (!username) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
} 