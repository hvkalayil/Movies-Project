const express = require('express')
const multer = require('multer')
const mongoose = require('mongoose')

const router = express.Router()

const storage = multer.memoryStorage();
const upload = multer({ dest: 'uploads', storage: storage })

module.exports = () => {
    router
        .get('/', async (req, res) => {
            let uploadDetails = []
            let item = await mongoose.connection.collection('UploadDetail').find()
            await item.forEach((ele) => {
                uploadDetails.push(ele)
            })

            res.render('upload', { title: 'Movies DB | Upload' ,uploadDetails:uploadDetails})
        })
        .post('/', upload.single('jsonFile'), async (req, res) => {
            const json = Buffer.from(req.file.buffer).toString()
            const jsonData = JSON.parse(json)

            let movies = mongoose.connection.collection('Movies');
            let record = 0
            let good = 0
            let evil = 0
            let duplicate = 0
            for (let item of jsonData) {
                const dt = new Date(item.ReleaseDate)
                item.ReleaseDate = dt
                item.Day = dt.getUTCDate()
                item.Month = dt.getUTCMonth()+1

                const it = await movies.findOne(item)
                if (it) {
                    duplicate += 1
                }
                else {
                    record += 1
                    if (item?.Poster){
                        good += 1
                        item.isGood = true
                    }
                    else{
                        evil += 1
                        item.isGood = false
                    }
                    console.log(`#${item.isGood ? good : evil} - Inserting ${item.MovieName}`);
                    await movies.insertOne(item)
                }
            }

            mongoose.connection.collection('UploadDetail').insertOne({
                'UploadedOn': new Date(),
                'CleanRecords': good,
                'DirtyRecords': evil,
                'TotalRecords': record,
                'Duplicate': duplicate
            })
            res.redirect('/')
        })
    return router
}