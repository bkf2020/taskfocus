var timers = document.getElementsByClassName('timer');
var endTimes = [];
var taskStarted = [];

for(var i = 0; i < timers.length; i++) {
	var secondsDiff = timers[i].getAttribute('start-time') - timers[i].getAttribute('curr-server-time');
	endTimes.push(Date.now() + 1000 * secondsDiff);
    taskStarted.push(false);
}

function updateTimers() {
	var timers = document.getElementsByClassName('timer');
	for(var i = 0; i < timers.length; i++) {
		var millisecondsLeft = endTimes[i] - Date.now();
		if(millisecondsLeft >= 1000) {
			var totSeconds = Math.floor(millisecondsLeft / 1000);
			var seconds = totSeconds % 60;
			totSeconds -= totSeconds % 60;
			totSeconds /= 60;
			
			var minutes = totSeconds % 60;
			totSeconds -= totSeconds % 60;
			totSeconds /= 60;

			var hours = totSeconds;

			timers[i].querySelector('.hour').innerText = hours + "h";
            timers[i].querySelector('.min').innerText = minutes + "m";
            timers[i].querySelector('.sec').innerText = seconds + "s";
			setTimeout(updateTimers, 100);
        } else if (!taskStarted[i]) {
            taskStarted[i] = true;
            var secondsDiff = timers[i].getAttribute('end-time') - Math.max(timers[i].getAttribute('start-time'), timers[i].getAttribute('curr-server-time'));
            endTimes[i] = Date.now() + 1000 * secondsDiff;
            timers[i].querySelector('.starting-desc').innerText = "Ending in: ";
            setTimeout(updateTimers, 100);
        } else {
            timers[i].querySelector('.starting-desc').innerText = "Completed: ";
        }
	}
}
updateTimers();