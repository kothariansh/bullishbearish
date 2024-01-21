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
    res.redirect('/login');
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
        res.redirect('/');
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

app.get('/dashboard', async (req, res) => {
    if (req.session.user) {
        try {
            // Define an array of stock symbols
            const stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'];

            // Specify the desired date (YYYY-MM-DD format)
            const desiredDate = '2023-01-20'; // Replace with your desired date

            // Fetch stock data from Polygon API for the specified date
            const stockDataPromises = stocks.map(async (symbol) => {
                const stockResponse = await axios.get(`https://api.polygon.io/v2/aggs/ticker/${symbol}/range/1/day/${desiredDate}/${desiredDate}`, {
                    params: {
                        apiKey: 'IK8sNfOtObOQfYSZbuso9NBrb6Lvc0z6',
                    },
                });
                return {
                    symbol,
                    name: 'Company Name',  // Replace with actual company name (you might need an additional API for this)
                    price: stockResponse.data.results[0]?.c || 'N/A',
                };
            });

            // Wait for all promises to resolve
            const stockData = await Promise.all(stockDataPromises);

            res.render('dashboard.ejs', { user: req.session.user, stockData });
        } catch (error) {
            console.error('Error fetching stock data:', error);
            res.render('dashboard.ejs', { user: req.session.user, stockData: [] });
        }
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

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});