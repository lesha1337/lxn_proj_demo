const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const path = require("path");
const videos = require('./routes/api/videos')

const app = express();
app.use(bodyParser.json())

const db = require("./config/mongoDB").mongoURI;

//cloud mongo
mongoose.connect(db, { useNewUrlParser: true })
    .then(() => console.log('Cloud mongoDB connected'))
    .catch((err) => console.log(err))


//routes
app.use('/api/videos', videos)

app.get('/', (req, res) => {
    res.send('200')
})


const PORT = process.env.PORT || 5000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => console.log(PORT));