document.addEventListener("DOMContentLoaded", chat)

function chat() {
    namespace = '';

    // Connect to the Socket.IO server.
    // The connection URL has the format: http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed under "Received"
    socket.on('my_response', function(msg) {
	var log = document.getElementById('log');
	var item = document.createElement('li');
        item.innerHTML = msg.message;
	log.appendChild(item);
	console.log(msg);
	//log.append('<li>' + message.message + '</li>').html();
    });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server
//    var form = document.getElementById('broadcast');
//    form.addEventListener('submit', function(event) {
//	message = {name: form.children[0].value, message: form.children[1].value}
//	socket.emit('my_broadcast_event', message);
//	form.reset();
//	return false;
//    });
    
    $('form#broadcast').submit(function(event) {
	socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
	return false;
    });

    $('form#disconnect').submit(function(event) {
	socket.emit('disconnect_request');
	return false;
    });

    // Interval function that tests message latency by sending a "ping" 
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
	start_time = (new Date).getTime();
	socket.emit('my_ping');
    }, 1000);

    // Handler for "pong" message. When the pong is received, the time 
    // from the ping is stored, the average of the last 30 samples is displayed.
    socket.on('my_pong', function() {
	var latency = (new Date).getTime() - start_time;
	ping_pong_times.push(latency);
	ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
	var sum = 0;
	for (var i = 0; i < ping_pong_times.length; i++)
	    sum += ping_pong_times[i];
	$('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });

};
