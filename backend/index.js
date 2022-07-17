/* eslint-disable */

const express = require('express')
const path = require('path')
const multer = require('multer')
const fs = require('fs')
const { promisify } = require('util')
const unlinkAsync = promisify(fs.unlink)
const bodyParser = require('body-parser')
const app = express()
const updir = "/src/assets";  //  "./src/assets" をアップロード先にしている。
app.use(bodyParser.json())

// CORSポリシーを無効にしている。
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

const storage = multer.diskStorage({
    destination(req, file, cb) {
      cb(null, './src/assets/')
    },
    filename(req, file, cb) {
      if(file.originalname == 'img'){
        cb(null, `${Math.random().toString(36).slice(-9)}_${Date.now()}.png`)
      }else if(file.originalname == 'csv'){
        cb(null, `${Math.random().toString(36).slice(-9)}_${Date.now()}.csv`)
      }else if(file.originalname == 'NoFile'){
        cb(null, `${Math.random().toString(36).slice(-9)}_${Date.now()}.txt`)
      }
    }
  })

const upload = multer({ storage: storage })

app.post('/api', upload.array('files'), async (req, res) =>{
  console.log('get!')
  var {PythonShell} = require('python-shell');

  csvPath = './src/assets/default.csv'
  if(req.files[1].originalname=='csv'){
    csvPath = req.files[1].path
  }
  console.log(csvPath)
  const options = {
    mode: 'json',
    args: [req.files[0].path, csvPath],
  }
  
  PythonShell.run('./backend/face_reshape.py', options, function(err, data){
    if(err){
      console.log(err)
    }else{
      console.log('send!')
      // Delete the file like normal
      unlinkAsync(req.files[0].path)
      unlinkAsync(req.files[1].path)
      console.log(data)
      console.log(data[0]['resultImages'])
      res.send({
        resultImages: data[0]['resultImages']   //pythonで実施した演算結果をフロントエンドに返している。
      })
    }
  })
})

app.listen(3000)