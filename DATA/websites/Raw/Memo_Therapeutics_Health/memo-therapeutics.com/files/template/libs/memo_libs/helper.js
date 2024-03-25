/**
 * Depending on your markup and styling you are gonna need different selectors and properties. The stored data properties are there as example.
 */


function lockScroll() {
	var scrollPosition = [
		self.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft,
		self.pageYOffset || document.documentElement.scrollTop  || document.body.scrollTop
	];
	
	var $html = jQuery('html'); // it would make more sense to apply this to body, but IE7 won't have that
	var $header = jQuery('#header .header-wrapper');
	var headerWidth = $header.innerWidth();
	
	$html.data('scroll-position', scrollPosition);
	$html.data('previous-overflow', $html.css('overflow'));
	$html.data('previous-width', $html.css('width'));
	
	$html.css({
		'overflow': 'hidden',
		'width': $html.width(),
	});
	$header.css("width", headerWidth );
	window.scrollTo(scrollPosition[0], scrollPosition[1]);
}

function unlockScroll() {
	// un-lock scroll position
	var $html = jQuery('html');
	var $header = jQuery('#header .header-wrapper');
	var scrollPosition = $html.data('scroll-position');
	
	$html.css({
		'overflow': '',
		'width': '',
	});
	$header.css("width", "");
	
	window.scrollTo(scrollPosition[0], scrollPosition[1])
}

function isIE(){
	var ua = window.navigator.userAgent;
	var msie = ua.indexOf("MSIE ");
	
	var isIE;
	
	if( msie > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./) ) {
		isIE = true;
	} else {
		isIE = false;
	}
	
	return isIE;
}
