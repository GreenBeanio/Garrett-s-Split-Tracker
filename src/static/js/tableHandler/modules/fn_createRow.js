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
 * @param {Array} data An array of data to make a row out of
 * 
 * @returns a row
 * 
 * NOTE: I may want to create a function that takes a DataTable and an array of headers from an existing
 * table and matches up the locations in the row.
 * 
 */
function createRow(data) {
    // This doesn't check for any existing headers or anything
    // Create the row
    const row = document.createElement("tr");
    for (cl in data) {
        // Create a table cell
        const cell = document.createElement("td");
        // Create text for the cell
        const cell_text = document.createTextNode(i);
        // Add the text to the cell
        cell.appendChild(cell_text);
        // Add it to the header row
        row.appendChild(cell);
    }
    // Return the row
    return (row);
}

export { createRow };

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/