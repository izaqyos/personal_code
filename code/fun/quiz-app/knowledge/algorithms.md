# Algorithms Used in This Project

## Scoring Algorithm

### Points Calculation

```javascript
function calculatePoints(isCorrect, timeRemaining) {
  if (!isCorrect) return 0;
  
  // Base points + time bonus
  const BASE_POINTS = 10;
  const TIME_BONUS_MULTIPLIER = 1;
  
  return BASE_POINTS + (timeRemaining * TIME_BONUS_MULTIPLIER);
}
```

### In This Project (api/game.js)

```javascript
if (isCorrect) {
  const points = Math.max(1, Math.floor(timeRemaining / 2));
  gameState.scores[participantId] = 
    (gameState.scores[participantId] || 0) + points;
}
```

**Scoring Formula:**
- Correct: `floor(timeRemaining / 2)` points (minimum 1)
- Incorrect: 0 points

**Example:**
- Answer correct with 16 seconds left: 8 points
- Answer correct with 3 seconds left: 1 point
- Answer incorrect: 0 points

### Time Complexity
- O(1) - constant time calculation

## Array Shuffling (Fisher-Yates)

### Purpose
Randomly order quiz questions or answer options.

### Algorithm

```javascript
function shuffle(array) {
  const result = [...array]; // Don't mutate original
  
  for (let i = result.length - 1; i > 0; i--) {
    // Pick random index from 0 to i
    const j = Math.floor(Math.random() * (i + 1));
    // Swap elements
    [result[i], result[j]] = [result[j], result[i]];
  }
  
  return result;
}
```

### Why Fisher-Yates?

**Correct:**
- Each permutation equally likely
- Unbiased randomness

**Simple approaches are WRONG:**
```javascript
// ❌ Bad: Biased toward original order
array.sort(() => Math.random() - 0.5);

// ❌ Bad: Not uniform distribution
array.sort(() => 0.5 - Math.random());
```

### In This Project

```javascript
// Select random subset for smoke test
const selectedQuestions = smokeTest
  ? [...allQuestions].sort(() => Math.random() - 0.5).slice(0, 3)
  : allQuestions;
```

Note: The simple `.sort(() => Math.random() - 0.5)` is used here because perfect uniformity isn't critical for selecting 3 random questions. For actual shuffling, use Fisher-Yates.

### Time Complexity
- O(n) - linear time, single pass through array

## Ranking Algorithm

### Purpose
Sort participants by score for leaderboard.

### Implementation

```javascript
function sortParticipantsByScore(participants, scores) {
  return [...participants].sort((a, b) => {
    const scoreA = scores[a.id] || 0;
    const scoreB = scores[b.id] || 0;
    return scoreB - scoreA; // Descending order
  });
}

function getTopParticipants(participants, scores, count) {
  const sorted = sortParticipantsByScore(participants, scores);
  return sorted.slice(0, count);
}
```

### Tie Breaking

Current: First one with that score wins (stable sort).

Enhanced version:
```javascript
function sortWithTiebreaker(participants, scores, responses) {
  return [...participants].sort((a, b) => {
    const scoreA = scores[a.id] || 0;
    const scoreB = scores[b.id] || 0;
    
    if (scoreA !== scoreB) {
      return scoreB - scoreA; // Higher score wins
    }
    
    // Tiebreaker: Faster total response time
    const timeA = getTotalTime(responses, a.id);
    const timeB = getTotalTime(responses, b.id);
    return timeB - timeA; // More time remaining = faster
  });
}
```

### Time Complexity
- O(n log n) - standard comparison sort

## Statistics Calculation

### Accuracy Calculation

```javascript
function calculateStats(responses, questions) {
  const totalQuestions = questions.length;
  const totalResponses = responses.length;
  const correctResponses = responses.filter(r => r.isCorrect).length;
  
  const accuracy = totalResponses > 0
    ? Math.round((correctResponses / totalResponses) * 100)
    : 0;
  
  return {
    totalQuestions,
    totalResponses,
    correctResponses,
    accuracy
  };
}
```

### Per-Question Analysis

```javascript
function analyzeQuestion(responses, questionIndex) {
  const questionResponses = responses.filter(
    r => r.questionIndex === questionIndex
  );
  
  const total = questionResponses.length;
  const correct = questionResponses.filter(r => r.isCorrect).length;
  
  // Answer distribution
  const distribution = questionResponses.reduce((acc, r) => {
    acc[r.answer] = (acc[r.answer] || 0) + 1;
    return acc;
  }, {});
  
  return {
    total,
    correct,
    accuracy: total > 0 ? (correct / total) * 100 : 0,
    distribution
  };
}
```

### Time Complexity
- O(n) - single pass through responses

## Duplicate Detection

### Purpose
Prevent submitting same answer twice.

### Implementation

```javascript
// Using Array.some() - O(n)
const alreadySubmitted = gameState.responses.some(
  r => r.participantId === participantId && 
       r.questionIndex === questionIndex
);

if (!alreadySubmitted) {
  gameState.responses.push(response);
}
```

### Optimized with Set - O(1)

```javascript
// Create lookup key
const key = `${participantId}_${questionIndex}`;

// Build Set on initialization
const submittedKeys = new Set(
  responses.map(r => `${r.participantId}_${r.questionIndex}`)
);

// Check - O(1)
if (!submittedKeys.has(key)) {
  // Process submission
}
```

### In This Project (useMemo optimization)

```javascript
const submittedParticipantIds = useMemo(() => {
  return new Set(
    responses
      .filter(r => r.questionIndex === questionNumber - 1)
      .map(r => r.participantId)
  );
}, [responses, questionNumber]);

// Usage - O(1) lookup
const hasSubmitted = submittedParticipantIds.has(participantId);
```

## Timer Logic

### Countdown Algorithm

```javascript
function useCountdown(initialSeconds) {
  const [timeRemaining, setTimeRemaining] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(true);

  useEffect(() => {
    if (!isRunning || timeRemaining <= 0) return;

    const timer = setTimeout(() => {
      setTimeRemaining(prev => prev - 1);
    }, 1000);

    return () => clearTimeout(timer);
  }, [timeRemaining, isRunning]);

  return { timeRemaining, isRunning, pause, resume };
}
```

### Why setTimeout over setInterval?

- **setInterval drift**: Intervals can accumulate delay
- **setTimeout chaining**: Each tick based on previous, more accurate
- **Cleanup**: Easier to manage with useEffect

### Accurate Timer (for precision-critical apps)

```javascript
function usePreciseCountdown(durationMs) {
  const [remaining, setRemaining] = useState(durationMs);
  const endTimeRef = useRef(null);

  useEffect(() => {
    endTimeRef.current = Date.now() + durationMs;
    
    const tick = () => {
      const now = Date.now();
      const remaining = Math.max(0, endTimeRef.current - now);
      setRemaining(remaining);
      
      if (remaining > 0) {
        requestAnimationFrame(tick);
      }
    };
    
    requestAnimationFrame(tick);
  }, [durationMs]);

  return Math.ceil(remaining / 1000);
}
```

## Summary

| Algorithm | Purpose | Complexity |
|-----------|---------|------------|
| Score Calculation | Points per answer | O(1) |
| Fisher-Yates Shuffle | Randomize array | O(n) |
| Comparison Sort | Leaderboard ranking | O(n log n) |
| Statistics | Accuracy, counts | O(n) |
| Duplicate Detection | Prevent re-submission | O(1) with Set |
| Countdown Timer | Question timer | O(1) per tick |
