document.addEventListener('deviceready',onDeviceReady, false);
var socket;
function onDeviceReady (){
    screen.orientation.lock('portrait'); //Fix de position
    document.addEventListener("backbutton", onBackPressed, false);

    $("#button_scan").click(openQrReader);
    $("#save_data").click(sendDataToDb);

    socket = new Socket();
    socket.open(
      '192.168.0.74',
      5005,
      function() {
          var startByte= new Uint8Array(1);
          startByte[0]=1
          socket.write(startByte);
          socket.onData = function(dataReceived) {
                // invoked after new batch of data is received (typed array of bytes Uint8Array)
                var result="";
                dataReceived.forEach(function (char){
                        result = result.concat(String.fromCharCode(char))  //Cocatenate our result
                });
                $("#result").addClass("animated bounceInRight").text(result);
                socket.close()
            };
      },
      function(errorMessage) {
        // invoked after unsuccessful opening of socket
      });
}

//On Click Responses
function sendDataToDb(){
    var form_data=$("#form_with_data").serializeArray();
    var data_to_send=""
    for (var input in form_data){
    		var element=$("#form_with_data_"+form_data[input]['name']);
            if (element.val()==""){
                alert("O formulário não está correto")
                return;
            }else{
                if(form_data[input]['name']=="weight_input"){
                    data_to_send= data_to_send+element.val()+";"
                }else {
                    data_to_send= data_to_send+element.val()+";";

                }
            }
    	}
    var startByte= new Uint8Array(1);
    startByte[0]=2
    socket = new Socket();
    socket.open(
      '192.168.0.74',
      5005,
      function() {
          socket.write(startByte);
          var data = new Uint8Array(data_to_send.length);
          for (var i = 0; i < data_to_send.length; i++) {
            data[i] = data_to_send.charCodeAt(i);
          }
          socket.write(data);
          socket.close();
      },
      function(errorMessage) {
        // invoked after unsuccessful opening of socket
      });
}
function openQrReader(){
    QRScanner.prepare(onDone);
}
//------------------------------
function onDone(err, status){
  if (err) {
   // here we can handle errors and clean up any loose ends.
   console.error(err);
  }
  if (status.authorized) {
    // W00t, you have camera access and the scanner is initialized.
    // QRscanner.show() should feel very fast.
    QRScanner.show(function(status){
        $(".container").addClass("d-none");
        $("body").css('background-image', 'none');
        QRScanner.scan(displayContents);
    });
  } else if (status.denied) {
   // The video preview will remain black, and scanning is disabled. We can
   // try to ask the user to change their mind, but we'll have to send them
   // to their device settings with `QRScanner.openSettings()`.
  } else {
    // we didn't get permission, but we didn't get permanently denied. (On
    // Android, a denial isn't permanent unless the user checks the "Don't
    // ask again" box.) We can ask again at the next relevant opportunity.
  }
}

function displayContents(err, text){
  if(err){
    // an error occurred, or the scan was canceled (error code `6`)
  } else {
    // The scan completed, display the contents of the QR code:
    var input= text.split(";");
    $("#form_with_data_name_input").val(input[0]);
    $("#form_with_data_age_input").val(input[1]);
    $("#form_with_data_weight_input").val(input[2]);
    QRScanner.destroy(function(status){
        $(".container").removeClass("d-none").addClass("animated fadeInRight");
    });

  }
}

function onBackPressed(){
    if(socket.state == Socket.State.OPENED){
        socket.close()
    }
    //Return to last openned page
    history.go(-1);
    navigator.app.backHistory();

}
