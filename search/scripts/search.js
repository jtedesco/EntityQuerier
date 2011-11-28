/**
 * The status of the popup
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
        $("#backgroundPopup").fadeIn("slow");
        $("#popup").fadeIn("slow");
        popupStatus = 1;
    }
}

/**
 * Hide the progess display
 */
function hideProgress() {

    // If the popup's displayed, fade it out
    if(popupStatus == 1) {
        $("#backgroundPopup").fadeOut("slow");
        $("#popup").fadeOut("slow");
        popupStatus = 0;
    }
}

/**
 * Submit a query via AJAX to the search system
 */
function submitQuery() {

    // Grab the query from the page
    var query = $('#query').val();
    var idField = $('#id').val();

    // Launch an AJAX request to query the system
    var searchUrl = "/search";
    var ajaxRequest = $.getJSON(searchUrl, {
        'query' : query,
        'idField' : idField
    }, function(data) {
        handleResponse(data, query);
    });
}


/**
 * Handles an AJAX response, and triggers
 * 
 *  @param data The data received from the server
 */
function handleResponse(data, query) {

    console.log(data);

    // If this was just a status update, update the progress
    var status = data['status'];
    if(status != 'done') {

        // Update the popup
        showProgress(status);

        // Then wait for more progress updates
        $.getJSON("/update", {
            'query': query
        }, function(data){
            handleResponse(data, query);
        });

    } else {

        // Hide the popup
        hideProgress();
        console.log(data);
    }
}