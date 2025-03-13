import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Star, StarHalf } from "lucide-react"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card"
import { Button } from "@/components/ui/button"

interface MovieCardProps {
  id: number
  estimation: number
  title: string
  image_url: string
  avg_rating: number
}

function StarRating({ rating }: { rating: number }) {
  const totalStars = 5;
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 >= 0.5;
  const emptyStars = totalStars - fullStars - (hasHalfStar ? 1 : 0);

  return (
    <div className="flex">
      {/* Full stars */}
      {Array.from({ length: fullStars }).map((_, i) => (
        <Star key={`full-${i}`} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
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
        <Star key={`empty-${i}`} className="h-4 w-4 text-yellow-400/30" />
      ))}
    </div>
  );
}

export function MovieCard({ estimation, title, image_url, avg_rating }: MovieCardProps) {
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
        <CardDescription className="space-y-1">
          <HoverCard>
            <HoverCardTrigger>
            <div className="flex items-center gap-2">
              <StarRating rating={avg_rating} />
            </div>           
            </HoverCardTrigger>
            <HoverCardContent>
              <span className="text-sm">Calificación promedio: {avg_rating}/5</span>
            </HoverCardContent>
          </HoverCard>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex gap-2 justify-end">
          <Button variant="outline">
            Ver más
          </Button>
          <Button>
            Calificar
          </Button>
        </div>
      </CardContent>
    </Card>
  )
} 