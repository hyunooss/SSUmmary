//-----button for iframe-----//
var button = document.createElement('div'); 
button.id = 'floating-button';
button.classList.add('small');
document.body.appendChild(button);


//-----iframe for popup.html-----//
var iframe = document.createElement('iframe');
iframe.src = chrome.runtime.getURL('html/popup.html');
iframe.scrolling = 'no';


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
        button.style.left = event.clientX - x + 'px';
        button.style.top = event.clientY - y + 'px';
    }
    var mouseup = function(event) {
        let dx = Math.abs(event.clientX - x1);
        let dy = Math.abs(event.clientY - y1);
        if (dx < 5 && dy < 5) {
            document.body.appendChild(iframe);
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
            iframe.parentNode.removeChild(iframe);
        }
    }
};
