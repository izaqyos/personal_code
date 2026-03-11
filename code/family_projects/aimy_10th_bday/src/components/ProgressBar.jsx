import './ProgressBar.css'

export default function ProgressBar({ current, total }) {
  return (
    <div className="progress-bar" data-testid="progress-bar">
      {Array.from({ length: total }, (_, i) => (
        <div
          key={i}
          className={`progress-dot ${i < current ? 'completed' : ''} ${i === current ? 'active' : ''}`}
          data-testid={`progress-dot-${i}`}
        />
      ))}
    </div>
  )
}
