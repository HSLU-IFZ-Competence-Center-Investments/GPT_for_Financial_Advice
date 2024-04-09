jQuery(function($){


	$(document).ready(function(){

		/**
		 * Slick init
		 */
	    initSlick();

		/**
		 * smooth scroll
		 */
		 
		// smooth scroll START	
		// Startpunkt für Scroll wenn per neue Seite anvisiert
		if ( window.location.hash ) scroll(0,0);
		
		// Bugfixing
		setTimeout( function() { scroll(0,0); }, 1);
		
		//Scrollfunktion zur Wiederverwendung
		function goToByScroll(hash, offsettop, time){
        	
        	console.log("Scroll gestartet");
        	
        	if($('html.csspositionsticky header').length){
	        	var headeroffset = $('header').height();
        	} else {
	        	var headeroffset = 0;
        	}
        	
        	var offsettop = offsettop || headeroffset;
        	var time = time || 2500;
        
		    var page = $("html, body");
		    
		   if (hash.length) {
			   
			   console.log("Scroll mit Offset: " + offsettop);
			   
				page.on("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove", function(){
		       		page.stop();
			   	});
			   	
			   page.animate({
					scrollTop: $(hash).offset().top-offsettop
				},{
					duration: time,
					done: function() {

						if($('header').height() < offsettop){
							console.log("Korrektur mit Offset: " + offsettop);
							offsettop = $('header').height() - 2;
							page.animate({ scrollTop: $(hash).offset().top-offsettop }, 100, function(){
								page.off("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove");
							});
						}
				   }	
				});
		   	}  
		}
		
// 		$(function() {
		
		    // Fall: Klick auf Link
		    $('a[href*="#"]:not([href="#"]):not(a[href="#mmenu_start"]):not([href="contact.html#subscribe"])').on('click', function(e) {
			    console.log("Klick erkannt");
		        goToByScroll($(this.hash));
		        
		        e.preventDefault();
		    });
		
		    // Fall: Anchor in URL
		    if(window.location.hash) {
			    setTimeout(function(){
				    goToByScroll(window.location.hash, 0, 2500);
				},500);
		    }
		
// 		});
		// smooth scroll END	


		/**
		 * scroll to top
		 */
		// scroll to top START
			var $scrollToTopLinks = $('.backtotop');
			
		    $scrollToTopLinks.click(function () {
				$("html, body").animate({
					scrollTop: 0
				}, 1000);
				return false;
		    });
		// scroll to top END

		/**
		 * Window resize/Window width change
		 */
		// window resize START
			var windowWidth = $(window).width();
	
			$(window).resize(function() {
				// timeout for resize
				// http://stackoverflow.com/questions/4298612/jquery-how-to-call-resize-event-only-once-its-finished-resizing
				var id;
				clearTimeout(id);
	
				if ($(window).width() != windowWidth) {
					windowWidth = $(window).width();
					id = setTimeout(function(){
						console.log('window width has changed');
					}, 500);
				}
			});
		
			$(window).on("orientationchange", function() {
				//console.log('orientation has changed');
			});
		// window resize END


		/**
		 * memo-tabs
		 */
		// memo-tabs START
			
			$(".tabs-wrapper").memoTabs();

		// memo-tabs END




		/**
		 * memo-moving-underline
		 */
		// memo-moving-underline START
			var $mainNavigation = $("#header .menu .mod_navigation ul");
			
			$mainNavigation.memoMovingUnderline({
				snakeDelay: 0,
			});

		// memo-moving-underline END


		/**
		 * object-fit fallback
		 */
		// object-fit fallback START
			
			if ( ! Modernizr.objectfit) {
				$('img').filter(function(){ return $(this).css('background-size') == 'cover'; }).each(function () {
				
				    var $image = $(this),
				        imgUrl = $image.prop('src');
				    if (imgUrl) {
				    	$image.parent()
				        .css('backgroundImage', 'url("./imgUrl.html")')
				        .addClass('object-fit-fallback');
				    }  
				});
			}

		// object-fit fallback END

		/**
		 * Responive tables
		 */
		// responive tables START
			if ($(".ce_table").length){
				var headertext = [];
				var headers = document.querySelectorAll("thead");
				var tablebody = document.querySelectorAll("tbody");
				
				for (var i = 0; i < headers.length; i++) {
					headertext[i]=[];
					for (var j = 0, headrow; headrow = headers[i].rows[0].cells[j]; j++) {
					  var current = headrow;
					  headertext[i].push(current.textContent);
					  }
				} 
				
				for (var h = 0, tbody; tbody = tablebody[h]; h++) {
					for (var i = 0, row; row = tbody.rows[i]; i++) {
					  for (var j = 0, col; col = row.cells[j]; j++) {
					    col.setAttribute("data-th", headertext[h][j]);
					  } 
					}
				}
			}
		// responive tables END
		
		
		/**
		 * featherlight load content from linked page
		 */
		// featherlight load content START
			$('a.featherlight-link').on('click', function(e){
				var currentURL = $(this).attr('href'),
				    contentSelector = '#main',
				    featherlightAjaxSelector = currentURL + ' ' + contentSelector;
			
				// featherlight
				$.featherlight(
					featherlightAjaxSelector,
					{
						variant: 'featherlight-base',
						closeIcon: '<img src="/files/template/img/icons/cross.svg" height="20" width="20">',
						afterContent: initSlick,
						type: true,
						loading: '<img src="/files/template/img/icons/loading-DNA.svg">',
						openSpeed: 100,
						closeSpeed: 500
					}
				)
				
				e.preventDefault();
			});
		// featherlight load content END

		
		/**
		 * Masonry init
		 */
		// masonry init START
			/*
			var $masonryContainer = $('.masonry-container'),
			    masonryItem = '.masonry-item';
			if ($masonryContainer.length){
				$masonryContainer.masonry({
					itemSelector: masonryItem,
					columnWidth: 200
				});
			}
		*/
		// masonry init END
		
	});
	
	$(window).load(function(){
		/**
		 * memo-progress-bar
		 */
		// memo-progress-bar START
			$(document).memoProgressBar({
				appendTo: "#header",
			});
		// memo-progress-bar END
		
		/**
		 * isotope init
		 */
		// isotope init START
			// remove margin of the columns
			/*
			if ($(".isotope-item").length){
				$('.isotope-item').css('margin-right', 0);
		
				// get the gutter width. Based on the margin of another element.
				var colRightMarginPx = $('.other-element-with-same-gutter-width').css('margin-right'),
				    colRightMargin = Math.ceil( parseFloat(colRightMarginPx) );
				    
				$(".isotope-container").isotope({
					layoutMode: 'moduloColumns',
					moduloColumns: {
						columnWidth: $('.element-with-same-width').outerWidth(),
						gutter: colRightMargin
					}
				});
			}
			*/
		// isotope init END
	});
	
	/**
	 * Simple slick init
	 */
	 
	// slick init START
	function initSlick(){
		var $slickSliderContainer = $(".slick-container");
		
		if ($slickSliderContainer.length){
			$slickSliderContainer.slick({
			    slidesToShow: 1,
				slidesToScroll: 1,
				autoplay: true,
				speed: 1000,
				autoplaySpeed: 2000,
			});
		}

	}
	// slick init END
	

	
});

