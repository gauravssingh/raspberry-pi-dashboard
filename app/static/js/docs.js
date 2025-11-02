// Documentation page JavaScript

// Show specific documentation section
function showSection(sectionId) {
  // Hide all sections
  document.querySelectorAll('.docs-content-section').forEach(section => {
    section.style.display = 'none';
  });
  
  // Remove active class from all nav buttons
  document.querySelectorAll('.docs-nav-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  
  // Show selected section
  const section = document.getElementById(`section-${sectionId}`);
  if (section) {
    section.style.display = 'block';
  }
  
  // Add active class to clicked button
  event.target.closest('.docs-nav-btn').classList.add('active');
  
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Copy code examples to clipboard
function copyCode(button) {
  const codeBlock = button.nextElementSibling;
  if (codeBlock) {
    const text = codeBlock.textContent;
    navigator.clipboard.writeText(text).then(() => {
      const originalText = button.textContent;
      button.textContent = '✓ Copied!';
      setTimeout(() => {
        button.textContent = originalText;
      }, 2000);
    });
  }
}

// Test API endpoint
async function testEndpoint(endpoint) {
  const resultDiv = document.getElementById(`result-${endpoint}`);
  if (!resultDiv) return;
  
  resultDiv.innerHTML = '<span class="loading">Testing...</span>';
  
  try {
    const response = await fetch(endpoint);
    const data = await response.json();
    
    resultDiv.innerHTML = `
      <div class="api-result success">
        <strong>Status:</strong> ${response.status} ${response.statusText}<br>
        <strong>Response:</strong>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      </div>
    `;
  } catch (error) {
    resultDiv.innerHTML = `
      <div class="api-result error">
        <strong>Error:</strong> ${error.message}
      </div>
    `;
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Add copy buttons to code blocks
  document.querySelectorAll('code').forEach(codeBlock => {
    if (codeBlock.textContent.length > 20) {
      const button = document.createElement('button');
      button.className = 'copy-btn';
      button.textContent = '📋 Copy';
      button.onclick = function() { copyCode(this); };
      
      codeBlock.parentNode.insertBefore(button, codeBlock);
    }
  });
  
  // Highlight current section in URL hash
  const hash = window.location.hash.substring(1);
  if (hash) {
    const sectionBtn = document.querySelector(`[onclick="showSection('${hash}')"]`);
    if (sectionBtn) {
      sectionBtn.click();
    }
  }
});

// Handle hash changes
window.addEventListener('hashchange', () => {
  const hash = window.location.hash.substring(1);
  if (hash) {
    showSection(hash);
  }
});

