var button = document.createElement('div'); 
button.id = 'floating-button';
button.innerText = "Click";
button.classList.add('small');
document.body.appendChild(button);


button.onmouseover = function(event) {
    // add  big class
    event.target.className = 'big';
};

button.onmouseleave = function(event) {
    // add small class
    event.target.className = 'small';
};


var iframe = document.createElement('iframe');
iframe.src = chrome.runtime.getURL('popup.html');
iframe.scrolling = 'no';


button.onclick = function() {
    // floating popup iframe
    document.body.appendChild(iframe);
};


// close when click out of iframe
window.onclick = function(event) {
    if (event.target !== button) {
        if (document.body.hasChildNodes(iframe)) {
            document.body.removeChild(iframe);
        }
    }
};


// button draggable
button.onmousedown = function(event) {
    var x = event.clientX - button.offsetLeft;
    var y = event.clientY - button.offsetTop;
    var mousemove = function(event) {
        button.style.left = event.clientX - x + 'px';
        button.style.top = event.clientY - y + 'px';
    }
    var mouseup = function() {
        document.removeEventListener('mousemove', mousemove);
        document.removeEventListener('mouseup', mouseup);
    }
    document.addEventListener('mousemove', mousemove);
    document.addEventListener('mouseup', mouseup);
};