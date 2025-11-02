# Dashboard API Documentation

Complete API reference for the Raspberry Pi Dashboard with performance optimization details.

---

## 📚 Table of Contents

- [Quick Reference](#-quick-reference)
- [Performance Overview](#-performance-overview)
- [Base URL](#base-url)
- [Fast Endpoints](#-fast-endpoints-real-time)
- [Cached Endpoints](#-cached-endpoints-expensive-operations)
- [Service Endpoints](#-service-endpoints)
- [Response Formats](#-response-formats)
- [Usage Examples](#-usage-examples)
- [Best Practices](#-best-practices)
- [Error Handling](#-error-handling)
- [Testing](#-testing)

---

## 🚀 Quick Reference

### Fast Endpoints (Use for real-time updates)

| Endpoint | Speed | Cache | Description |
|----------|-------|-------|-------------|
| `/api/system/stats` | ~10ms | No | Essential stats (CPU, memory, disk, uptime) |
| `/api/system/system-info` | <5ms | No | Static system info (model, OS, CPU cores) |
| `/api/system/health` | <1ms | No | Health check |
| `/api/system/world-clocks` | <5ms | No | Time in multiple timezones |

**Use these for:**
- Main dashboard displays
- Real-time monitoring
- Frequent polling (every 5s is fine)

### Cached Endpoints (Use with caching)

| Endpoint | 1st Call | Cached | Cache TTL | Description |
|----------|----------|--------|-----------|-------------|
| `/api/system/weather` | ~3-5s | instant | 10 min | Local weather |
| `/api/system/network/public-ip` | ~2-3s | instant | 5 min | Public IP address |
| `/api/system/network` | ~200ms | instant | 30 sec | Full network info |
| `/api/system/network/wifi` | ~100ms | instant | 30 sec | WiFi signal only |
| `/api/system/audio` | ~100ms | instant | 1 min | Audio devices |
| `/api/system/stats/detailed` | ~500ms | instant | 5 sec | All system stats |

**Use these for:**
- Widgets that don't need frequent updates
- One-time info displays
- Less critical data

---

## 📊 Performance Overview

### Major Improvements

The main stats endpoint has been optimized from **~9,500ms to ~10ms** response time — a **950x improvement**!

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Response Time | ~9,500ms | ~10ms | **950x faster** |
| Data Size | ~3,000 bytes | 242 bytes | **92% smaller** |
| Blocking Operations | 4+ | 0 | **100% removed** |
| External Dependencies | 2 APIs | 0 APIs | **No external delays** |

### What Changed

#### 1. Removed Blocking CPU Measurements
**Before:**
```python
cpu_percent = psutil.cpu_percent(interval=1)  # Blocked for 1000ms
cpu_per_core = get_cpu_per_core()  # interval=0.5, blocked for 500ms
```

**After:**
```python
cpu_percent = psutil.cpu_percent(interval=0)  # Non-blocking, returns immediately
# Removed per-core stats (not used by UI)
```

**Savings:** 1,500ms

#### 2. Removed External API Calls from Main Endpoint
**Before:**
- `get_weather()` - HTTP request to wttr.in (5s timeout)
- `get_public_ip()` - HTTP request to ipify.org (3s timeout)

**After:** Moved to separate cached endpoints

**Savings:** Up to 8,000ms

#### 3. Removed Subprocess Calls from Main Endpoint
**Before:**
- `get_wifi_signal()` - Called `iwconfig` subprocess
- `get_audio_devices()` - Called `aplay -l` subprocess

**After:** Moved to separate cached endpoints

**Savings:** 100-500ms

#### 4. Streamlined Data Response
**Before:** Sending ~3KB of JSON with tons of unused data  
**After:** Sending only 242 bytes with exactly what UI needs

### Cache Strategy

All expensive operations now use a simple TTL-based cache:

```python
def cached_endpoint(ttl_seconds):
    """Decorator to cache endpoint results with TTL"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = func.__name__
            now = time.time()
            
            if cache_key in _cache:
                cached_data, timestamp = _cache[cache_key]
                if now - timestamp < ttl_seconds:
                    return cached_data
            
            result = func(*args, **kwargs)
            _cache[cache_key] = (result, now)
            return result
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
```

**Cache TTL Values:**
- Weather: 10 minutes (data doesn't change fast)
- Public IP: 5 minutes (rarely changes)
- Network info: 30 seconds (moderate updates)
- WiFi signal: 30 seconds (can fluctuate)
- Audio devices: 1 minute (rarely changes)
- Detailed stats: 5 seconds (for real-time monitoring)

---

## Base URL

**Development:**
```
http://localhost:5050
```

**Production (with nginx):**
```
http://your-pi-ip
```

All endpoint paths are relative to this base URL.

---

## ⚡ Fast Endpoints (Real-Time)

### `GET /api/system/stats`

Get essential system statistics optimized for the dashboard UI.

**Response Time:** ~10ms  
**Cache:** None (real-time data)

**Response:**
```json
{
  "cpu": {
    "percent": 54.5,
    "temperature": 40.8
  },
  "memory": {
    "total": 0.88,
    "used": 0.69,
    "percent": 85.1
  },
  "disk": {
    "total": 116.64,
    "used": 6.08,
    "percent": 5.4
  },
  "system": {
    "uptime": {
      "days": 0,
      "hours": 6,
      "minutes": 32,
      "seconds": 23545
    }
  }
}
```

**Use Case:** Main dashboard - updates every 5 seconds

**What's Included:**
- ✅ CPU usage percentage
- ✅ CPU temperature
- ✅ Memory usage (percent, used, total)
- ✅ Disk usage (percent, used, total)
- ✅ System uptime

---

### `GET /api/system/system-info`

Get static system information (model, OS, CPU cores, etc.).

**Response Time:** <5ms  
**Cache:** None (static data)

**Response:**
```json
{
  "hostname": "raspberrypi",
  "pi_model": "Raspberry Pi 3 Model B Rev 1.2",
  "os": "Raspbian GNU/Linux 11 (bullseye)",
  "architecture": "aarch64",
  "cpu_cores": 4,
  "cpu_threads": 4
}
```

**Use Case:** System info page, footer

---

### `GET /api/system/health`

Health check endpoint for monitoring.

**Response Time:** <1ms

**Response:**
```json
{
  "status": "ok",
  "service": "system"
}
```

**Use Case:** Load balancer health checks, monitoring tools

---

### `GET /api/system/world-clocks`

Get current time in multiple timezones.

**Response Time:** <5ms

**Response:**
```json
{
  "Mumbai": {
    "time": "22:15:30",
    "date": "2025-10-29",
    "timezone": "Asia/Kolkata"
  },
  "New York": {
    "time": "12:45:30",
    "date": "2025-10-29",
    "timezone": "America/New_York"
  },
  "London": {
    "time": "17:45:30",
    "date": "2025-10-29",
    "timezone": "Europe/London"
  }
}
```

**Use Case:** World clock widget

---

## 🐌 Cached Endpoints (Expensive Operations)

### `GET /api/system/stats/detailed`

Get comprehensive system statistics including all available data.

**Response Time:** ~100-500ms (first call), instant (cached)  
**Cache:** 5 seconds

**Response:** Full system stats including:
- Complete CPU info (per-core, throttle status, load average)
- Memory details (swap, buffers, cached, top processes)
- Disk partitions
- Network interfaces and connections
- WiFi signal
- Public IP
- Audio devices
- Weather

**Use Case:** Advanced system monitoring page

---

### `GET /api/system/weather`

Get current local weather information.

**Response Time:** ~3-5s (first call), instant (cached)  
**Cache:** 10 minutes (600 seconds)

**Response:**
```json
{
  "success": true,
  "data": {
    "temp_c": "15",
    "feels_like": "13",
    "description": "Partly cloudy",
    "humidity": "72",
    "wind_kmph": "15"
  },
  "cached": true,
  "cache_ttl": 600
}
```

**Error Response (503):**
```json
{
  "success": false,
  "error": "Unable to fetch weather data",
  "message": "Weather service unavailable"
}
```

**Use Case:** Weather widget on dashboard

---

### `GET /api/system/network`

Get complete network information.

**Response Time:** ~100-300ms (first call), instant (cached)  
**Cache:** 30 seconds

**Response:**
```json
{
  "success": true,
  "interfaces": {
    "wlan0": {
      "ip": "192.168.1.100",
      "is_up": true,
      "speed": 0
    },
    "eth0": {
      "ip": null,
      "is_up": false,
      "speed": 0
    }
  },
  "wifi_signal": "-45 dBm",
  "public_ip": "203.0.113.42",
  "cached": true,
  "cache_ttl": 30
}
```

**Use Case:** Network status page

---

### `GET /api/system/network/public-ip`

Get public IP address only.

**Response Time:** ~2-3s (first call), instant (cached)  
**Cache:** 5 minutes (300 seconds)

**Response:**
```json
{
  "success": true,
  "ip": "203.0.113.42",
  "cached": true,
  "cache_ttl": 300
}
```

**Error Response (503):**
```json
{
  "success": false,
  "error": "Unable to fetch public IP",
  "message": "IP service unavailable"
}
```

**Use Case:** Network info widget

---

### `GET /api/system/network/wifi`

Get WiFi signal strength.

**Response Time:** ~100ms (first call), instant (cached)  
**Cache:** 30 seconds

**Response (connected):**
```json
{
  "success": true,
  "signal": "-45 dBm",
  "cached": true,
  "cache_ttl": 30
}
```

**Response (not connected):**
```json
{
  "success": false,
  "error": "Unable to get WiFi signal",
  "message": "WiFi not available or not connected"
}
```

**Use Case:** WiFi status indicator

---

### `GET /api/system/audio`

Get list of connected audio devices.

**Response Time:** ~100ms (first call), instant (cached)  
**Cache:** 1 minute (60 seconds)

**Response:**
```json
{
  "success": true,
  "devices": [
    "card 0: Headphones [bcm2835 Headphones], device 0: bcm2835 Headphones [bcm2835 Headphones]",
    "card 1: Device [USB Audio Device], device 0: USB Audio [USB Audio]"
  ],
  "count": 2,
  "cached": true,
  "cache_ttl": 60
}
```

**Use Case:** Audio settings page

---

## 🎵 Service Endpoints

### `GET /api/services/list`

List all available services.

**Response:**
```json
{
  "services": [
    {
      "name": "Raspotify",
      "id": "raspotify",
      "description": "Spotify Connect for Raspberry Pi",
      "endpoints": {
        "status": "/api/services/raspotify/status",
        "current": "/api/services/raspotify/current"
      }
    },
    {
      "name": "Shairport Sync",
      "id": "shairport-sync",
      "description": "AirPlay Audio Receiver",
      "endpoints": {
        "status": "/api/services/shairport-sync/status",
        "current": "/api/services/shairport-sync/current"
      }
    }
  ]
}
```

---

### `GET /api/services/raspotify/status`

Get Raspotify service status.

**Response:**
```json
{
  "service": "raspotify",
  "device_name": "Raspotify",
  "running": true,
  "enabled": true,
  "status": "active"
}
```

---

### `GET /api/services/raspotify/current`

Get currently playing track on Raspotify.

**Response:**
```json
{
  "service": "raspotify",
  "playing": false,
  "message": "Raspotify is running and ready for connections",
  "note": "Real-time track info requires Spotify Web API integration"
}
```

---

### `GET /api/services/shairport-sync/status`

Get Shairport Sync service status.

**Response:**
```json
{
  "service": "shairport-sync",
  "device_name": "rpi",
  "running": true,
  "enabled": true,
  "status": "active",
  "pid": "1054"
}
```

---

### `GET /api/services/shairport-sync/current`

Get current playback on Shairport Sync.

**Response:**
```json
{
  "service": "shairport-sync",
  "playing": false,
  "message": "Shairport Sync is running and ready for AirPlay connections",
  "metadata_available": false,
  "note": "Enable metadata pipe in config for playback info"
}
```

---

### `GET /api/services/health`

Service health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "services"
}
```

---

## 📋 Response Formats

### Fast Stats Response
```json
{
  "cpu": { "percent": 54.5, "temperature": 40.8 },
  "memory": { "total": 0.88, "used": 0.69, "percent": 85.1 },
  "disk": { "total": 116.64, "used": 6.08, "percent": 5.4 },
  "system": { "uptime": { "days": 0, "hours": 6, "minutes": 32 } }
}
```

### Cached Endpoint Success Response
```json
{
  "success": true,
  "data": { /* actual data */ },
  "cached": true,
  "cache_ttl": 600
}
```

### Error Response
```json
{
  "success": false,
  "error": "Brief error message",
  "message": "Detailed explanation"
}
```

### Cache Information

All cached endpoints include cache metadata:
- `cached`: Boolean indicating if caching is enabled
- `cache_ttl`: Time-to-live in seconds

---

## 💻 Usage Examples

### JavaScript (Fetch API)

#### Fast Stats for Main Dashboard
```javascript
// Update every 5 seconds
async function updateDashboard() {
  const res = await fetch('/api/system/stats');
  const data = await res.json();
  updateUI(data);
}
setInterval(updateDashboard, 5000);
```

#### Weather Widget (Cached)
```javascript
// Update every minute (cache handles it)
async function updateWeather() {
  const res = await fetch('/api/system/weather');
  const data = await res.json();
  if (data.success) {
    displayWeather(data.data);
  }
}
setInterval(updateWeather, 60000);
```

#### Network Info
```javascript
// Fetch once on page load
async function loadNetworkInfo() {
  const res = await fetch('/api/system/network');
  const data = await res.json();
  console.log('Public IP:', data.public_ip);
  console.log('WiFi Signal:', data.wifi_signal);
  console.log('Interfaces:', data.interfaces);
}
```

#### Batch Multiple Requests
```javascript
// Good - parallel requests
const [stats, weather, network] = await Promise.all([
  fetch('/api/system/stats').then(r => r.json()),
  fetch('/api/system/weather').then(r => r.json()),
  fetch('/api/system/network').then(r => r.json())
]);
```

### Python (Requests)

```python
import requests

# Get stats
response = requests.get('http://localhost:5050/api/system/stats')
stats = response.json()
print(f"CPU: {stats['cpu']['percent']}%")

# Get weather
response = requests.get('http://localhost:5050/api/system/weather')
weather = response.json()
if weather['success']:
    print(f"Temperature: {weather['data']['temp_c']}°C")

# Get public IP
response = requests.get('http://localhost:5050/api/system/network/public-ip')
ip_data = response.json()
if ip_data['success']:
    print(f"Public IP: {ip_data['ip']}")
```

### cURL

```bash
# Quick stats
curl http://localhost:5050/api/system/stats | jq

# Weather with timing
curl -w "\nTime: %{time_total}s\n" http://localhost:5050/api/system/weather | jq

# Public IP only
curl http://localhost:5050/api/system/network/public-ip | jq '.ip'

# Health check
curl http://localhost:5050/api/system/health

# All services
curl http://localhost:5050/api/services/list | jq
```

---

## ✅ Best Practices

### 1. Use `/stats` for Real-Time Updates
It's optimized and fast (~10ms). Perfect for dashboards that update every 5 seconds.

```javascript
// Good
setInterval(() => fetch('/api/system/stats'), 5000);
```

### 2. Use Cached Endpoints for Expensive Data
Weather, IP, WiFi, etc. are cached. Don't poll them too frequently.

```javascript
// Good - respects cache TTL
setInterval(() => fetch('/api/system/weather'), 60000);  // Every minute

// Bad - wastes resources
setInterval(() => fetch('/api/system/weather'), 1000);   // Every second
```

### 3. Don't Poll Cached Endpoints Too Frequently
Respect the cache TTL. The cache handles efficient updates.

### 4. Handle Errors Gracefully
Some services may be unavailable. Always check the `success` field.

```javascript
async function fetchWeather() {
  try {
    const res = await fetch('/api/system/weather');
    const data = await res.json();
    
    if (!data.success) {
      console.error('Weather unavailable:', data.message);
      return null;
    }
    
    return data.data;
  } catch (error) {
    console.error('Network error:', error);
    return null;
  }
}
```

### 5. Use `/stats/detailed` Sparingly
Only when you need all the data. It's heavier than the fast endpoints.

### 6. Batch Parallel Requests
Use `Promise.all()` for multiple independent requests.

```javascript
const [stats, weather] = await Promise.all([
  fetch('/api/system/stats').then(r => r.json()),
  fetch('/api/system/weather').then(r => r.json())
]);
```

---

## ⚠️ Error Handling

### Common Error Patterns

#### External Service Unavailable
```json
{
  "success": false,
  "error": "Unable to fetch weather data",
  "message": "Weather service unavailable"
}
```

**Causes:**
- No internet connection
- External API down
- Request timeout

**Handling:**
```javascript
if (!response.success) {
  // Show cached data or placeholder
  displayError(response.message);
}
```

#### Service Not Available
```json
{
  "success": false,
  "error": "Unable to get WiFi signal",
  "message": "WiFi not available or not connected"
}
```

**Causes:**
- Hardware not present
- Service not running
- Permission issues

**Handling:**
```javascript
if (!response.success) {
  // Hide widget or show "N/A"
  hideWifiWidget();
}
```

### HTTP Status Codes

| Code | Meaning | When It Happens |
|------|---------|-----------------|
| 200 | Success | Request completed successfully |
| 404 | Not Found | Invalid endpoint |
| 500 | Server Error | Python exception occurred |
| 503 | Service Unavailable | External dependency failed |

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Test all fast endpoints
curl http://localhost:5050/api/system/stats | jq
curl http://localhost:5050/api/system/system-info | jq
curl http://localhost:5050/api/system/health | jq
curl http://localhost:5050/api/system/world-clocks | jq

# Test cached endpoints
curl http://localhost:5050/api/system/weather | jq
curl http://localhost:5050/api/system/network | jq
curl http://localhost:5050/api/system/network/public-ip | jq
curl http://localhost:5050/api/system/network/wifi | jq
curl http://localhost:5050/api/system/audio | jq

# Test services
curl http://localhost:5050/api/services/list | jq
curl http://localhost:5050/api/services/raspotify/status | jq

# Test with timing
curl -w "\nTime: %{time_total}s\n" -o /dev/null -s http://localhost:5050/api/system/stats
```

### Performance Testing

```bash
# Test response time
time curl -s http://localhost:5050/api/system/stats > /dev/null

# Test with detailed timing
curl -w "Time: %{time_total}s\nSize: %{size_download} bytes\n" \
  http://localhost:5050/api/system/stats | jq
```

### Python Test Script

```python
import requests
import time

def test_endpoint(url, name):
    start = time.time()
    response = requests.get(url)
    elapsed = time.time() - start
    
    print(f"{name}:")
    print(f"  Status: {response.status_code}")
    print(f"  Time: {elapsed*1000:.2f}ms")
    print(f"  Size: {len(response.text)} bytes")
    print()

# Test fast endpoints
base = 'http://localhost:5050'
test_endpoint(f'{base}/api/system/stats', 'Fast Stats')
test_endpoint(f'{base}/api/system/system-info', 'System Info')
test_endpoint(f'{base}/api/system/health', 'Health Check')

# Test cached endpoints
test_endpoint(f'{base}/api/system/weather', 'Weather (1st call)')
test_endpoint(f'{base}/api/system/weather', 'Weather (cached)')
```

### Automated Test Script

Use the included test script:

```bash
./scripts/test_new_endpoints.sh
```

---

## 📊 Performance Comparison Table

| Endpoint | Response Time | Blocking | Use Case |
|----------|---------------|----------|----------|
| `/stats` | ~10ms | No | ⚡ Main dashboard |
| `/stats/detailed` | ~100-500ms | No (cached) | 📊 Advanced monitoring |
| `/weather` | ~3-5s / instant | No (cached) | 🌤️ Weather widget |
| `/network` | ~100-300ms / instant | No (cached) | 🌐 Network status |
| `/network/public-ip` | ~2-3s / instant | No (cached) | 🌍 IP display |
| `/network/wifi` | ~100ms / instant | No (cached) | 📶 WiFi indicator |
| `/audio` | ~100ms / instant | No (cached) | 🔊 Audio settings |
| `/system-info` | <5ms | No | ℹ️ System details |
| `/health` | <1ms | No | ✅ Monitoring |
| `/world-clocks` | <5ms | No | 🕐 Time widget |

---

## 🔄 Migration from Old API

If you were using the old `/api/system/stats` endpoint that took 9+ seconds:

**Before (slow):**
```javascript
// This used to take 9+ seconds and included everything
const stats = await fetch('/api/system/stats').then(r => r.json());
const weather = stats.weather;
const publicIP = stats.network.public_ip;
```

**After (fast):**
```javascript
// Now split into separate endpoints
const stats = await fetch('/api/system/stats').then(r => r.json());
const weather = await fetch('/api/system/weather').then(r => r.json());
const ip = await fetch('/api/system/network/public-ip').then(r => r.json());
```

**Benefits:**
- Main stats load in 10ms instead of 9 seconds (950x faster!)
- Weather/IP load once and use cache
- Better error handling per service
- More flexible API design
- No blocking on expensive operations

---

## 💡 Tips & Tricks

1. **Cache warming**: First load may be slow for cached endpoints, but subsequent requests are instant
2. **Parallel requests**: Use `Promise.all()` to fetch multiple endpoints simultaneously
3. **Error resilience**: Always have fallback UI for failed service calls
4. **Respect TTLs**: Don't poll cached endpoints more frequently than their TTL
5. **Monitor performance**: Use browser DevTools Network tab to verify response times

---

## 📞 Support

For questions or issues:
- Check [GETTING_STARTED.md](GETTING_STARTED.md) for setup help
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production configuration
- See [ADDING_SERVICES.md](ADDING_SERVICES.md) to extend the API

---

*Last updated: October 29, 2025*

