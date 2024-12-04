# 411-Final_Project
Project Members: John Adams, Chiron Phanbuh, Ting Shing Liu, Shiven Sharma
---
API routes
---

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
