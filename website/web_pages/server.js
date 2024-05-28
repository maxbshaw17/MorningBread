const express = require('express');
const app = express();
const https = require('https');
const fs = require('fs');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const session = require('express-session');
const path = require('path');
const cors = require('cors');
const csrf = require('csurf');
const helmet = require('helmet');

// CORS Configuration
const allowedOrigins = ['http://127.0.0.1:3000', 'http://127.0.0.1:3001'];

app.use(
  cors({
    origin: (origin, callback) => {
      console.log('CORS middleware called for origin:', origin);
      // Allow requests with no origin (like mobile apps, curl requests)
      if (!origin) {
        console.log('No origin, allowing request');
        return callback(null, true);
      }

      // Check if the origin is allowed
      if (allowedOrigins.includes(origin)) {
        console.log('Origin allowed:', origin);
        return callback(null, true);
      } else {
        console.log('Origin not allowed:', origin);
        return callback(new Error('Not allowed by CORS'));
      }
    },
    credentials: true, // Allow credentials
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    optionsSuccessStatus: 200, // For legacy browser support
  })
);

// Additional middleware to handle preflight OPTIONS request
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", allowedOrigins.join(', '));
  res.header("Access-Control-Allow-Credentials", "true");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

// Deprecation
mongoose.set('strictQuery', false);

mongoose.connect('mongodb://localhost:27017/', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => console.log('MongoDB connected'))
  .catch(err => {
    console.error('MongoDB connection error:', err);
    process.exit(1); // Exit the process if there's an error
  });

// User schema
const userSchema = new mongoose.Schema({
  firstName: String,
  lastName: String,
  email: { type: String, unique: true },
  password: String,
});

// User model
const User = mongoose.model('User', userSchema);

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: true,
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production', // Use secure cookies in production
    maxAge: 1000 * 60 * 60 * 24, // 1 day
  },
}));

const csrfProtection = csrf({ cookie: true });
app.use(csrfProtection);

// Serve static files from the parent directory of web_pages
app.use(express.static(path.join(__dirname, '..')));

// Sign up route
app.get('/signup', (req, res) => {
  res.sendFile(path.join(__dirname, 'signup.html'));
});

// Login route
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

// Signup POST route
app.post('/signup', async (req, res) => {
  const { firstName, lastName, email, password } = req.body;

  try {
    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: 'User already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create new user
    const newUser = new User({
      firstName,
      lastName,
      email,
      password: hashedPassword,
    });

    // Save user to database
    await newUser.save();

    res.status(201).json({ message: 'User created successfully' });
  } catch (err) {
    console.error('Error creating user:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Login POST route
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    // Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: 'Invalid email or password' });
    }

    // Compare password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(400).json({ message: 'Invalid email or password' });
    }

    // Set user session
    req.session.user = user;

    res.status(200).json({ message: 'Login successful' });
  } catch (err) {
    console.error('Error logging in:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// HTTPS configuration
const options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
};

// Start the server
https.createServer(options, app).listen(3001, () => {
  console.log('HTTPS Server started on port 3001');
});