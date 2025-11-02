// Configuration Page JavaScript
// Note: API_BASE, showError, and clearError are already defined in dashboard.js

// API_BASE is inherited from dashboard.js loaded in base.html

// Helper function to show/hide loading and content
function showContent(loadingId, contentId) {
  const loading = document.getElementById(loadingId);
  const content = document.getElementById(contentId);
  
  if (loading) loading.style.display = 'none';
  if (content) {
    content.style.display = '';
    content.classList.add('fade-in');
  }
}

// Update network interface information
function updateNetworkInterfaces(interfaces) {
  const container = document.getElementById('network-interfaces-container');
  if (!container || !interfaces) return;
  
  let html = '';
  
  for (const [interfaceName, data] of Object.entries(interfaces)) {
    const statusClass = data.is_up ? 'status-active' : 'status-inactive';
    const statusText = data.is_up ? 'Up' : 'Down';
    const ipAddress = data.ip || 'N/A';
    const speed = data.speed > 0 ? `${data.speed} Mbps` : 'N/A';
    
    // Choose icon based on interface type
    let icon = '🔌';
    if (interfaceName.includes('wlan')) {
      icon = '📶';
    } else if (interfaceName.includes('eth')) {
      icon = '🔌';
    } else if (interfaceName.includes('lo')) {
      icon = '🔄';
    }
    
    html += `
      <div class="interface-card">
        <div class="interface-header">
          <span class="interface-icon">${icon}</span>
          <span class="interface-name">${interfaceName}</span>
          <span class="status-badge ${statusClass}">${statusText}</span>
        </div>
        <div class="interface-details">
          <div class="detail-row">
            <span class="detail-label">IP Address:</span>
            <span class="detail-value">${ipAddress}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Speed:</span>
            <span class="detail-value">${speed}</span>
          </div>
        </div>
      </div>
    `;
  }
  
  container.innerHTML = html;
  showContent('network-interfaces-loading', 'network-interfaces-container');
}

// Update WiFi information
function updateWiFiInfo(data) {
  if (!data) return;
  
  const wifiInterface = data.wlan0_interface;
  const details = data.wifi_details;
  
  // Update WiFi status
  if (wifiInterface) {
    const statusElem = document.getElementById('wifi-status');
    if (statusElem) {
      statusElem.textContent = wifiInterface.is_up ? 'Connected' : 'Disconnected';
      statusElem.className = wifiInterface.is_up ? 'wifi-status status-active' : 'wifi-status status-inactive';
    }
    
    const ipElem = document.getElementById('wifi-ip');
    if (ipElem) {
      ipElem.textContent = wifiInterface.ip || 'N/A';
    }
    
    const upStatusElem = document.getElementById('wifi-up-status');
    if (upStatusElem) {
      upStatusElem.textContent = wifiInterface.is_up ? 'Active' : 'Inactive';
      upStatusElem.className = wifiInterface.is_up ? 'detail-value status-text-active' : 'detail-value status-text-inactive';
    }
  }
  
  // Update WiFi detailed information
  if (details) {
    // Update SSID
    const ssidElem = document.getElementById('wifi-ssid');
    if (ssidElem) {
      ssidElem.textContent = details.ssid || 'N/A';
      if (details.ssid) {
        ssidElem.style.fontWeight = '600';
        ssidElem.style.color = 'var(--accent-light)';
      }
    }
    
    // Update band
    const bandElem = document.getElementById('wifi-band');
    if (bandElem) {
      bandElem.textContent = details.band || 'N/A';
      if (details.band) {
        // Highlight 5 GHz differently
        if (details.band.includes('5 GHz')) {
          bandElem.style.color = '#4ade80';
        } else if (details.band.includes('2.4 GHz')) {
          bandElem.style.color = '#fbbf24';
        }
      }
    }
    
    // Update frequency
    const freqElem = document.getElementById('wifi-frequency');
    if (freqElem) {
      freqElem.textContent = details.frequency || 'N/A';
    }
    
    // Update signal strength
    const signalElem = document.getElementById('wifi-signal');
    if (signalElem) {
      signalElem.textContent = details.signal_strength || data.signal || 'N/A';
      
      // Color code based on signal strength
      if (details.signal_strength && details.signal_strength.includes('dBm')) {
        const dbm = parseInt(details.signal_strength);
        if (dbm >= -50) {
          signalElem.style.color = '#4ade80'; // Excellent
        } else if (dbm >= -60) {
          signalElem.style.color = '#a3e635'; // Good
        } else if (dbm >= -70) {
          signalElem.style.color = '#fbbf24'; // Fair
        } else {
          signalElem.style.color = '#ef4444'; // Poor
        }
      }
    }
    
    // Update signal quality
    const qualityElem = document.getElementById('wifi-quality');
    if (qualityElem) {
      qualityElem.textContent = details.signal_quality || 'N/A';
      
      // Color code based on quality percentage
      if (details.signal_quality) {
        const quality = parseInt(details.signal_quality);
        if (quality >= 75) {
          qualityElem.style.color = '#4ade80'; // Excellent
        } else if (quality >= 50) {
          qualityElem.style.color = '#fbbf24'; // Good
        } else {
          qualityElem.style.color = '#ef4444'; // Poor
        }
      }
    }
    
    // Update link quality
    const linkQualityElem = document.getElementById('wifi-link-quality');
    if (linkQualityElem) {
      linkQualityElem.textContent = details.link_quality || 'N/A';
    }
    
    // Update bit rate
    const bitrateElem = document.getElementById('wifi-bitrate');
    if (bitrateElem) {
      bitrateElem.textContent = details.bit_rate || 'N/A';
    }
  }
  
  showContent('wifi-info-loading', 'wifi-info-container');
}

// Update system information
function updateSystemInfo(info) {
  if (!info) return;
  
  const hostnameElem = document.getElementById('hostname');
  if (hostnameElem) hostnameElem.textContent = info.hostname || '--';
  
  const piModelElem = document.getElementById('pi-model');
  if (piModelElem) piModelElem.textContent = info.pi_model || '--';
  
  const osElem = document.getElementById('os-info');
  if (osElem) osElem.textContent = info.os || '--';
  
  const archElem = document.getElementById('architecture');
  if (archElem) archElem.textContent = info.architecture || '--';
  
  const coresElem = document.getElementById('cpu-cores');
  if (coresElem) {
    coresElem.textContent = info.cpu_threads ? 
      `${info.cpu_cores || 0} (${info.cpu_threads} threads)` : 
      (info.cpu_cores || '--');
  }
  
  const bootTimeElem = document.getElementById('boot-time');
  if (bootTimeElem) bootTimeElem.textContent = info.boot_time || '--';
  
  showContent('system-info-loading', 'system-info-grid');
}

// Update network statistics
function updateNetworkStats(stats) {
  if (!stats) return;
  
  const bytesSentElem = document.getElementById('bytes-sent');
  if (bytesSentElem) {
    bytesSentElem.textContent = stats.bytes_sent ? 
      `${stats.bytes_sent} MB` : '-- MB';
  }
  
  const bytesRecvElem = document.getElementById('bytes-recv');
  if (bytesRecvElem) {
    bytesRecvElem.textContent = stats.bytes_recv ? 
      `${stats.bytes_recv} MB` : '-- MB';
  }
  
  const connectionsElem = document.getElementById('active-connections');
  if (connectionsElem) {
    connectionsElem.textContent = stats.active_connections || '--';
  }
  
  showContent('network-stats-loading', 'network-stats-grid');
}

// Fetch system information (fast, cached)
async function fetchSystemInfo() {
  try {
    const res = await fetch(`${API_BASE}/api/system/system-info`);
    if (!res.ok) throw new Error('Failed to fetch system info');
    const data = await res.json();
    updateSystemInfo(data);
  } catch (error) {
    console.error('Error fetching system info:', error);
    const loading = document.getElementById('system-info-loading');
    if (loading) loading.innerHTML = '<span style="color: #ef4444;">Failed to load</span>';
  }
}

// Fetch network statistics (fast)
async function fetchNetworkStats() {
  try {
    const res = await fetch(`${API_BASE}/api/system/network-stats`);
    if (!res.ok) throw new Error('Failed to fetch network stats');
    const data = await res.json();
    updateNetworkStats(data);
    
    // Update network interfaces
    if (data.interfaces) {
      updateNetworkInterfaces(data.interfaces);
    }
  } catch (error) {
    console.error('Error fetching network stats:', error);
    const loading = document.getElementById('network-stats-loading');
    if (loading) loading.innerHTML = '<span style="color: #ef4444;">Failed to load</span>';
  }
}

// Fetch WiFi details (moderate speed)
async function fetchWiFiDetails() {
  try {
    const res = await fetch(`${API_BASE}/api/system/wifi-details`);
    if (!res.ok) throw new Error('Failed to fetch WiFi details');
    const data = await res.json();
    updateWiFiInfo(data);
  } catch (error) {
    console.error('Error fetching WiFi details:', error);
    const loading = document.getElementById('wifi-info-loading');
    if (loading) loading.innerHTML = '<span style="color: #ef4444;">Failed to load</span>';
  }
}

// Fetch public IP (slow, separate call)
async function fetchPublicIP() {
  try {
    const res = await fetch(`${API_BASE}/api/system/network/public-ip`);
    if (!res.ok) throw new Error('Failed to fetch public IP');
    const data = await res.json();
    
    const publicIpElem = document.getElementById('public-ip');
    if (publicIpElem && data.ip) {
      publicIpElem.textContent = data.ip;
    }
  } catch (error) {
    console.error('Error fetching public IP:', error);
    const publicIpElem = document.getElementById('public-ip');
    if (publicIpElem) {
      publicIpElem.textContent = 'N/A';
    }
  }
}

// Fetch all data in parallel
async function fetchAllData() {
  const startTime = performance.now();
  
  // Clear any previous errors
  clearError();
  
  // Fetch all APIs in parallel for maximum speed
  await Promise.all([
    fetchSystemInfo(),
    fetchNetworkStats(),
    fetchWiFiDetails(),
    fetchPublicIP()
  ]);
  
  const endTime = performance.now();
  console.log(`Configuration page loaded in ${Math.round(endTime - startTime)}ms`);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  // Fetch all data immediately
  fetchAllData();
  
  // Refresh every 10 seconds (except system info which is cached longer)
  setInterval(() => {
    fetchNetworkStats();
    fetchWiFiDetails();
    fetchPublicIP();
  }, 10000);
  
  // Refresh system info less frequently (every 60 seconds)
  setInterval(fetchSystemInfo, 60000);
});
