import { Star, StarHalf } from "lucide-react"

interface StarRatingProps {
  rating: number
  onClick?: (rating: number) => void
  size?: "sm" | "md" | "lg"
}

export function StarRating({ rating, onClick, size = "sm" }: StarRatingProps) {
  const totalStars = 5
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 >= 0.5
  const emptyStars = totalStars - fullStars - (hasHalfStar ? 1 : 0)
  
  const sizeClass = {
    sm: "h-4 w-4",
    md: "h-5 w-5",
    lg: "h-6 w-6"
  }
  
  const starSize = sizeClass[size]

  return (
    <div className="flex">
      {/* Full stars */}
      {Array.from({ length: fullStars }).map((_, i) => (
        <Star 
          key={`full-${i}`} 
          className={`${starSize} fill-yellow-400 text-yellow-400 ${onClick ? 'cursor-pointer' : ''}`}
          onClick={() => onClick?.(i + 1)}
        />
      ))}
      
      {/* Half star */}
      {hasHalfStar && (
        <div className="relative">
          <Star className={`${starSize} text-yellow-400/30`} />
          <StarHalf className={`absolute left-0 top-0 ${starSize} fill-yellow-400 text-yellow-400`} />
        </div>
      )}
      
      {/* Empty stars */}
      {Array.from({ length: emptyStars }).map((_, i) => (
        <Star 
          key={`empty-${i}`} 
          className={`${starSize} text-yellow-400/30 ${onClick ? 'cursor-pointer' : ''}`}
          onClick={() => onClick?.(fullStars + (hasHalfStar ? 1 : 0) + i + 1)}
        />
      ))}
    </div>
  )
} 