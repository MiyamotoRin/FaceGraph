/* eslint-disable */

const express = require('express')
const multer = require('multer')
const fs = require('fs')
const { promisify } = require('util')
const unlinkAsync = promisify(fs.unlink)
const bodyParser = require('body-parser')
// const { fsum } = require('d3')
const app = express()
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
      cb(null, `${Math.random().toString(36).slice(-9)}_${Date.now()}.png`)
    }
  })

const upload = multer({ storage: storage }).single('image')

app.post('/api', upload, async (req, res) =>{
    pathPython(req, res)
    console.log('11111')
})

function pathPython (req, res) {

  var {PythonShell} = require('python-shell');

  console.log(req.query.image)

  const options = {
    mode: 'json',
    args: [req.file.path],
  }

  PythonShell.run('./backend/face_reshape.py', options, function(err, data){
    if(err){
      console.log(err)
    }else{
      console.log('send!')
      // Delete the file like normal
      unlinkAsync(req.file.path)
      res.send({
        resultImages: data[0]['resultImages']   //pythonで実施した演算結果をフロントエンドに返している。
      })
    }
  })
}

app.listen(3000)