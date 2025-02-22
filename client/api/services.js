// apiService.js
import { API_BASE_URL, ENDPOINTS } from './config.js';

const apiService = {
    healthCheck: async() =>{
        try {
        const response = await fetch(`${API_BASE_URL}${ENDPOINTS.HEALTH_CHECK}`);
        
        if (!response.ok) throw new Error('Health check failed');
        return await response.json();
        } catch (error) {
        console.error('Error:', error);
        return null;
        }
    }
};

export default apiService;
