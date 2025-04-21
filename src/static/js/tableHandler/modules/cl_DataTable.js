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
     * @param {Array[<number[]|string[]>]} row_data The row data ( a 2d array basically)
     * @param {number[]|string[]} col_headers The column headers in the table (if null passed it will use the loop order)
     * @param {number[]|string[]} row_headers The row headers in the table (if there are any)
     * @param {string} col_header An optional parameter to change the row header for the column headers (Default: Index)
     * 
     * This is kind of stupid because you'll need to process all the data before you send it instead of just using the
     * first row as the row headers and the first item in the array as the column header... but it might add more flexibility.
     * 
     */
    constructor(row_data, col_headers, row_headers, col_header = "Index") {
        this.row_data = row_data;
        this.col_headers = col_headers;
        this.row_headers = row_headers;
        this.col_header = col_header;
    }
}

export { DataTable };

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/