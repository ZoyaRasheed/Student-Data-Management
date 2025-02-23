
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
    },
    teacherSIgnup: async(formData) =>{
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.AUTH}/?type=signup_teacher`,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
                
            });
            if (!response.ok) throw new Error('Sign up failed');
            return await response.json();

        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }
};

export default apiService;
