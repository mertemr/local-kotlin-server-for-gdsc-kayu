# GDSC Kayseri Online Kotlin Compiler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Compose Action](https://github.com/mertemr/gdsc-local-kotlin-server/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/mertemr/gdsc-local-kotlin-server/actions/workflows/main.yml)

A simple Kotlin compiler that runs in a docker container.

It was done in less than 12 hours by a single person (me) so it's not perfect.  
It's part of a challenging process. I build this because GSBWifi is sucks.

## Limitations
- You can't use `readLine()` function because there is no _stdin_.
- idk what else

## Launch 🚀
1. Clone the repository
2. Run `docker-compose up` in the root directory
3. Open `localhost:8080` in your browser

## How to use
1. Write your code in the left box
2. Click `Run` button
3. See the result in the right box

## Technologies used
- Kotlin
- Spring Boot
- Docker & Docker Compose
- Flask
- Bootstrap

## How it works
The website sends the code to the backend, server creates a file with the code.  
Backend runs the docker container with the file after sends the output to the website.

## LICENSE
This project is licensed under the terms of the MIT license. So free to use :)
