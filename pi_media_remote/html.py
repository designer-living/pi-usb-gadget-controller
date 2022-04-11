
JS_HOMEPAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>REMOTE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <script>
        function send_button(button) {
            fetch('/rest/' + button)
              .then(response => response.json())
              .then(data => console.log(data));
        } 
    </script>
</head>
<body class="bg-dark">
    <br>
    <div class="container-sm bg-dark rounded text-center">
            <br>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <button class="btn btn-dark btn-lg text-light btn-outline-primary" onclick="send_button('up')">&uarr;</button>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mt-1 mb-1">
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('left')">&larr;</button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('select')"><small>ok</small></button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('right')">&rarr;</button>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mb-5">
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('down')">&darr;</button>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row mb-4">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col">
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('home')">&thinsp;&nbsp;&#8962;&nbsp;&thinsp;</button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('play')">&#9658;&par;</button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('back')">&nbsp;&crarr;&nbsp;</button>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/" role="button">&nbsp;&#9212;&nbsp;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-2">
                    &emsp;
                </div>
                <div class="col-8" id="dropDownDiv">
                    
                </div>
                <div class="col-2">
                    &emsp;
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <p class="text-light"><small id="statusMessage">&emsp;</small></p>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <br>
        <br>
    </div>
</body>
</html>
"""

WS_HOMEPAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>REMOTE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <script>
        try{
            var sock = new WebSocket('ws://' + window.location.host + '/ws');
        }
        catch(err){
            var sock = new WebSocket('wss://' + window.location.host + '/ws');
        }

        // income message handler
        sock.onmessage = function(event) {
            console.log(event.data);
        };

        sock.onclose = function(event){
            console.log(event);
        };

        sock.onerror = function(error){
            console.log(error);
        }


        function send_button(button) {
            sock.send(button);
        } 
    </script>
</head>
<body class="bg-dark">
    <br>
    <div class="container-sm bg-dark rounded text-center">
            <br>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <button class="btn btn-dark btn-lg text-light btn-outline-primary" onclick="send_button('up')">&uarr;</button>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mt-1 mb-1">
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('left')">&larr;</button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('select')"><small>ok</small></button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('right')">&rarr;</button>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mb-5">
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('down')">&darr;</button>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row mb-4">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col">
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('home')">&thinsp;&nbsp;&#8962;&nbsp;&thinsp;</button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('play')">&#9658;&par;</button>
                    <button class="btn brn-dark btn-lg text-light btn-outline-primary" onclick="send_button('back')">&nbsp;&crarr;&nbsp;</button>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/" role="button">&nbsp;&#9212;&nbsp;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-2">
                    &emsp;
                </div>
                <div class="col-8" id="dropDownDiv">
                    
                </div>
                <div class="col-2">
                    &emsp;
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <p class="text-light"><small id="statusMessage">&emsp;</small></p>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <br>
        <br>
    </div>
</body>
</html>
"""

HOMEPAGE_GET_REQUEST = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>REMOTE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body class="bg-dark">
    <br>
    <div class="container-sm bg-dark rounded text-center">
            <br>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <a class="btn btn-dark btn-lg text-light btn-outline-primary" href="/get/up" role="button">&uarr;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mt-1 mb-1">
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/left" role="button">&larr;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/select" role="button"><small>ok</small></a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/right" role="button">&rarr;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10 mb-5">
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/down" role="button">&darr;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row mb-4">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col">

                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/home" role="button">&thinsp;&nbsp;&#8962;&nbsp;&thinsp;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/play" role="button">&#9658;&par;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/back" role="button">&nbsp;&crarr;&nbsp;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/get/home" role="button">&nbsp;&#9212;&nbsp;</a>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <div class="row">
                <div class="col-2">
                    &emsp;
                </div>
                <div class="col-8" id="dropDownDiv">
                    
                </div>
                <div class="col-2">
                    &emsp;
                </div>
            </div>
            <div class="row mt-5">
                <div class="col-1">
                    &emsp;
                </div>
                <div class="col-10">
                    <p class="text-light"><small id="statusMessage">&emsp;</small></p>
                </div>
                <div class="col-1">
                    &emsp;
                </div>
            </div>
            <br>
        <br>
    </div>
</body>
</html>
"""