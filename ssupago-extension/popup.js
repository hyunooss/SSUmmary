'use strict';

function bnt1_fn() {
    // jquery code
    chrome.tabs.executeScript({
        file: 'jquery.js'
    }, function(result) {
        document.getElementById('result').innerText = "요약중...";
    });

    // sum3에서 크롤링해서 텍스트박스에 보여주기
    chrome.tabs.executeScript({ 
        file: 'sum.js', 
    }, function (result) {
        document.getElementById('result').innerText = result[0];
    });
};

document.addEventListener('DOMContentLoaded', function () {   
    // add click event to button
    document.getElementById("btn1").addEventListener('click', bnt1_fn);
});
