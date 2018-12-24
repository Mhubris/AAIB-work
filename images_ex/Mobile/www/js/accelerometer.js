document.addEventListener('deviceready',onDeviceReady, false);

//Arrays to fill while the aquisition time
var matrixWithValues =[];
var socket;
var socketOpened=false;
var fileName;
var watchID;
function onDeviceReady (){
    screen.orientation.lock('portrait'); //Fix de position

    //Define onclicks for tall buttons
    $("#save_as_pdf").click(save_as_pdf);
    $("#record_icon").click(hide_show_graph);

    socket = new Socket();
    socket.open(
      '192.168.0.74',
      5005,
      function() {
            var startByte= new Uint8Array(1);
            startByte[0]=0;
            socket.write(startByte);
      },
      function(errorMessage) {
        // invoked after unsuccessful opening of socket
      });
    var mp3URL = getMediaURL("../sound/beep.mp3");
    var media = new Media('/android_asset/www/sound/beep.mp3', startTest);
    prepareForTest(media);
    prepareGraph();
}

function prepareGraph(){
    //Here we define all the css and defenitions off plot
    Plotly.plot('chart', [{
      y: [],
      mode: 'lines',
      marker: {color: 'pink', size: 8},
      line: {width: 4}
    }, {
      y: [],
      mode: 'lines',
      marker: {color: 'gray', size:8},
      line: {width: 4}
    }, {
      y: [],
      mode: 'lines',
      marker: {color: 'rgb(66, 134, 244)', size:8},
      line: {width: 4}
    }],
      {
          autosize: false,
          width: 500,
          margin: {
              l: 10,
              r: 0,
              b: 0,
              t: 0,
              pad: 4
            },
            xaxis: {
              fixedrange: true,
              showgrid: false,
              zeroline: false,
              showline: false,
              autotick: true,
              ticks: '',
              showticklabels: false
            },
            yaxis: {
              fixedrange:true,
              showgrid: false,
              zeroline: false,
              showline: false,
              autotick: true,
              ticks: '',
              showticklabels: false
          },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          showlegend: false
      });
}

//On click functions
function save_as_pdf(){
    navigator.notification.prompt(
        'Nome do Ficheiro',  // message
        onPrompt,                  // callback to invoke
        'Registration',            // title
        ['Ok','Exit'],             // buttonLabels
        'teste'                 // defaultText
    );
}

function hide_show_graph(){
    if($("#chart_row").hasClass("d-none")){
        $("#chart_row").removeClass("d-none")
        $(".centered").addClass("d-none");
    }else {
        $("#chart_row").addClass("d-none")
        $(".centered").removeClass("d-none");
    }
}


function onPrompt(results) {

    if(results.buttonIndex = "2"){
        fileName=results.input1;
        window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, gotFS, fail);
    }else{
        return;
    }
}

function gotFS(fileSystem) {
        fileSystem.root.getDirectory("AAIB", {create: true}, gotDir,fail);
        console.log(fileSystem.root);
}

function gotDir(dirEntry) {
        dirEntry.getFile(fileName+".csv", {create: true, exclusive: true}, writeFile,fail);
}

function prepareForTest(media){
    media.play();
    $("h2").text("A preparar");
    $("h1").addClass("animated bounceInLeft")
    window.setTimeout(function() {
        $("h1").removeClass("bounceInLeft")
        $("h1").text("2").addClass("animated bounceInRight")
        setTimeout(function() {
            $("h1").removeClass("bounceInRight")
            $("h1").text("1").addClass("animated bounceInLeft")
            setTimeout(function() {
                $("h1").removeClass("bounceInLeft")
                $("h1").text("0").addClass("animated swing")
            }, 1000);
        }, 1200);
    }, 1200);
}


function startTest(){
    //Timeout for executing the text

    $("h1").addClass("d-none")
    $("h2").addClass("animated bounceInUp").text("A testar");


    matrixWithValues=[]; //Reset data
    var matrixWithValues8=[]
    var options = { frequency: 50 };  // Update every 50 ms
    watchID = navigator.accelerometer.watchAcceleration(onSuccess, onError, options);

    window.setTimeout(function (){
        $("h2").text("Analisar Dados");
        $("#record_icon").addClass("d-none")
        if(!$("#chart_row").hasClass("d-none")){
            $("#chart_row").addClass("d-none");
            $(".centered").removeClass("d-none");
        }

        navigator.accelerometer.clearWatch(watchID);
        prepareMatrix();
        //Event made to requestFileSystem
        var data= new Uint8Array(8);
        var a = 0
        var b = 0
        var c = 0
        var i=0
        matrixWithValues.forEach(function(infoArray, index){
            data[0]=Math.floor(infoArray[0]/100)
            data[1]=infoArray[0]%100
            aux=Math.round(infoArray[1]*100)+7800
            data[2]=Math.floor(aux/255) //Quociente
            data[3]=aux%255 //Resto
            aux=Math.round(infoArray[2]*100)+7800
            data[4]=Math.floor(aux/255)
            data[5]=aux%255
            aux=Math.round(infoArray[3]*100)+7800
            data[6]=Math.floor(aux/255)
            data[7]=aux%255
            socket.write(data);
        });
        data[0]=0; data[1]=0; data[2]=0; data[3]=0; data[4]=0; data[5]=0,data[6]=0,data[7]=0;
        socket.write(data);
        socket.close();


        window.setTimeout(function(){
            if(!$("#chart_row").hasClass("d-none")){
                $("#chart_row").addClass("d-none");
            }
            $(".centered").addClass("d-none");
            $("h2").removeClass('d-none');
            $("img").removeClass("d-none").addClass("animated bounceInLeft");
            $("h2").text("Teste Terminado").animate({top : '60%'});
            $(".button").removeClass('d-none');
            $("#record_icon").addClass("d-none");
        },6000);
    }, 10000);
}


function prepareMatrix(){
    var firstTimestamp;
    matrixWithValues.forEach(function (infoArray, index) {
        if(index==0)
            firstTimestamp=infoArray[0];
        infoArray[0]=infoArray[0]-firstTimestamp;
        matrixWithValues[index]=infoArray;
    });
}


function writeFile(fileEntry) {
    // Create a FileWriter object for our FileEntry (log.txt).
    fileEntry.createWriter(function (fileWriter) {
        // If data object is not passed in,
        // create a new Blob instead.
        var lineArray = [];
        matrixWithValues.forEach(function (infoArray, index) {
            var line = infoArray.join(";");
            lineArray.push(line);
        });
        var csvContent = lineArray.join("\n");
        console.log(csvContent);
        fileWriter.write(csvContent);
        });
}
function fail(error) {
    console.log(error.code);
}


function onSuccess(acceleration) {
    Plotly.extendTraces('chart', { y: [[acceleration.x],[acceleration.y],[acceleration.z]] }, [0,1,2])
    matrixWithValues.push([acceleration.timestamp,acceleration.x,acceleration.y,acceleration.z]);
}

function onError() {
    alert('onError!');
}

function getMediaURL(s) {
    if(device.platform.toLowerCase() === "android")
        return "../../android_asset/www/sound/beep.mp3";
    return s;
}

function onBackPressed(){
    if(socket.state == Socket.State.OPENED){
        socket.close()
    }
    //Return to last openned page
    history.go(-1);
    navigator.app.backHistory();
}
