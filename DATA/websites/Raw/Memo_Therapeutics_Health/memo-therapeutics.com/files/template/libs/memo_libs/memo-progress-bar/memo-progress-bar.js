'use strict';

(function( $ ) {
	
	$.fn.memoProgressBar = function(options) {
		var settings = $.extend({
			appendTo: $("body"),
			progressCssProperty: "width",
		}, options);
		
		var $progressBar = $("<div class='progress-wrapper'><div class='progress'></div></div>").appendTo(settings.appendTo);
		var $progress = $progressBar.find(".progress");
		
		$progressBar.addClass("property-" + settings.progressCssProperty);
		
		this.on("scroll", function(){
			$progress.css(settings.progressCssProperty, getScrolledProportion() + "%");
		});
		
		var getScrolledProportion = function(){
			var documentHeight = $(document).height(),
			    scrollWay = documentHeight - $(window).height();
			    
			var scrolled = $(document).scrollTop(),
			    scrolled = scrolled / scrollWay * 100;
			
			return scrolled;
		}
		
		return this;
	}
} (jQuery) );