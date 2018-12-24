<?php
$connect = mysqli_connect('localhost', 'myuser', 'mypassword','mydb') or die('ERROOOOO' . mysqli_error($connect));
if(isset($_FILES['file'])){ //check if form was submitted
    $imagetmp=addslashes(file_get_contents($_FILES['file']['tmp_name']));
    $query = 'UPDATE Utilizadores SET picture = "'.$imagetmp.'" WHERE Utilizadores.id = "'.$_GET['id'].'"';
    $result_create = mysqli_query($connect ,$query) or die('The query failed: ' . mysqli_error($connect));
}
$get_users_query = "SELECT * FROM Utilizadores";
$get_users_result = mysqli_query($connect, $get_users_query);

function classify($number){
	          switch ($number) {
              case '0':
                  echo '<h4>Resultado: Permaneceu Parado</h4>';
                  break;
              case '1':
                  echo '<h4>Resultado: Teste Inválido</h4>';
                  break;
              case '2':
                  echo '<h4>Resultado: Cadeira Elétrica</h4>';
                  break;
              case '3':
                  echo '<h4>Resultado: Cadeira Manual</h4>';
                  break;
              case '4':
                  echo '<h4>Resultado: Foi Empurrado</h4>';
                  break;
              case '5':
                  echo '<h4>Resultado: Retaguarda</h4>';
                  break;
              case '6':
                  echo '<h4>Resultado: <a href="https://github.com/Mhubris/AAIB-work/blob/master/images_ex/cadeira.JPG?raw=true"> Use o nosso suporte</a></h4>';
                  break;
              default:
                  // code...
                  break;
          }
}

 ?>


<html>
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width">
    <link rel="stylesheet" type="text/css" href="css/vendor/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="css/vendor/animate.css">
    <link rel="stylesheet" type="text/css" href="css/index.css">
    <title>Welcome to Example.com!</title>
  </head>
  <body>
      <nav class="navbar navbar-expand-lg navbar-light bg-dark">
          <a class="navbar-brand" href="#">AAIB</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
      </nav>
      <div class="container d-flex align-items-center flex-column justify-content-center">
          <?php
            while($row = mysqli_fetch_array($get_users_result)){
                switch ($row['picture']) {
                    case Null:
                    echo'
                    <div class="row w-100 mt-4 slideInRight animated">
                          <div class="col-sm-4 p-0 d-flex justify-content-center pl-0" >
                              <form class="w-100 m-0 d-flex justify-content-center" action="?id='.$row['id'].'" method="POST" enctype="multipart/form-data">
                                  <label for="file-input" class="w-100 d-flex flex-column align-items-center m-0  justify-content-center">
                                          <img src="src/camera.png" width="90px"/>
                                          <p>Clique para carregar uma foto</p>
                                  </label>
                                  <input id="file-input" type="file" name="file" onchange="this.form.submit()"/>
                               </form>
                          </div>
                      <div class="col-sm-8">
                          <h1><a href="details.php?id='.$row['id'].'">'.$row['name'].'</a></h1> <br>
                          <h4>Idade:'.$row['age'].'</h4>
                          <h4>Peso: '.$row['weight'].' kg</h4>';?>
                          <?php classify($row['result']);
                      echo'</div>
                     </div>';
                        break;
                    default:
                        echo'
                        <div class="row w-100 mt-4 slideInRight animated">
                              <div class="col-sm-4 d-flex justify-content-center pl-0" style="background-image:url(data:image/jpeg;base64,'.base64_encode($row['picture']).')">
                              </div>
                          <div class="col-sm-8">
                              <h1><a href="details.php?id='.$row['id'].'">'.$row['name'].'</a></h1> <br>
                              <h4>Idade:'.$row['age'].'</h4>
                              <h4>Peso: '.$row['weight'].' kg</h4>';?>
                              <?php classify($row['result']);
                          echo '</div>
                         </div>';
                        break;
                }
            }
          ?>
      </div>

      <script type="text/javascript" src="js/vendor/jquery-3.3.1.min.js"></script>
      <script type="text/javascript" src="js/vendor/require.js"></script>

  </body>
</html>
