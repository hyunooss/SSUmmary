'use strict';

var myInterval;

function preprocess_text(text) {
    let ret = "";
    let textList = text.split('\n');

    textList.forEach(function (line) {
        line += ".";
        if (line.length > 50) { ret += " " + line; }
    });
    
    ret = ret.replaceAll('。', '.');
    ret = ret.replaceAll('、', ',');
    return ret;
};

function progress_bar_fn(leng) {
    let time = 5;
    document.getElementById("progress_bar").max = time;

    var cur = 0;
    function myTimer() {
        document.getElementById("progress_bar").value = cur;
        if (cur < document.getElementById("progress_bar").max-0.5) {
            cur += 0.01;
        }
    }
    myInterval = setInterval(myTimer, 10);
}

async function result_textarea_fn(text, deep, target_lang) {
    var result = await summarize_fn(text, deep, target_lang);
    document.getElementById('result_textarea').innerText = await result;

    // stop progress bar
    clearInterval(myInterval);
    document.getElementById("progress_bar").value = document.getElementById("progress_bar").max;

    // set data to storage
    chrome.tabs.executeScript({ 
        code: "document.location.href;"
    }, function (current_url) {
        chrome.storage.sync.set({'url': current_url[0]});
        chrome.storage.sync.set({'result': result});
    });

    document.getElementById('btn1').disabled = false;
};

function bnt1_fn() {
    
    chrome.tabs.executeScript({ 
        code: "document.body.innerText"
    }, function (text) {
        if (!text) {
            document.getElementById('result_textarea').innerText = 'Error';
            return;
        }
        document.getElementById('result_textarea').innerText = "Wait...";
        document.getElementById('btn1').disabled = true;

        let preprocessed_text = preprocess_text(text[0]);

        // progress bar animate
        progress_bar_fn(preprocessed_text.length);

        // summarize
        chrome.storage.sync.get(function (data) {
            const deep = data.deep ? true : false;
            const target_lang = data.target_lang ? data.target_lang : 'ko';

            result_textarea_fn(preprocessed_text, deep, target_lang);
        });
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
            document.getElementById('result_textarea').innerText = data.result;
            if (data.url != current_url[0]) {
                document.getElementById('result_textarea').innerText = "";
            }
        });
    });
});
