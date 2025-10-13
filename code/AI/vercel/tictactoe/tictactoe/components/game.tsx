"use client"

import { useState } from "react"
import Board from "./board"

export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)])
  const [currentMove, setCurrentMove] = useState(0)
  const xIsNext = currentMove % 2 === 0
  const currentSquares = history[currentMove]

  function handlePlay(nextSquares: (string | null)[]) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares]
    setHistory(nextHistory)
    setCurrentMove(nextHistory.length - 1)
  }

  function jumpTo(nextMove: number) {
    setCurrentMove(nextMove)
  }

  const moves = history.map((squares, move) => {
    let description
    if (move > 0) {
      description = `Go to move #${move}`
    } else {
      description = "Go to game start"
    }

    if (move === currentMove) {
      return (
        <li key={move} className="my-1">
          <span className="font-medium">You are at move #{move}</span>
        </li>
      )
    }

    return (
      <li key={move} className="my-1">
        <button
          onClick={() => jumpTo(move)}
          className="px-3 py-1 bg-gray-200 dark:bg-gray-700 rounded hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-sm"
        >
          {description}
        </button>
      </li>
    )
  })

  return (
    <div className="flex flex-col md:flex-row gap-8 w-full max-w-3xl">
      <div className="flex-1">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="flex-1">
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">Game History</h2>
          <ol className="list-decimal list-inside">{moves}</ol>
        </div>
      </div>
    </div>
  )
}

