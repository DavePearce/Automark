/**
 * Provides a bunch of helper methods for the Automark automated
 * marking system.
 *
 * By David J. Pearce, 2014
 */

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
      row.insertCell(i).innerHTML=data[heading];
  }
}

/**
 * Populate an HTML table with JSON data in the form of a list of
 * records.  The given headings determine which fields are populated,
 * and in which order.
 */
function populateTable(table,data,headings) {
    var studentsTable = document.getElementById("students");
    $.each(data,function(key,value){
       populateRow(table,value,headings);
    });    
}
