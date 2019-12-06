var remain = 0

function startTimer() {
    remain = 3
    doInterval()
    setInterval("doInterval()", 1000)
}

function doInterval() {
    if (remain > 0) {
        remain -= 1
    }

    document.getElementById("Remainseconds").innerHTML = remain
    document.getElementById("Global-time").innerHTML = Date()

    if (remain > 0) {
        hideBaidu()
    } else {
        showBaidu()
    }
}

function showBaidu() {
    document.getElementById("baidu-float").style.visibility = "visible";
}

function hideBaidu() {
    document.getElementById("baidu-float").style.visibility = 'hidden';
}

hideBaidu()
startTimer()