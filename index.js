const express = require('express');
const http = require('http');

const app = express();

const CONN = process.env.CONN || "localhost";
const CONN_PORT = process.env.CONN_PORT || 8002;

var GLOBAL_FILE_ID = 0;

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.use(express.static('public'));

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    next();
});

app.get("/css/:file", (req, res) => {
    res.sendFile(__dirname + "/public/css/" + req.params.file);
});

app.get("/js/:file", (req, res) => {
    res.sendFile(__dirname + "/public/js/" + req.params.file);
});

app.get("/img/:file", (req, res) => {
    res.sendFile(__dirname + "/public/img/" + req.params.file);
});

app.get("/", (req, res) => {
    res.render("index");
});

app.get("/api/version", (req, res) => {
    http.get(`http://${CONN}:${CONN_PORT}/version`, (response) => {
        let data = "";
        response.on("data", (chunk) => {
            data += chunk;
        });
        response.on("end", () => {
            console.log(JSON.parse(data));
            res.send(JSON.parse(data));
        });
    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });
});

app.get("/api/run", (req, res) => {
    let code = req.query.code;
    let filename = `file_${process.pid}_${GLOBAL_FILE_ID}.kt`
    
    GLOBAL_FILE_ID++;

    http.get(`http://${CONN}:${CONN_PORT}/run?code=${code}&filename=${filename}`, (response) => {
        let data = "";
        response.on("data", (chunk) => {
            data += chunk;
        });
        response.on("end", () => {
            console.log(JSON.parse(data));
            res.send(JSON.parse(data));
        });
    }).on("error", (err) => {
        console.log("Error: " + err.message);
    });
});

const PORT = process.env.PORT || 8000;

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});