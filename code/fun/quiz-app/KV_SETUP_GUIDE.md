# Vercel KV Setup Issue - Troubleshooting Guide

## Problem
You have `REDIS_URL` but `@vercel/kv` needs REST API credentials.

## Current State
- ✅ Redis database created (Upstash)
- ❌ Missing required KV environment variables
- Environment variable found: `REDIS_URL` only

## Required Environment Variables
`@vercel/kv` needs these variables:
- `KV_REST_API_URL`
- `KV_REST_API_TOKEN`
- `KV_REST_API_READ_ONLY_TOKEN`
- `KV_URL` (optional)

## Solution Options

### Option 1: Get REST API Credentials from Upstash (Recommended)

1. Go to Vercel Dashboard: https://vercel.com/izaqyos-projects/quiz-app/stores
2. Click on your Redis database (`quiz-game`)
3. Look for **REST API** section or **Environment Variables** tab
4. Copy the REST API credentials
5. Add them to your project:
   ```bash
   vercel env add KV_REST_API_URL
   vercel env add KV_REST_API_TOKEN
   vercel env add KV_REST_API_READ_ONLY_TOKEN
   ```
6. Redeploy:
   ```bash
   vercel --prod
   ```

### Option 2: Use Redis Client Directly

Modify the code to use a standard Redis client instead of `@vercel/kv`:

1. Install Redis client:
   ```bash
   npm install ioredis
   ```

2. Update `api/game.js` to use `ioredis` with `REDIS_URL`

### Option 3: Reconnect Database with Proper KV

1. Go to Vercel Dashboard Storage
2. Disconnect current Redis database
3. Create new **KV** database (not Redis from Marketplace)
4. Vercel will auto-inject the correct variables
5. Redeploy

## Quick Test

After setup, test the API:
```bash
curl https://quiz-app-iota-nine-74.vercel.app/api/debug
```

Should return:
```json
{
  "envVars": {
    "KV_REST_API_URL": true,
    "KV_REST_API_TOKEN": true,
    ...
  },
  "kvTest": {
    "success": true
  }
}
```

## Current Error
The `@vercel/kv` package is trying to connect but can't find the REST API credentials, so it silently fails and returns empty game state.

## Next Steps
1. Check Upstash dashboard for REST API credentials
2. Add missing environment variables
3. Redeploy
4. Test with `/api/debug` endpoint
