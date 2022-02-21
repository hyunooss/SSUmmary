'use strict';

var cur = 0;
function myTimer() {
    // const d = new Date();
    document.getElementById("probar").value = cur;
    cur ++;
}

function end_time(){
    clearTimeout(myTimer);
}


function bnt1_fn() {
    // jquery code
    chrome.tabs.executeScript({
        file: 'jquery.js',
    }, function(result) { 
        // document.getElementById('result').innerText = "요약중...";
    });

    // progress 
    chrome.tabs.executeScript({
        file: 'progress.js',
    }, function(result) { 
        document.getElementById('result').innerText = "요약중 ...\r\n예상 대기 시간 약 " + result[0];
        document.getElementById("probar").max = result[0];
        
        
        let myVar1 = setInterval(myTimer, 1000);

        
    });
    

    // sum.js code
    chrome.tabs.executeScript({ 
        file: 'sum.js', 
    }, function (result) {
        // print result
        document.getElementById('result').innerText = result[0];
    
        // set result to storage
        chrome.storage.sync.set({'result': result[0]});

        // 
        end_time();
        document.getElementById("probar").value = document.getElementById("probar").max;
    });

    // set url to storage
    chrome.tabs.executeScript({ 
        code: "chrome.storage.sync.set({'url': document.location.href});"
    });




    // chrome.tabs.executeScript(null, { file: "jquery.js" }, function(result) {
    //     document.getElementById('result').innerText = "요약중...";

    //     chrome.tabs.executeScript(null, { file: "sum.js" }, function(result) {
    //         document.getElementById('result').innerText = result[0];

    //         chrome.tabs.executeScript({ code: "chrome.storage.sync.set({'url': document.location.href});" })
    //     })
    // });
    
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
