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
File Description: [JavaScript to get the cookies from a webpage]
*/


// My JavaScript skills aren't great. I've been trying to figure out how I can
// log out using just the cookies.
// For now I've just gone and not used this and instead put it into readonly boxes.
// It's really stupid, but I'm tired and it works for now.
function GetCookies() {
    // Get cookies from the webpage
    cookies = document.cookie;
    split_cookies = cookies.split('; ');
    // Create a map
    cookieMap = new Map();
    // Add the cookies to the map
    for (i in split_cookies) {
        cookie = split_cookies[i].split('=');
        cookieMap.set(cookie[0], cookie[1]);
    }
    return cookieMap;
}

/*
Footer Comment
History of Contributions:
[2024-2024] - [Garrett Johnson (GreenBeanio) - https://github.com/greenbeanio] - [The entire document] 
*/