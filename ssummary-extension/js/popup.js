'use strict';

// when popup.html is loaded
document.addEventListener('DOMContentLoaded', function () {   
    document.querySelector('#switch').onclick = function (event) {
        const on_off = event.target.checked;
        // on/off floating_button
        chrome.tabs.executeScript({
            code: "document.getElementById('floating_button').style.display = '" + (on_off ? 'block' : 'none') + "';"
        });
        
        document.querySelector('#Floating_ONOFF').innerHTML = on_off ? "<b>ON</b>" : "<b>OFF</b>";

        // set on_off to storage
        chrome.storage.sync.set({'on_off': on_off});
    };

    document.querySelector('#switch2').onclick = function (event) {
        const on_off = event.target.checked;

        // set on_off to storage
        chrome.storage.sync.set({'deep': on_off});
    };

    // get on_off from storage
    chrome.storage.sync.get(function (data) {
        document.querySelector('#switch').checked = data.on_off;
        document.querySelector('#switch2').checked = data.deep;
        document.querySelector('#Floating_ONOFF').innerHTML = data.on_off ? "<b>ON</b>" : "<b>OFF</b>";
    });
});