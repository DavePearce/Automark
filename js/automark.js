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
    for (var i = 1, row; row = table.rows[i]; i++) {
	selected.push(row.cells[2].innerHTML);
    }
    return selected;
}

/**
 * Run a selected task on the server.  User must have permission for 
 * this operation.
 */
function runTask(course,assignment,task,students) {
    alert("TASK " + students);
}

// ===============================================================
// GUI Helpers
// ===============================================================

/**
 * Add a row of data to a given HTML table, whilst ensuring this is
 * properly annotated with an ID to ensure correct CSS styling
 * (e.g. that rows have alternativing colours, etc). 
 */
function populateRow(table,data,headings) {
  var row=table.insertRow(-1);
  var length = table.rows.length;
  if (length%2 == 1) { row.id="odd"; }
  else { row.id="even"; }
  for(i = 0; i < headings.length;++i) {
      var heading = headings[i];
      var item = data[heading];
      if(typeof item == 'undefined') {
	  item = "";
      } 
      row.insertCell(i).innerHTML=item;
  }
}

/**
 * Populate an HTML table with JSON data in the form of a list of
 * records.  The given headings determine which fields are populated,
 * and in which order.
 */
function populateTable(table,data,headings) {
    // First, create headings
    var header = table.createTHead().insertRow(0);
    for(i = 0; i < headings.length;++i) {
	header.insertCell(i).innerHTML="<b>" + headings[i] + "</b>"
    }    
    // Second, populate data
    $.each(data,function(key,value){
       populateRow(table,value,headings);
    });    
}
