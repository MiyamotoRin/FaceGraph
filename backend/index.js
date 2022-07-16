/* eslint-disable */

const express = require('express')
const bodyParser = require('body-parser')
const app = express()
app.use(bodyParser.json())

// CORSポリシーを無効にしている。
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});


app.get('/api', function(req, res) {

  var {PythonShell} = require('python-shell');
  // var pyshell = new PythonShell('./backend/face_reshape.py');

  console.log('ok')

  const options = {
    mode: 'json',
    args: [req.query.image],
  }

  PythonShell.run('./backend/face_reshape.py', options, function(err, data){
    if(err){
      console.log(err)
    }else{
      console.log('send!')
      res.send({
        resultImages: data[0]['resultImages']   //pythonで実施した演算結果をフロントエンドに返している。
      })
    }
  })

  // pyshell.send(req.query.image); //本コードからpythonコードに'req.query.dat'を入力データとして提供する 

  // pythonコード実施後にpythonから本コードにデータが引き渡される。
  // pyshell.on('message',  function (data) {
  //   console.log('return data')
  //   console.log(typeof(data), data)
  //   res.send({
  //     resultImages: data[0]['resultImages']   //pythonで実施した演算結果をフロントエンドに返している。
  //   })
  // })

  // end the input stream and allow the process to exit
  // pyshell.end(function (err,code,signal) {
  //   if (err) throw err
  //   console.log('The exit code was: ' + code)
  //   console.log('The exit signal was: ' + signal)
  //   console.log('finished')
  // })
})

app.listen(3000)