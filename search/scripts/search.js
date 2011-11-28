/** SETTING UP OUR POPUP
 * 0 means disabled; 1 means enabled;
 */
var popupStatus = 0;

/**
 * Centers the popup
 */
function centerPopup(){
    
    //request data for centering
    var windowWidth = document.documentElement.clientWidth;
    var windowHeight = document.documentElement.clientHeight;
    var popupHeight = $("#popup").height();
    var popupWidth = $("#popup").width();

    //centering
    $("#popup").css({
        "position": "absolute",
        "top": windowHeight/2-popupHeight/2,
        "left": windowWidth/2-popupWidth/2
    });
    //only need force for IE6

    $("#backgroundPopup").css({
        "height": windowHeight
    });  
}

/**
 * Show search underway with a given message displaying.
 *
 *  @param  message The message to display
 */
function showProgress(message) {

    // Set the popup's text
    $("#popupText").text(message);
    centerPopup();

    // If the popup's not displayed, fade it in
    if(popupStatus == 0) {
        $("#backgroundPopup").fadeIn("fast");
        $("#popup").fadeIn("fast");
        popupStatus = 1;
    }
}

/**
 * Update a displayed busy message with a new message
 *  @param  message  The new message to display
 */
function updateProgress(message) {
    
    // Set the popup's text
    $("#popupText").text(message);
    centerPopup();
}

/**
 * Hide the progess display
 */
function hideProgress() {

    // If the popup's displayed, fade it out
    if(popupStatus == 1) {
        $("#backgroundPopup").fadeOut("fast");
        $("#popup").fadeOut("fast");
        popupStatus = 0;
    }
}

/**
 * Submit a query via AJAX to the search system
 */
function submitQuery() {

    // Grab the query from the page
    var query = $('#query').val();
    console.log(query);

    // Launch an AJAX request to query the system
    var url = "/search";
    var ajaxRequest = $.post(url, {'query' : query}, undefined, "json");

    showProgress("Submitted query...");
}