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

    // set url to storage
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
        // if url is not same, then clear result
        chrome.tabs.executeScript({ 
            code: "document.location.href;"
        }, function (current_url) {
            document.getElementById('result').innerText = data.result;
            if (data.url != current_url) {
                document.getElementById('result').innerText = "";
            }
        });
    });
});
