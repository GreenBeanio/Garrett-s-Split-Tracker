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
 * @param {string} id The id to assign the table (Default: "data_table")
 * @param {string} table_class The id to assign the table (Default: "table")
 * @param {string} body_class The id to assign the table (Default: "table-body")
 * 
 * @returns An html table from a DataTable, or null if the id is null or already exists
 * 
 */
function createTable(dt, id = "data_table", table_class = "table", body_class = "table-body") {
    // Check that the id doesn't exist
    if (id == null || document.getElementById(id) != null) {
        return (null)
    }
    // Create a table element and body
    const tbl = document.createElement("table");
    tbl.className = table_class;
    tbl.id = `${id}`;
    const tbl_body = document.createElement("tbody");
    tbl_body.className = body_class;
    tbl_body.id = `${id}_body`;
    // Add the header row
    tbl_body.appendChild(createRow(dt.col_header, dt.col_headers, dt.col_header, dt.col_headers, id, true,
        "table-row-col-header", "table-col-header", "table-input-header"));
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
        tbl_body.appendChild(createRow(use_headers[i], dt.row_data[i], dt.col_header, dt.col_headers, id));
    }
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