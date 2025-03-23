import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Star, StarHalf, Info } from "lucide-react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { toast } from "sonner"


interface MovieCardProps {
  id: number
  estimation: number
  title: string
  image_url: string
  avg_rating: number
  reason: string
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
          className={`h-4 w-4 fill-yellow-400 text-yellow-400 ${onClick ? 'cursor-pointer' : ''}`}
          onClick={() => onClick?.(i + 1)}
        />
      ))}
      
      {/* Half star */}
      {hasHalfStar && (
        <div className="relative">
          <Star className="h-4 w-4 text-yellow-400/30" />
          <StarHalf className="absolute left-0 top-0 h-4 w-4 fill-yellow-400 text-yellow-400" />
        </div>
      )}
      
      {/* Empty stars */}
      {Array.from({ length: emptyStars }).map((_, i) => (
        <Star 
          key={`empty-${i}`} 
          className={`h-4 w-4 text-yellow-400/30 ${onClick ? 'cursor-pointer' : ''}`}
          onClick={() => onClick?.(fullStars + (hasHalfStar ? 1 : 0) + i + 1)}
        />
      ))}
    </div>
  );
}

export function MovieCard({ id, title, image_url, avg_rating, reason }: MovieCardProps) {
  const [isRating, setIsRating] = useState(false);
  const [selectedRating, setSelectedRating] = useState(0);
  const backendUrl = import.meta.env.VITE_BACKEND_URL;
  const userId = localStorage.getItem("username");

  const rateMutation = useMutation({
    mutationFn: async (rating: number) => {
      const response = await fetch(`${backendUrl}/movies/rate_movie/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: Number(userId), rating: rating }),
      });

      if (!response.ok) {
        throw new Error("Error al calificar la película");
      }

      return response.json();
    },
    onSuccess: () => {
      toast.success("Película calificada con éxito");
      setIsRating(false);
      setSelectedRating(0);
    },
  });

  const handleRate = () => {
    if (selectedRating > 0) {
      rateMutation.mutate(selectedRating);
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
        <div className="flex items-center justify-between">
          <CardTitle className="line-clamp-1">{title}</CardTitle>
          <HoverCard>
            <HoverCardTrigger>
              <Info className="h-4 w-4 text-muted-foreground hover:text-primary cursor-help" />
            </HoverCardTrigger>
            <HoverCardContent>
              <span className="text-sm">{reason}</span>
            </HoverCardContent>
          </HoverCard>
        </div>
        <CardDescription className="space-y-1">
          <HoverCard>
            <HoverCardTrigger>
              <div className="flex items-center gap-2">
                <StarRating rating={avg_rating} />
              </div>           
            </HoverCardTrigger>
            <HoverCardContent>
              <span className="text-sm">Calificación promedio: {avg_rating.toFixed(2)}/5</span>
            </HoverCardContent>
          </HoverCard>
        </CardDescription>
      </CardHeader>
      <CardContent>
        {isRating ? (
          <div className="space-y-4">
            <div className="flex justify-center">
              <StarRating rating={selectedRating} onClick={setSelectedRating} />
            </div>
            <div className="flex gap-2 justify-end">
              <Button variant="outline" onClick={() => {
                setIsRating(false);
                setSelectedRating(0);
              }}>
                Cancelar
              </Button>
              <Button 
                onClick={handleRate}
                disabled={selectedRating === 0 || rateMutation.isPending}
              >
                {rateMutation.isPending ? "Calificando..." : "Confirmar"}
              </Button>
            </div>
          </div>
        ) : (
          <div className="flex gap-2 justify-end">
            <Button variant="outline">
              Ver más
            </Button>
            <Button onClick={() => setIsRating(true)}>
              Calificar
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
} 