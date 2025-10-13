"use client"

interface SquareProps {
  value: string | null
  onSquareClick: () => void
  isWinningSquare?: boolean
}

export default function Square({ value, onSquareClick, isWinningSquare = false }: SquareProps) {
  const getValueColor = () => {
    if (!value) return ""
    return value === "X" ? "text-blue-600 dark:text-blue-400" : "text-red-600 dark:text-red-400"
  }

  return (
    <button
      className={`w-20 h-20 border border-gray-400 dark:border-gray-600 text-4xl font-bold flex items-center justify-center ${
        isWinningSquare ? "bg-green-200 dark:bg-green-900" : "bg-white dark:bg-gray-800"
      } ${getValueColor()}`}
      onClick={onSquareClick}
    >
      {value}
    </button>
  )
}

