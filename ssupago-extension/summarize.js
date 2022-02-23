//-----get text from document-----//
result = document.body.innerText;


//-----preprocess text-----//
ret = "";
result.split('\n').forEach(function(line) {
    if (line.length > 50) { ret += line; }
});
ret = ret.replaceAll('。', '.');
ret = ret.replaceAll('、', '.');
result = ret


//-----send text to server and get result-----//
ssupago_url = "http://127.0.0.1:8000/"
$.ajax({
    type: 'POST',
    url: ssupago_url,
    data: { 'content': result },
    Headers: {
        'Access-Control-Allow-Origin': '*',
    },
    async: false,
    beforeSend: function(){
        console.log("length: " + result.length);
        console.log("before:\n" + result);
    },
    success: function(data, status){
        console.log("length: " + data.length);
        console.log("after:\n" + data);
        result = data;
    },
    error: function(xhr, status, error){
        console.log(error);
        result = error;
    }
});


//-----return result to popup.js-----//
result
