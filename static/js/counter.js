function counter(increment, start) {
	this.increment = increment;
	this.start = start;
	this.get_counter_path = 'http://127.0.0.1:5000/getcounter?increment=' + this.increment + '&counter=' + this.start;
	this.rowid = undefined;
	this.increment_path = undefined;
}

var counters = [new counter(1, 0), new counter(-1, 100)];

var ajax_ = function(path, callback, params) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			callback(JSON.parse(xhttp.responseText), params);
		}
	};
	xhttp.open("GET", path, true);
	xhttp.send();
};

var change_text = function(new_count, domid) {
	var counter_text = document.getElementById('counter' + domid);
	counter_text.innerHTML = new_count;
};

var init_counter = function(response, idx) {
	counters[idx].rowid = response['rowid'];
	counters[idx].increment_path = 'http://127.0.0.1:5000/increment/' + response['rowid'];
};

window.onload = function() {
	for (var i = 0; i < counters.length; i++) {
		change_text(counters[i].start, i);
		ajax_(counters[i].get_counter_path, init_counter, i);
	}
}

setInterval(function() {
	for (var i = 0; i < counters.length; i++) {
		ajax_(counters[i].increment_path,
			function(response, idx) {
				change_text(response['counter'], idx);
			}, 
		i);
	}
}, 1000);




