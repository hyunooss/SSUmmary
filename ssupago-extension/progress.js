//-----get text from document-----//
document_text = document.body.innerText;
result = document_text;


//-----preprocess text-----//
ret = "";
result.split('\n').forEach(function(line) {
    if (line.length > 50) { ret += line; }
});
ret = ret.replace('。', '.');
ret = ret.replace('、', '.');


//-----process time-----//
leng = ret.length

if (leng > 5000){
    result = 50;
}
else if (leng > 4000){
    result = 40;
}
else if (leng > 3000){
    result = 30;
}
else if (leng > 2000){
    result = 20;
}
else if (leng > 1000){
    result = 10;
}
else {
    result = 10;
}


//-----return result to popup.js-----//
result
