(function( $ ) {
	
	$.fn.memoTabs = function(options) {
		var settings = $.extend({
			tabSelector: ".tab",
			tabTitleSelector: ".tab-title",
			removeTitle: true,
		}, options);
		
		var $currentWrapper = this;
		
		this.wrapInner("<div class='tabs'></div>");
		
		var $ul = this.prepend("<ul class='tab-nav'></ul>");
		var $tabNav = this.find(".tab-nav");
		
		this.find(settings.tabSelector + ":first").addClass("active").each(function(){
			var childrenHeight = getSummarizedChildrenHeight( $(this) );
			
			$(this).css("height", childrenHeight );
		});
		
		this.find(settings.tabSelector).each(function(){
			
			$(this).wrapInner("<div class='tab-content'></div>");
			
			var id = generateID();
			var currentTabTitle = $(this).find(settings.tabTitleSelector).html();
			
			if( settings.removeTitle ) {
				$(this).find(settings.tabTitleSelector).remove();
			}
			
			$(this).attr("id", id);
			
			$tabNav.append("<li><a href=#" + id + ">" + currentTabTitle + "</a></li>");
		});
		
		this.find("a").off("click");
		
		this.find(".tab-nav").on("click", "a", function(e){
			var $tab = $( $(this).attr("href") );
			var childrenHeight = getSummarizedChildrenHeight( $tab );
			
			$(this).parent().siblings().find("a").removeClass("active");
			$(this).addClass("active");
			
			$tab.siblings().removeClass("active").removeAttr("style");
			$tab.addClass("active").css("height", childrenHeight);
			
			e.preventDefault();
		});
		
		return this;
	}
	
} (jQuery) );

function generateID() {
	var S4 = function() {
		return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
	};
	
	return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}

function getSummarizedChildrenHeight($parent) {
	var childrenHeight = 0;
	
	$parent.children().each(function(){
		childrenHeight = $(this).outerHeight(true);
	});
	
	return childrenHeight;
}
