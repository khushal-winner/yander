import { Redis } from "ioredis";

const redisUrl =
  process.env.REDIS_URL ||
  "redis://default:AUGcAAIncDIwMmRjODYwMzg2NWY0OGU1YTliOTk4YzFhMGIyNTE2ZHAyMTY3OTY@touching-filly-16796.upstash.io:6379";

// Debug: Log the Redis URL (without password for security)
const safeRedisUrl = redisUrl.includes("@")
  ? redisUrl.split("@")[0]?.split(":")[0] +
    ":***@" +
    (redisUrl.split("@")[1] || "")
  : redisUrl;
console.log("🔍 Redis URL:", safeRedisUrl);

// Parse Redis URL to extract connection details
const isUpstash =
  redisUrl.includes("upstash.io") || redisUrl.includes("rediss://");

console.log("🔍 Is Upstash:", isUpstash);

export const redis = new Redis(redisUrl, {
  maxRetriesPerRequest: isUpstash ? 2 : 3,
  retryStrategy(times: number) {
    if (times > 5) {
      console.log("❌ Max Redis reconnection attempts reached, giving up");
      return null;
    }
    const delay = Math.min(times * 1000, 5000);
    console.log(`🔄 Redis reconnection attempt ${times + 1} in ${delay}ms`);
    return delay;
  },
  tls: isUpstash
    ? {
        rejectUnauthorized: false,
        servername: redisUrl.includes("upstash.io")
          ? redisUrl.split("@")[1]?.split(":")[0] || undefined
          : undefined,
      }
    : undefined,
  connectTimeout: 10000,
  commandTimeout: 5000,
  lazyConnect: true,
  reconnectOnError(err) {
    const targetError = "READONLY";
    if (err.message.includes(targetError)) {
      return true;
    }
    return false;
  },
  // Upstash specific settings
  enableOfflineQueue: false,
});

let connectionAttempts = 0;
const MAX_CONNECTION_ATTEMPTS = 3;

redis.on("connect", () => {
  console.log("✅ Redis connected");
  connectionAttempts = 0;
});

redis.on("ready", () => {
  console.log("✅ Redis ready for commands");
});

redis.on("error", (err: Error) => {
  connectionAttempts++;
  if (connectionAttempts >= MAX_CONNECTION_ATTEMPTS) {
    console.error(
      "❌ Redis connection failed after multiple attempts:",
      err.message,
    );
    console.log("⚠️ Continuing without Redis (caching disabled)");
    redis.disconnect();
  } else {
    console.error(
      `❌ Redis error (${connectionAttempts}/${MAX_CONNECTION_ATTEMPTS}):`,
      err.message,
    );
  }
});

redis.on("close", () => {
  if (connectionAttempts < MAX_CONNECTION_ATTEMPTS) {
    console.log("⚠️ Redis connection closed");
  }
});

redis.on("reconnecting", () => {
  if (connectionAttempts < MAX_CONNECTION_ATTEMPTS) {
    console.log("🔄 Redis reconnecting...");
  }
});
