jQuery(function($){

	$(document).ready(function(){
	
		var $flexcontainer = $(".header-wrapper");
		var $backgroundcontainer = $(".header-background");
	
		//Scroll erkennen und Klase hinzufügen/enternen
		$(window).scroll(function() {
		    var scroll = $(window).scrollTop();
		    
		    //$container.height('auto');
		    if (scroll >= 150) {
		        $flexcontainer.removeClass("large");
		        $backgroundcontainer.removeClass("large");
		        layoutleft();
		        layoutright();
		        animateheight();
		    } else if(scroll <= 50) {
		        $flexcontainer.addClass("large");
		        $backgroundcontainer.addClass("large");
		        layoutleft();
		        layoutright();
		        animateheight();
		    }
		});
		
		$(window).resize(function(){
			if ($(window).width() <= 768){	
				var additionalheight = 20;
			} else {
				var additionalheight = 5;
			}
		});
		
		function animateheight(){
			var currentheight = $backgroundcontainer.css("max-height");
			var newheight = $flexcontainer.outerHeight() + 20;
		    
		    if(currentheight != newheight){
			    $backgroundcontainer.outerHeight(newheight);
			    $backgroundcontainer.css("max-height", newheight);
		    }
		}
	
		/* Für links */
	
		var boxNodeleft = $(".menu.left")[0];
		
		// Initialize transforms on node
		TweenLite.set(boxNodeleft, { x: "+=0" });
		
		var boxleft = {
		  node: boxNodeleft,
		  x: boxNodeleft.offsetLeft,
		  y: boxNodeleft.offsetTop,
		  transform: boxNodeleft._gsTransform
		};
		
		function layoutleft(event) {
			
			// Last offset position
			var lastX = boxleft.x;
			var lastY = boxleft.y;
			
			// Record new offset position
			boxleft.x = boxleft.node.offsetLeft;
			boxleft.y = boxleft.node.offsetTop;
			
			//console.log('lastX: ' + lastX + ', box.x: ' + box.x + ', lastY: ' + lastY + ', box.y: ' + box.y);
			
			// Exit if box hasn't moved
			if (lastX === boxleft.x && lastY === boxleft.y) return;
			
			// Reversed delta values taking into account current
			// transforms in case animation was interrupted
			var x = boxleft.transform.x + lastX - boxleft.x;
			var y = boxleft.transform.y + lastY - boxleft.y;  
			
			var duration = event && event.type === "resize" ? 0 : 0.5;
			
			
			
			// Tween to 0,0 to remove the transforms
			TweenLite.fromTo(boxleft.node, duration, { x: x, y: y }, { x: 0, y: 0, ease: Power1.easeInOut }); 
		}
		
		
		/* Für rechts */
		
		var boxNoderight = $(".menu.right")[0];
		
		// Initialize transforms on node
		TweenLite.set(boxNoderight, { x: "+=0" });
		
		var boxright = {
		  node: boxNoderight,
		  x: boxNoderight.offsetLeft,
		  y: boxNoderight.offsetTop,
		  transform: boxNoderight._gsTransform
		};
		
		function layoutright(event) {
			
			// Last offset position
			var lastX = boxright.x;
			var lastY = boxright.y;
			
			// Record new offset position
			boxright.x = boxright.node.offsetLeft;
			boxright.y = boxright.node.offsetTop;
			
			//console.log('lastX: ' + lastX + ', box.x: ' + box.x + ', lastY: ' + lastY + ', box.y: ' + box.y);
			
			// Exit if box hasn't moved
			if (lastX === boxright.x && lastY === boxright.y) return;
			
			// Reversed delta values taking into account current
			// transforms in case animation was interrupted
			var x = boxright.transform.x + lastX - boxright.x;
			var y = boxright.transform.y + lastY - boxright.y;  
			
			var duration = event && event.type === "resize" ? 0 : 0.5;
			
			
			
			// Tween to 0,0 to remove the transforms
			TweenLite.fromTo(boxright.node, duration, { x: x, y: y }, { x: 0, y: 0, ease: Power1.easeInOut }); 
		}
	});
});