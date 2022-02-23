'use strict';

var myInterval;

function preprocess_text(text) {
    let ret = "";
    text.split('\n').forEach(function (line) {
        if (line.length > 50) { ret += line; }
    });
    ret = ret.replaceAll('。', '.');
    ret = ret.replaceAll('、', '.');
    return ret;
};

function progress_bar_fn(leng) {
    let time = 20;
    if (leng > 5000) {
        time = 50;
    }
    else if (leng > 4000) {
        time = 40;
    }
    else if (leng > 3000) {
        time = 30;
    }

    if (!time) {
        document.getElementById('result').innerText = 'Error';
        return;
    }

    document.getElementById('result').innerText = "요약중...";
    document.getElementById("probar").max = time;

    var cur = 0;
    function myTimer() {
        document.getElementById("probar").value = cur;
        if (cur < document.getElementById("probar").max-0.5) {
            cur += 0.1;
        }
    }
    myInterval = setInterval(myTimer, 100);
}

async function result_textarea_fn(text) {
    document.getElementById('result').innerText = await summarize_fn(text);

    // stop progress bar
    clearInterval(myInterval);
    document.getElementById("probar").value = document.getElementById("probar").max;

    // set url to storage
    chrome.storage.sync.set({'url': document.location.href});
};

function bnt1_fn() {
    chrome.tabs.executeScript({ 
        code: "document.body.innerText"
    }, function (text) {
        if (!text) {
            document.getElementById('result').innerText = 'Error';
            return;
        }

        document.getElementById('result').innerText = "요약중...";

        let preprocessed_text = preprocess_text(text[0]);

        // progress bar animate
        progress_bar_fn(preprocessed_text.length);

        // summarize
        result_textarea_fn(preprocessed_text);
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
