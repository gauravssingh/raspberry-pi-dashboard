/**
 * GPIO Control JavaScript
 * Handles GPIO pin control interface
 */

// API Base URL for GPIO endpoints
// Use existing API_BASE from dashboard.js if available, otherwise use GPIO-specific path
const GPIO_API_BASE = (typeof API_BASE !== 'undefined' ? API_BASE : '') + '/api/gpio';

// Toast notification utility - fixed position, won't shift layout
function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? '✓' : type === 'error' ? '⚠️' : 'ℹ️';
    toast.innerHTML = `<strong>${icon}</strong> ${message}`;
    
    // Add to container
    container.appendChild(toast);
    
    // Auto-remove after duration
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300); // Wait for animation to finish
    }, duration);
}

// Error display utility
function showError(message) {
    showToast(message, 'error', 5000);
}

// Success message utility
function showSuccess(message) {
    showToast(message, 'success', 3000);
}

// Info message utility
function showInfo(message) {
    showToast(message, 'info', 3000);
}

// Get type badge HTML
function getTypeBadge(type) {
    return `<span class="gpio-type-badge gpio-type-${type}">${type}</span>`;
}

// Get status indicator HTML
function getStatusIndicator(state) {
    const stateClass = state === 1 ? 'high' : 'low';
    const stateText = state === 1 ? 'HIGH' : 'LOW';
    
    return `
        <div class="gpio-status">
            <div class="status-indicator ${stateClass}"></div>
            <span class="status-text ${stateClass}">${stateText}</span>
        </div>
    `;
}

// Create GPIO card HTML
function createGPIOCard(pin) {
    const isChecked = pin.state === 1 ? 'checked' : '';
    
    return `
        <div class="gpio-card" data-pin-id="${pin.id}">
            <div class="gpio-header">
                <div class="gpio-name">${pin.name}</div>
                ${getTypeBadge(pin.type)}
            </div>
            <div class="gpio-info">GPIO ${pin.gpio_number} • ${pin.direction.toUpperCase()}</div>
            <div class="gpio-description">${pin.description}</div>
            <div class="gpio-controls">
                <div class="gpio-status-container">
                    ${getStatusIndicator(pin.state)}
                </div>
                <label class="toggle-switch">
                    <input type="checkbox" ${isChecked} onchange="toggleGPIO('${pin.id}')" data-pin-id="${pin.id}">
                    <span class="toggle-slider"></span>
                </label>
            </div>
        </div>
    `;
}

// Update pin state in UI
function updatePinState(pinId, state) {
    const card = document.querySelector(`[data-pin-id="${pinId}"]`);
    if (!card) return;
    
    // Update toggle switch
    const toggle = card.querySelector('input[type="checkbox"]');
    if (toggle) {
        toggle.checked = state === 1;
    }
    
    // Update status indicator
    const statusContainer = card.querySelector('.gpio-status-container');
    if (statusContainer) {
        statusContainer.innerHTML = getStatusIndicator(state);
    }
}

// Toggle GPIO pin
async function toggleGPIO(pinId) {
    const toggle = document.querySelector(`input[data-pin-id="${pinId}"]`);
    if (!toggle) return;
    
    // Get desired state from toggle
    const desiredState = toggle.checked ? 1 : 0;
    
    // Disable toggle during request
    toggle.disabled = true;
    
    try {
        const response = await fetch(`${GPIO_API_BASE}/pin/${pinId}/set`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ state: desiredState })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to toggle GPIO');
        }
        
        if (data.success) {
            // Update UI with actual state from server
            updatePinState(pinId, data.state);
            showSuccess(`${pinId} set to ${data.state_name}`);
        } else {
            throw new Error(data.error || 'Unknown error');
        }
        
    } catch (error) {
        console.error('Error toggling GPIO:', error);
        showError(error.message);
        
        // Revert toggle to previous state
        toggle.checked = !toggle.checked;
    } finally {
        // Re-enable toggle
        toggle.disabled = false;
    }
}

// Load and display GPIO pins
async function loadGPIOPins() {
    const container = document.getElementById('gpio-container');
    if (!container) {
        console.error('GPIO container not found');
        return;
    }
    
    try {
        console.log('Loading GPIO pins from', `${GPIO_API_BASE}/pins`);
        const response = await fetch(`${GPIO_API_BASE}/pins`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('GPIO pins response:', data);
        
        if (!data.success) {
            throw new Error(data.error || 'Failed to load GPIO pins');
        }
        
        if (!data.grouped) {
            throw new Error('Invalid response format: missing grouped data');
        }
        
        // Clear loading message
        container.innerHTML = '';
        
        // Check if any pins configured
        if (Object.keys(data.grouped).length === 0) {
            container.innerHTML = `
                <div class="info-box warning" style="text-align: center;">
                    <p><strong>No GPIO pins configured</strong></p>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                        Add pin configurations to <code>configs/gpio_config.json</code> to get started.
                    </p>
                </div>
            `;
            return;
        }
        
        // Create groups
        for (const [groupName, pins] of Object.entries(data.grouped)) {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'gpio-group';
            
            const groupTitle = document.createElement('h2');
            groupTitle.className = 'gpio-group-title';
            groupTitle.textContent = groupName;
            
            const gridDiv = document.createElement('div');
            gridDiv.className = 'gpio-grid';
            
            pins.forEach(pin => {
                gridDiv.innerHTML += createGPIOCard(pin);
            });
            
            groupDiv.appendChild(groupTitle);
            groupDiv.appendChild(gridDiv);
            container.appendChild(groupDiv);
        }
        
        console.log('GPIO pins loaded successfully');
        
    } catch (error) {
        console.error('Error loading GPIO pins:', error);
        const container = document.getElementById('gpio-container');
        if (container) {
            container.innerHTML = `
                <div class="info-box warning" style="text-align: center;">
                    <p><strong>⚠️ Error loading GPIO configuration</strong></p>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem;">${error.message}</p>
                    <p style="margin-top: 0.5rem; font-size: 0.8rem;">Check browser console for details.</p>
                </div>
            `;
        }
        showError(`Failed to load GPIO pins: ${error.message}`);
    }
}

// Load GPIO mode/config info
async function loadGPIOMode() {
    const modeIndicator = document.getElementById('gpio-mode');
    if (!modeIndicator) return;
    
    try {
        const response = await fetch(`${GPIO_API_BASE}/config`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load GPIO config');
        }
        
        if (data.success) {
            const mode = data.mode === 'hardware' ? '🔧 Hardware Mode' : '🖥️  Simulation Mode';
            const gpiodStatus = data.gpiod_available ? '✓ gpiod available' : '⚠️ gpiod not available';
            
            modeIndicator.innerHTML = `${mode} • ${gpiodStatus}`;
            
            // Add warning if in simulation mode
            if (data.mode === 'simulation') {
                const container = document.getElementById('gpio-container');
                if (container) {
                    const warning = document.createElement('div');
                    warning.className = 'info-box warning';
                    warning.style.textAlign = 'center';
                    warning.style.marginBottom = '2rem';
                    warning.innerHTML = `
                        <p><strong>⚠️ Running in Simulation Mode</strong></p>
                        <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                            GPIO hardware not detected. Controls will simulate pin changes without affecting actual GPIO pins.
                        </p>
                    `;
                    container.insertBefore(warning, container.firstChild);
                }
            }
        }
        
    } catch (error) {
        console.error('Error loading GPIO mode:', error);
        modeIndicator.innerHTML = 'Error loading status';
    }
}

// Auto-refresh pin states
let refreshInterval = null;

function startAutoRefresh(intervalSeconds = 5) {
    stopAutoRefresh();
    
    refreshInterval = setInterval(async () => {
        try {
            const response = await fetch(`${GPIO_API_BASE}/pins`);
            const data = await response.json();
            
            if (data.success && data.pins) {
                data.pins.forEach(pin => {
                    updatePinState(pin.id, pin.state);
                });
            }
        } catch (error) {
            console.error('Error refreshing pin states:', error);
        }
    }, intervalSeconds * 1000);
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

// Initialize GPIO controls
async function initGPIOControls() {
    console.log('Initializing GPIO controls...');
    try {
        await loadGPIOMode();
        await loadGPIOPins();
        
        // Start auto-refresh every 5 seconds
        startAutoRefresh(5);
        console.log('GPIO controls initialized successfully');
    } catch (error) {
        console.error('Error initializing GPIO controls:', error);
        showError(`Failed to initialize GPIO controls: ${error.message}`);
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopAutoRefresh();
});

// Make functions globally available
window.toggleGPIO = toggleGPIO;
window.initGPIOControls = initGPIOControls;
window.loadGPIOPins = loadGPIOPins;
window.loadGPIOMode = loadGPIOMode;
window.startAutoRefresh = startAutoRefresh;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGPIOControls);
} else {
    // DOM is already ready
    initGPIOControls();
}

