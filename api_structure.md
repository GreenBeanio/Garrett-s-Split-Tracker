# Structure of the API

("#" meaning in progress)

- Symbols
  - o7 separates the endpoint, method, type, and description
  - ! Means it's being worked on
  - & Ignored by git
  - \<type:argument>

| Endpoint | Method | Type | Description |
| --- | --- | --- | --- |
| / | GET | Webpage | Main page for the website |
| /auth/user/\<string:username> | GET | Webpage | Returns the homepage of a user |
| /auth/login | GET | Webpage | Returns the login page |
| /auth/login-attempt | POST | Webpage | Redirects to the the user's page (/auth/user/...) if successful or the login page (/auth/login) if unsuccessful |
| /auth/logout | GET | Webpage | Returns the logout page if the user is logged in or the login page (/auth/login) if not logged in |
| /auth/logout | POST | Webpage | Returns the login page (/auth/login) |
| /auth/new-user | GET | Webpage | Returns the page to create a new user if not logged in or redirects to the root (/) if logged in |
| /auth/create-attempt | POST | Webpage | Returns the user's page (/auth/user/...) if successful or redirects to the root (/) if logged in |
| /tracker/user/\<string:username> | GET | Webpage | Returns the user's tracking interface if they are accessing their own account, shows them their account if they're trying to access someone else's, or redirects to the login page (/auth/login) if not logged in  |
| /tracker/user/\<string:username>/activities | GET | Webpage | Returns the user's tracking activities interface if they are accessing their own account, shows them their account if they're trying to access someone else's, or redirects to the login page (/auth/login) if not logged in |
