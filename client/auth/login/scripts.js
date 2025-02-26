import apiService from '../../api/services.js';

document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
  
    try {
      const response = await apiService.studentLogin(
        { email, password }
      )
      
      if (response.success) {
        localStorage.setItem('token', response.token);
        alert('Login successful!');
        window.location.href = 'home/index.html';
      } else {
        alert(data.message || 'Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  });