document.addEventListener('DOMContentLoaded', () => {
  // Sign up
  const signupForm = document.querySelector('.form_signup');
  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const firstName = document.getElementById('firstName').value;
      const lastName = document.getElementById('lastName').value;
      const email = document.querySelector('.form_signup input[type="email"]').value;
      const password = document.querySelector('.form_signup input[type="password"]').value;
      const confirmPassword = document.getElementById('confirmPassword').value;

      // Check if passwords match
      if (password !== confirmPassword) {
        displayMessage('Passwords do not match.', 'error');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:3001/signup', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ firstName, lastName, email, password }),
        });

        const data = await response.json();
        if (response.ok) {
          displayMessage(data.message, 'success');
          // Redirect to a different page or clear the form
        } else {
          displayMessage(data.message, 'error');
        }
      } catch (err) {
        console.error(err);
        displayMessage('An error occurred. Please try again.', 'error');
      }
    });
  }

  // Login
  const loginForm = document.querySelector('.form_login');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.querySelector('.form_login input[type="email"]').value;
      const password = document.querySelector('.form_login input[type="password"]').value;

      try {
        const response = await fetch('http://127.0.0.1:3001/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        if (response.ok) {
          displayMessage(data.message, 'success');
          // Redirect to a different page or clear the form
        } else {
          displayMessage(data.message, 'error');
        }
      } catch (err) {
        console.error(err);
        displayMessage('An error occurred. Please try again.', 'error');
      }
    });
  }

  // Utility function to display messages to the user
  function displayMessage(message, type) {
    const messageBox = document.createElement('div');
    messageBox.className = `message ${type}`;
    messageBox.innerText = message;
    document.body.appendChild(messageBox);
  
    setTimeout(() => {
      messageBox.remove();
    }, 3000);
  }
});