// Tools page JavaScript

// API_BASE is defined in dashboard.js (loaded from base template)

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

// Perform system action
async function performAction(action, dangerous = false) {
  if (dangerous) {
    const confirmMsg = action === 'reboot' 
      ? 'Are you sure you want to reboot the system?' 
      : 'Are you sure you want to shutdown the system?';
    
    if (!confirm(confirmMsg)) {
      return;
    }
  }
  
  try {
    const response = await fetch(`${API_BASE}/api/tools/action/${action}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ confirmed: true })
    });
    
    const data = await response.json();
    
    if (data.success) {
      showSuccess(data.message);
      
      if (action === 'reboot' || action === 'shutdown') {
        setTimeout(() => {
          document.body.innerHTML = `
            <div style="text-align: center; padding: 3rem; font-size: 1.2rem;">
              <h2>${action === 'reboot' ? 'System Rebooting...' : 'System Shutting Down...'}</h2>
              <p>Please wait...</p>
            </div>
          `;
        }, 1000);
      }
    } else {
      showError(data.error || 'Action failed');
    }
  } catch (error) {
    showError('Failed to execute action: ' + error.message);
  }
}

// Run diagnostics
async function runDiagnostics() {
  const resultsDiv = document.getElementById('diagnostics-results');
  resultsDiv.style.display = 'block';
  
  try {
    const response = await fetch(`${API_BASE}/api/tools/diagnostics`);
    const data = await response.json();
    
    // Update system health
    if (data.system) {
      document.getElementById('diag-system-status').textContent = 
        data.system.responsive ? '✅ Responsive' : '❌ Not Responsive';
      document.getElementById('diag-system-load').textContent = 
        data.system.load_average || 'N/A';
    }
    
    // Update services
    const servicesDiv = document.getElementById('diag-services');
    servicesDiv.innerHTML = '';
    if (data.services) {
      Object.entries(data.services).forEach(([service, info]) => {
        const item = document.createElement('div');
        item.className = 'diagnostic-item';
        item.innerHTML = `
          <span class="diagnostic-label">${service}:</span>
          <span class="diagnostic-value">${info.healthy ? '✅' : '❌'} ${info.status}</span>
        `;
        servicesDiv.appendChild(item);
      });
    }
    
    // Update connectivity
    if (data.connectivity) {
      document.getElementById('diag-internet').textContent = 
        data.connectivity.internet ? '✅ Connected' : '❌ No Connection';
      document.getElementById('diag-dns').textContent = 
        data.connectivity.dns ? '✅ Working' : '❌ Failed';
    }
    
    // Update storage
    if (data.storage && data.storage.root) {
      document.getElementById('diag-storage-total').textContent = data.storage.root.total;
      document.getElementById('diag-storage-used').textContent = data.storage.root.used;
      document.getElementById('diag-storage-avail').textContent = data.storage.root.available;
    }
    
    showSuccess('Diagnostics complete');
  } catch (error) {
    showError('Failed to run diagnostics: ' + error.message);
  }
}

// Execute terminal command
async function executeCommand() {
  const input = document.getElementById('terminal-input');
  const output = document.getElementById('terminal-output');
  const command = input.value.trim();
  
  if (!command) {
    showError('Please enter a command');
    return;
  }
  
  // Add command to output
  const cmdLine = document.createElement('div');
  cmdLine.className = 'terminal-line';
  cmdLine.innerHTML = `<span class="terminal-prompt">$</span> ${command}`;
  output.appendChild(cmdLine);
  
  try {
    const response = await fetch(`${API_BASE}/api/tools/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command })
    });
    
    const data = await response.json();
    
    const resultDiv = document.createElement('div');
    resultDiv.className = 'terminal-output-block';
    
    if (data.success) {
      if (data.stdout) {
        resultDiv.innerHTML += `<pre class="terminal-stdout">${escapeHtml(data.stdout)}</pre>`;
      }
      if (data.stderr) {
        resultDiv.innerHTML += `<pre class="terminal-stderr">${escapeHtml(data.stderr)}</pre>`;
      }
      if (!data.stdout && !data.stderr) {
        resultDiv.innerHTML = '<span class="terminal-info">Command executed successfully (no output)</span>';
      }
    } else {
      resultDiv.innerHTML = `<span class="terminal-error">Error: ${data.error}</span>`;
      if (data.message) {
        resultDiv.innerHTML += `<br><span class="terminal-info">${data.message}</span>`;
      }
    }
    
    output.appendChild(resultDiv);
    output.scrollTop = output.scrollHeight;
    
    input.value = '';
  } catch (error) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'terminal-error';
    errorDiv.textContent = 'Request failed: ' + error.message;
    output.appendChild(errorDiv);
  }
}

// Load service logs
async function loadServiceLogs() {
  const service = document.getElementById('service-selector').value;
  const logsDiv = document.getElementById('quick-logs');
  const content = document.getElementById('logs-content');
  
  logsDiv.style.display = 'block';
  content.textContent = 'Loading logs...';
  
  try {
    const response = await fetch(`${API_BASE}/api/tools/logs/${service}?lines=50`);
    const data = await response.json();
    
    if (data.success) {
      content.textContent = data.logs || 'No logs available';
    } else {
      content.textContent = `Error: ${data.error}`;
    }
  } catch (error) {
    content.textContent = 'Failed to load logs: ' + error.message;
  }
}

// Escape HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Enter key support for terminal
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('terminal-input');
  if (input) {
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        executeCommand();
      }
    });
  }
});

