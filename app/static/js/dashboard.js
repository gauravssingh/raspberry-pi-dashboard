// Raspberry Pi Dashboard JavaScript

// Use relative URL for API - works with nginx proxy
const API_BASE = '';

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

function updateStats(stats) {
  const { system, cpu, memory, disk } = stats;
  
  // Update uptime
  if (system && system.uptime) {
    const elem = document.getElementById('uptime');
    if (elem) {
      elem.textContent = `${system.uptime.days}d ${system.uptime.hours}h ${system.uptime.minutes}m`;
    }
  }
  
  // Update CPU
  if (cpu) {
    const tempElem = document.getElementById('cpu-temp');
    if (tempElem) {
      tempElem.textContent = cpu.temperature ? `${cpu.temperature}°C` : 'N/A';
    }
    
    const usageElem = document.getElementById('cpu-usage');
    if (usageElem) {
      usageElem.textContent = `CPU: ${cpu.percent}%`;
    }
  }
  
  // Update Memory
  if (memory) {
    const percentElem = document.getElementById('memory-percent');
    if (percentElem) {
      percentElem.textContent = `${memory.percent}%`;
    }
    
    const detailElem = document.getElementById('memory-detail');
    if (detailElem) {
      detailElem.textContent = `${memory.used} / ${memory.total} GB`;
    }
    
    const progressElem = document.getElementById('memory-progress');
    if (progressElem) {
      progressElem.style.width = `${memory.percent}%`;
    }
  }
  
  // Update Disk
  if (disk) {
    const percentElem = document.getElementById('disk-percent');
    if (percentElem) {
      percentElem.textContent = `${disk.percent}%`;
    }
    
    const detailElem = document.getElementById('disk-detail');
    if (detailElem) {
      detailElem.textContent = `${disk.used} / ${disk.total} GB`;
    }
    
    const progressElem = document.getElementById('disk-progress');
    if (progressElem) {
      progressElem.style.width = `${disk.percent}%`;
    }
  }
}

async function fetchStats() {
  try {
    const res = await fetch(`${API_BASE}/api/system/stats`);
    if (!res.ok) throw new Error('Failed to fetch stats');
    const data = await res.json();
    updateStats(data);
    clearError();
  } catch (error) {
    showError('Unable to connect to backend. Ensure Flask server is running.');
    console.error('Error fetching stats:', error);
  }
}

// Initialize stats fetching if we're on a page that needs it
if (document.getElementById('uptime')) {
  fetchStats();
  setInterval(fetchStats, 5000);
}

// Services page functionality
async function loadServices() {
  const container = document.getElementById('services-container');
  if (!container) return;
  
  try {
    // Load Raspotify status
    const raspotifyStatusRes = await fetch(`${API_BASE}/api/services/raspotify/status`);
    const raspotifyStatusData = await raspotifyStatusRes.json();
    
    const raspotifyCurrentRes = await fetch(`${API_BASE}/api/services/raspotify/current`);
    const raspotifyCurrentData = await raspotifyCurrentRes.json();
    
    // Load Shairport Sync status
    const shairportStatusRes = await fetch(`${API_BASE}/api/services/shairport-sync/status`);
    const shairportStatusData = await shairportStatusRes.json();
    
    const shairportCurrentRes = await fetch(`${API_BASE}/api/services/shairport-sync/current`);
    const shairportCurrentData = await shairportCurrentRes.json();
    
    // Render both cards
    let html = '';
    html += renderRaspotifyCard(raspotifyStatusData, raspotifyCurrentData);
    html += renderShairportCard(shairportStatusData, shairportCurrentData);
    
    container.innerHTML = html;
    clearError();
  } catch (error) {
    showError('Unable to load services. Ensure Flask server is running.');
    console.error('Error loading services:', error);
  }
}

function renderRaspotifyCard(status, current) {
  const statusClass = status.running ? 'status-active' : 'status-inactive';
  const statusText = status.running ? 'Active' : 'Inactive';
  
  let currentTrackHTML = '';
  if (current.playing) {
    currentTrackHTML = `<div class="service-info">🎵 Currently playing track info will appear here</div>`;
  } else if (current.message) {
    currentTrackHTML = `<div class="service-info">${current.message}</div>`;
  }
  
  if (current.note) {
    currentTrackHTML += `<div class="service-info" style="margin-top: 0.5rem; font-size: 0.85rem; opacity: 0.7;">${current.note}</div>`;
  }
  
  return `
    <div class="service-card">
      <div class="service-header">
        <div class="service-name">🎵 Raspotify</div>
        <div class="status-badge ${statusClass}">${statusText}</div>
      </div>
      <div class="service-info">
        <strong>Device:</strong> ${status.device_name || 'Raspotify'}<br>
        <strong>Status:</strong> ${status.status}
      </div>
      ${currentTrackHTML}
    </div>
  `;
}

function renderShairportCard(status, current) {
  const statusClass = status.running ? 'status-active' : 'status-inactive';
  const statusText = status.running ? 'Active' : 'Inactive';
  
  let currentInfoHTML = '';
  if (current.playing) {
    currentInfoHTML = `<div class="service-info">🎵 Currently playing AirPlay audio</div>`;
  } else if (current.message) {
    currentInfoHTML = `<div class="service-info">${current.message}</div>`;
  }
  
  if (current.note) {
    currentInfoHTML += `<div class="service-info" style="margin-top: 0.5rem; font-size: 0.85rem; opacity: 0.7;">${current.note}</div>`;
  }
  
  return `
    <div class="service-card">
      <div class="service-header">
        <div class="service-name">📻 Shairport Sync</div>
        <div class="status-badge ${statusClass}">${statusText}</div>
      </div>
      <div class="service-info">
        <strong>Device:</strong> ${status.device_name || 'Shairport Sync'}<br>
        <strong>Status:</strong> ${status.status}
        ${status.pid ? `<br><strong>PID:</strong> ${status.pid}` : ''}
      </div>
      ${currentInfoHTML}
    </div>
  `;
}

// Initialize services page if we're on it
if (document.getElementById('services-container')) {
  loadServices();
  setInterval(loadServices, 10000); // Refresh every 10 seconds
}

