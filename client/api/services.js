import { API_BASE_URL, ENDPOINTS } from './config.js';

const apiService = {
    // Health Check
    healthCheck: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.HEALTH_CHECK}`);
            if (!response.ok) throw new Error('Health check failed');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Teacher Signup
    teacherSignup: async (formData) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.AUTH}/?type=signup_teacher`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Student Signup
    studentSignup: async (formData) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.AUTH}/?type=signup_student`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Teacher Login
    teacherLogin: async (credentials) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.AUTH}/?type=teacher_login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Student Login
    studentLogin: async (credentials) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.AUTH}/?type=student_login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Self Identification
    selfIdentification: async (token) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.AUTH}/?type=self_identification`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Add Student Marks
    addStudentMarks: async (token, marksData) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.TEACHER_SERVICE}/?type=add_marks`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(marksData),
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Get Student Marks
    getStudentMarks: async (token) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.TEACHER_SERVICE}/?type=get_student_marks`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },

    // Update Student Marks
    updateStudentMarks: async (token, updateData) => {
        try {
            const response = await fetch(`${API_BASE_URL}${ENDPOINTS.TEACHER_SERVICE}/?type=update_student_marks`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData),
            });
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    },
};

export default apiService;