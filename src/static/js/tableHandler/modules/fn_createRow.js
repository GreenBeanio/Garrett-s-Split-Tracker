/*
Header Comment 
Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
Copyright: Copyright (c) [2024]-[2025] [Garrett's Split Tracker] Contributors
Version: [0.1]
Status: [Development]
License: [MIT]
Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
File Description: [Create a table row]
*/

/**
 * Create A Row
 * 
 * Creates a row from an Array of data
 * 
 * @param {Array} header An array of row headers to use
 * @param {Array} data An array of data to make a row out of
 * @param {boolean} all_header An optional parameter if all cells should be headers (Default: false)
 * @param {string} header_class An optional parameter to set the header class (Default: "table-row-header")
 * @param {string} cell_class An optional parameter to set the cell class (Default: "table-cell")
 * 
 * @returns A row of data if inputs are valid, null if data is bad
 * 
 */
function createRow(header, data, all_header = false, header_class = "table-row-header", cell_class = "table-cell", row_class = "table-row") {
    // Replicating the code here to only do 1 if statement instead of repeating it
    if (all_header == true || all_header == false) {
        // Create the row
        const row = document.createElement("tr");
        row.className = row_class;
        // Create the column cell
        const cell_h = document.createElement("th");
        const cell_h_text = document.createTextNode(header);
        cell_h.appendChild(cell_h_text);
        cell_h.className = header_class;
        row.appendChild(cell_h);
        // Add the data cells
        if (all_header) {
            for (let i = 0; i < data.length; i++) {
                // Create a table cell
                const cell = document.createElement("th");
                // Create text for the cell
                const cell_text = document.createTextNode(data[i]);
                // Add the text to the cell
                cell.appendChild(cell_text);
                // Add a class to the cell
                cell.className = cell_class;
                // Add it to the header row
                row.appendChild(cell);
            }
        } else {
            for (let i = 0; i < data.length; i++) {
                // Create a table cell
                const cell = document.createElement("td");
                // Create text for the cell
                const cell_text = document.createTextNode(data[i]);
                // Add the text to the cell
                cell.appendChild(cell_text);
                // Add a class to the cell
                cell.className = cell_class;
                // Add it to the header row
                row.appendChild(cell);
            }
        }
        // Return the row
        return (row);
    } else {
        return (null)
    }
}

export { createRow };

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/