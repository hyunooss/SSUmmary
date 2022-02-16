'use strict';

function bnt1_fn() {
    // jquery code
    chrome.tabs.executeScript(null, {
        file: 'jquery.js',
        allFrames: true,
        runAt: "document_idle"
    });

    // sum3에서 크롤링해서 텍스트박스에 보여주기
    chrome.tabs.executeScript(null, {
        file: 'sum.js',
        allFrames: true,
        runAt: "document_idle"
    });
};

document.addEventListener('DOMContentLoaded', function () {   
    // add click event to button
    document.getElementById("btn1").addEventListener('click', bnt1_fn);
});
