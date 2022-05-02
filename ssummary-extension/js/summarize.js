function summarize_fn(text, deep) {
    return new Promise(function (resolve, reject) {
        //-----send text to server and get result-----//
        ssummary_url = "http://127.0.0.1:8000/"
        $.ajax({
            type: 'POST',
            url: ssummary_url,
            data: { 'content': text, 'deep': deep},
            Headers: {
                'Access-Control-Allow-Origin': '*',
            },
            beforeSend: function(){
                console.log("length: " + text.length + "\nbefore:\n" + text);
            },
            success: function(data, status){
                console.log("length: " + data.length + "\nafter:\n" + data);
                resolve(data);
            },
            error: function(xhr, status, error){
                console.log(error);
                reject(error);
            }
        });
    });
}