const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const VideoSchema = new Schema({
    title: String,
    timeData: Array,
    video: String,
    date: {
        type: Date,
        default: Date.now,
    },
})

module.exports = Video = mongoose.model('video', VideoSchema);