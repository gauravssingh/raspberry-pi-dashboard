// Settings page JavaScript

const SETTINGS_KEY = 'dashboardSettings';

// Default settings
const defaultSettings = {
  theme: 'dark',
  accentColor: 'blue',
  refreshInterval: 5,
  widgets: {
    uptime: true,
    cpu: true,
    memory: true,
    disk: true
  },
  notifications: {
    highCpu: true,
    highTemp: true,
    lowDisk: true,
    serviceDown: false
  },
  notificationMethods: {
    browser: true,
    sound: false,
    email: false
  }
};

// Load settings from localStorage
function loadSettings() {
  try {
    const stored = localStorage.getItem(SETTINGS_KEY);
    if (stored) {
      return { ...defaultSettings, ...JSON.parse(stored) };
    }
  } catch (error) {
    console.error('Failed to load settings:', error);
  }
  return defaultSettings;
}

// Save settings to localStorage
function saveSettings(settings) {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    showSuccess('Settings saved');
    return true;
  } catch (error) {
    console.error('Failed to save settings:', error);
    showError('Failed to save settings');
    return false;
  }
}

// Apply theme
function setTheme(theme) {
  const settings = loadSettings();
  settings.theme = theme;
  saveSettings(settings);
  
  // Update active button
  document.querySelectorAll('.theme-option').forEach(btn => {
    btn.classList.remove('active');
    if (btn.dataset.theme === theme) {
      btn.classList.add('active');
    }
  });
  
  // Apply theme to body
  document.body.classList.remove('theme-light', 'theme-dark', 'theme-auto');
  
  if (theme === 'auto') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.body.classList.add(prefersDark ? 'theme-dark' : 'theme-light');
  } else {
    document.body.classList.add(`theme-${theme}`);
  }
  
  showSuccess(`Theme changed to ${theme}`);
}

// Set accent color
function setAccentColor(color) {
  const settings = loadSettings();
  settings.accentColor = color;
  saveSettings(settings);
  
  // Update active button
  document.querySelectorAll('.color-option').forEach(btn => {
    btn.classList.remove('active');
    if (btn.dataset.color === color) {
      btn.classList.add('active');
    }
  });
  
  // Apply color (you can expand this with CSS variables)
  document.documentElement.style.setProperty('--accent-color', color);
  
  showSuccess(`Accent color changed to ${color}`);
}

// Set refresh interval
function setRefreshInterval(seconds) {
  const settings = loadSettings();
  settings.refreshInterval = parseInt(seconds);
  saveSettings(settings);
  
  showSuccess(`Refresh interval set to ${seconds} seconds`);
}

// Toggle widget visibility
function toggleWidget(widget) {
  const settings = loadSettings();
  const checkbox = event.target;
  settings.widgets[widget] = checkbox.checked;
  saveSettings(settings);
  
  showSuccess(`Widget ${widget} ${checkbox.checked ? 'enabled' : 'disabled'}`);
}

// Toggle notification
function toggleNotification(type) {
  const settings = loadSettings();
  const checkbox = event.target;
  settings.notifications[type] = checkbox.checked;
  saveSettings(settings);
}

// Toggle notification method
function toggleNotificationMethod(method) {
  const settings = loadSettings();
  const checkbox = event.target;
  settings.notificationMethods[method] = checkbox.checked;
  saveSettings(settings);
  
  if (method === 'browser' && checkbox.checked) {
    requestNotificationPermission();
  }
}

// Request browser notification permission
async function requestNotificationPermission() {
  if ('Notification' in window) {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      showSuccess('Browser notifications enabled');
    } else {
      showError('Notification permission denied');
    }
  }
}

// Clear all settings
function clearSettings() {
  if (confirm('Are you sure you want to clear all settings? This will reset everything to defaults.')) {
    localStorage.removeItem(SETTINGS_KEY);
    showSuccess('Settings cleared. Reloading...');
    setTimeout(() => location.reload(), 1500);
  }
}

// Export settings
function exportSettings() {
  const settings = loadSettings();
  const dataStr = JSON.stringify(settings, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  
  const link = document.createElement('a');
  link.href = URL.createObjectURL(dataBlob);
  link.download = `dashboard-settings-${new Date().toISOString().split('T')[0]}.json`;
  link.click();
  
  showSuccess('Settings exported');
}

// Import settings
function importSettings(input) {
  const file = input.files[0];
  if (!file) return;
  
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const imported = JSON.parse(e.target.result);
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(imported));
      showSuccess('Settings imported. Reloading...');
      setTimeout(() => location.reload(), 1500);
    } catch (error) {
      showError('Invalid settings file');
    }
  };
  reader.readAsText(file);
}

// Update storage display
function updateStorageDisplay() {
  try {
    const settings = localStorage.getItem(SETTINGS_KEY);
    const size = new Blob([settings || '']).size;
    const sizeKB = (size / 1024).toFixed(2);
    
    const elem = document.getElementById('storage-used');
    if (elem) {
      elem.textContent = `${sizeKB} KB`;
    }
  } catch (error) {
    console.error('Failed to calculate storage:', error);
  }
}

// Show success message
function showSuccess(msg) {
  const container = document.getElementById('success-container');
  if (container) {
    container.innerHTML = `<div class="success-message">✅ ${msg}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
  }
}

// Show error message
function showError(msg) {
  const container = document.getElementById('error-container');
  if (container) {
    container.innerHTML = `<div class="error-message">⚠️ ${msg}</div>`;
    setTimeout(() => container.innerHTML = '', 5000);
  }
}

// Initialize settings on page load
document.addEventListener('DOMContentLoaded', () => {
  const settings = loadSettings();
  
  // Set theme buttons
  document.querySelectorAll('.theme-option').forEach(btn => {
    if (btn.dataset.theme === settings.theme) {
      btn.classList.add('active');
    }
  });
  
  // Set accent color buttons
  document.querySelectorAll('.color-option').forEach(btn => {
    if (btn.dataset.color === settings.accentColor) {
      btn.classList.add('active');
    }
  });
  
  // Set refresh interval
  const refreshSelect = document.getElementById('refresh-interval');
  if (refreshSelect) {
    refreshSelect.value = settings.refreshInterval;
  }
  
  // Update storage display
  updateStorageDisplay();
  
  // Apply current theme
  setTheme(settings.theme);
});

