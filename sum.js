// get text from document
text = document.body.innerHTML;
text = "김병만이 친구 김병만이";
result = text;


// do something with text
papago_url = "https://papago.naver.com/?sk=auto&tk=ko&st=";
papago_url += encodeURIComponent(text);
papago_url = papago_url.slice(0, 2000);

// $.ajax({
//     type: 'GET',
//     url: papago_url, 
//     dataType: 'jsonp',
//     success: function(data, status) {
//         console.log("success");
//         result = data.getElementById('txtTarget').innerText;
//     }
// });



// do same thing to sum3
sumz3_url = "https://summariz3.herokuapp.com/";

// $.ajax({
//     type: 'POST',
//     url: sumz3_url, 
//     data: { content: result },
//     Headers: {
//         'Access-Control-Allow-Origin': '*',
//     },
//     success: function(data, status){
//         console.log(data);
//     }
// });


// send text to server and get result
$.ajax({
    type: 'POST',
    url: "http://localhost:8000/ssupago/",
    data: { content: text },
    success: function(data, status){
        console.log(data);
    }
});

// print result
// console.log(result);

// test