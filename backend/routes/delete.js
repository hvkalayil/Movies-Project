const express = require('express')
const mongoose = require('mongoose')

const router = express.Router()

module.exports = () => {
    router.get('/',async (req,res)=>{
        let allDuplicates = []
        await mongoose.connection.collection('Movies').aggregate([
            { $match: { name: { "$ne": '' }}},
            { $group: { 
                _id: { MovieName: "$MovieName"},
                dups: { "$addToSet": "$_id" }, 
                count: { "$sum": 1 } 
            }},
            { $match: { count: { "$gt": 1 }}}
        ]).forEach((ele)=>{
            allDuplicates.push(ele.dups)
        })

        let duplicateIds = []
        for (const duplicateSet of allDuplicates) {
            const duplicateDetails = await mongoose.connection.collection('Movies').find({
                '_id' :{ $in : duplicateSet}
            })

            let max = 0
            let maxItem = null
            let minId = []
            await duplicateDetails.forEach(value => {
                const t = Object.keys(value).length
                if(t > max){
                    max = t
                    if (maxItem != null) minId.push(maxItem)
                    maxItem = value._id
                } else {
                    minId.push(value._id)
                }
            });
                
            duplicateIds.push(...minId)
        }

        await mongoose.connection.collection('Movies').deleteMany({
            _id:{$in:duplicateIds}
        })
        
        res.redirect('/')
    })

    return router
}