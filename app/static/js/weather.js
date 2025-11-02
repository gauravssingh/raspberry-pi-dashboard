// Weather and World Clocks JavaScript

// API_BASE is defined in dashboard.js (loaded from base template)

function showError(msg) {
  const container = document.getElementById('error-container');
  if (container) {
    container.innerHTML = `<div class="error-message">⚠️ ${msg}</div>`;
  }
}

function clearError() {
  const container = document.getElementById('error-container');
  if (container) {
    container.innerHTML = '';
  }
}

// Update local time
function updateLocalTime() {
  const now = new Date();
  
  const timeElem = document.getElementById('local-time');
  if (timeElem) {
    timeElem.textContent = now.toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    });
  }
  
  const dateElem = document.getElementById('local-date');
  if (dateElem) {
    dateElem.textContent = now.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }
  
  const tzElem = document.getElementById('local-timezone');
  if (tzElem) {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    tzElem.textContent = tz;
  }
}

// Get weather icon emoji
function getWeatherIcon(condition) {
  const icons = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'drizzle': '🌦️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
    'fog': '🌫️',
    'haze': '🌫️'
  };
  
  const key = condition.toLowerCase();
  for (const [term, icon] of Object.entries(icons)) {
    if (key.includes(term)) {
      return icon;
    }
  }
  return '🌤️';
}

// Load weather data
async function loadWeather() {
  const loadingElem = document.getElementById('weather-loading');
  const containerElem = document.getElementById('weather-container');
  const errorElem = document.getElementById('weather-error');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  if (containerElem) containerElem.style.display = 'none';
  if (errorElem) errorElem.style.display = 'none';
  
  try {
    const response = await fetch(`${API_BASE}/api/system/weather`);
    const result = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (result.success && result.data) {
      const weather = result.data;
      
      // Update location
      const locationElem = document.getElementById('weather-location');
      if (locationElem) {
        locationElem.textContent = weather.location || 'Unknown';
      }
      
      // Update timestamp
      const updatedElem = document.getElementById('weather-updated');
      if (updatedElem) {
        updatedElem.textContent = new Date().toLocaleTimeString();
      }
      
      // Update icon
      const iconElem = document.getElementById('weather-icon');
      if (iconElem) {
        iconElem.textContent = getWeatherIcon(weather.condition || '');
      }
      
      // Update temperature
      const tempElem = document.getElementById('weather-temp');
      if (tempElem) {
        tempElem.textContent = Math.round(weather.temperature || 0);
      }
      
      // Update description
      const descElem = document.getElementById('weather-description');
      if (descElem) {
        descElem.textContent = weather.description || weather.condition || 'Unknown';
      }
      
      // Update feels like
      const feelsLikeElem = document.getElementById('weather-feels-like');
      if (feelsLikeElem) {
        feelsLikeElem.textContent = `${Math.round(weather.feels_like || weather.temperature || 0)}°C`;
      }
      
      // Update humidity
      const humidityElem = document.getElementById('weather-humidity');
      if (humidityElem) {
        humidityElem.textContent = `${weather.humidity || 0}%`;
      }
      
      // Update wind
      const windElem = document.getElementById('weather-wind');
      if (windElem) {
        windElem.textContent = `${(weather.wind_speed || 0).toFixed(1)} km/h`;
      }
      
      // Update pressure
      const pressureElem = document.getElementById('weather-pressure');
      if (pressureElem) {
        pressureElem.textContent = `${weather.pressure || 0} hPa`;
      }
      
      // Update visibility
      const visibilityElem = document.getElementById('weather-visibility');
      if (visibilityElem) {
        const visKm = (weather.visibility || 0) / 1000;
        visibilityElem.textContent = `${visKm.toFixed(1)} km`;
      }
      
      // Update cloudiness
      const cloudsElem = document.getElementById('weather-clouds');
      if (cloudsElem) {
        cloudsElem.textContent = `${weather.cloudiness || 0}%`;
      }
      
      // Update sunrise/sunset
      if (weather.sunrise) {
        const sunriseElem = document.getElementById('weather-sunrise');
        if (sunriseElem) {
          const sunriseTime = new Date(weather.sunrise * 1000);
          sunriseElem.textContent = sunriseTime.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
          });
        }
      }
      
      if (weather.sunset) {
        const sunsetElem = document.getElementById('weather-sunset');
        if (sunsetElem) {
          const sunsetTime = new Date(weather.sunset * 1000);
          sunsetElem.textContent = sunsetTime.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
          });
        }
      }
      
      if (containerElem) containerElem.style.display = 'block';
      clearError();
    } else {
      if (errorElem) errorElem.style.display = 'block';
    }
  } catch (error) {
    console.error('Weather error:', error);
    if (loadingElem) loadingElem.style.display = 'none';
    if (errorElem) errorElem.style.display = 'block';
  }
}

// Load world clocks
async function loadWorldClocks() {
  const loadingElem = document.getElementById('clocks-loading');
  const containerElem = document.getElementById('world-clocks-container');
  const gridElem = document.getElementById('clocks-grid');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  if (containerElem) containerElem.style.display = 'none';
  
  try {
    const response = await fetch(`${API_BASE}/api/system/world-clocks`);
    const clocks = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (gridElem && clocks) {
      gridElem.innerHTML = '';
      
      Object.entries(clocks).forEach(([city, data]) => {
        const clockCard = document.createElement('div');
        clockCard.className = 'clock-card';
        clockCard.innerHTML = `
          <div class="clock-city">${city}</div>
          <div class="clock-time" data-city="${city}">${data.time}</div>
          <div class="clock-date">${data.date}</div>
          <div class="clock-timezone">${data.timezone}</div>
        `;
        gridElem.appendChild(clockCard);
      });
      
      if (containerElem) containerElem.style.display = 'block';
    }
  } catch (error) {
    console.error('World clocks error:', error);
    if (loadingElem) loadingElem.style.display = 'none';
    showError('Failed to load world clocks');
  }
}

// Update world clocks in real-time (local update)
function updateWorldClocksRealtime() {
  // This is a simple local update - not fetching from server every second
  const clockElems = document.querySelectorAll('.clock-time');
  
  clockElems.forEach(elem => {
    const city = elem.dataset.city;
    // For simplicity, we'll just increment the displayed time
    // In production, you'd want to use proper timezone libraries
    const currentTime = elem.textContent;
    // Skip updating for now - would need timezone library for proper implementation
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Update local time immediately and every second
  updateLocalTime();
  setInterval(updateLocalTime, 1000);
  
  // Load weather data
  loadWeather();
  
  // Reload weather every 10 minutes
  setInterval(loadWeather, 10 * 60 * 1000);
  
  // Load world clocks
  loadWorldClocks();
  
  // Reload world clocks every minute
  setInterval(loadWorldClocks, 60 * 1000);
});

