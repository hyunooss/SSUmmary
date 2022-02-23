'use strict';

// when popup.html is loaded
document.addEventListener('DOMContentLoaded', function () {   
    document.querySelector('#switch').onclick = function (event) {
        let on_off = event.target.checked;
        // on/off floating_button
        chrome.tabs.executeScript({
            code: "document.getElementById('floating-button').style.display = '" + (on_off ? 'block' : 'none') + "';"
        });
        
        // set on_off to storage
        chrome.storage.sync.set({'on_off': on_off});
    };

    // get on_off from storage
    chrome.storage.sync.get(function (data) {
        document.querySelector('#switch').checked = data.on_off;
    });
});