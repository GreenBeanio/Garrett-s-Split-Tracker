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
File Description: [A Class to store the data used in tables]
*/

/**
 * Data Table
 * 
 * Create a data storage for a table
 * 
 */
class DataTable {
    /**
     * Create the Data Storage for the table
     * @param {string[]} col_headers The column headers in the table
     * @param {number[]|string[]} row_headers The row headers in the table (if there are any)
     */
    constructor(col_headers, row_headers) {
        this.col_headers = col_headers;
        this.row_headers = row_headers;
    }
}

export { DataTable };

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/