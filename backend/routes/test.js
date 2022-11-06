const express = require('express')
const { default: mongoose } = require('mongoose')

const router = express.Router()

module.exports = () => {
    router.get('/',async (req,res)=>{
        await mongoose.connection.collection('UploadDetail').deleteMany({})
        res.send('SUCCESS')
    })
    return router
}