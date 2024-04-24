// Sign up
const signupForm = document.querySelector('.form_signup');
signupForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const firstName = document.getElementById('firstName').value;
  const lastName = document.getElementById('lastName').value;
  const email = document.querySelector('input[type="email"]').value;
  const password = document.querySelector('input[type="password"]').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  // Check if passwords match
  if (password !== confirmPassword) {
    alert('Passwords do not match.');
    return;
  }

  try {
    const response = await fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ firstName, lastName, email, password }),
    });

    const data = await response.json();
    console.log(data.message);
    // Handle success or error
  } catch (err) {
    console.error(err);
  }
});

// Login
const loginForm = document.querySelector('.form_login');
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.querySelector('input[type="email"]').value;
  const password = document.querySelector('input[type="password"]').value;

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    console.log(data.message);
    // Handle success or error
  } catch (err) {
    console.error(err);
  }
});