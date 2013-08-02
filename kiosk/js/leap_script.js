var pingResetTime = 5000; // 5 Sec
var rfidResetTime = 5000; // 20 Sec Idle

var CALIBRATE = 0;
var MOVE_CONTROLLER = 1;
var calibrateClicked = false;

var docWidth = -1;
var docHeight = -1;

var initX = -20;//-1;
var initY = 130;//-1;
var mulX  = 6.58;//-1;
var mulY  = 6.58;//-1;
var virtualMouseDown = false;

var frameIndex = 0;
var mode = -1;
var currCal = 1;
var currAd = 0;
var controller = new Leap.Controller({enableGestures: false});
var timer1 = null;
var hoverElem = null;
var hoverClasses = Array('view-trans', 'view-related');

controller.loop(function(frame) {
	// Uses 3 frames per second
	frameIndex += 1;
	if (frameIndex % 3 != 0)
		return;
		
	frameIndex = 0;
	if (mode == CALIBRATE) {
		$('#cal-'+currCal).css('background-color', (frame.hands.length == 1 ? 'green' : 'white'));
		if (calibrateClicked && frame.hands.length == 1) {
			hand = frame.hands[0];
			posX = hand.palmPosition[0];
			posY = hand.palmPosition[1];
			posZ = hand.palmPosition[2];
		
			if (currCal == 1) {
				initX = posX;
				initY = posY;
				console.log(hand.palmPosition);
			} else if (currCal == 2) {
				mulX = docWidth / (posX - initX);
			} else if (currCal == 3) {
				mulY = docHeight / (initY - posY);
				console.log(mulX);
				console.log(mulY);
			}
		
			$('#cal-'+currCal).css('display', 'none');					
			if (currCal >= 3) {
				changeMode(MOVE_CONTROLLER);
				alert('Calibration Complete.');
			} else {
				$('#cal-'+(currCal+1)).css('display', 'block');
				currCal += 1;
			}
		}
		
		calibrateClicked = false;
		
	// Move Controller method
	} else if (mode == MOVE_CONTROLLER){
		if (frame.hands.length == 0) {
			$('#square').fadeOut('fast');
		} else {
			$('#square').fadeIn('fast');
		}
	
		if (frame.fingers.length >= 1) {
			for (var i=0; i<frame.hands.length; i++) {
				hand = frame.hands[i];
				posX = (hand.palmPosition[0] - initX) * mulX;
				posY = (initY - hand.palmPosition[1]) * mulY;
				posZ = hand.palmPosition[2] / 2;
				
				$('#square').css('left', posX + 45);
				$('#square').css('top', posY + 45);
				

				pageX = $('#square').css('left');
				pageY = $('#square').css('top');
				
				pageX = parseInt(pageX.substring(0, pageX.length-2)) - 1;
				pageY = parseInt(pageY.substring(0, pageY.length-2)) - 1;
				
				// Set hover
				var hElem = document.elementFromPoint(pageX, pageY);
				for (i=0;i<hoverClasses.length;i++) {
					if (hoverElem == null && $(hElem).attr('id') == hoverClasses[i]) {
						hoverElem = $(hElem);
						hoverElem.addClass('hover');
						break;
					}
				}	
				
				if (hoverElem != null) { 
					if ($(hElem).attr('id') != hoverElem.attr('id')) {
						hoverElem.removeClass('hover');
						hoverElem = null;
					}
				}
				
				width = posZ
				if (width > 30)
					width = 30;
				else if (width < 10) {
					width = 10;
					$('#square').css('background-color', '#BADA55');
					virtualMouseDown = true;
				} else {
					$('#square').css('background-color', 'white');
					if (virtualMouseDown) {
						virtualMouseDown = false;
						
						
						var elem = document.elementFromPoint(pageX, pageY);
						if ($(elem).get(0).nodeName != 'HTML' && $(elem).get(0).nodeName != 'BODY') {
							$(elem).click();
						}
						//$(elem).css('background-color', 'black');
						
						
					}
				}
				$('#square').css('width', width);
				$('#square').css('height', width);
				$('#square').css('border-radius', (width / 2) + 5);
			}
		}
		for (var i=0; i < frame.gestures.length; i++)
			console.log(frame.gestures);
	}
});

controller.connect();

function calibrationClick() {
	if (mode != CALIBRATE)
		return;
		
	calibrateClicked = true;
}

function changeMode(newMode) {
	if (mode == CALIBRATE)
		$('#calibrate-group').css('display', 'none');
	if (newMode == CALIBRATE)
		$('#calibrate-group').css('display', 'block');
		
	if (mode == MOVE_CONTROLLER)
		$('#hand-group').css('display', 'none');
	if (newMode == MOVE_CONTROLLER)
		$('#hand-group').css('display', 'block');
		
	mode = newMode;
}

function processWsData(data) {
	params = data.split(',');
	
	if (params[0] == 'rfid') {
		clearTimeout(timer1);
		resetHome();
		processRfid(params[1]);
		console.log('Display RFID data: '+ params[1]);
	
	// Card been removed
	} else if (params[0] == 'rcard') {
		clearTimeout(timer1);
		timer1 = setTimeout(setToAds, rfidResetTime);
	
	} else if (params[0] == 'ping') {
		if (params[1] < 10 && $('#home-content').css('display') == 'none') {
			clearTimeout(timer1);
			$('body').children('div:not(#square):not(#near-content)').fadeOut('fast');
			$('#square').css('display', 'block');
			$('#near-content').css('display', 'block');
			timer1 = setTimeout(setToAds, pingResetTime);
		}
	
		console.log('Ping detected. Distance: ' + params[1] + 'cm.');
	}
	
}

function resetHome() {
	d_data = $('#home-content-default').html();
	$('#home-content').html(d_data);
}

function setToAds() {
	$('body').children('div:not(#ad-content)').fadeOut('fast');
	$('#ad-content').css('display', 'block');
}


trans_data = null;
function processRfid(id) {
	$('body').children('div:not(#square):not(#home-content)').fadeOut('fast');
	$('#square').css('display', 'block');
	$('#home-content').css('display', 'block');
	$('#home-content .content .functions').prepend('<h3>Card Identifier: '+id+'</h3>');
	
	
	id = '90D9B';
	$.ajax({
		url:"proxy.php?type=purchases&id="+id,
		type:'GET',
		dataType: 'JSON',
		success:function(data){
			enableRfidFunctions();
			trans_data = data;
		}
	});
}

function enableRfidFunctions() {
	$('#home-content .content .functions').css('display', 'block');
	$('#home-content .content .loading-msg').css('display', 'none');
}

function startWebSocket() {
	var ws = new WebSocket("ws://localhost:8888/websocket");
	ws.onopen = function() {
	   ws.send("ping");
	};
	ws.onmessage = function (evt) {
		processWsData(evt.data);
	};
}

function loopAdGallery() {
	adImg = $('.ad-img');
	$('.ad-img').eq(currAd).css('z-index', adImg.length);
	if (currAd >= adImg.length) {
		currAd = 0;
	} else {
		currAd += 1;
	}
	
	adImg.eq(currAd).css('display', 'none');
	adImg.eq(currAd).css('z-index', adImg.length + 1);
	adImg.fadeIn('fast');
}

$(document).ready(function() {
	startWebSocket();
	setInterval(loopAdGallery, 5000);
	
	docWidth = $(document).width() - 90;
	docHeight = $(document).height() - 90;
	changeMode(MOVE_CONTROLLER);//CALIBRATE);
	
	$('body').keyup(function(e){
		if(e.keyCode == 32){
			calibrationClick();
		}
	});
	
	$('body').click(function(e) {
		calibrationClick();
	});
	
	$('#click-icon').click(function(e) {
		console.log('btn clicked.');
		$('#popup-group').fadeIn('fast');
	});
	
	$(document).on('scroll', '', function(){
		$('.header').css('top', $('body').scrollTop());
	});
	
	$(document).on('click', '#view-trans', function() {
		transContent = '<div class="transaction">ID: {0}<br/>Items Purchased:<br/>{1}</div>';
		htmlContent = '';
		
		for (var index in trans_data) {
			products = '<ol>{0}</ol>';
			
			transaction = trans_data[index];
			trans_str = ''
			for (var i in transaction) {
				trans_str += '<li>'+transaction[i]['name']+' -> $'+transaction[i]['price'] + '</li>';
			}
			
			newContent = transContent.replace('{1}', products.replace('{0}', trans_str));
			htmlContent += newContent.replace('{0}', index);
		}
		$('#trans-content .content').html(htmlContent);
	
		$('body').children('div:not(#square):not(#trans-content)').fadeOut('fast');
		$('#square').css('display', 'block');
		$('#trans-content').css('display', 'block');
	});
	
	$(document).on('click', '#view-related', function() {
		console.log('Viewing Related');
	});
	
	$('#popup-group .overlay').click(function() {
		$('#popup-group').fadeOut();
	});
	
	$('.back-home').click(function() {
		$('body').children('div:not(#square):not(#home-content)').fadeOut('fast');
		$('#square').css('display', 'block');
		$('#home-content').css('display', 'block');
	})
});