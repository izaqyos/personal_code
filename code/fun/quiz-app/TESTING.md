# 🧪 Testing Guide

Comprehensive testing guide for the Programming Languages Quiz App.

## Quick Start

```bash
# Install dependencies (includes test dependencies)
npm install

# Run all tests
npm run test:all

# Run unit/component tests only
npm test

# Run E2E tests only
npm run test:e2e
```

## Test Structure

```
quiz-app/
├── src/
│   ├── utils/
│   │   ├── quizUtils.js
│   │   └── __tests__/
│   │       └── quizUtils.test.js          # Unit tests
│   └── components/
│       ├── JoinScreen.jsx
│       ├── WaitingRoom.jsx
│       ├── QuizScreen.jsx
│       ├── ResultsScreen.jsx
│       └── __tests__/
│           ├── JoinScreen.test.jsx        # Component tests
│           ├── WaitingRoom.test.jsx
│           ├── QuizScreen.test.jsx
│           └── ResultsScreen.test.jsx
├── tests/
│   └── e2e/
│       └── quiz-flow.spec.js              # E2E tests
└── src/test/
    └── setup.js                            # Test configuration
```

## Unit Tests

**Location:** `src/utils/__tests__/`

**Purpose:** Test pure functions and utility logic

**Example:**
```javascript
import { calculatePoints } from '../quizUtils'

describe('calculatePoints', () => {
  it('should return 0 for incorrect answers', () => {
    expect(calculatePoints(15, false)).toBe(0)
  })
  
  it('should calculate points based on time', () => {
    expect(calculatePoints(15, true)).toBe(7)
  })
})
```

**Run unit tests:**
```bash
npm test quizUtils.test.js
```

## Component Tests

**Location:** `src/components/__tests__/`

**Purpose:** Test React component behavior and user interactions

**Testing Library:** React Testing Library + Vitest

**Example:**
```javascript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import JoinScreen from '../JoinScreen'

test('should call onJoin when form submitted', async () => {
  const mockOnJoin = vi.fn()
  const user = userEvent.setup()
  
  render(<JoinScreen onJoin={mockOnJoin} />)
  
  await user.type(screen.getByPlaceholderText(/name/i), 'Alice')
  await user.click(screen.getByRole('button', { name: /join/i }))
  
  expect(mockOnJoin).toHaveBeenCalledWith('Alice')
})
```

**Run component tests:**
```bash
npm test JoinScreen.test.jsx
```

**Watch mode:**
```bash
npm test -- --watch
```

## E2E Tests

**Location:** `tests/e2e/`

**Purpose:** Test complete user flows end-to-end

**Testing Framework:** Playwright

**Example:**
```javascript
import { test, expect } from '@playwright/test'

test('complete quiz flow', async ({ page }) => {
  await page.goto('/')
  await page.fill('[placeholder="Your name"]', 'Test User')
  await page.click('button:has-text("Join Quiz")')
  // ... continue flow
})
```

**Run E2E tests:**
```bash
# Run all E2E tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui

# Run specific browser
npx playwright test --project=chromium

# Run headed (see browser)
npx playwright test --headed

# Debug mode
npx playwright test --debug
```

## Test Commands Reference

| Command | Description |
|---------|-------------|
| `npm test` | Run unit + component tests |
| `npm test -- --watch` | Watch mode for unit/component tests |
| `npm test -- --ui` | Visual test UI (Vitest) |
| `npm test -- --coverage` | Generate coverage report |
| `npm run test:e2e` | Run E2E tests |
| `npm run test:e2e:ui` | Playwright UI mode |
| `npm run test:all` | Run all tests |

## Coverage

**View coverage:**
```bash
npm run test:coverage
```

Coverage reports are generated in:
- `coverage/` directory
- HTML report: `coverage/index.html`

**Coverage goals:**
- Unit tests: >90%
- Component tests: All major interactions
- E2E tests: Critical user flows

## Writing Tests

### Unit Test Template

```javascript
import { describe, it, expect } from 'vitest'
import { myFunction } from '../myModule'

describe('myFunction', () => {
  it('should handle case 1', () => {
    expect(myFunction(input)).toBe(expected)
  })
  
  it('should handle edge case', () => {
    expect(myFunction(null)).toBe(null)
  })
})
```

### Component Test Template

```javascript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import MyComponent from '../MyComponent'

describe('MyComponent', () => {
  it('should render correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
  
  it('should handle user interaction', async () => {
    const user = userEvent.setup()
    render(<MyComponent />)
    
    await user.click(screen.getByRole('button'))
    expect(screen.getByText('Clicked')).toBeInTheDocument()
  })
})
```

### E2E Test Template

```javascript
import { test, expect } from '@playwright/test'

test.describe('Feature Name', () => {
  test('should complete user flow', async ({ page }) => {
    await page.goto('/')
    
    // Step 1
    await page.fill('selector', 'value')
    
    // Step 2
    await page.click('button')
    
    // Assert
    await expect(page.getByText('Success')).toBeVisible()
  })
})
```

## Best Practices

1. **Test Behavior, Not Implementation**
   - ✅ Test what user sees/does
   - ❌ Don't test internal state directly

2. **Use Semantic Queries**
   - ✅ `getByRole`, `getByLabelText`
   - ❌ `getByTestId` (unless necessary)

3. **Keep Tests Isolated**
   - Each test should be independent
   - Clean up after each test

4. **Test User Flows**
   - Test complete workflows, not just individual functions

5. **Mock External Dependencies**
   - Mock API calls, timers, etc.

## Debugging Tests

### Vitest Debugging

```bash
# Run specific test
npm test -- -t "test name"

# Run tests in file
npm test -- filename.test.js

# Debug mode
npm test -- --inspect-brk
```

### Playwright Debugging

```bash
# Debug mode (step through)
npx playwright test --debug

# Show browser
npx playwright test --headed

# Slow motion
npx playwright test --slow-mo=1000

# Pause on failure
npx playwright test --pause
```

## CI/CD Integration

Tests run automatically on:
- Push to main/master
- Pull requests

See `.github/workflows/test.yml` for CI configuration.

**Local CI simulation:**
```bash
# Run tests like CI
CI=true npm run test:all
```

## Troubleshooting

**Tests failing locally but pass in CI:**
- Clear node_modules and reinstall
- Check Node.js version matches CI
- Clear test cache: `npm test -- --no-cache`

**Playwright browsers not installing:**
```bash
npx playwright install
```

**Coverage not generating:**
- Ensure `--coverage` flag is used
- Check `vitest.config.js` coverage settings

**E2E tests timing out:**
- Increase timeout in `playwright.config.js`
- Check if dev server is running
- Verify selectors are correct

## Manual Testing Instructions

### Local Development Testing

#### 1. Start the Dev Server

```bash
cd /Users/yosii/work/git/personal_code/code/fun/quiz-app
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.x.x:3000/
```

**Console should show:**
```
[useGameSync] 🏠 Running in LOCAL DEV mode (using localStorage)
```

#### 2. Test Multiplayer Locally

Open **two browser tabs** (or windows):

**Tab 1 - Host:**
1. Go to `http://localhost:3000`
2. Click "Join as Host"
3. You should see "Waiting Room" with your name as Host

**Tab 2 - Player:**
1. Go to `http://localhost:3000`
2. Enter name (e.g., "Player 1")
3. Click "Join Quiz"
4. You should see "Waiting Room" with both participants

**Back to Tab 1 (Host):**
1. Click "Start Quiz"
2. Both tabs should show the quiz question

**Test answering:**
- Select an answer in each tab
- Click "Submit Answer"
- Verify both tabs update when all players submit

#### 3. Check Browser Console

Look for logs like:
```
[useGameSync] Action: JOIN
[useGameSync] ✅ Action processed locally
[useGameSync] 🔄 Detected state change from another tab
```

### Deployment Testing (Vercel)

#### Deploy to Vercel

**Option A: Via Git (Recommended)**

```bash
# Commit all changes
git add .
git commit -m "feat: add multiplayer support with local dev mode"

# Push to GitHub
git push origin main
```

Vercel will auto-deploy if connected to your GitHub repo.

**Option B: Via Vercel CLI**

```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Deploy
cd /Users/yosii/work/git/personal_code/code/fun/quiz-app
vercel

# Follow prompts:
# - Link to existing project or create new
# - Select settings (use defaults)
```

#### After Deployment

1. **Set up Vercel KV** (required for multiplayer):
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Select your project
   - Go to **Storage** → **Create Database** → **KV**
   - Name it `quiz-game-state`
   - Click **Connect to Project**

2. **Redeploy** (to pick up KV env vars):
   ```bash
   vercel --prod
   ```
   Or push an empty commit:
   ```bash
   git commit --allow-empty -m "chore: redeploy with KV"
   git push
   ```

3. **Test on Vercel**:
   - Open your Vercel URL (e.g., `https://your-app.vercel.app`)
   - Test with multiple devices/browsers
   - Check console for: `[useGameSync] 🌐 Running in API mode`

#### Testing Checklist

- [ ] Join screen loads correctly
- [ ] Can join as regular participant
- [ ] Can join as host
- [ ] Waiting room shows all participants
- [ ] Host can start quiz
- [ ] Timer counts down
- [ ] Can select and submit answers
- [ ] Leaderboard updates correctly
- [ ] Results screen shows final scores
- [ ] Can reset and play again
- [ ] Multiple tabs/devices sync properly
- [ ] Mobile responsive design works

## Resources

- [Vitest Docs](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Docs](https://playwright.dev/)
- [Vercel Deployment Guide](./docs/VERCEL_DEPLOYMENT.md)

