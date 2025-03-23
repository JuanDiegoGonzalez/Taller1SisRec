import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Star, StarHalf } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { toast } from "sonner"

interface UserRatedMovieCardProps {
  id: number
  title: string
  image_url: string
  user_rating: number
}

function StarRating({ rating, onClick }: { rating: number, onClick?: (rating: number) => void }) {
  const totalStars = 5;
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = totalStars - fullStars - (hasHalfStar ? 1 : 0);

  return (
    <div className="flex">
      {/* Full stars */}
      {Array.from({ length: fullStars }).map((_, i) => (
        <Star 
          key={`full-${i}`} 
          className={`h-5 w-5 fill-yellow-400 text-yellow-400 ${onClick ? 'cursor-pointer' : ''}`}
          onClick={() => onClick?.(i + 1)}
        />
      ))}
      
      {/* Half star */}
      {hasHalfStar && (
        <div className="relative">
          <Star className="h-5 w-5 text-yellow-400/30" />
          <StarHalf className="absolute left-0 top-0 h-5 w-5 fill-yellow-400 text-yellow-400" />
        </div>
      )}
      
      {/* Empty stars */}
      {Array.from({ length: emptyStars }).map((_, i) => (
        <Star 
          key={`empty-${i}`} 
          className={`h-5 w-5 text-yellow-400/30 ${onClick ? 'cursor-pointer' : ''}`}
          onClick={() => onClick?.(fullStars + (hasHalfStar ? 1 : 0) + i + 1)}
        />
      ))}
    </div>
  );
}

export function UserRatedMovieCard({ id, title, image_url, user_rating }: UserRatedMovieCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [selectedRating, setSelectedRating] = useState(user_rating);
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const userId = localStorage.getItem("username");
  const queryClient = useQueryClient();

  const updateRatingMutation = useMutation({
    mutationFn: async (newRating: number) => {
      const response = await fetch(`${backendUrl}/movies/rate_movie/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: Number(userId), rating: newRating }),
      });

      if (!response.ok) {
        throw new Error("Error al actualizar la calificación");
      }

      return response.json();
    },
    onSuccess: () => {
      toast.success("Calificación actualizada con éxito");
      setIsEditing(false);
      // Invalidate and refetch the user ratings query
      queryClient.invalidateQueries({ queryKey: ["userRatings", userId] });
    },
    onError: () => {
      toast.error("Error al actualizar la calificación");
      setSelectedRating(user_rating); // Reset to original rating
      setIsEditing(false);
    }
  });

  const handleUpdate = () => {
    if (selectedRating !== user_rating) {
      updateRatingMutation.mutate(selectedRating);
    } else {
      setIsEditing(false);
    }
  };

  return (
    <Card className="w-[300px] overflow-hidden pt-0">
      <div className="relative h-[400px] w-full">
        <img
          src={image_url}
          alt={title}
          className="absolute inset-0 h-full w-full object-cover"
        />
      </div>
      <CardHeader>
        <CardTitle className="line-clamp-1">{title}</CardTitle>
        <CardDescription className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium">Tu calificación:</span>
            {isEditing ? (
              <StarRating rating={selectedRating} onClick={setSelectedRating} />
            ) : (
              <StarRating rating={user_rating} />
            )}
          </div>
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isEditing ? (
          <div className="flex gap-2 justify-end">
            <Button 
              variant="outline" 
              onClick={() => {
                setIsEditing(false);
                setSelectedRating(user_rating);
              }}
            >
              Cancelar
            </Button>
            <Button 
              onClick={handleUpdate}
              disabled={updateRatingMutation.isPending}
            >
              {updateRatingMutation.isPending ? "Actualizando..." : "Guardar"}
            </Button>
          </div>
        ) : (
          <Button 
            onClick={() => setIsEditing(true)} 
            className="w-full"
            variant="outline"
          >
            Modificar calificación
          </Button>
        )}
      </CardContent>
    </Card>
  )
} 