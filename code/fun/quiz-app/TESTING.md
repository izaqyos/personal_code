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

## Resources

- [Vitest Docs](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Docs](https://playwright.dev/)

