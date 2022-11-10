const express = require('express')
const path = require('path')
const mongoose = require('mongoose')
const cors = require('cors')

const app = express()
const PORT = 4000

app.use(express.static(path.join(__dirname,'./static')))
app.use(cors())
app.set('view engine','ejs')

// ADMIN PANEL ROUTES
const homeRoute = require('./routes')
const uploadRoute = require('./routes/upload')
const deleteRoute = require('./routes/delete')
const testRoute = require('./routes/test')
app.use('/',homeRoute())
app.use('/upload',uploadRoute())
app.use('/delete',deleteRoute())
app.use('/test',testRoute())

// API ROUTES
const movieAPI = require('./routes/api/movies')
app.use('/api/movies',movieAPI())

app.listen(PORT, () => {
    mongoose.connect('mongodb+srv://hvk:qwerty1234@cluster0.d5rde.mongodb.net/MoviesDB?retryWrites=true&w=majority')
    .catch(err => console.log(err))

    console.log(`Backend process have started. Goto http://localhost:${PORT}`);
})