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
import { DataTable } from "./cl_DataTable.js";
import { createRow } from "./fn_createRow.js";

/**
 * Create A Table
 * 
 * Creates a HTML table from a DataTable object
 * @param {DataTable} dt The DataTable to get the data from 
 * @param {string} id The id to assign the table (Default: null)
 * @param {string} table_class The id to assign the table (Default: "table")
 * @param {string} body_class The id to assign the table (Default: "table-body")
 * 
 * @returns Nothing? Just modify a table
 * 
 */
function createTable(dt, id = null, table_class = "table", body_class = "table-body") {
    // Create a table element and body
    const tbl = document.createElement("table");
    tbl.className = table_class;
    const tbl_body = document.createElement("tbody");
    tbl_body.className = body_class;
    // Add the header row
    tbl_body.appendChild(createRow(dt.col_header, dt.col_headers, true, "table-row-col-header", "table-col-header"));
    // Check if row_headers isn't null and if it is create an array to read from
    // (this creates a duplicate of the data. RIP RAM, but it's just 1 array shouldn't be an issue)
    let use_headers = [dt.row_data.length];
    if (dt.row_headers == null || dt.row_headers.length != dt.row_data.length) {
        //use_headers = Array.from(Array(dt.row_data.length).keys());
        use_headers = Array.from({ length: dt.row_data.length }, (_, i) => i + 1);
    } else {
        use_headers = dt.row_headers;
    }
    // Add the data rows
    for (let i = 0; i < dt.row_data.length; i++) {
        tbl_body.appendChild(createRow(use_headers[i], dt.row_data[i]));
    }
    // Add the body to the table
    tbl.appendChild(tbl_body);
    // Add an id if one is passed and it doesn't already exist
    if (id != null && document.getElementById(id) == null) {
        tbl.id = id;
    }
    // Return the table
    return (tbl);
}

export { createTable };

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/