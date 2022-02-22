var button = document.createElement('div'); 
button.innerHTML = '<div id=\"floating-button\" style=\"position:fixed;bottom:20px;right:20px;width:50px;height:50px;background-color:red;text-align:center;line-height:50px;color:white;cursor:pointer;\">Click</div>';
button.style.zIndex = '999';
document.body.appendChild(button);

button.onclick = function() {
    // floating popup iframe
    var iframe = document.createElement('iframe');
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