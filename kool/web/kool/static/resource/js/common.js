function setDateFormat(dateValue){
    var day = lpad((dateValue.getDate()).toString(), 2, 0);
    var month = lpad((dateValue.getMonth() + 1).toString(), 2, 0);
    var year = dateValue.getFullYear();
    return year+"-"+month+"-"+day;
}
function getMinusDate(days,today){
    var date = today;
    date.setDate(date.getDate() - parseInt(days));
    return setDateFormat(date);
}
function lpad(str ,padLength, padString){
    var string = str;
    while(string.length < padLength)
        string = padString + string;
    return string;
}
function isNotEmpty(value){
    if(value != null && value != "undefined" && value != ""){
        return true;
    }
    return false;
}
// back menu
function goMenu(){
   window.location.assign("{% url 'home' %}");
}
function isObject(value){
    if(typeof value == 'object'){
        return true;
    }
    return false;
}