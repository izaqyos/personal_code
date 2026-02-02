# React Testing Patterns

## Testing Philosophy

### Testing Trophy (Kent C. Dodds)
```
        ┌──────────┐
        │   E2E    │  → User flows, critical paths
        ├──────────┤
        │Integration│ → Component interactions
        ├──────────┤
        │  Unit    │  → Pure functions, utilities
        └──────────┘
```

**Focus on Integration Tests**: Test components as users interact with them.

## Tools in This Project

| Tool | Purpose |
|------|---------|
| Vitest | Test runner (Jest-compatible, Vite-native) |
| React Testing Library | DOM-based component testing |
| user-event | Simulate real user interactions |
| jsdom | Browser environment in Node.js |
| Playwright | End-to-end browser testing |

## Testing Library Principles

1. **Query by accessible roles** (not implementation details)
2. **Test behavior, not implementation**
3. **Write tests that resemble how users use the app**

## Query Priority

```jsx
// Preferred (most accessible)
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText(/email/i)
screen.getByPlaceholderText(/search/i)
screen.getByText(/welcome/i)

// Less preferred
screen.getByTestId('submit-button')  // Only when others don't work
```

### Query Types

| Prefix | Returns | When Not Found |
|--------|---------|----------------|
| `getBy` | Element | Throws error |
| `queryBy` | Element or `null` | Returns `null` |
| `findBy` | Promise<Element> | Throws (async) |
| `getAllBy` | Array | Throws error |
| `queryAllBy` | Array | Empty array |
| `findAllBy` | Promise<Array> | Throws (async) |

## Common Patterns

### Basic Component Test
```jsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('should render title', () => {
    render(<MyComponent title="Hello" />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })

  it('should call onClick when button clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    
    render(<MyComponent onClick={handleClick} />)
    
    await user.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### Testing Forms
```jsx
it('should submit form with entered data', async () => {
  const user = userEvent.setup()
  const handleSubmit = vi.fn()
  
  render(<LoginForm onSubmit={handleSubmit} />)
  
  // Fill form
  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.type(screen.getByLabelText(/password/i), 'secret123')
  
  // Submit
  await user.click(screen.getByRole('button', { name: /login/i }))
  
  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'secret123'
  })
})

it('should show validation error for empty email', async () => {
  const user = userEvent.setup()
  
  render(<LoginForm onSubmit={vi.fn()} />)
  
  await user.click(screen.getByRole('button', { name: /login/i }))
  
  expect(screen.getByRole('alert')).toHaveTextContent(/email is required/i)
})
```

### Testing Async Operations
```jsx
it('should load and display data', async () => {
  // Mock fetch
  vi.spyOn(global, 'fetch').mockResolvedValue({
    ok: true,
    json: () => Promise.resolve([{ id: 1, name: 'Item 1' }])
  })
  
  render(<DataList />)
  
  // Wait for loading to complete
  expect(screen.getByText(/loading/i)).toBeInTheDocument()
  
  // findBy is async - waits for element
  expect(await screen.findByText('Item 1')).toBeInTheDocument()
  
  // Cleanup
  global.fetch.mockRestore()
})
```

### Testing with Timers
```jsx
import { vi, beforeEach, afterEach } from 'vitest'
import { act } from '@testing-library/react'

describe('Timer Component', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('should countdown from 10', async () => {
    render(<Timer seconds={10} />)
    
    expect(screen.getByText('10s')).toBeInTheDocument()
    
    await act(async () => {
      vi.advanceTimersByTime(1000)
    })
    
    expect(screen.getByText('9s')).toBeInTheDocument()
  })
})
```

### Testing Error States
```jsx
it('should display error message on API failure', async () => {
  vi.spyOn(global, 'fetch').mockRejectedValue(new Error('Network error'))
  
  render(<DataFetcher />)
  
  expect(await screen.findByText(/network error/i)).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument()
})
```

### Testing Context Providers
```jsx
// Custom render helper
function renderWithProviders(ui, { theme = 'light', user = null } = {}) {
  return render(
    <ThemeContext.Provider value={theme}>
      <UserContext.Provider value={user}>
        {ui}
      </UserContext.Provider>
    </ThemeContext.Provider>
  )
}

it('should display username from context', () => {
  renderWithProviders(<Header />, { user: { name: 'Alice' } })
  expect(screen.getByText('Welcome, Alice')).toBeInTheDocument()
})
```

## Mocking in Vitest

### Mock Functions
```jsx
const mockFn = vi.fn()
mockFn('arg1', 'arg2')

expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenCalledTimes(1)

// Return value
const mockFn = vi.fn().mockReturnValue(42)
// Async return
const mockFn = vi.fn().mockResolvedValue({ data: 'result' })
```

### Mock Modules
```jsx
// Mock entire module
vi.mock('./api', () => ({
  fetchData: vi.fn().mockResolvedValue([])
}))

// Mock specific export
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils')
  return {
    ...actual,
    formatDate: vi.fn().mockReturnValue('2024-01-01')
  }
})
```

### Spy on Methods
```jsx
const spy = vi.spyOn(console, 'error')
// ... do something
expect(spy).toHaveBeenCalled()
spy.mockRestore()  // Restore original
```

## Snapshot Testing

```jsx
it('should match snapshot', () => {
  const { asFragment } = render(<StaticComponent />)
  expect(asFragment()).toMatchSnapshot()
})
```

**When to Use:**
- Large static output
- Visual regression detection
- NOT for dynamic content

## Testing Best Practices

### ✅ DO

1. **Test user behavior**
   ```jsx
   // Good: Test what user sees
   expect(screen.getByText('Welcome back!')).toBeInTheDocument()
   ```

2. **Use accessible queries**
   ```jsx
   // Good: Query by role
   screen.getByRole('button', { name: /submit/i })
   ```

3. **Assert on visible changes**
   ```jsx
   // Good: Assert on result
   expect(screen.getByText(/success/i)).toBeInTheDocument()
   ```

### ❌ DON'T

1. **Test implementation details**
   ```jsx
   // Bad: Testing internal state
   expect(component.state.isLoading).toBe(false)
   ```

2. **Use test IDs unnecessarily**
   ```jsx
   // Bad when role exists
   screen.getByTestId('submit-btn')
   ```

3. **Test library code**
   ```jsx
   // Bad: Testing React itself
   expect(useState).toBeDefined()
   ```

## Coverage

Run coverage report:
```bash
npm run test:coverage
```

Target coverage:
- **Statements**: 80%+
- **Branches**: 75%+ (if/else, ternary)
- **Functions**: 80%+
- **Lines**: 80%+

## Resources

- [Testing Library Docs](https://testing-library.com/docs/)
- [Vitest Docs](https://vitest.dev/)
- [Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
