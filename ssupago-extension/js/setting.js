'use strict';



// when popup.html is loaded
document.addEventListener('DOMContentLoaded', function () {   
    // add click event to button
    $(":checkbox[name=tester']").on({
        click: function(e){
            
        }
    })

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