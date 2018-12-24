<?php
$connect = mysqli_connect('localhost', 'myuser', 'mypassword','mydb') or die('ERROOOOO' . mysqli_error($connect));
$get_users_query = 'SELECT * FROM Utilizadores WHERE Utilizadores.id = "'.$_GET['id'].'"';
$get_users_result = mysqli_query($connect, $get_users_query);
$results = mysqli_fetch_array($get_users_result);
 ?>

<html>
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width">
    <link rel="stylesheet" type="text/css" href="css/vendor/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/vendor/animate.css">
    <link rel="stylesheet" type="text/css" href="css/details.css">
    <title>AAIB</title>
  </head>
  <body>
      <nav class="navbar navbar-expand-lg navbar-light bg-dark">
          <a class="navbar-brand" href="#">AAIB</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
      </nav>
      <div class="container">
          <div class="row">
              <div class="col-sm-12 d-flex justify-content-center mt-4 slideInRight animated" >
                  <?php
                  echo '<h1>'.$results[2].'</h1>';
                  ?>
              </div>
          </div>
          <div class="row slideInRight animated">
              <?php
              echo '<img src="images/plot_signals'.$_GET['id'].'.jpg" style="height:250px; width:100%;">';
              ?>
          </div>
          <div class="row mt-3">
              <div class="col-sm-6 pl-0 jackInTheBox animated">
                  <?php
                  echo '<img src="images/spectrograms'.$_GET['id'].'.jpg" style="height:300px; width:100%;">';
                  ?>
              </div>
              <div class="col-sm-6 pr-0 jackInTheBox animated">
                  <?php
                  echo '<img src="images/histograms'.$_GET['id'].'.jpg" style="height:300px; width:100%;">';
                  ?>
              </div>
          </div>
          <div class="row d-flex justify-content-center mt-4">
              <h1>Resultado: </h1>
          <?php
          switch ($results[5]) {
              case '0':
                  echo '<h1 id="result">Permaneceu Parado<h1>';
                  break;
              case '1':
                  echo '<h1 id="result">Teste Inválido<h1>';
                  break;
              case '2':
                  echo '<h1 id="result">Cadeira Elétrica<h1>';
                  break;
              case '3':
                  echo '<h1 id="result">Cadeira Manual<h1>';
                  break;
              case '4':
                  echo '<h1 id="result">Foi Empurrado<h1>';
                  break;
              case '5':
                  echo '<h1 id="result">Retaguarda<h1>';
                  break;
              case '6':
                  echo '<h1 id="result"><a href="https://github.com/Mhubris/AAIB-work/blob/master/images_ex/cadeira.JPG?raw=true"> Use o nosso suporte<a><h1>';
                  break;
              default:
                  // code...
                  break;
          }

          ?>
          </div>

      </div>

      <script type="text/javascript" src="js/vendor/jquery-3.3.1.min.js"></script>
      <script type="text/javascript" src="js/vendor/require.js"></script>
      <script>

      </script>

  </body>
</html>
