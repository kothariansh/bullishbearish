const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const bcrypt = require('bcrypt');
const app = express();
const User = require('./models/User');
const axios = require('axios'); 


// Connect to MongoDB
mongoose.connect('mongodb://localhost/mywebsite', { useNewUrlParser: true, useUnifiedTopology: true });

// Set up middleware
app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'your_secret_key', resave: true, saveUninitialized: true }));

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

// Routes
app.get('/', (req, res) => {
    res.redirect('/index');
});

// Add this route for "/index"
app.get('/index', (req, res) => {
    res.render('index.ejs');  // Assuming your index.ejs file is in the 'views' folder
});

// Registration route
app.get('/register', (req, res) => {
    res.render('register.ejs');
});


app.post('/register', async (req, res) => {
    try {
        const hashedPassword = await bcrypt.hash(req.body.password, 10);
        const user = new User({
            username: req.body.username,
            password: hashedPassword,
        });
        await user.save();

        // Redirect to the dashboard after successful registration
        
        res.redirect('/login');
    } catch (error) {
        res.redirect('/register');
    }

});


// Login route
app.get('/login', (req, res) => {
    res.render('login.ejs');
});

app.post('/login', async (req, res) => {
    const user = await User.findOne({ username: req.body.username });
    if (user && await bcrypt.compare(req.body.password, user.password)) {
        req.session.user = user;
        res.redirect('/dashboard');
    } else {
        res.redirect('/login');
    }
});



// Other routes...

app.post('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error('Error destroying session:', err);
        }
        res.redirect('/login');
    });
});


app.get('/dashboard', (req, res) => {
    if (req.session.user) {
        res.render('dashboard.ejs');
    } else {
        res.redirect('/login');
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

