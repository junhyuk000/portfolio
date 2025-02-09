function printDate() {
    document.getElementById("date").innerHTML= Date();
}
function showOn(){
   document.getElementById("img").innerHTML="<img src ='aa.jpg' width = '300px'>";
}
function showOff(){
    document.getElementById("img").innerHTML="<img src = '강아지.jpg' width = '300px'>"
}

function showToggle() {
    var a=document.getElementById("a").value
    
    if(a == '딸기'){
        document.getElementById("img").innerHTML="<img src ='aa.jpg' width = '300px'>";
    }else if(a == '강아지'){
        document.getElementById("img").innerHTML="<img src = '강아지.jpg' width = '300px'>";
    }else{
        document.getElementById("img").innerHTML="none";
    }

}