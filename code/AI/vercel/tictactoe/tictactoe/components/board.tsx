"use client"
import Square from "./square"

interface BoardProps {
  xIsNext: boolean
  squares: (string | null)[]
  onPlay: (squares: (string | null)[]) => void
}

export default function Board({ xIsNext, squares, onPlay }: BoardProps) {
  function handleClick(i: number) {
    if (calculateWinner(squares) || squares[i]) {
      return
    }
    const nextSquares = squares.slice()
    if (xIsNext) {
      nextSquares[i] = "X"
    } else {
      nextSquares[i] = "O"
    }
    onPlay(nextSquares)
  }

  const winner = calculateWinner(squares)
  let status
  if (winner) {
    status = `Winner: ${winner}`
  } else if (squares.every((square) => square)) {
    status = "Draw: Game Over"
  } else {
    status = `Next player: ${xIsNext ? "X" : "O"}`
  }

  // Get winning line if there is a winner
  const winningLine = getWinningLine(squares)

  // Render the board using loops
  const renderBoard = () => {
    const board = []
    for (let row = 0; row < 3; row++) {
      const boardRow = []
      for (let col = 0; col < 3; col++) {
        const index = row * 3 + col
        const isWinningSquare = winningLine && winningLine.includes(index)
        boardRow.push(
          <Square
            key={index}
            value={squares[index]}
            onSquareClick={() => handleClick(index)}
            isWinningSquare={isWinningSquare}
          />,
        )
      }
      board.push(
        <div key={row} className="flex">
          {boardRow}
        </div>,
      )
    }
    return board
  }

  return (
    <div className="flex flex-col items-center">
      <div className="mb-4 text-xl font-bold text-gray-800 dark:text-gray-100">{status}</div>
      <div className="mb-6">{renderBoard()}</div>
      <button
        onClick={() => onPlay(Array(9).fill(null))}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
      >
        Reset Game
      </button>
    </div>
  )
}

function calculateWinner(squares: (string | null)[]) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ]
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i]
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a]
    }
  }
  return null
}

function getWinningLine(squares: (string | null)[]) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ]
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i]
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return lines[i]
    }
  }
  return null
}

