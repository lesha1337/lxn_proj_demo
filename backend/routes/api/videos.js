const express = require("express");
const path = require("path");
const router = express.Router();


//Model
const Video = require('../../models/Video')

// @route  GET api/videos
// @desc   GET All Videos
router.get('/', (req, res) => {
    Video.find()
      .sort({ date: -1 })
      .then(videos => res.json(videos))
      .catch(err => res.status(404));
})

// @route  GET api/videos
// @desc   GET One Video Data
router.get('/:id', (req, res) => {
    Video.findById(req.params.id)
      .then(video => res.json(video))
      .catch(err => res.status(404));
})

// @route  GET api/videos/file/:id
// @desc   GET One Video File
router.get('/file/:id', (req, res) => {
    Video.findById(req.params.id)
        .then(data => {
            const file = path.join(data.video);
            res.sendFile(file)
        })
        .catch(err => res.status(404))
})

// @route  POST api/videos/new_vid_from_flask
// @desc   ADD NEW VID
router.post('/add_vid_from_flask/', (req, res) => {
    const { title, timeData, video} = req.body;
    console.log('body>>> ', req.body);
    res.send('200')
    
    const newVid = new Video({title, timeData, video});
    
    newVid.save()
      .then(video => res.json(video))
      .catch(err => res.status(404));
})

module.exports = router;