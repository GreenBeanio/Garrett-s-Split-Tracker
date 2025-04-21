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
File Description: [JavaScript Module for handling Tables]
*/

/* This is my first attempt at ever doing a JavaScript module and I've hardly used
   JavasScipt at all. Don't judge me too harshly. 🙏 */

// Imports
import { DataTable } from './modules/cl_DataTable.js';
import { createTable } from './modules/fn_createTable.js';
import { createRow } from './modules/fn_createRow.js';

// MDN Docs led me astray and didn't tell me I had to do this in the import script to use them in HTML non-modules
window.DataTable = DataTable;
window.createTable = createTable;
window.createRow = createRow;

/*
Footer Comment
History of Contributions:
[2024-2025] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/