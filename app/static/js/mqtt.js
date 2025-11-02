/**
 * MQTT/IoT Device Control JavaScript
 * Handles Tasmota ESP32 device control via MQTT
 */

// Global state
let mqttConnected = false;
let devices = [];
let currentDeviceTopic = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  loadMQTTStatus();
  
  // Set up event listeners
  document.getElementById('connect-btn').addEventListener('click', connectToMQTT);
  document.getElementById('disconnect-btn').addEventListener('click', disconnectFromMQTT);
  document.getElementById('config-btn').addEventListener('click', openConfigModal);
  document.getElementById('add-device-btn').addEventListener('click', openAddDeviceModal);
  document.getElementById('mqtt-config-form').addEventListener('submit', saveConfiguration);
  document.getElementById('add-device-form').addEventListener('submit', addDevice);
  
  // Auto-refresh status every 5 seconds
  setInterval(loadMQTTStatus, 5000);
});

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  
  container.appendChild(toast);
  
  // Remove after 4 seconds
  setTimeout(() => {
    toast.style.animation = 'slideIn 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

/**
 * Load MQTT connection status
 */
async function loadMQTTStatus() {
  try {
    const response = await fetch('/api/mqtt/status');
    const data = await response.json();
    
    if (data.success) {
      mqttConnected = data.connected;
      updateStatusUI(data);
      
      if (mqttConnected) {
        loadDevices();
      }
    }
  } catch (error) {
    console.error('Error loading MQTT status:', error);
  }
}

/**
 * Update status UI
 */
function updateStatusUI(status) {
  const indicator = document.getElementById('mqtt-status-indicator');
  const statusText = document.getElementById('mqtt-status-text');
  const brokerInfo = document.getElementById('mqtt-broker-info');
  const connectBtn = document.getElementById('connect-btn');
  const disconnectBtn = document.getElementById('disconnect-btn');
  
  if (status.connected) {
    indicator.textContent = '🟢';
    statusText.textContent = 'Connected';
    brokerInfo.textContent = `${status.broker.host}:${status.broker.port} • ${status.device_count} device(s)`;
    connectBtn.disabled = true;
    disconnectBtn.disabled = false;
  } else {
    indicator.textContent = '🔴';
    statusText.textContent = 'Disconnected';
    
    if (status.broker && status.broker.host) {
      brokerInfo.textContent = `${status.broker.host}:${status.broker.port}`;
    } else {
      brokerInfo.textContent = 'Not configured';
    }
    
    connectBtn.disabled = false;
    disconnectBtn.disabled = true;
  }
}

/**
 * Connect to MQTT broker
 */
async function connectToMQTT() {
  try {
    showToast('Connecting to MQTT broker...', 'info');
    
    const response = await fetch('/api/mqtt/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast('Connected to MQTT broker!', 'success');
      loadMQTTStatus();
    } else {
      showToast(`Connection failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error connecting to MQTT:', error);
    showToast('Failed to connect to MQTT broker', 'error');
  }
}

/**
 * Disconnect from MQTT broker
 */
async function disconnectFromMQTT() {
  try {
    const response = await fetch('/api/mqtt/disconnect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast('Disconnected from MQTT broker', 'info');
      loadMQTTStatus();
      
      // Clear devices display
      const grid = document.getElementById('devices-grid');
      grid.innerHTML = '<div class="loading-message">Connect to MQTT broker to view devices...</div>';
    } else {
      showToast(`Disconnect failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error disconnecting from MQTT:', error);
    showToast('Failed to disconnect from MQTT broker', 'error');
  }
}

/**
 * Load devices
 */
async function loadDevices() {
  try {
    const response = await fetch('/api/mqtt/devices');
    const data = await response.json();
    
    if (data.success) {
      devices = data.devices;
      renderDevices(devices);
    }
  } catch (error) {
    console.error('Error loading devices:', error);
  }
}

/**
 * Render devices grid
 */
function renderDevices(devices) {
  const grid = document.getElementById('devices-grid');
  
  if (devices.length === 0) {
    grid.innerHTML = '<div class="loading-message">No devices configured. Click "Add Device" to get started.</div>';
    return;
  }
  
  grid.innerHTML = '';
  
  devices.forEach(device => {
    const card = createDeviceCard(device);
    grid.appendChild(card);
  });
}

/**
 * Create device card element
 */
function createDeviceCard(device) {
  const card = document.createElement('div');
  card.className = `device-card ${device.online ? '' : 'offline'}`;
  
  const statusClass = device.online ? 'online' : 'offline';
  const statusText = device.online ? 'Online' : 'Offline';
  
  // Get device type icon
  const typeIcons = {
    'switch': '🔌',
    'light': '💡',
    'rgb': '🌈',
    'sensor': '📊',
    'generic': '📡'
  };
  const typeIcon = typeIcons[device.device_type] || '📡';
  
  card.innerHTML = `
    <div class="device-header">
      <div>
        <div class="device-name">${typeIcon} ${device.name}</div>
        <div class="device-topic">${device.topic}</div>
        <span class="device-type-badge">${device.device_type}</span>
      </div>
      <span class="device-status ${statusClass}">${statusText}</span>
    </div>
    <div class="device-info">
      ${device.last_seen ? `Last seen: ${new Date(device.last_seen * 1000).toLocaleString()}` : 'Never seen'}
    </div>
    <div class="device-actions">
      <button class="btn btn-success btn-small" onclick="controlPower('${device.topic}', 'on')" ${!device.online ? 'disabled' : ''}>
        ON
      </button>
      <button class="btn btn-danger btn-small" onclick="controlPower('${device.topic}', 'off')" ${!device.online ? 'disabled' : ''}>
        OFF
      </button>
      <button class="btn btn-warning btn-small" onclick="controlPower('${device.topic}', 'toggle')" ${!device.online ? 'disabled' : ''}>
        TOGGLE
      </button>
      <button class="btn btn-secondary btn-small" onclick="openControlModal('${device.topic}')" ${!device.online ? 'disabled' : ''}>
        More...
      </button>
      <button class="btn btn-secondary btn-small" onclick="removeDevice('${device.topic}')">
        🗑️
      </button>
    </div>
  `;
  
  return card;
}

/**
 * Control device power
 */
async function controlPower(deviceTopic, action) {
  try {
    const response = await fetch(`/api/mqtt/power/${deviceTopic}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast(`Power ${action} command sent`, 'success');
      // Refresh devices after a short delay
      setTimeout(loadDevices, 1000);
    } else {
      showToast(`Failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error controlling power:', error);
    showToast('Failed to send command', 'error');
  }
}

/**
 * Open configuration modal
 */
async function openConfigModal() {
  try {
    const response = await fetch('/api/mqtt/config');
    const data = await response.json();
    
    if (data.success) {
      const config = data.config;
      
      document.getElementById('broker-host').value = config.broker.host || 'localhost';
      document.getElementById('broker-port').value = config.broker.port || 1883;
      document.getElementById('broker-username').value = config.broker.username || '';
      document.getElementById('broker-password').value = config.broker.password || '';
      
      document.getElementById('config-modal').style.display = 'flex';
    }
  } catch (error) {
    console.error('Error loading config:', error);
    showToast('Failed to load configuration', 'error');
  }
}

/**
 * Close configuration modal
 */
function closeConfigModal() {
  document.getElementById('config-modal').style.display = 'none';
}

/**
 * Save configuration
 */
async function saveConfiguration(e) {
  e.preventDefault();
  
  const config = {
    broker: {
      host: document.getElementById('broker-host').value,
      port: parseInt(document.getElementById('broker-port').value),
      username: document.getElementById('broker-username').value,
      password: document.getElementById('broker-password').value,
      auto_connect: true
    },
    devices: devices.map(d => ({
      name: d.name,
      topic: d.topic,
      device_type: d.device_type,
      description: ''
    })),
    settings: {
      discovery_enabled: true,
      retain_messages: false,
      qos: 1
    }
  };
  
  try {
    const response = await fetch('/api/mqtt/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast('Configuration saved successfully', 'success');
      closeConfigModal();
      loadMQTTStatus();
    } else {
      showToast(`Failed to save: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error saving config:', error);
    showToast('Failed to save configuration', 'error');
  }
}

/**
 * Open add device modal
 */
function openAddDeviceModal() {
  document.getElementById('add-device-form').reset();
  document.getElementById('add-device-modal').style.display = 'flex';
}

/**
 * Close add device modal
 */
function closeAddDeviceModal() {
  document.getElementById('add-device-modal').style.display = 'none';
}

/**
 * Add new device
 */
async function addDevice(e) {
  e.preventDefault();
  
  const deviceData = {
    name: document.getElementById('device-name').value,
    topic: document.getElementById('device-topic').value,
    device_type: document.getElementById('device-type').value,
    description: document.getElementById('device-description').value
  };
  
  try {
    const response = await fetch('/api/mqtt/devices', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(deviceData)
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast(`Device "${deviceData.name}" added successfully`, 'success');
      closeAddDeviceModal();
      loadDevices();
    } else {
      showToast(`Failed to add device: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error adding device:', error);
    showToast('Failed to add device', 'error');
  }
}

/**
 * Remove device
 */
async function removeDevice(deviceTopic) {
  if (!confirm('Are you sure you want to remove this device?')) {
    return;
  }
  
  try {
    const response = await fetch(`/api/mqtt/devices/${deviceTopic}`, {
      method: 'DELETE'
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast('Device removed successfully', 'success');
      loadDevices();
    } else {
      showToast(`Failed to remove device: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error removing device:', error);
    showToast('Failed to remove device', 'error');
  }
}

/**
 * Open device control modal
 */
function openControlModal(deviceTopic) {
  currentDeviceTopic = deviceTopic;
  const device = devices.find(d => d.topic === deviceTopic);
  
  if (!device) return;
  
  document.getElementById('control-device-name').textContent = device.name;
  
  // Generate control options based on device type
  let controlHTML = '';
  
  if (device.device_type === 'light' || device.device_type === 'rgb') {
    controlHTML = `
      <div class="form-group">
        <label>Dimmer Level (0-100%):</label>
        <input type="range" id="dimmer-slider" min="0" max="100" value="50" style="width: 100%;">
        <div style="text-align: center; margin-top: 0.5rem;">
          <span id="dimmer-value">50</span>%
        </div>
        <button class="btn btn-primary" onclick="setDimmer()" style="width: 100%; margin-top: 0.5rem;">Set Dimmer</button>
      </div>
    `;
  }
  
  if (device.device_type === 'rgb') {
    controlHTML += `
      <div class="form-group" style="margin-top: 1rem;">
        <label>RGB Color:</label>
        <input type="color" id="color-picker" value="#ffffff" style="width: 100%; height: 50px; cursor: pointer;">
        <button class="btn btn-primary" onclick="setColor()" style="width: 100%; margin-top: 0.5rem;">Set Color</button>
      </div>
    `;
  }
  
  controlHTML += `
    <div class="form-group" style="margin-top: 1rem;">
      <label>Advanced Commands:</label>
      <button class="btn btn-secondary" onclick="requestStatus()" style="width: 100%; margin-bottom: 0.5rem;">Request Status</button>
      <button class="btn btn-warning" onclick="restartDevice()" style="width: 100%;">Restart Device</button>
    </div>
  `;
  
  document.getElementById('control-content').innerHTML = controlHTML;
  
  // Add event listener for dimmer slider
  const dimmerSlider = document.getElementById('dimmer-slider');
  if (dimmerSlider) {
    dimmerSlider.addEventListener('input', function() {
      document.getElementById('dimmer-value').textContent = this.value;
    });
  }
  
  document.getElementById('device-control-modal').style.display = 'flex';
}

/**
 * Close control modal
 */
function closeControlModal() {
  document.getElementById('device-control-modal').style.display = 'none';
  currentDeviceTopic = null;
}

/**
 * Set dimmer level
 */
async function setDimmer() {
  const level = document.getElementById('dimmer-slider').value;
  
  try {
    const response = await fetch(`/api/mqtt/dimmer/${currentDeviceTopic}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ level: parseInt(level) })
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast(`Dimmer set to ${level}%`, 'success');
    } else {
      showToast(`Failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error setting dimmer:', error);
    showToast('Failed to set dimmer', 'error');
  }
}

/**
 * Set RGB color
 */
async function setColor() {
  const color = document.getElementById('color-picker').value;
  
  try {
    const response = await fetch(`/api/mqtt/color/${currentDeviceTopic}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ color })
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast(`Color set to ${color}`, 'success');
    } else {
      showToast(`Failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error setting color:', error);
    showToast('Failed to set color', 'error');
  }
}

/**
 * Request device status
 */
async function requestStatus() {
  try {
    const response = await fetch(`/api/mqtt/status/${currentDeviceTopic}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 0 })
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast('Status request sent', 'info');
    } else {
      showToast(`Failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error requesting status:', error);
    showToast('Failed to request status', 'error');
  }
}

/**
 * Restart device
 */
async function restartDevice() {
  if (!confirm('Are you sure you want to restart this device?')) {
    return;
  }
  
  try {
    const response = await fetch(`/api/mqtt/restart/${currentDeviceTopic}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    const data = await response.json();
    
    if (data.success) {
      showToast('Restart command sent', 'warning');
      closeControlModal();
    } else {
      showToast(`Failed: ${data.error}`, 'error');
    }
  } catch (error) {
    console.error('Error restarting device:', error);
    showToast('Failed to restart device', 'error');
  }
}

// Close modals when clicking outside
window.onclick = function(event) {
  const configModal = document.getElementById('config-modal');
  const addDeviceModal = document.getElementById('add-device-modal');
  const controlModal = document.getElementById('device-control-modal');
  
  if (event.target === configModal) {
    closeConfigModal();
  } else if (event.target === addDeviceModal) {
    closeAddDeviceModal();
  } else if (event.target === controlModal) {
    closeControlModal();
  }
};

