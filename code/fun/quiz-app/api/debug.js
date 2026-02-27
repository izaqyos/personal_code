import Redis from 'ioredis'

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*')

  const envVars = {
    REDIS_URL: !!process.env.REDIS_URL,
  }

  let redisTest = null
  try {
    const redis = new Redis(process.env.REDIS_URL, {
      connectTimeout: 5000,
      maxRetriesPerRequest: 1
    })
    await redis.set('test_key', 'test_value')
    const value = await redis.get('test_key')
    await redis.quit()
    redisTest = { success: true, testValue: value }
  } catch (error) {
    redisTest = { success: false, error: error.message }
  }

  return res.status(200).json({
    envVars,
    redisTest,
    timestamp: new Date().toISOString()
  })
}
