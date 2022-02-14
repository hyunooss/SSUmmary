'use strict';

function bnt1_fn() {
    // sum3에서 크롤링해서 텍스트박스에 보여주기
    chrome.tabs.executeScript(null, {
        file: 'sum.js'
    }, function() {
        window.close();
    });
};

document.addEventListener('DOMContentLoaded', function () {   
    // add click event to button
    document.getElementById("btn1").addEventListener('click', bnt1_fn);
});