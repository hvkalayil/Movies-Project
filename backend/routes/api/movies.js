const express = require('express')
const mongoose = require('mongoose')

const router = express.Router()

module.exports = () => {
    router.get('/',async (req,res)=>{
        const today = new Date()

        // Params
        const page = parseInt(req.query?.page ?? '1')
        const size = parseInt(req.query?.size ?? '10')
        const day = parseInt(req.query?.day ?? `${today.getUTCDate()}`)
        const month = parseInt(req.query?.month ?? `${today.getUTCMonth()+1}`)

        const data = []
        let result = {'Message':'Loading'}
        await mongoose.connection.collection('Movies').find({
            Day:day,Month:month,isGood:true
        },{
            limit:size,
            skip:(page-1)*size
        }).sort({
            ReleaseDate:'desc'
        }).forEach((mov)=>data.push(mov)).then(()=>{
            result = res.status(200).json(data)
        }).catch((err)=>{
            console.log(err);
            result = res.status(400).json({
                'Message':'Unable to get movies'
            })
        })

        return result
    })
    return router
}