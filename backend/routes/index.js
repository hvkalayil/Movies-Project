const express = require('express')
const router = express.Router()
const mongoose = require('mongoose')

module.exports = () => {
    router.get('/',async (req,res)=>{
        // Getting Total
        const total = await mongoose.connection.collection('Movies').countDocuments()

        // Getting Duplicates
        let duplicates = 0
        await mongoose.connection.collection('Movies').aggregate([
            { $match: { name: { "$ne": '' }}},
            { $group: { 
                _id: { MovieName: "$MovieName"},
                dups: { "$addToSet": "$_id" }, 
                count: { "$sum": 1 } 
            }},
            { $match: { count: { "$gt": 1 }}}
        ]).forEach((ele)=>{
            duplicates += (ele.count) - 1
        })
        const clean = total - duplicates

        // Setting Doc
        doc = [
            {
                type:'GET',
                path:'/api/movies',
                description:'To get details of movies released on current date over the years with pagination.',
                params:[
                    'page ~ To Specify current page, Default = 1',
                    'size ~ To Specify number of items per page, Default = 10',
                    'day ~ To Specify day of month, Default = Current Day',
                    'month ~ To Specify month, Default = Current Month',
                ]
            }
        ]
        res.render('index',{title:'Movies DB | Welcome',total,duplicates,doc})
    })

    return router
}