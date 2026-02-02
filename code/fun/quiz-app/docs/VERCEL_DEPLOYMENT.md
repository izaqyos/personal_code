# Vercel Deployment Guide

This guide covers deploying the Quiz App to Vercel with full multiplayer support.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Vercel KV Database**: Required for multiplayer state sync

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Vercel Platform                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐     ┌──────────────────┐     ┌─────────────┐  │
│  │   Vercel Edge    │     │  Serverless API  │     │  Vercel KV  │  │
│  │   (Static CDN)   │────►│  /api/game.js    │◄───►│  (Redis)    │  │
│  │                  │     │                  │     │             │  │
│  │  - index.html    │     │  - GET state     │     │  - Game     │  │
│  │  - JS bundles    │     │  - POST actions  │     │    state    │  │
│  │  - CSS assets    │     │  - CORS enabled  │     │  - Scores   │  │
│  └──────────────────┘     └──────────────────┘     └─────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              ▲                ▲
                              │                │
              ┌───────────────┴────────────────┴───────────────┐
              │                  Browser Clients                │
              │                                                 │
              │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
              │  │  Host    │  │ Player 1 │  │ Player 2 │      │
              │  │  (Tab 1) │  │  (Tab 2) │  │ (Phone)  │      │
              │  └──────────┘  └──────────┘  └──────────┘      │
              └─────────────────────────────────────────────────┘
```

## Step-by-Step Deployment

### 1. Connect GitHub Repository

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Vercel auto-detects Vite framework
4. Click "Deploy" (initial deploy without KV will show connection error)

### 2. Set Up Vercel KV

**Important**: Vercel KV is required for multiplayer functionality.

1. Go to your project on Vercel dashboard
2. Navigate to **Storage** → **Create Database**
3. Select **KV (Redis)**
4. Name it (e.g., `quiz-game-state`)
5. Choose region (prefer close to most users)
6. Click **Create**

### 3. Connect KV to Project

1. In the KV database page, click **Connect to Project**
2. Select your quiz app project
3. Vercel automatically adds environment variables:
   - `KV_REST_API_URL`
   - `KV_REST_API_TOKEN`
   - `KV_REST_API_READ_ONLY_TOKEN`
   - `KV_URL`

### 4. Redeploy

After connecting KV, trigger a new deployment:

```bash
# Push any change, or manually redeploy
git commit --allow-empty -m "chore: trigger redeploy with KV"
git push
```

Or redeploy from Vercel dashboard: **Deployments** → **Latest** → **Redeploy**

## Environment Variables

### Production (Vercel)

Set automatically when connecting Vercel KV:

| Variable | Description |
|----------|-------------|
| `KV_REST_API_URL` | Vercel KV REST API endpoint |
| `KV_REST_API_TOKEN` | Full access token |
| `KV_REST_API_READ_ONLY_TOKEN` | Read-only token |
| `KV_URL` | Redis protocol URL |

### Local Development

For local development, the app uses localStorage by default (no KV needed).

To test with real KV locally:

```bash
# Download env vars from Vercel
vercel env pull .env.local

# Run with API mode
npm run dev:api
```

## API Endpoint Details

### GET `/api/game`

Fetches current game state.

**Response:**
```json
{
  "participants": [
    { "id": "123", "name": "Alice", "joinedAt": "2024-01-01T00:00:00Z" }
  ],
  "scores": { "123": 25 },
  "responses": [...],
  "screen": "waiting",
  "currentQuestionIndex": 0,
  "activeQuestions": null,
  "quizStarted": false,
  "lastUpdated": 1704067200000
}
```

### POST `/api/game`

Sends game actions.

**Actions:**

| Action | Payload | Description |
|--------|---------|-------------|
| `JOIN` | `{ participant: { id, name, joinedAt } }` | Add player |
| `START` | `{ activeQuestions: [...] }` | Start quiz |
| `SUBMIT_ANSWER` | `{ participantId, answer, isCorrect, timeRemaining, questionIndex, questionId }` | Record answer |
| `NEXT_QUESTION` | `{ totalQuestions }` | Advance question |
| `RESET` | `{}` | Reset game state |

**Example:**
```bash
curl -X POST https://your-app.vercel.app/api/game \
  -H "Content-Type: application/json" \
  -d '{"action": "JOIN", "payload": {"participant": {"id": "1", "name": "Bob"}}}'
```

## Multiplayer Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Host      │     │   API       │     │   Player    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                    │
       │  POST /api/game   │                    │
       │  action: JOIN     │                    │
       ├──────────────────►│                    │
       │                   │                    │
       │   game state      │                    │
       │◄──────────────────┤                    │
       │                   │                    │
       │                   │   POST /api/game   │
       │                   │   action: JOIN     │
       │                   │◄───────────────────┤
       │                   │                    │
       │                   │   game state       │
       │                   ├───────────────────►│
       │                   │                    │
       │  (polling every 1s)                    │
       │◄─────────────────►│◄──────────────────►│
       │                   │                    │
       │  POST /api/game   │                    │
       │  action: START    │                    │
       ├──────────────────►│                    │
       │                   │                    │
       │                   │  (players see quiz via poll)
       │                   │◄──────────────────►│
```

## Troubleshooting

### "Connection Error" on Load

**Cause**: API is unreachable or returning non-JSON

**Solutions:**
1. Check if KV is connected in Vercel dashboard
2. Verify environment variables are set
3. Check deployment logs for errors

### State Not Syncing Between Players

**Cause**: Each player has different state

**Solutions:**
1. Ensure all players are on same URL (not localhost)
2. Check browser console for API errors
3. Reset game state: Click "Reset Game" as host

### KV Connection Errors

**Cause**: Invalid or missing KV credentials

**Solutions:**
1. Reconnect KV database in Vercel dashboard
2. Redeploy after connecting
3. Check `/api/game` endpoint directly for errors

### Local Dev Shows "is not valid JSON"

**Cause**: Vite dev server doesn't serve `/api/game`

**Solution**: This is expected! Local dev uses localStorage mode by default. The error appears because the browser tries the API first. You can ignore it or:

```bash
# Use API mode with vercel dev
npm install -g vercel
vercel dev
```

## Performance Considerations

### Polling Interval

The app polls `/api/game` every 1 second for state updates.

**Pros:**
- Simple implementation
- Works reliably across all browsers
- No WebSocket complexity

**Cons:**
- 1-second delay for state updates
- Higher request volume

**Future Enhancement**: WebSocket support for real-time updates

### KV Limits

Vercel KV (Hobby tier):
- 256 MB storage
- 30,000 requests/day
- Perfect for casual quiz games

For high-traffic use, consider:
- Redis caching layer
- WebSocket server (e.g., Pusher, Ably)
- Rate limiting on API

## Custom Domain

1. Go to project **Settings** → **Domains**
2. Add your domain (e.g., `quiz.example.com`)
3. Update DNS records as instructed
4. Vercel automatically provisions SSL

## Monitoring

1. **Function Logs**: Vercel dashboard → **Logs**
2. **Analytics**: Vercel dashboard → **Analytics** (Pro plan)
3. **KV Metrics**: Storage → KV database → **Metrics**

## CI/CD

Vercel automatically deploys on:
- Push to `main` branch → Production
- Push to other branches → Preview deployments
- Pull requests → Preview deployments with comments

To disable auto-deploy:
1. **Settings** → **Git** → **Ignored Build Step**
2. Or use `vercel.json`:
```json
{
  "github": {
    "silent": true
  }
}
```
