'use strict';

(function( $ ) {
	
	$.fn.memoMovingUnderline = function(options) {
		var settings = $.extend({
			line: $("<li class='line'></li>"),
			item: "li",
			activeClass: "active",
			lineContainerClass: "line-container",
			snakeDelay: 200,
		}, options);
		
		/**
		 * Navigation hover
		 */
		// navigation hover START
		var $mainNavigation = this,
		    $line = settings.line;
		
		$mainNavigation.addClass(settings.lineContainerClass);
		$line.appendTo( $mainNavigation );
		
// 		function getParentOffset

		var linePosition = {};
		linePosition.left = function(){
// 			console.log($(this));
			var position = $line.position();
			
			return position.left;
		};
		
		linePosition.right = function(){
			var position = $line.position();
			var offsetRight = $mainNavigation.width() - position.left - $line.innerWidth();
			
			return offsetRight;
		};
		
		var mainNavigationWidth = $mainNavigation.width(),
		    lineDelay = 200;
		
		moveLineToInitalActiveItem( $line[0] );
/*
		var $initialActiveItem = $mainNavigation.find("li.active");
		
		if ( $initialActiveItem.length ) {
			moveLineToItem( $line[0], $initialActiveItem[0] );
		}
*/
		
		$mainNavigation.children(settings.item).not($line).on("mouseenter", function(){
			moveLineToItem( $line[0], this);
		});
		
		$mainNavigation.on("mouseleave", function(){
			moveLineToInitalActiveItem( $line[0] )
		});
		// navigation hover END
		
		function itemPosition( currentItem ) {
			var $currentItem = $( currentItem );
			var $relativeParent = $currentItem.offsetParent();
			
			var currentItemPosition = $currentItem.position(),
			    elementWidth = $currentItem.innerWidth(),
			    currentItemRight = $relativeParent.width() - currentItemPosition.left - $currentItem.innerWidth();
			
			var left = currentItemPosition.left;
			this.left = left;
			
			var right = $relativeParent.width() - currentItemPosition.left - elementWidth;
			this.right = right;
		}
		
		function moveLineToItem( line, targetItem ){
			var lineDelay = settings.snakeDelay;
			
			var linePos = new itemPosition( line ),
			    targetPos = new itemPosition( targetItem );
			
			var leftProperty = { delay: lineDelay },
			    rightProperty = { delay: 0 };
			
			if( targetPos.left < linePos.left ) {
				leftProperty.delay = 0;
				rightProperty.delay = lineDelay;
			}
			
			// set timeout for both. Delay depends on the previous position of the line.
			setTimeout(function(){
				$(line).css("left", targetPos.left );
			}, leftProperty.delay);
			
			setTimeout(function(){
				$(line).css("right", targetPos.right );
			}, rightProperty.delay);
		}
		
		function moveLineToInitalActiveItem( line ) {
			var $initialActiveItem = $mainNavigation.find( settings.item + "." + settings.activeClass );
			
			if ( $initialActiveItem.length ) {
				moveLineToItem( $line[0], $initialActiveItem[0] );
			} else {
				$(line).removeAttr("style");
			}
		}
		
		return this;
	}
	
/*
	function moveLine($current){
		var currentPosition = $(this).position(),
		    elementWidth = $(this).innerWidth(),
		    currentItemLeft = currentPosition.left,
		    currentItemRight = mainNavigationWidth - currentPosition.left - elementWidth;
		
		var leftProperty = { delay: lineDelay },
		    rightProperty = { delay: 0 };
		
		if( currentItemLeft < linePosition.left() ) {
			leftProperty.delay = 0;
			rightProperty.delay = lineDelay;
		}
		
		// set timeout for both. Delay depends on the previous position of the line.
		setTimeout(function(){
			$line.css("left", currentItemLeft);
		}, leftProperty.delay);
		
		setTimeout(function(){
			$line.css("right", currentItemRight );
		}, rightProperty.delay);
	}
*/
	
// 	function moveLine($current)
} (jQuery) );