// Logs page JavaScript

// API_BASE is defined in dashboard.js (loaded from base template)

let autoRefreshInterval = null;
let autoRefreshEnabled = false;

function showError(msg) {
  const container = document.getElementById('error-container');
  if (container) {
    container.innerHTML = `<div class="error-message">⚠️ ${msg}</div>`;
    setTimeout(() => container.innerHTML = '', 5000);
  }
}

function showSuccess(msg) {
  const container = document.getElementById('error-container');
  if (container) {
    container.innerHTML = `<div class="success-message">✅ ${msg}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
  }
}

// Load logs
async function loadLogs() {
  const service = document.getElementById('service-selector').value;
  const lines = document.getElementById('lines-selector').value;
  const priority = document.getElementById('priority-selector').value;
  
  const loadingElem = document.getElementById('logs-loading');
  const contentElem = document.getElementById('logs-content');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  
  try {
    let url = `${API_BASE}/api/logs/view/${service}?lines=${lines}`;
    if (priority) {
      url += `&priority=${priority}`;
    }
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (data.success && data.logs) {
      // Format logs for display
      const formattedLogs = data.logs.map(log => log.raw).join('\n');
      contentElem.textContent = formattedLogs || 'No logs found';
      
      // Update stats
      document.getElementById('current-service').textContent = service;
      document.getElementById('log-count').textContent = data.count;
      document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
      
      // Auto-scroll to bottom
      contentElem.scrollTop = contentElem.scrollHeight;
    } else {
      contentElem.textContent = `Error: ${data.error || 'Failed to load logs'}`;
    }
  } catch (error) {
    if (loadingElem) loadingElem.style.display = 'none';
    contentElem.textContent = `Failed to load logs: ${error.message}`;
  }
}

// Search logs
async function searchLogs() {
  const query = document.getElementById('search-input').value.trim();
  
  if (!query) {
    showError('Please enter a search term');
    return;
  }
  
  const loadingElem = document.getElementById('logs-loading');
  const contentElem = document.getElementById('logs-content');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  
  try {
    const response = await fetch(`${API_BASE}/api/logs/search?query=${encodeURIComponent(query)}`);
    const data = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (data.success && data.logs) {
      const formattedLogs = data.logs.map(log => log.raw).join('\n');
      contentElem.textContent = formattedLogs || 'No results found';
      
      document.getElementById('current-service').textContent = `Search: "${query}"`;
      document.getElementById('log-count').textContent = data.count;
      document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
    } else {
      contentElem.textContent = `Error: ${data.error || 'Search failed'}`;
    }
  } catch (error) {
    if (loadingElem) loadingElem.style.display = 'none';
    contentElem.textContent = `Search failed: ${error.message}`;
  }
}

// Show recent errors
async function showErrors() {
  const loadingElem = document.getElementById('logs-loading');
  const contentElem = document.getElementById('logs-content');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  
  try {
    const response = await fetch(`${API_BASE}/api/logs/errors?hours=1`);
    const data = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (data.success && data.logs) {
      const formattedLogs = data.logs.map(log => log.raw).join('\n');
      contentElem.textContent = formattedLogs || 'No errors found in the last hour';
      
      document.getElementById('current-service').textContent = 'Recent Errors';
      document.getElementById('log-count').textContent = data.count;
      document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
    } else {
      contentElem.textContent = `Error: ${data.error || 'Failed to load errors'}`;
    }
  } catch (error) {
    if (loadingElem) loadingElem.style.display = 'none';
    contentElem.textContent = `Failed to load errors: ${error.message}`;
  }
}

// Show boot logs
async function showBootLogs() {
  const loadingElem = document.getElementById('logs-loading');
  const contentElem = document.getElementById('logs-content');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  
  try {
    const response = await fetch(`${API_BASE}/api/logs/boot`);
    const data = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (data.success && data.logs) {
      const formattedLogs = data.logs.map(log => log.raw).join('\n');
      contentElem.textContent = formattedLogs || 'No boot logs found';
      
      document.getElementById('current-service').textContent = 'Boot Logs';
      document.getElementById('log-count').textContent = data.count;
      document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
    } else {
      contentElem.textContent = `Error: ${data.error || 'Failed to load boot logs'}`;
    }
  } catch (error) {
    if (loadingElem) loadingElem.style.display = 'none';
    contentElem.textContent = `Failed to load boot logs: ${error.message}`;
  }
}

// Toggle auto-refresh
function toggleAutoRefresh() {
  autoRefreshEnabled = !autoRefreshEnabled;
  
  const iconElem = document.getElementById('auto-refresh-icon');
  const textElem = document.getElementById('auto-refresh-text');
  const statusElem = document.getElementById('auto-status');
  
  if (autoRefreshEnabled) {
    iconElem.textContent = '⏸️';
    textElem.textContent = 'Stop';
    statusElem.textContent = 'On (5s)';
    
    // Start auto-refresh every 5 seconds
    autoRefreshInterval = setInterval(loadLogs, 5000);
    
    showSuccess('Auto-refresh enabled');
  } else {
    iconElem.textContent = '▶️';
    textElem.textContent = 'Auto';
    statusElem.textContent = 'Off';
    
    // Stop auto-refresh
    if (autoRefreshInterval) {
      clearInterval(autoRefreshInterval);
      autoRefreshInterval = null;
    }
    
    showSuccess('Auto-refresh disabled');
  }
}

// Clear logs display
function clearLogsDisplay() {
  const contentElem = document.getElementById('logs-content');
  if (contentElem) {
    contentElem.innerHTML = `
<span class="log-welcome">Logs cleared</span>

Select a service and click "Refresh" to view logs.
    `;
  }
  
  document.getElementById('current-service').textContent = '-';
  document.getElementById('log-count').textContent = '0';
}

// Export logs
function exportLogs() {
  const contentElem = document.getElementById('logs-content');
  const service = document.getElementById('current-service').textContent;
  
  if (!contentElem || !contentElem.textContent.trim()) {
    showError('No logs to export');
    return;
  }
  
  const logs = contentElem.textContent;
  const blob = new Blob([logs], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = `${service}-logs-${new Date().toISOString().split('T')[0]}.txt`;
  link.click();
  
  URL.revokeObjectURL(url);
  showSuccess('Logs exported');
}

// Scroll functions
function scrollToTop() {
  const contentElem = document.getElementById('logs-content');
  if (contentElem) {
    contentElem.scrollTop = 0;
  }
}

function scrollToBottom() {
  const contentElem = document.getElementById('logs-content');
  if (contentElem) {
    contentElem.scrollTop = contentElem.scrollHeight;
  }
}

// Toggle line wrap
function toggleWrap() {
  const contentElem = document.getElementById('logs-content');
  if (contentElem) {
    if (contentElem.style.whiteSpace === 'pre-wrap') {
      contentElem.style.whiteSpace = 'pre';
      showSuccess('Line wrap disabled');
    } else {
      contentElem.style.whiteSpace = 'pre-wrap';
      showSuccess('Line wrap enabled');
    }
  }
}

// Load service status
async function loadServiceStatus() {
  const loadingElem = document.getElementById('services-loading');
  const gridElem = document.getElementById('services-status-grid');
  
  if (loadingElem) loadingElem.style.display = 'flex';
  
  try {
    const response = await fetch(`${API_BASE}/api/logs/services`);
    const data = await response.json();
    
    if (loadingElem) loadingElem.style.display = 'none';
    
    if (data.services && gridElem) {
      gridElem.innerHTML = '';
      
      data.services.forEach(service => {
        const card = document.createElement('div');
        card.className = 'service-status-card';
        card.innerHTML = `
          <div class="service-icon">${service.icon}</div>
          <div class="service-name">${service.name}</div>
          <button class="btn-small" onclick="viewServiceLogs('${service.id}')">View Logs</button>
        `;
        gridElem.appendChild(card);
      });
      
      gridElem.style.display = 'grid';
    }
  } catch (error) {
    console.error('Failed to load service status:', error);
    if (loadingElem) loadingElem.style.display = 'none';
  }
}

// View specific service logs
function viewServiceLogs(serviceId) {
  document.getElementById('service-selector').value = serviceId;
  loadLogs();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Load service status cards
  loadServiceStatus();
  
  // Add enter key support for search
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        searchLogs();
      }
    });
  }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (autoRefreshInterval) {
    clearInterval(autoRefreshInterval);
  }
});

