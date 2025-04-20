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
File Description: [Create a table]
*/

// Imports
import { DataTable } from "./cl_DataTable";
import { createRow } from "./fn_createRow";

/**
 * Create A Table
 * 
 * Creates a HTML table from a DataTable object
 * @param {DataTable} dt The DataTable to get the data from 
 * 
 * @returns Nothing? Just modify a table
 * 
 */
function createTable(dt) {
    // Create a table element and body
    const tbl = document.createElement("table");
    const tbl_body = document.createElement("tbody");
    // Add the header row
    tbl_body.appendChild(createRow(dt.col_headers));



    // Add the body to the table
    tbl.appendChild(tbl_body);
    // Return the table
    return (tbl);
}


export { createTable };

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/