//-----button for iframe-----//
var button = document.createElement('div'); 
button.id = 'floating_button';
button.classList.add('small');
document.body.appendChild(button);


//-----iframe for iframe.html-----//
var iframe = document.createElement('iframe');
iframe.id = 'ssupago_iframe';
iframe.src = chrome.runtime.getURL('html/iframe.html');
iframe.scrolling = 'no';
iframe.style.display = 'none';
document.body.appendChild(iframe);


//-----big/small when mouseover-----//
button.onmouseover = function(event) {
    event.target.className = 'big';
};
button.onmouseleave = function(event) {
    event.target.className = 'small';
};


//-----button draggable-----//
button.onmousedown = function(event) {
    var x1 = event.clientX;
    var y1 = event.clientY;
    var x = x1 - button.offsetLeft;
    var y = y1 - button.offsetTop;

    var mousemove = function(event) {
        // drag text disabled
        event.preventDefault();

        let x2 = event.clientX - x;
        let y2 = event.clientY - y;

        // stop going beyond the window
        x2 = Math.min(Math.max(x2, 0), window.window.innerWidth - button.offsetWidth);
        y2 = Math.min(Math.max(y2, 0), window.window.innerHeight - button.offsetHeight);
        button.style.left = x2 + 'px';
        button.style.top = y2 + 'px';

        // iframe follow button position
        let iframeWidth = 250;
        let iframeHeight = 170;
        if (x2 > window.window.innerWidth - iframeWidth) {
            iframe.style.left = x2 - iframeWidth + 'px';
        }
        else {
            iframe.style.left = x2 + 20 + 'px';
        }
        if (y2 > window.window.innerHeight - iframeHeight) {
            iframe.style.top = y2 - iframeHeight + 'px';
        }
        else {
            iframe.style.top = y2 + 20 + 'px';
        }
    }
    var mouseup = function(event) {
        let dx = Math.abs(event.clientX - x1);
        let dy = Math.abs(event.clientY - y1);
        
        // if click and not drag
        if (dx < 2 && dy < 2) {
            iframe.style.display = 'block';
        }

        document.removeEventListener('mousemove', mousemove);
        document.removeEventListener('mouseup', mouseup);
    }
    document.addEventListener('mousemove', mousemove);
    document.addEventListener('mouseup', mouseup);
};


//-----close when click out of iframe-----//
window.onclick = function(event) {
    if (event.target !== button) {
        // remove iframe if it is exist
        if (iframe.parentNode) {
            iframe.style.display = 'none';
        }
    }
};


// get on_off from storage
chrome.storage.sync.get(function (data) {
    document.getElementById('floating_button').style.display = data.on_off ? 'block' : 'none';
});