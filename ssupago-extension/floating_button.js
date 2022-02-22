var button = document.createElement('div'); 
button.id = 'floating-button';
button.innerText = "Click";
button.style.position = 'fixed';
button.style.bottom = '20px';
button.style.right = '20px';
button.style.width = '40px';
button.style.height = '40px';
button.style.backgroundColor = '#00bcd4';
button.style.textAlign = 'center';
button.style.color = 'white';
button.style.lineHeight = '40px';
button.style.cursor = 'pointer';
button.style.borderRadius = '10px';
button.style.zIndex = '999';
document.body.appendChild(button);

var iframe = document.createElement('iframe');

button.onclick = function() {
    // floating popup iframe
    iframe.src = chrome.runtime.getURL('popup.html');
    iframe.style.position = 'fixed';
    iframe.style.bottom = '40px';
    iframe.style.right = '40px';
    iframe.style.width = '250px';
    iframe.style.height = '170px';
    iframe.style.border = 'none';
    iframe.scrolling = 'no';
    iframe.style.zIndex = '9999';
    iframe.style.backgroundColor = 'white';
    iframe.style.opacity = '0.95';
    iframe.style.borderRadius = '5px';
    document.body.appendChild(iframe);
};

window.onclick = function(event) {
    if (event.target !== button) {
        if (document.body.hasChildNodes(iframe)) {
            document.body.removeChild(iframe);
        }
    }
};
