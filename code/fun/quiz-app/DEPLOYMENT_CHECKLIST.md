# 🚀 Vercel Deployment Checklist

## Prerequisites
- [ ] Vercel CLI installed globally (`npm install -g vercel`)
- [ ] Vercel account created at https://vercel.com
- [ ] Quiz app working locally on `localhost:3001`

---

## Step 1: Initial Deployment (5 minutes)

### 1.1 Login to Vercel
```bash
cd /Users/yosii/work/git/personal_code/code/fun/quiz-app
vercel login
```
- Opens browser for authentication
- Login with GitHub/GitLab/Bitbucket/Email

### 1.2 Deploy to Preview
```bash
vercel
```

**Answer the prompts:**
```
? Set up and deploy "~/path/to/quiz-app"? [Y/n] → Y
? Which scope do you want to deploy to? → [Select your account]
? Link to existing project? [y/N] → N
? What's your project's name? → quiz-app (or your choice)
? In which directory is your code located? → ./ (press Enter)
? Want to override the settings? [y/N] → N
```

**Expected output:**
```
✅  Preview: https://quiz-app-xxxxx.vercel.app
📝  Inspect: https://vercel.com/your-name/quiz-app/xxxxx
```

### 1.3 Test Preview Deployment
- [ ] Open the preview URL in browser
- [ ] Verify the join screen loads
- [ ] Check browser console for errors
- [ ] **Expected:** App works but game state doesn't persist (no KV yet)

---

## Step 2: Set Up Vercel KV Database (3 minutes)

### 2.1 Create KV Database
1. [ ] Go to https://vercel.com/dashboard
2. [ ] Click on your project (`quiz-app`)
3. [ ] Click **Storage** tab (top navigation)
4. [ ] Click **Create Database** button
5. [ ] Select **KV** (Redis-compatible key-value store)
6. [ ] Name: `quiz-game` (or your choice)
7. [ ] Region: Choose closest to your users
8. [ ] Click **Create**

### 2.2 Connect KV to Project
1. [ ] After creation, click **Connect to Project**
2. [ ] Select your `quiz-app` project
3. [ ] Click **Connect**
4. [ ] Verify environment variables are added:
   - `KV_URL`
   - `KV_REST_API_URL`
   - `KV_REST_API_TOKEN`
   - `KV_REST_API_READ_ONLY_TOKEN`

---

## Step 3: Production Deployment (2 minutes)

### 3.1 Deploy to Production
```bash
vercel --prod
```

**Expected output:**
```
✅  Production: https://quiz-app.vercel.app (or your custom domain)
📝  Inspect: https://vercel.com/your-name/quiz-app/xxxxx
```

### 3.2 Verify KV Connection
- [ ] Check deployment logs for KV connection
- [ ] No errors about missing environment variables

---

## Step 4: Testing Multiplayer (10 minutes)

### 4.1 Single Device Test
- [ ] Open production URL in browser
- [ ] Click "👑 I'm the Host" → Enter name → Join
- [ ] Open incognito window → Same URL
- [ ] Click "🎮 I'm a Player" → Enter name → Join
- [ ] Verify player appears in host's lobby
- [ ] Host clicks "Start Quiz"
- [ ] Both screens show the same question
- [ ] Submit answers on both
- [ ] Verify scores update
- [ ] Complete quiz and check results

### 4.2 Multi-Device Test
**Device 1 (Computer - Host):**
- [ ] Open `https://quiz-app.vercel.app`
- [ ] Join as Host

**Device 2 (Phone - Player 1):**
- [ ] Open same URL
- [ ] Join as Player
- [ ] Verify appears in lobby

**Device 3 (Tablet/Another Phone - Player 2):**
- [ ] Open same URL
- [ ] Join as Player
- [ ] Verify appears in lobby

**Run Full Quiz:**
- [ ] Host starts quiz
- [ ] All devices show same question simultaneously
- [ ] Players submit answers
- [ ] Scores update in real-time
- [ ] Host advances to next question
- [ ] Complete all questions
- [ ] View final results on all devices

### 4.3 Edge Cases
- [ ] Player joins mid-quiz (should wait for next question)
- [ ] Player closes browser and rejoins (should maintain state)
- [ ] Host leaves (game should continue or show error)
- [ ] Network interruption (should reconnect)
- [ ] Multiple tabs same player (should sync)

---

## Step 5: Custom Domain (Optional, 5 minutes)

### 5.1 Add Custom Domain
1. [ ] Go to Project Settings → Domains
2. [ ] Click **Add Domain**
3. [ ] Enter your domain (e.g., `quiz.yourdomain.com`)
4. [ ] Follow DNS configuration instructions
5. [ ] Wait for SSL certificate (automatic)

---

## Troubleshooting

### Issue: "Failed to fetch game state"
**Solution:**
- Check KV is connected in Vercel dashboard
- Verify environment variables are set
- Redeploy: `vercel --prod`

### Issue: Game state not syncing across devices
**Solution:**
- Open browser console on both devices
- Check for API errors
- Verify both are hitting the same URL (not preview vs production)
- Check KV dashboard for stored data

### Issue: "Protocol Error" or MCP connection issues
**Solution:**
- This is expected - MCP servers only work in Cursor locally
- The deployed app uses Vercel KV, not MCP

### Issue: Players can't join
**Solution:**
- Verify they're on the same URL (share exact link)
- Check if game already started (join before start)
- Try resetting game from host screen

---

## Monitoring & Maintenance

### Check Deployment Status
```bash
vercel ls
```

### View Logs
```bash
vercel logs [deployment-url]
```

### Rollback to Previous Deployment
1. Go to Vercel dashboard → Deployments
2. Find working deployment
3. Click "..." → Promote to Production

### Check KV Usage
1. Vercel dashboard → Storage → quiz-game
2. View keys, memory usage, request count
3. Free tier: 30K requests/month, 256MB storage

---

## Quick Commands Reference

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# List deployments
vercel ls

# View logs
vercel logs

# Remove deployment
vercel rm [deployment-url]

# Open project in browser
vercel open

# Check environment variables
vercel env ls
```

---

## Success Criteria ✅

- [ ] App deployed to production URL
- [ ] KV database connected and working
- [ ] Host can create and control game
- [ ] Multiple players can join from different devices
- [ ] Game state syncs in real-time across all devices
- [ ] Scores update correctly
- [ ] Results screen shows final standings
- [ ] No console errors on any device
- [ ] Mobile-responsive (works on phones/tablets)

---

## Next Steps After Deployment

1. **Share the URL** with your team/family
2. **Test with real users** (5+ people)
3. **Monitor KV usage** in Vercel dashboard
4. **Consider custom domain** for easier sharing
5. **Add more quizzes** by creating new JSON files in `src/data/`
6. **Customize styling** in CSS files
7. **Add analytics** (optional - Vercel Analytics)

---

## Support & Resources

- **Vercel Docs:** https://vercel.com/docs
- **Vercel KV Docs:** https://vercel.com/docs/storage/vercel-kv
- **Quiz App README:** `/code/fun/quiz-app/README.md`
- **Testing Guide:** `/code/fun/quiz-app/TESTING.md`

---

## Notes

- **Free Tier Limits:**
  - 100GB bandwidth/month
  - 30K KV requests/month
  - 256MB KV storage
  - Unlimited deployments

- **Cost Estimate:**
  - Free for personal use
  - ~10-20 users playing simultaneously: FREE
  - 100+ concurrent users: Consider Pro plan ($20/month)

- **Data Persistence:**
  - Game state stored in Vercel KV
  - Persists across deployments
  - Reset by calling `/api/game` with `RESET` action

---

**Last Updated:** 2026-01-19
**Version:** 1.0.0
