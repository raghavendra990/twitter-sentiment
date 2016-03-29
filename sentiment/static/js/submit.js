function submitthis()
{
    var val = document.getElementById('sizes').value;
    console.log(val);
    var xmlhttp;
    
    if (window.XMLHttpRequest)
{// code for IE7+, Firefox, Chrome, Opera, Safari
 xmlhttp=new XMLHttpRequest();
 }
else
 {// code for IE6, IE5
 xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
    xmlhttp.onreadystatechange=function()
{
if (xmlhttp.readyState==4 && xmlhttp.status==200)
 {
     document.getElementById("drop").innerHTML=xmlhttp.responseText;
 }
 }
 xmlhttp.open("GET","reply.php?size="+val,true);
 xmlhttp.send();
}