# 411-Final_Project
Project Members: John Adams, Chiron Phanbuh, Ting Shing Liu, Shiven Sharma
---

This app uses the TMDB API to manage lists of films, and get information on films. You can create new lists, add and remove from them, and also delete the list. You can also get a plethora of information on a given film.

API ROUTES:
---

**CREATE ACCOUNT**

Route: /create-account

- Request Type: POST

- Purpose: Creates a new user account with a username and password.

- Request Body:

  - username (String): User\'s chosen username.

  - password (String): User\'s chosen password.

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: { \"message\": \"Account created successfully\" }

<!-- -->

- Example Request:

  - {

\"username\": \"newuser123\",

\"password\": \"securepassword\"

}

- Example Response:

  - {

\"message\": \"Account created successfully\",

\"status\": \"200\"

}

**UPDATE PASSWORD**

Route: /update-password

- Request Type: PUT

- Purpose: Allows User to change password

- Request Body:

  - username (String): User\'s username.

  - old password (String): User\'s old password.

  - new password (String): User\'s chosen password.

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: { \"message\": \"Password changed successfully\" }

<!-- -->

- Example Request:

  - {

\"username\": \"newuser123\",

\"OldPassword\": \"securepassword\",

\"NewPassword\": \"anotherpassword\"

}

- Example Response:

  - {

\"message\": \"Password changed successfully\",

\"status\": \"200\"

}

**LOGIN**

Route: /login

- Request Type: POST

- Purpose: Allows User to change password

- Request Body:

  - username (String): User\'s username.

  - password (String): User\'s password.

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: { \"message\": \"Login successful\" }

<!-- -->

- Example Request:

  - {

\"username\": \"newuser123\",

\"password\": \"password\"

}

- Example Response:

  - {

\"message\": \"login successful\",

\"status\": \"200\"

}

**ADD MOVIE**

Route: /3/list/{list_id}/add_item

- Request Type: POST

- Purpose: Add a movie to a given list

- Request Body:

  - username (String): User\'s username.

  - password (String): User\'s password.

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 12

    - Content: {

\"status_code\": \"12\",

\"status_message\": \"The item/record was updated successfully.\"

}

- Example Request:

{ \"items\": \[

{ \"media_type\": \"movie\",

\"media_id\": 550 }

\]

}

- Example Response:

  - {

\"status_code\": \"12\",

\"status_message\": \"The item/record was updated successfully.\"

}

**CREATE LIST**

Route: /3/list/

- Request Type: POST

- Purpose: Creates a new list

- Request Body:

  - None

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: {

\"status_message\": \"The item/record was created successfully.\",

\"success\": true,

\"status_code\": 1,

\"list_id\": 5861

}

- Example Request:

  - None

<!-- -->

- Example Response:

  - {

\"status_message\": \"The item/record was created successfully.\",

\"success\": true,

\"status_code\": 1,

\"list_id\": 5861

}

**DELETE LIST**

Route: /3/list/{list_id}

- Request Type: DELETE

- Purpose: Deletes a given list

- Request Body:

  - None

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: {

\"status_code\": \"12\",

\"status_message\": \"The item/record was updated successfully.\"

}

- Example Request:

  - {"confirm" "true"}

<!-- -->

- Example Response:

  - {

\"status_code\": \"12\",

\"status_message\": \"The item/record was updated successfully.\"

}

**REMOVE MOVIE FROM LIST**

Route: /3/list/{list_id}/remove_item

- Request Type: POST

- Purpose: Creates a new list

- Request Body:

  - list_id (int): list you want to delete from

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: {

\"status_code\": 13,

\"status_message\": \"The item/record was deleted successfully.\"

}

- Example Request:

  - {"list_id": 5861}

<!-- -->

- Example Response:

  - {

\"status_code\": 13,

\"status_message\": \"The item/record was deleted successfully.\"

}

**GET MOVIE DETAILS**

Route: /3/movie/{movie_id}

- Request Type: GET

- Purpose: Gets information about a given movie

- Request Body:

  - movie_id (int): the movie you want info on

<!-- -->

- Response Format: JSON

  - Success Response Example:

    - Code: 200

    - Content: {

\"adult\": false,

\"backdrop_path\": \"/hZkgoQYus5vegHoetLkCJzb17zJ.jpg\",

\"belongs_to_collection\": null,

\"budget\": 63000000,

\"genres\": \[

{

\"id\": 18,

\"name\": \"Drama\"

},

{

\"id\": 53,

\"name\": \"Thriller\"

},

{

\"id\": 35,

\"name\": \"Comedy\"

}

\],

\"homepage\": \"http://www.foxmovies.com/movies/fight-club\",

\"id\": 550,

\"imdb_id\": \"tt0137523\",

\"original_language\": \"en\",

\"original_title\": \"Fight Club\",

\"overview\": \"A ticking-time-bomb insomniac and a slippery soap
salesman channel primal male aggression into a shocking new form of
therapy. Their concept catches on, with underground \\fight clubs\\
forming in every town, until an eccentric gets in the way and ignites an
out-of-control spiral toward oblivion.\",

\"popularity\": 61.416,

\"poster_path\": \"/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg\",

\"production_companies\": \[

{

\"id\": 508,

\"logo_path\": \"/7cxRWzi4LsVm4Utfpr1hfARNurT.png\",

\"name\": \"Regency Enterprises\",

\"origin_country\": \"US\"

},

{

\"id\": 711,

\"logo_path\": \"/tEiIH5QesdheJmDAqQwvtN60727.png\",

\"name\": \"Fox 2000 Pictures\",

\"origin_country\": \"US\"

},

{

\"id\": 20555,

\"logo_path\": \"/hD8yEGUBlHOcfHYbujp71vD8gZp.png\",

\"name\": \"Taurus Film\",

\"origin_country\": \"DE\"

},

{

\"id\": 54051,

\"logo_path\": null,

\"name\": \"Atman Entertainment\",

\"origin_country\": \"\"

},

{

\"id\": 54052,

\"logo_path\": null,

\"name\": \"Knickerbocker Films\",

\"origin_country\": \"US\"

},

{

\"id\": 4700,

\"logo_path\": \"/A32wmjrs9Psf4zw0uaixF0GXfxq.png\",

\"name\": \"The Linson Company\",

\"origin_country\": \"US\"

},

{

\"id\": 25,

\"logo_path\": \"/qZCc1lty5FzX30aOCVRBLzaVmcp.png\",

\"name\": \"20th Century Fox\",

\"origin_country\": \"US\"

}

\],

\"production_countries\": \[

{

\"iso_3166_1\": \"US\",

\"name\": \"United States of America\"

}

\],

\"release_date\": \"1999-10-15\",

\"revenue\": 100853753,

\"runtime\": 139,

\"spoken_languages\": \[

{

\"english_name\": \"English\",

\"iso_639_1\": \"en\",

\"name\": \"English\"

}

\],

\"status\": \"Released\",

\"tagline\": \"Mischief. Mayhem. Soap.\",

\"title\": \"Fight Club\",

\"video\": false,

\"vote_average\": 8.433,

\"vote_count\": 26280

}

- Example Request:

  - {"movie_id": 550}

<!-- -->

- Example Response:

{

\"adult\": false,

\"backdrop_path\": \"/hZkgoQYus5vegHoetLkCJzb17zJ.jpg\",

\"belongs_to_collection\": null,

\"budget\": 63000000,

\"genres\": \[

{

\"id\": 18,

\"name\": \"Drama\"

},

{

\"id\": 53,

\"name\": \"Thriller\"

},

{

\"id\": 35,

\"name\": \"Comedy\"

}

\],

\"homepage\": \"http://www.foxmovies.com/movies/fight-club\",

\"id\": 550,

\"imdb_id\": \"tt0137523\",

\"original_language\": \"en\",

\"original_title\": \"Fight Club\",

\"overview\": \"A ticking-time-bomb insomniac and a slippery soap
salesman channel primal male aggression into a shocking new form of
therapy. Their concept catches on, with underground \\fight clubs\\
forming in every town, until an eccentric gets in the way and ignites an
out-of-control spiral toward oblivion.\",

\"popularity\": 61.416,

\"poster_path\": \"/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg\",

\"production_companies\": \[

{

\"id\": 508,

\"logo_path\": \"/7cxRWzi4LsVm4Utfpr1hfARNurT.png\",

\"name\": \"Regency Enterprises\",

\"origin_country\": \"US\"

},

{

\"id\": 711,

\"logo_path\": \"/tEiIH5QesdheJmDAqQwvtN60727.png\",

\"name\": \"Fox 2000 Pictures\",

\"origin_country\": \"US\"

},

{

\"id\": 20555,

\"logo_path\": \"/hD8yEGUBlHOcfHYbujp71vD8gZp.png\",

\"name\": \"Taurus Film\",

\"origin_country\": \"DE\"

},

{

\"id\": 54051,

\"logo_path\": null,

\"name\": \"Atman Entertainment\",

\"origin_country\": \"\"

},

{

\"id\": 54052,

\"logo_path\": null,

\"name\": \"Knickerbocker Films\",

\"origin_country\": \"US\"

},

{

\"id\": 4700,

\"logo_path\": \"/A32wmjrs9Psf4zw0uaixF0GXfxq.png\",

\"name\": \"The Linson Company\",

\"origin_country\": \"US\"

},

{

\"id\": 25,

\"logo_path\": \"/qZCc1lty5FzX30aOCVRBLzaVmcp.png\",

\"name\": \"20th Century Fox\",

\"origin_country\": \"US\"

}

\],

\"production_countries\": \[

{

\"iso_3166_1\": \"US\",

\"name\": \"United States of America\"

}

\],

\"release_date\": \"1999-10-15\",

\"revenue\": 100853753,

\"runtime\": 139,

\"spoken_languages\": \[

{

\"english_name\": \"English\",

\"iso_639_1\": \"en\",

\"name\": \"English\"

}

\],

\"status\": \"Released\",

\"tagline\": \"Mischief. Mayhem. Soap.\",

\"title\": \"Fight Club\",

\"video\": false,

\"vote_average\": 8.433,

\"vote_count\": 26280

}
