import apiService from './api/services.js';

document.addEventListener('DOMContentLoaded', async () => {
  const statusIndicator = document.querySelector('.status-indicator');
  const statusText = document.querySelector('.status-text');
  console.log(statusText);
  

  try {
    const healthStatus = await apiService.healthCheck();
    console.log(healthStatus);
    
    if (healthStatus && healthStatus.success) {
      statusIndicator.classList.remove('error');
      statusIndicator.classList.add('active');
      statusText.textContent = `${healthStatus.message} - Version: ${healthStatus.version}`;
    } else {
      statusIndicator.classList.remove('active');
      statusIndicator.classList.add('error');
      statusText.textContent = 'System issues detected';
    }
  } catch (error) {
    statusIndicator.classList.remove('active');
    statusIndicator.classList.add('error');
    statusText.textContent = 'System error - Could not connect';
  }
});