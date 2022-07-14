const express = require('express')
const bodyParser = require('body-parser')
const app = express()
app.use(bodyParser.json())


//CORSポリシーを無効にしている。
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});


app.get('/api', function(req, res) {

  var {PythonShell} = require('python-shell');
  var pyshell = new PythonShell('./backend/sample.py');  
  console.log("req")
  console.log(req.query.dat) //フロントエンドから受け取ったデータをconsole.logしている。

  pyshell.send(req.query.dat); //本コードからpythonコードに'req.query.dat'を入力データとして提供する 

  //pythonコード実施後にpythonから本コードにデータが引き渡される。
  pyshell.on('message',  function (data) {
    console.log("return data")
    console.log(data)
    res.send({
      message: data   //pythonで実施した演算結果をフロントエンドに返している。
    })
  })
})

app.listen(3000)