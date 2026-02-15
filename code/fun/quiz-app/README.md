# 🎮 Programming Languages Quiz App

A React-based interactive quiz application for team building and fun! Supports multiple participants, real-time scoring, and mobile-friendly interface.

## Features

- ✅ **Real multiplayer** - each player on their own device
- ✅ Multiple quiz selection (Dogs Hebrew, Programming Languages, Web Development)
- ✅ Host mode - one person controls game flow
- ✅ Real-time sync via Vercel KV
- ✅ Configurable timer per quiz (default 15-20 seconds)
- ✅ Individual answer submission per participant
- ✅ Real-time score tracking and leaderboard
- ✅ Results screen with winner and top 3 players
- ✅ Download results as JSON file
- ✅ Mobile-responsive design
- ✅ Hebrew language support
- ✅ Accessible UI (ARIA labels, keyboard navigation)

## Quick Start

### Prerequisites

- Node.js 16+ and npm/yarn/pnpm

### Local Development

```bash
npm install
npm run dev
```

The app will be available at `http://localhost:5173`

### Deploy to Vercel (Multiplayer)

For real multiplayer (each person on their own device):

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# Follow the prompts:
# - Set up and deploy? yes
# - Which scope? (select your account)
# - Link to existing project? no
# - Project name? quiz-app (or your preferred name)
# - Code directory? ./
# - Modify settings? no
# - Change additional settings? no

# 3. Create KV Database (for persistent game state)
#    - Go to vercel.com → Your Project → Storage
#    - Click "Create Database" → Select "KV"
#    - Name it "quiz-game" → Connect to Project

# 4. Redeploy with KV connected
vercel --prod
```

**What to expect after deployment:**
- ✅ Vercel auto-detects Vite framework and builds automatically
- ✅ Creates `.vercel` folder (added to `.gitignore`)
- ✅ Provides 2 URLs:
  - **Aliased URL** (permanent): `https://quiz-app-xxxxx.vercel.app`
  - **Production URL** (deployment-specific): `https://quiz-xxxxx-your-projects.vercel.app`
- ✅ Dashboard link to manage settings and view deployments

**To update your app:**
```bash
vercel --prod
```

Share the Vercel URL with your family/friends - each person joins on their own phone!

### Build for Production

```bash
npm run build
npm run preview
```

## How to Use

1. **Start the server** (see instructions below)
2. **Participants join** by entering their name
3. **Host views waiting room** and clicks "Start Quiz" when ready
4. **Each question** has a 15-second timer
5. **Participants submit answers** individually
6. **View results** after all questions are answered
7. **Download results** as JSON file

## Serving the App for Mobile Access

### Option 1: Local Network (Recommended for Same WiFi Team)

The app is configured to be accessible on your local network:

1. **Find your computer's IP address:**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # macOS specific
   ipconfig getifaddr en0
   
   # Linux
   hostname -I
   
   # Windows
   ipconfig
   ```

2. **Start the dev server:**
   ```bash
   npm run dev
   ```

3. **Share the URL** with your team:
   ```
   http://YOUR_IP_ADDRESS:3000
   ```
   Example: `http://192.168.1.100:3000`

4. **Participants open** the URL on their mobile browsers

**Note:** Make sure all devices are on the same WiFi network!

**Pros:** Fast, no external dependencies, free  
**Cons:** Only works on same network

---

### Option 2: ngrok (Best for Remote Teams)

Perfect for teams not on the same network:

1. **Install ngrok:**
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/download
   ```

2. **Start the dev server:**
   ```bash
   npm run dev
   ```

3. **In another terminal, run ngrok:**
   ```bash
   ngrok http 3000
   ```

4. **Share the ngrok URL** (e.g., `https://abc123.ngrok.io`) with your team

**Free tier:** 1 tunnel, 40 connections/min  
**Pros:** Works anywhere, HTTPS, easy setup  
**Cons:** Free tier has limitations, URL changes each time

**For persistent URL (paid):**
```bash
ngrok http 3000 --domain=your-custom-domain.ngrok.io
```

---

### Option 3: Vercel (Recommended for Multiplayer)

Best for real multiplayer - each player on their own device:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Set up Vercel KV (for game state persistence):**
   - Go to [vercel.com](https://vercel.com) → Your Project → **Storage** tab
   - Click **Create Database** → Select **KV**
   - Name it `quiz-game` → Click **Connect to Project**

4. **Redeploy with KV:**
   ```bash
   vercel --prod
   ```

**How multiplayer works:**
- One person joins as **Host** (controls game flow)
- Others join as **Participants** (answer on their own phones)
- Game state syncs via polling every second

**Pros:** Free tier (30K requests/month), real multiplayer, fast CDN, HTTPS
**Cons:** Requires account

**Custom domain setup:**
- Add domain in Vercel dashboard
- Update DNS records
- Automatic SSL certificate

---

### Option 4: Netlify (Alternative Free Hosting)

Similar to Vercel:

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Build and deploy:**
   ```bash
   npm run build
   netlify deploy --prod --dir=dist
   ```

**Pros:** Free tier, good performance, easy setup  
**Cons:** Requires account

---

### Option 5: Production Build + Simple Server

For local network without dev server:

1. **Build the app:**
   ```bash
   npm run build
   ```

2. **Serve the dist folder:**

   **Using Python:**
   ```bash
   cd dist
   python3 -m http.server 3000 --bind 0.0.0.0
   ```

   **Using Node.js (http-server):**
   ```bash
   npm install -g http-server
   cd dist
   http-server -p 3000 --host 0.0.0.0
   ```

   **Using Node.js (serve):**
   ```bash
   npm install -g serve
   serve -s dist -l 3000 --hostname 0.0.0.0
   ```

3. **Access via:** `http://YOUR_IP_ADDRESS:3000`

**Pros:** Production-ready, faster than dev server  
**Cons:** Need to rebuild after changes

---

### Option 6: GitHub Pages (For Public Repos)

Free hosting via GitHub:

1. **Install gh-pages:**
   ```bash
   npm install --save-dev gh-pages
   ```

2. **Add to package.json:**
   ```json
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d dist"
   }
   ```

3. **Deploy:**
   ```bash
   npm run deploy
   ```

4. **Enable GitHub Pages** in repo settings → Pages → Source: `gh-pages` branch

**URL format:** `https://USERNAME.github.io/REPO_NAME`

**Pros:** Free, version controlled  
**Cons:** Public repo required, slower updates

---

### Option 7: Railway / Render / Fly.io

Other modern hosting platforms:

**Railway:**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**Render:**
- Connect GitHub repo
- Auto-deploys on push
- Free tier available

**Fly.io:**
```bash
flyctl launch
flyctl deploy
```

---

## Quick Comparison

| Method | Setup Time | Cost | Best For |
|--------|-----------|------|----------|
| **Local Network** | 1 min | Free | Same WiFi team |
| **ngrok** | 2 min | Free/Paid | Remote teams, testing |
| **Vercel** | 5 min | Free | Permanent deployment |
| **Netlify** | 5 min | Free | Permanent deployment |
| **Production Build** | 3 min | Free | Local network, production |
| **GitHub Pages** | 10 min | Free | Public projects |
| **Railway/Render** | 10 min | Free/Paid | Full-stack apps |

## Data Storage

- **LocalStorage:** All participant data, scores, and responses are saved in browser localStorage
- **JSON Export:** Results can be downloaded as a JSON file from the results screen
- **File Location:** Results are saved to `quiz-results-YYYY-MM-DD.json`

## Quiz Data

Questions are stored in JSON files in `src/data/`:
- `src/data/questions.json` - Programming Languages quiz
- `src/data/web-development.json` - Web Development quiz

Each quiz JSON file includes:
- `id` - Unique quiz identifier
- `title` - Quiz display name
- `description` - Brief quiz description
- `timerSeconds` - Time per question (default: 15)
- `questions` - Array of question objects

To add a new quiz:
1. Create a new JSON file in `src/data/`
2. Export it in `src/data/index.js`
3. The quiz will automatically appear in the quiz selector

## Customization

- **Timer duration:** Set `timerSeconds` in the quiz JSON file
- **Styling:** Edit CSS files in `src/components/` and `src/App.css`
- **Questions:** Edit quiz JSON files in `src/data/`
- **Add new quiz:** Create new JSON file in `src/data/` and export in `index.js`

## Troubleshooting

**Can't access from mobile:**
- Ensure devices are on the same WiFi network
- Check firewall settings (port 3000)
- Try using your computer's IP address instead of `localhost`

**Port already in use:**
- Change port in `vite.config.js` or use `npm run dev -- --port 3001`

**Data not persisting:**
- Check browser localStorage is enabled
- Results are also saved to JSON file on results screen

## Testing

This project includes comprehensive test coverage. See [TESTING.md](./TESTING.md) for detailed testing guide.

### Test Types

- **Unit Tests:** Test utility functions and logic (`src/utils/__tests__/`)
- **Component Tests:** Test React components (`src/components/__tests__/`)
- **E2E Tests:** Test complete user flows (`tests/e2e/`)

### Running Tests

**Unit & Component Tests (Vitest):**
```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

**E2E Tests (Playwright):**
```bash
# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests in specific browser
npx playwright test --project=chromium
```

**Run All Tests:**
```bash
npm run test:all
```

### Test Structure

```
quiz-app/
├── src/
│   ├── utils/
│   │   └── __tests__/
│   │       └── quizUtils.test.js      # Unit tests
│   └── components/
│       └── __tests__/
│           ├── JoinScreen.test.jsx     # Component tests
│           ├── WaitingRoom.test.jsx
│           ├── QuizScreen.test.jsx
│           └── ResultsScreen.test.jsx
└── tests/
    └── e2e/
        └── quiz-flow.spec.js           # E2E tests
```

### Writing New Tests

**Unit Test Example:**
```javascript
import { describe, it, expect } from 'vitest'
import { calculatePoints } from '../quizUtils'

describe('calculatePoints', () => {
  it('should return 0 for incorrect answers', () => {
    expect(calculatePoints(15, false)).toBe(0)
  })
})
```

**Component Test Example:**
```javascript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import MyComponent from '../MyComponent'

test('should handle user interaction', async () => {
  const user = userEvent.setup()
  render(<MyComponent />)
  await user.click(screen.getByRole('button'))
  expect(screen.getByText('Clicked')).toBeInTheDocument()
})
```

**E2E Test Example:**
```javascript
import { test, expect } from '@playwright/test'

test('should complete quiz flow', async ({ page }) => {
  await page.goto('/')
  await page.fill('[placeholder="Your name"]', 'Test User')
  await page.click('button:has-text("Join Quiz")')
  // ... more steps
})
```

### Test Coverage Goals

- **Unit Tests:** >90% coverage for utility functions
- **Component Tests:** All major user interactions
- **E2E Tests:** Complete user flows (join → quiz → results)

### Debugging Tests

**Vitest:**
```bash
# Run specific test file
npm test quizUtils.test.js

# Run tests matching pattern
npm test -- -t "calculatePoints"

# Debug mode
npm test -- --inspect-brk
```

**Playwright:**
```bash
# Run with headed browser
npx playwright test --headed

# Debug mode
npx playwright test --debug

# Show browser
npx playwright test --ui
```

### CI/CD Integration

Tests can be integrated into CI/CD pipelines:

**GitHub Actions Example:**
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm test
      - run: npm run test:e2e
```

## Tech Stack

- **Frontend:** React 18, Vite
- **Styling:** CSS3 (no external UI libraries)
- **Testing:** Vitest, React Testing Library, Playwright
- **Build:** Vite

## License

MIT

