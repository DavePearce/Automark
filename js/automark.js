/**
 * Provides a bunch of helper methods for the Automark automated
 * marking system.
 *
 * By David J. Pearce, 2014
 */

// ===============================================================
// Task helpers
// ===============================================================

/**
 * Determine the set of selected students in a given table of
 * students.  The current assumption is that the login is the third
 * index in the table.
 */
function getSelectedStudents(table) {
    var selected = [];
    $(".ui-selected", table).each(function() {	
	selected.push(this.cells[2].innerHTML);
    });
    return selected;
}

function execTask(root,items,output,index) {
    if(index == items.length) {
	// base case, all items iterated over
    } else {
	// at least one item left to iterate over
	$.getJSON(root + items[index],function(result) {
	    output.write(items[index] + ":\t" + result + "<br/>");
	    execTask(root,items,output,index+1);
        });
    }
}

/**
 * Run a selected task on the server.  User must have permission for 
 * this operation.
 */
function runTask(root,items) {
    var w = window.open('', '', 'width=400,height=400,resizeable,scrollbars,menubar=no,location=no,directories=no');
    execTask(root,items,w.document,0);
    w.document.close();
}

// ===============================================================
// GUI Helpers
// ===============================================================

/**
 * Populate an HTML table with JSON data in the form of a list of
 * records.  The given headings determine which fields are populated,
 * and in which order.
 */
function populateTable(table,data,headings) {
    // First, create headings
    var header = table.createTHead().insertRow(0);
    $.each(headings,function(key,value) {
	header.insertCell(key).innerHTML=value;
    });
    // Second, create table body
    var body = table.createTBody();
    $.each(data,function(key,value){
	var row=body.insertRow(-1);
	$.each(headings,function(i,heading) { 
	    row.insertCell(i).innerHTML=value[heading];
	});
    });    
}
