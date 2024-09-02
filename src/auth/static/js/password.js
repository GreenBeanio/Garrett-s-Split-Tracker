/*
Header Comment 
Project: [Garrett's Split Tracker] [https://github.com/GreenBeanio/Garrett-s-Split-Tracker]
Copyright: Copyright (c) [2024]-[2024] [Garrett's Split Tracker] Contributors
Version: [0.1]
Status: [Development]
License: [MIT]
Author(s): [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
Maintainer: [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio]
Project Description: [This project is used to track "splits" in games or activities. With the ability to display them on a livestream.]
File Description: [JavaScript to validate the password]
*/


// Function to validate the password
function validatePassword() {
    // Get the passwords
    var password = document.getElementById("pass_text").value
    var password_conf = document.getElementById("confirm_pass_text").value
    // Check that they are the same (this is all I should need to do because regex should do the rest)
    if (password === password_conf) {
        return true
    } else {
        return false
    }
}

/* Was testing RegEx
x = "^(?=.*[0-9].*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_\\-+=<,>{};:'\"|\\\\/.?]).{16,32}$"
y = RegExp(x)
console.log(y)
*/

/*
Footer Comment
History of Contributions:
[2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/