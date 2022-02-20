'use strict';

function bnt1_fn() {
    // jquery code
    chrome.tabs.executeScript({
        file: 'jquery.js'
    }, function(result) {
        document.getElementById('result').innerText = "요약중...";
    });

    // sum.js code
    chrome.tabs.executeScript({ 
        file: 'sum.js', 
    }, function (result) {
        // print result
        document.getElementById('result').innerText = result[0];

        // set result to storage
        chrome.storage.sync.set({'result': result[0]});
    });

    chrome.tabs.executeScript({ 
        code: "chrome.storage.sync.set({'url': document.location.href});"
    });
};


// when popup.html is loaded
document.addEventListener('DOMContentLoaded', function () {   
    // add click event to button
    document.getElementById("btn1").addEventListener('click', bnt1_fn);

    // get result from storage
    chrome.storage.sync.get(function (data) {
        let result = data.result ? data.result : "";

        chrome.tabs.executeScript({ 
            code: "chrome.storage.sync.get(function (data) { \
                let url = data.url ? data.url : ''; \
                return url; \
            });"
        });
            
        let textarea = document.getElementById('result')
        textarea.innerText = data.url + "\n" +  document.location.href;

        // if url is not same, then clear result
        if (data.url !== document.location.href) {
            result = "";
        }

        // document.getElementById('result').innerText = result;
    });
});
