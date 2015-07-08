var clickInDataTable = false;
var tooltip = null;

/* =============================================================================
special functions initiated by document.ready/onLoad
========================================================================== */

// init elements after main content is loaded
$(function() {
	//initSuggest();
	initLazyLoad();
	searchFilters();
	filterLayer();
	morePcatsLink();
	hoverBigImage();
	loadOfferDesc();
	//loadTuevFooter();
	loadProductProductTestInfo();
	showHideTileLayer();
	//mobileDesktopSwitch();
	//mobileApps();

	// Click Events in Popups but 'hinweis' page because of agb link
	if ($('body.popup div#header:not(body#hinweis div#header)').length > 0) {
		$('body.popup div#header').click(function() {
			window.close();
		});
	}

	if ($('body.popup img.footer').length > 0) {
		$('body.popup img.footer').click(function() {
			window.close();
		});
	}

	// init jPop for simple overlay(popup) handling
	try {
		$('').jpop('init');
	} catch(e) {}

	// open product picture gallery
	if($('#productPicPopup').length > 0) {
		$('#product-image-cell').click(function (event) {
			$('#productPicPopup').jpop('show',event);
		});
	}

	// skyscraper positioning, init and bind to window resize
	$(window).resize(positionSkyscraper);
	positionSkyscraper();

	// product certificates (yet another "blauer Engel")
	var $certImage = $('#product-certs img');
	$certImage.hover(
		function() {
			var $newCertLayerImage = $('<img></img>', { src : $certImage.data('original') });
			if ($('#product-certs img + img').length === 0) {
				$certImage.after($newCertLayerImage);
			} else {
				$('#product-certs img + img').show();
			}
		},
		function() {
			$('#product-certs img + img').hide();
		}
	);

	if ($('#pcat-hitmap').length > 0) {
		$('#pcat-hitmap .hitmapPcat span').click(function() {
			$('#pcat-hitmap .hide').removeClass('hide');
		});
	}

	// init fittext for .price in tiles
	if ($('.tile .cta .price').length > 0) {
		$('.tile .cta .price').fitText(1.05, {
			minFontSize:'14px',
			maxFontSize:'18px'}
		);
	}

	// open offer info layer at OoP tile view
	$('.oopTileLayer').on('click', function(event) {
		var element = $(this);
		$('#offer' + element.data('offer') + ' .offer-table .right').html($('#shopInfos' + element.data('offer')).html());
		$('#offer' + element.data('offer')).jpop('show',event);
	});

	// show product rating layer
	$('.product-rating-popup').on('click', function(event) {
		$('#productRatingPopup').jpop('show',event);
		return false;
	});

});

function setCookie(name, value, expires, path, domain) {
	var curCookie = name + "=" + escape(value) +
		((expires) ? "; expires=" + expires.toGMTString() : "") +
		((path) ? "; path=" + path : "") +
		((domain) ? "; domain=" + domain : "");
	document.cookie = curCookie;
}

function getCookie(name) {
	var dc = document.cookie;
	var prefix = name + "=";
	var begin = dc.indexOf("; " + prefix);
	if (begin === -1) {
		begin = dc.indexOf(prefix);
		if (begin !== 0) {
			return null;
		}
	} else {
		begin += 2;
	}
	var end = document.cookie.indexOf(";", begin);
	if (end === -1) {
		end = dc.length;
	}
	return unescape(dc.substring(begin + prefix.length, end));
}

/*
 * NotifyClick (nc)
 * @param linkName - not allowed to contain spaces, only \w
 * @return
 */
function nc(linkName) {
	var img = new Image(1, 1);
	img.src = idealoApp.appContext + '/sp/1.gif?linkName=' + escape(linkName);
	var hiddenInput = document.getElementById("clicked_link");
	if (hiddenInput) {
		hiddenInput.value = linkName;
	}
	return true;
}

function initLazyLoad() {
	var $lazyLoadImages = $('img.lazy'),
		errorFallbackImagePath = $('#header').attr('data-cdn-prefix') + '/pics/common/no_image_168x140.png';
	if ($lazyLoadImages.length > 0) {
		$lazyLoadImages.show().lazyload({
			effect: 'fadeIn',
			threshold: 200,
			error: function() {
				this.src = errorFallbackImagePath;
			}
		});
	}
}


/* =============================================================================
common functions, some used during page load others called on demand
============================================================================= */

/***************************************************************************/
/*  Function:	absPosInsideCell
/*  Object:		calculates size of tiles and their childs
/*  Author:		Ronny Buergermeister
/*  Version:	0.0.1
/*  Built:		03.06.14
/*  Updated:	2015-06-16 Aicke Schulz
/*  Issues:
/***************************************************************************/
var initAbsPosInsideCell = false;
function absPosInsideCell(rows) {

	var $rows;
	if (typeof rows === 'string' || (typeof rows === 'object' && typeof rows.type !== 'string')) {
		// if rows is a string or an object (but no event)
		$rows = $(rows);
	} else {
		$rows = $('#tiles tr:not(.info tr, .offer-details-popup tr, .spacer, .special-offer-row)');
	}

	// start each for table rows
	$rows.each(function() {
		var $wrapperClass = 'wrapper-inner'; // wrapper to position container at the bottom of the cell
		var $excludeClass = '.h-spacer, .info td, .offer-details-popup td'; // cells to exclude
		var $cellHeight = 0; // height of cell to set container height
		var $infoHeight = 0; // height for info container to place shipping/details at the bottom
		var $tr = $(this); // current table row

		if (initAbsPosInsideCell) {
			$('td', $tr).not($excludeClass).each(function() {
				var $td = $(this);
				// reset/delete sizes of wrapper-inner and info container
				$('.info', $td).height('auto');
				$('.' + $wrapperClass, $td).height('auto').css('padding-bottom', 0);
			});
		}

		// get height of first cell per row
		$cellHeight = $('td:first-child', $tr).not($excludeClass).height();

		var $ctaSize = [];
		$('td', $tr).not($excludeClass).each(function() {
			var $td = $(this);
			// add cta container height to array
			$ctaSize.push($('.cta', $td).innerHeight());
		});
		// sort array to have highest value in [0]
		$ctaSize.sort(function(a, b){return b-a});

		if (initAbsPosInsideCell) {
			$('td', $tr).not($excludeClass).each(function() {
				var $td = $(this);
				var $ctaHeight = $('.cta', $td).innerHeight();

				// add new size to inner-wrapper and info container
				$('.' + $wrapperClass, $td).height($cellHeight + calcCtaHeightDiff($ctaSize, $ctaHeight)).css('padding-bottom', $ctaHeight);
				$infoHeight = ($cellHeight + calcCtaHeightDiff($ctaSize, $ctaHeight)) - $('.img', $td).innerHeight() - (parseInt($('.info', $td).css('padding-top')) + parseInt($('.info', $td).css('padding-bottom')));
				$('.info', $td).height($infoHeight);
			});
		}

		if (!initAbsPosInsideCell) {
			$('td', $tr).not($excludeClass).each(function() {
				var $td = $(this);
				var $ctaHeight = $('.cta', $td).innerHeight();

				// create wrapper-inner and add styles
				var newDiv = $('<div />', {
					'class' : $wrapperClass,
					'css' : {
						'height' : $cellHeight + calcCtaHeightDiff($ctaSize, $ctaHeight),
						'padding-bottom' : $ctaHeight,
						'position' : 'relative',
						'width' : '100%'
					}
				});

				// remove <script> blocks with getContents(document.write) before inserting wrapper
				$('script', $td).remove();
				// add wrapper-inner to DOM
				$td.wrapInner(newDiv);
				// get max height for info container and apply it
				$infoHeight = ($cellHeight + calcCtaHeightDiff($ctaSize, $ctaHeight)) - $('.img', $td).innerHeight() - (parseInt($('.info', $td).css('padding-top')) + parseInt($('.info', $td).css('padding-bottom')));
				$('.info', $td).height($infoHeight);
			});
		}
	});
	initAbsPosInsideCell = true;

	function calcCtaHeightDiff($ctaSize, $ctaHeight) {
		return $ctaSize[0] - $ctaHeight;
	}
}
$(function() {
	var $tiles = $('#tiles');
	if ($tiles.length > 0) {
		$(window).on('resize', absPosInsideCell);
		$tiles.on('expander.expanded expander.collapsed', '.short-info', function() {
			absPosInsideCell($(this).closest('tr'));
		});
	}
});

function redirectBy(sortKey) {
	// don't redirect numbers
	window.location = $.isNumeric(sortKey) ? window.location.href : sortKey;
}

function updateTT(e) {
	var x, y = "";
	if (tooltip !== null) {
		x = (document.all) ? window.event.x + document.body.scrollLeft : e.pageX;
		y = (document.all) ? window.event.y + document.body.scrollTop  : e.pageY;
		tooltip.style.left = (x + 20) + "px";
		tooltip.style.top  = (y + 20) + "px";
	}
}

function zoom(datei, breit, hoch, resizable, scrollbars) {
	var big = window.open(datei, breit + "zoomed" + hoch, "width=" + breit + ",height=" + hoch + ",scrollbars=" + scrollbars + ",resizable=" + resizable + ",menubar=no,status=no,locationbar=no");
	if (big) {
		big.focus();
	}
}

// function limitInput(input, maxInput) {
// 	if (input.value.length > maxInput) {
// 		alert(input.getAttribute("data-limitwarning"));
// 		input.value = input.value.substring(0, maxInput);
// 		document.getElementById('ratingform').output.value = "0";
// 	} else {
// 		document.getElementById('ratingform').output.value = maxInput - input.value.length;
// 	}
// }

function limitInput(input, maxInput, id) {
	if (input.value.length > maxInput) {
		alert(input.getAttribute("data-limitwarning"));
		input.value = input.value.substring(0, maxInput);
		document.getElementById(id).value = "0";
	} else {
		document.getElementById(id).value = maxInput - input.value.length;
	}
}




var characterMap31 = [];
var characterSet31 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

var characterMap47 = [];
var characterSet47 = "!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";

for (var i = 0; i < characterSet31.length; i++) {
	characterMap31[characterSet31.charAt(i)] = characterSet31.charAt((i + 31) % 62);
}

for (var i = 0; i < characterSet47.length; i++) {
	characterMap47[characterSet47.charAt(i)] = characterSet47.charAt((i + 47) % 94);
}

function decode31(text) {
	var toReturn = '';

	for (var i = 0; i < text.length; i++) {
		var currentChar = text.charAt(i);
		if ((currentChar >= '0' && currentChar <= '9') || (currentChar >= 'A' && currentChar <= 'Z') || (currentChar >= 'a' && currentChar <= 'z')) {
			toReturn += characterMap31[currentChar];
		} else {
			toReturn += currentChar;
		}
	}
	return toReturn;
}

function decode47(text) {
	var toReturn = '';

	for (i = 0; i < text.length; i++) {
		var currentChar = text.charAt(i);
		if (currentChar >= '!' && currentChar <= '~') {
			toReturn += characterMap47[currentChar];
		} else {
			toReturn += currentChar;
		}
	}
	return toReturn;
}



function notifyAWPSubmit() {
	var parent = window.opener;
	if (parent) {
		var hiddenInput = parent.document.getElementById('clicked_link');
		if (hiddenInput) {
			var linkName = hiddenInput.value;
			if (linkName) {
				var img = new Image(1, 1);
				img.src = idealoApp.appContext + '/sp/1.gif?AWP_after=' + escape(linkName);
			}
		}
	}
	return true;
}

/* Known Issue: line break in var=text causes JS error */
function getContents(text) {
    idealoApp&&idealoApp.getContents(text);
}

//calls functor now or after the first sleeptime, sleeping sleepTime after each call, until maxCalls has been reached
function installLoopWithMaxCalls(functor, sleepTimeMillis, callNow, maxCalls) {
	var i = 0;
	var loop = function () {
		if (i < maxCalls) {
			i++;
			functor();
			setTimeout(loop, sleepTimeMillis);
		}
	};
	if (callNow) {
		loop();
	} else {
		setTimeout(loop, sleepTimeMillis);
	}
}

//for each selector in list, if there is a matching element in both jquery docs, then replace the one in doc1 with the one from doc2
function replaceElements(selectorList, doc1, doc2) {
	if (selectorList.length > 0) {
		for (var pos = 0; pos < selectorList.length; pos++) {
			var selector = selectorList[pos];
			var otherElement = doc2.find(selector);
			if (otherElement.length > 0) {
				var element = doc1.find(selector);
				if (element.length > 0) {
					element.replaceWith(otherElement);
				}
			}
		}
	}
}

// 1) fetches doc2 from remote URL and iff its available, then
// 2) for each selector in list, if there is a matching element in jquery's doc1 and remote jquery's doc2, then replace the one in doc1 with the one from doc2
function replaceElementsFromURL(selectorList, doc1, url) {
	if (selectorList.length > 0) {
		jQuery.ajax({
			url: url,
			beforeSend: function( xhr ) {
				try {
					xhr.overrideMimeType('text/html; charset=ISO-8859-1');
				} catch(e) {
					// ignore IE-Failures
				}
			},
			dataType: 'html',
			ifModified: true,
			timeout: 5000,
			complete: function (res, status) {
				if (status === 'success') {
					var doc2 = jQuery('<div />').append(res.responseText);
					replaceElements(selectorList, doc1, doc2);
				}
			}
		});
	}
}

// For unit tests only to check if this file is included there.
function unitTestAnchor() {
	return true;
}

function showExTests() {
	$('span.displayShort').hide();
	$('span.displayExtended').show();
}

function hideExTests() {
	$('span.displayShort').show();
	$('span.displayExtended').hide();
}

/* =============================================================================
Function:	positionSkyscraper
Object:		calculates position for skyscraper
Author:		Ronny Buergermeister
Version:	0.0.1
Built:		02.08.12
Updated:	09.04.14 (get skyscraperPosX dynamically)
Issues:		-
============================================================================= */
function positionSkyscraper() {
	var contentWidth = 0;
	var contentPosX = 0;
	var skyscraperPosX = 0;
	var skyscraperPosY = 0;
	var skyscraperOffset = 15;

	if($('#wrapper').length > 0) {
		contentWidth = $('#wrapper').width();
		contentPosX = $('#wrapper').offset().left;
		skyscraperPosY = ($('.search').length > 0) ? $('.search').offset().top : skyscraperOffset;
	}

	skyscraperPosX = parseInt(contentPosX + contentWidth + skyscraperOffset, 10);
	if($('#skyscraper').length > 0) {
		$('#skyscraper').css({'left':skyscraperPosX, 'top':skyscraperPosY}).show();
	}
}


/***************************************************************************/
/*  Function:	searchFiltersKatalog
/*  Object:		toggles extended search filter list
/*  Author:
/*  Version:	0.0.1
/*  Built:		06.06.13
/*  Updated:
/*  Issues:
/***************************************************************************/

$(function() {
	// check if filter box is available
	if ($('#sf-katalog').length > 0) {

		// set height to all search filter boxes to prevent toggling bug
		var sfHeight = 0;
		$('.search-filter').each(function(index) {
			if (sfHeight <= $(this).height()) {
				sfHeight = $(this).height();
			}
		});
		$('.search-filter').css('height',sfHeight);

		// webtrekk
		$('#sf-katalog .search-filter a').on('click', function() {
			var $this = $(this);
			var wt_linkid = 'filter.specific.';
			var optString = '-';
			var $li = $this.parent();
			var level = 0;
			var position = 0;

			// check for optString [open, close, all]
			if ($this.parent().hasClass('less')) {
				optString += 'close';
			} else if ($this.parent().hasClass('more')) {
				optString += 'open';
			} else if ($this.hasClass('wt-all')) {
				optString += 'all';
			} else {
				optString = '';
			}

			// get filter type from li.header
			wt_linkid += $this.closest('div').find('.header').text();

			// get level of link
			if ($li.parent().parent().hasClass('search-filter')) {
				level = 1;
			} else if ($li.parent().parent().parent().parent().hasClass('search-filter')) {
				level = 2;
			} else {
				level = 3;
			}

			// get position of link
			var indexOffset = ($li.parent().parent().is('div')) ? 0 : 1;
			position = $li.index()+indexOffset;

			$(document).trigger('webtrekk-click', [wt_linkid+optString, (level+'-'+position)]);
		});

		// add click event to all nested elements
		$('#sf-katalog .search-filter .more > a').on('click', function(event) {
			var $this = $(this);
			var $parent = $this.parent().parent().parent('div');
			// prevent default behaviour and event bubbling for links with a 2nd level
			event.preventDefault();
			event.stopPropagation();
			// if clicked element is already visible then hide it
			if ($this.parent('li').hasClass('less')) {
				$this.parent('li').removeClass('less');
				$this.next('.hidden').hide();
				// remove border class
				if ($parent.hasClass('search-filter-hover')) {
					$parent.removeClass('search-filter-hover');
				}
			} else {
				if ((!$parent.hasClass('search-filter-hover')) && ($this.parent().parent().parent().is('div'))) {
					// remove border class of other filter boxes and close their 1st level
					$('.search-filter-hover .less .hidden', '.search-filters').hide();
					$('.search-filter-hover .less', '.search-filters').removeClass('less');
					$('.search-filter-hover', '.search-filters').removeClass('search-filter-hover');
					// add border class to current filter box
					$parent.addClass('search-filter-hover');
				}
				// hide visible element on the same level
				var range = $this.closest('ul');
				$('.less', range).removeClass('less');
				$('.hidden', range).hide();
				// and show clicked one
				$this.parent('li').addClass('less');
				$this.next('.hidden').show();
			}
		});

		// hide all opened filter boxes
		$('html').click(
			function(event) {
				$('.search-filter-hover .less .hidden', '.search-filters').hide();
				$('.search-filter-hover .less', '.search-filters').removeClass('less');
				$('.search-filter-hover', '.search-filters').removeClass('search-filter-hover');
			}
		);
	}
});


/***************************************************************************/
/*  Function:	searchFilters
/*  Object:		toggles extended search filter list
/*  Author:		Ingo Stoecker
/*  Version:	0.0.4
/*  Built:		09.01.13
/*  Updated:	25.03.14
/*  Issues:		load LoadSearchFilter.html within loop and change href's
/***************************************************************************/

function searchFilters() {
	if($('#product-category').length > 0) {
		// event / click handling for toggling
		$('#product-category .search-filter ul li.more').parent('ul').parent('div').click(
			function(event) {
				clickEventHandling(event);
			}
		);
		// set height to all search filter boxes to prevent toggling bug
		var sfHeight = 0;
		$('.search-filter').each(function(index) {
			if (sfHeight <= $(this).height()) {
				sfHeight = $(this).height();
			}
		});
		$('.search-filter').css('height',sfHeight);

		// toggles the extended list elements and switches more/less link
		$('#product-category .search-filter ul li.more').click(
			function(event) {
				var element = $(this);
				var sf = element.parent('ul').attr('id');
				ajaxLoad = ($('#' + sf + ' li[class="hidden"] a').attr('href') === '#' ? true : false);


				if(!(element.parent('ul').parent('div').hasClass('sf-load'))) {
					if(element.hasClass('less')) {
						closeSearchFilter(element);
					} else {
						closeAllSearchFilter();
						openSearchFilter(element);
					}
				} else {
					if(element.hasClass('less')) {
						closeSearchFilter(element);
					} else {
						closeAllSearchFilter();
						if(ajaxLoad) {
							openSearchFilterAjax(element, sf);
						} else {
							var filterType = element.parents('.search-filter').data('wt-filtertype');
							var filterIndex = element.parents('.search-filter').index();
							$(document).trigger('webtrekk-click', ['filter.specific.' + filterType + '.toggle-open', String(filterIndex+1), String(element.data('more'))]);
							element.text(element.data('less'));
							element.parent('ul').children('.hidden').show();
							element.addClass('less');
							element.parent('ul').parent('div').addClass('search-filter-hover');
							// move >all filter< item to list bottom
							var list = element.parent('ul');
							element.parent('ul').children('.all').appendTo(list);
						}
					}
				}
			}
		);
		// event / click handling for toggling
		$('html').click(
			function(event) {
				clickEventHandling(event);
				closeAllSearchFilter();
			}
		);
	}

	var $mainSearchCatList = $('#mainsearch .cat-list');
	if ($mainSearchCatList.length) {
		$mainSearchCatList.find('li.more').on('click', function(event) {
			var $element = $(this);
			$element.hide();
			$element.prevAll('.hide').removeClass('hide').show();
		});
	}
}

/***************************************************************************/
/*  Function:	closeAllSearchFilter
/*  Object:		close all extended SF and switch the more-link wording
/*  Author:		Ingo Stoecker
/*  Version:	0.0.1
/*  Built:		04.02.13
/*  Updated:	25.03.14
/*  Issues:
/***************************************************************************/

function closeAllSearchFilter() {
	// check if any extended lists are visible
	$('#product-category .search-filter ul li.more').each(function(index) {
		if($('#product-category .search-filter ul li.more').eq(index).is('.less')) {
			var element = $('#product-category .search-filter ul li.more').eq(index);
			element.parent('ul').children('.hidden').hide();
			element.removeClass('less');
			element.parent('ul').parent('div').removeClass('search-filter-hover');
			element.text(element.data('more'));
		}
	});
}

/***************************************************************************/
/*  Function:	closeSearchFilter
/*  Object:		close current extended SF and switch the more-link wording
/*  Author:		Ingo Stoecker
/*  Version:	0.0.1
/*  Built:		04.02.13
/*  Updated: 	07.04.14 (webtrekk)
/*  Issues:
/***************************************************************************/

function closeSearchFilter(element) {
	var filterType = element.parents('.search-filter').data('wt-filtertype');
	var filterIndex = element.parents('.search-filter').index();
	$(document).trigger('webtrekk-click', ['filter.specific.' + filterType + '.toggle-close', String(filterIndex+1), String(element.data('less'))]);

	element.parent('ul').children('.hidden').hide();
	element.removeClass('less');
	element.parent('ul').parent('div').removeClass('search-filter-hover');
	element.text(element.data('more'));
}

/***************************************************************************/
/*  Function:	openSearchFilter
/*  Object:		open current extended SF and switch the more-link wording
/*  Author:		Ingo Stoecker
/*  Version:	0.0.1
/*  Built:		04.02.13
/*  Updated: 	07.04.14 (webtrekk)
/*  Issues:
/***************************************************************************/

function openSearchFilter(element) {
	var filterType = element.parents('.search-filter').data('wt-filtertype');
	var filterIndex = element.parents('.search-filter').index();
	$(document).trigger('webtrekk-click', ['filter.specific.' + filterType + '.toggle-open', String(filterIndex+1), String(element.data('more'))]);

	element.parent('ul').children('.hidden').show();
	element.addClass('less');
	element.parent('ul').parent('div').addClass('search-filter-hover');
	element.text(element.data('less'));
}

/***************************************************************************/
/*  Function:	openSearchFilterAjax
/*  Object:		open current extended SF (AJAX) and switch the more-link wording
/*  Author:		Ingo Stoecker
/*  Version:	0.0.1
/*  Built:		04.02.13
/*  Updated: 	07.04.14 (webtrekk)
/*  Issues:
/***************************************************************************/

var selectedCategoryFilterID = "";
function openSearchFilterAjax(element, sf) {
	var sfilter = window[sf];
	var all_hidden = element.parent('ul').children('.hidden');

	var filterType = element.parents('.search-filter').data('wt-filtertype');
	var filterIndex = element.parents('.search-filter').index();
	$(document).trigger('webtrekk-click', ['filter.specific.' + filterType + '.toggle-open', String(filterIndex+1), String(element.data('more'))]);

	// loop through  all search filter items
	for (var item in sfilter){

		var filterItemId = sfilter[item][1];
		var selectedDynamicFilter = filterItemId.substring(1, filterItemId.length);
		var combinedFilters = selectedCategoryFilterID + "F," + selectedDynamicFilter;
		var getParams = buildGetParameters();
		var url = idealoApp.appContext + "/LoadSearchFilter.html?param.pcatId=" + pcatId + "&param.filters=" + combinedFilters + "&param.getparams=" + getParams;

		$.ajax({
			url: url,
			cache: false,
			async: false,
			success: function(html) {
				// FIXME: try to set href value with JQuery in one line, but does not work. If it work, doesn't use 'setAHRefValue(...)' anymore.
				//$( 'hidden[data-filter-itemid=' + selectedDynamicFilter + ']' ).children('a').attr('href', html);

				//set href value using method to iterate every hidden child and find correct category reference
				setAHRefValue(html, all_hidden, selectedDynamicFilter);

				element.parent('ul').children('.hidden').show();
				element.addClass('less');
				element.parent('ul').parent('div').addClass('search-filter-hover');
				// move >all filter< item to list bottom
				var list = element.parent('ul');
				element.parent('ul').children('.all').appendTo(list);
			}
		});
	}

	element.text(element.data('less'));
}
/***************************************************************************/
/*  Function:	setAHRefValue
/*  Object:		set incoming pcat url reference returned by "/src/main/webapp/idealo.de/LoadSearchFilter.html" into a href tag.
/*  Author:		Carlos Baeza
/*  Version:	0.0.1
/*  Built:		19.02.13
/*  Updated:
/*  Issues:
/***************************************************************************/
function setAHRefValue(url, elements, selectedDynamicFilter) {
	$(elements).each( function(index, el) {
		var data = $(el).attr("data-filter-itemid");
		if(data === selectedDynamicFilter) {
			if($(this).has('a')){
				$(this).children('a').attr('href', url);
			}
			return false; // break loop
		}
	});
}

/***************************************************************************/
/*  Function:	buildGetParameters
/*  Object:		get current url parameters
/*  Author:		Angel Garcia
/*  Version:	0.0.1
/*  Built:		22.02.13
/*  Updated:
/*  Issues:
/***************************************************************************/
function buildGetParameters() {
	var getParams = "";

	if (!!getAlternative && getAlternative === "true"){
		getParams = "param.alternativeView,true";
	}

	if (!!getCount && getParams !== "") {
		getParams = getParams + ",param.resultlist.count," + getCount;
	} else if (!!getCount) {
		getParams = "param.resultlist.count," + getCount;
	}

	if (!!getSort && getParams !== "") {
		getParams = getParams + ",param.resultlist.sortKey," + getSort;
	} else if (!!getSort){
		getParams = "param.resultlist.sortKey," + getSort;
	}
	if (!!getSearch && getParams !== "") {
		getParams = getParams + ",q," + getSearch;
	} else if (!!getSearch){
		getParams = "q," + getSearch;
	}

	return getParams;
}

function clickEventHandling(event) {
	if (!event) {
		event = window.event;
	}
	event.cancelBubble = true;
	if (event.stopPropagation) {
		event.stopPropagation();
	}
}

/***************************************************************************/
/*  Function:	filterLayer
/*  Object:		open/close sub-filter-layer (KatalogFiltern)
/*  Author:		Ingo Stoecker
/*  Version:	0.0.1
/*  Built:		18.06.13
/*  Updated:
/*  Issues:
/***************************************************************************/
function filterLayer() {
	$('.filter-layer').click(function() {
		var $this = $(this);
		var $kids = $this.parent().children().not('div');
		var $index = $($kids).index($this);

		if($('.extended-filter').length > 0) {
			if(!$this.parents('.hide').is(':visible')) {
				$('.extended-filter .hide').hide();
				switch ($index) {
					case 0:
						$this.next().css('left','0');
						break;
					case 1:
						$this.next().css('left','25%');
						break;
					case 2:
						$this.next().css('left','50%');
						break;
					case 3:
						$this.next().css('left','75%');
						break;
					default:
						break;
				}
			}
		} else {
			if(!$this.parents('.hide').is(':visible')) {
				$('.filter-layer').next().hide();
			}
		}
		$this.next().show();
		return false;
	});
	$('.hide .close-filter-layer').click(function() {
		$(this).parent('.hide').hide();
	});
	$('#filter-layer','.extended-filter').click(function(event) {
		event.stopPropagation();
	});
	$(document).click(function(event) {
		$('#filter-layer .hide, .extended-filter .hide').hide();
	});
}

function morePcatsLink() {
	$("#morePcatsLink").click(function() {
		var div = $("#morePcatsElement");
		if (div.is(":visible")) {
			div.slideUp("fast");
		} else {
			$("#moreManusElement").hide();
			div.slideDown("fast");
		}
		return false;
	});

	$("#moreManusLink").click(function() {
		var div = $("#moreManusElement");
		if (div.is(":visible")) {
			div.slideUp("fast");
		} else {
			$("#morePcatsElement").hide();
			div.slideDown("fast");
		}
		return false;
	});

	$("#morePcatsElement").click(function(event) {
		event.stopPropagation();
	});
	$("#moreManusElement").click(function(event) {
		event.stopPropagation();
	});
	$(document).click(function() {
		$("#morePcatsElement, #moreManusElement").hide();
	});
}

/***************************************************************************/
/*  Function:	Sticky Filter Box
/*  Object:		make filter box sticky while scroll down or reload and jump
/*				to anchor
/*  Author:		Ronny Buergermeister
/*  Version:	0.0.1
/*  Built:		16.07.13
/*  Updated:	25.10.13
/*  Issues:
/***************************************************************************/
$(function() {
	var $filterBox = $('.selected-filter-box');
	var $pageName = $filterBox.data('pagename');
	var $mobile = $filterBox.data('mobile');

	if (($filterBox.length > 0) && ($pageName == 'KatalogFiltern' || $pageName == 'ProductCategoryFilters' || $pageName == 'TypFilter') && ($mobile == false)) {
		var $filterBoxMargTop = parseInt($filterBox.css('margin-top'));
		var $filterBoxHeight = $($filterBox).height() + $filterBoxMargTop;
		var $filterBoxTopPos = Math.round($filterBox.offset().top);

		function checkFilterBox() {
			var $contentWidth = $('#content').width() - 32; // less padding and border
			var $contentPos = Math.round($('#content').offset().left);
			var $scrollTop = $(window).scrollTop();
			var $scrollLeft = $(window).scrollLeft();
			var $filterBoxLeftPos = $contentPos - $scrollLeft;

			if ($filterBoxTopPos - $scrollTop <= 20) {
				if ($('#placeholder').length == 0) {
					$filterBox.after('<div id="placeholder" style="height:' + $filterBoxHeight + 'px;"></div>')
				}
				$filterBox.css({'position':'fixed', 'top':'20px', 'left':$filterBoxLeftPos + 'px', 'width':$contentWidth + 'px'});
			} else {
				$filterBox.css({'position':'static', 'top':0, 'width':'auto'});
				$('#placeholder').remove();
			}
		}

		$(window).on('scroll resize', checkFilterBox);

		checkFilterBox();

		if (window.location.hash) {
			setTimeout(function() {
				$(window).scrollTop($(window).scrollTop() - ($filterBoxHeight + 55));
			}, 250);
		}
	}
});

/***************************************************************************/
/*  Function:	loadOfferDesc
/*  Object:		load offer description via AJAX call
/*  Author:		Ingo Stoecker
/*  Version:	0.0.2
/*  Built:		18.06.13
/*  Updated:	26.05.14 (Ronny Buergermeister)
/*  Issues:
/***************************************************************************/

function loadOfferDesc() {
	$('[id*=extOfferDesc] strong').click(function() {
		var $elem = $(this);
		var $spinner = $('<img/>').attr('src', $elem.data('spinner-url'));
		var $offerDescURL = $elem.data('desc-url');
		var $noDesc = $elem.data('no-desc');

		$elem.next('span').append($spinner).load($offerDescURL, function(response, status, xhr) {
			if (status == 'error') {
				$elem.next('span').text($noDesc);
			}
			$elem.remove();
		});
	});
}

/***************************************************************************/
/*  Function:	loadProductProductTestInfo
/*  Object:		load product product test CONTENT via AJAX call
/*  Author:		Rüdiger Herrmann
/*  Version:	0.0.2
/*  Built:		20.02.14
/*  Updated:
/*  Issues:
/***************************************************************************/

function loadProductProductTestInfo() {
	var pptsehTrs = $('tr.pptseh');
	if (pptsehTrs.length > 0) {
		pptsehTrs.each(function() {
			var tr = $(this);
			$.ajax({
				url : tr.data('ppturl')
			}).done(function(data){
				var newTr = $(data);
				var wtlinks = newTr.find("a.webtrekk");
				wtlinks.each(function(){
					var linkid = $(this).data("wt-linkid");
					$(this).click(function(){
						$(document).trigger('webtrekk-click', linkid);
					});
				});
				tr.replaceWith(newTr);
			});
		});
	}
}

/***************************************************************************/
/*  Function:	hoverBigImage
/*  Object:		show bigger product image by hover thumbnails at list view
/*  Author:		Ingo Stoecker
/*  Version:	0.0.2
/*  Built:		26.07.13
/*  Updated:	23.05.14 (Ronny Buergermeister)
/*  Issues:
/***************************************************************************/
function hoverBigImage() {
	if ($('.img-popup').length > 0) {
		$('.img-popup').each(function() {
			var $init = false;
			var $popup = $(this);
			var $td = $popup.closest('td.img');
			var $zoom = $('.loupe', $td);
			var $imgURL = $zoom.data('image-url');
			var $cssClass = 'hide';

			$zoom.hover(
				function() {
					if (!$init) {
						$('img', $popup).attr('src', $imgURL);
						$init = true;
					}
					$popup.removeClass($cssClass);
				},
				function() {
					$popup.addClass($cssClass);
				}
			);
		});
	}
}

/***************************************************************************/
/*  Function:	showHideTileLayer
/*  Object:		show and hide layer at tiles
/*  Author:		Ingo Stoecker
/*  Version:	0.0.3
/*  Built:		30.07.13
/*  Updated:	15.05.14 (Ronny Buergermeister)
/*  			21.04.15 (Aicke Schulz)
/*  Issues:
/***************************************************************************/

function showHideTileLayer() {

	function hideVisibleLayers() {
		$('.tile .offer-details:visible').addClass('hide');
	}

	var $detailPopupLinks = $('.tile .link-details-popup, .tile .shipping');
	if($detailPopupLinks.length > 0) {
		$detailPopupLinks.click(function(event) {
			// stop event bubbling/capturing
			clickEventHandling(event);

			hideVisibleLayers();

			// create handle for current tile
			var $tile = $(this).closest('td.tile'),
				isInitialised = $tile.data('is-initialised'),
				$popup = $('.offer-details', $tile);

			// set content and calc position on first call for all types of tiles
			if ($tile.length > 0 && isInitialised !== true) {
				var leftPos = parseInt($popup.css('left')) - parseInt($popup.outerWidth() / 2),
					topPos = 0,
					type = $('.link-details-popup', $tile).data('type');

				// set positions and show selected layer
				$popup.css({left: leftPos, top: topPos}).removeClass('hide');

				// copy content (delivery, logo, rating, button) from tile into layer
				if (type === 'offer') {
					var $delivery = $('.wrapper-delivery', $tile).clone(),
						$content = $('[id*=shopInfos]', $tile).children().clone(true),
						$shopBtn = $('.btn-cta-shop', $tile).clone(),
						$offerDetailLeft = $('.offer-details-left', $popup),
						$offerDetailRight = $('.offer-details-right', $popup);

					// add delivery, logo, rating and button to details-popup
					// depends on existence of shop cert (prepend <=> append)
					$offerDetailLeft.find('.payment').prepend($delivery);
					if ($offerDetailRight.find('a').length > 0) {
						$offerDetailRight.find('a').before($content);
					} else {
						$offerDetailRight.append($content);
					}
					$offerDetailRight.find('img[src*=shop]').after($shopBtn);

					// request full offer description
					if ($('.offer-details-description', $popup).length > 0) {
						var $descriptionContainer = $('.offer-details-description', $popup),
							$spinner = $('<img/>').attr('src', $descriptionContainer.data('spinner')),
							url = $descriptionContainer.data('url') + $descriptionContainer.data('id') + '?view=tile';
						$descriptionContainer.append($spinner).load(url, function() {
							$spinner.remove();
						});
					}
				}

				// set popup as initialised
				$tile.data('is-initialised', true);
			}

			$popup.removeClass('hide');
		});

		// close layer
		$('html, .offer-details .offer-close, .offer-details .offer-footer div').click(hideVisibleLayers);
	}
}