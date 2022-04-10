
HOMEPAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>REMOTE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

<!--  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> -->
<!--  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script> -->
<!--  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> -->
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
                    <a class="btn btn-dark btn-lg text-light btn-outline-primary" href="/up" role="button">&uarr;</a>
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
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/left" role="button">&larr;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/select" role="button"><small>ok</small></a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/right" role="button">&rarr;</a>
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
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/down" role="button">&darr;</a>
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
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/home" role="button">&thinsp;&nbsp;&#8962;&nbsp;&thinsp;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/play" role="button">&#9658;&par;</a>
                    <a class="btn brn-dark btn-lg text-light btn-outline-primary" href="/back" role="button">&nbsp;&crarr;&nbsp;</a>
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