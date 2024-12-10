#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

###############################################
#
# User Account Management
#
###############################################

# Function to create a user account
create_account() {
  username=$1
  password=$2

  echo "Creating account for user: $username..."
  response=$(curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")

  if echo "$response" | grep -q '"message": "Account created successfully"'; then
    echo "Account created successfully for user: $username."
  else
    echo "Failed to create account for user: $username."
    exit 1
  fi
}

# Function to log in a user
login() {
  username=$1
  password=$2

  echo "Logging in user: $username..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")

  if echo "$response" | grep -q '"message": "Login successful"'; then
    echo "Login successful for user: $username."
  else
    echo "Failed to log in user: $username."
    exit 1
  fi
}

# Function to update a user's password
update_password() {
  username=$1
  current_password=$2
  new_password=$3

  echo "Updating password for user: $username..."
  response=$(curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"current_password\":\"$current_password\", \"new_password\":\"$new_password\"}")

  if echo "$response" | grep -q '"message": "Password updated successfully"'; then
    echo "Password updated successfully for user: $username."
  else
    echo "Failed to update password for user: $username."
    exit 1
  fi
}

#clears the user catalog
clear_user_catalog() {
  echo "Clearing the users..."
  curl -s -X DELETE "$BASE_URL/clear-user-catalog" | grep -q 'Catalog cleared successfully.'
}

###############################################
#
# Movie List Management
#
###############################################

#clears the movie catalog
clear_movie_catalog() {
  echo "Clearing the movies..."
  curl -s -X DELETE "$BASE_URL/clear-movie-catalog" | grep -q 'Catalog cleared successfully.'
}
# Function to create a movie list
create_movie_list() {
  name=$1

  echo "Creating movie list: $name..."
  response=$(curl -s -X POST "$BASE_URL/api/list/create" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\"}")

  if echo "$response" | grep -q '"status_code": 1'; then
    echo "Movie list created successfully: $name."
  else
    echo "Failed to create movie list: $name."
    exit 1
  fi
}

# Function to delete a movie list
delete_movie_list() {
  list_id=$1

  echo "Deleting movie list ID: $list_id..."
  response=$(curl -s -X DELETE "$BASE_URL/api/list/$list_id/delete")

  if echo "$response" | grep -q '"status_code": 1'; then
    echo "Movie list ID $list_id deleted successfully."
  else
    echo "Failed to delete movie list ID $list_id."
    exit 1
  fi
}

# Function to add a movie to a list
add_movie_to_list() {
  list_id=$1
  movie_id=$2

  echo "Adding movie ID $movie_id to list ID $list_id..."
  response=$(curl -s -X POST "$BASE_URL/api/list/$list_id/add_movie" -H "Content-Type: application/json" \
    -d "{\"movie_id\": $movie_id}")

  if echo "$response" | grep -q '"status_code": 1'; then
    echo "Movie ID $movie_id added to list ID $list_id successfully."
  else
    echo "Failed to add movie ID $movie_id to list ID $list_id."
    exit 1
  fi
}

# Function to remove a movie from a list
remove_movie_from_list() {
  list_id=$1
  movie_id=$2

  echo "Removing movie ID $movie_id from list ID $list_id..."
  response=$(curl -s -X POST "$BASE_URL/api/list/$list_id/remove_movie" -H "Content-Type: application/json" \
    -d "{\"movie_id\": $movie_id}")

  if echo "$response" | grep -q '"status_code": 1'; then
    echo "Movie ID $movie_id removed from list ID $list_id successfully."
  else
    echo "Failed to remove movie ID $movie_id from list ID $list_id."
    exit 1
  fi
}


###############################################
#
# Movie Details
#
###############################################

# Function to retrieve movie details
get_movie_details() {
  movie_id=$1

  echo "Retrieving details for movie ID: $movie_id..."
  response=$(curl -s -X GET "$BASE_URL/api/movie/$movie_id")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Movie details retrieved successfully for ID: $movie_id."
    if [ "$ECHO_JSON" = true ]; then
      echo "Movie JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve movie details for ID: $movie_id."
    exit 1
  fi
}

###############################################
#
# Test Calls
#
###############################################

# Health checks
check_health
check_db

#clear catalogs
clear_movie_catalog
clear_user_catalog

# User tests
create_account "testuser" "testpassword"
login "testuser" "testpassword"
update_password "testuser" "testpassword" "newpassword"

# Movie list tests
create_movie_list "Top 100"
add_movie_to_list 1 17473 
remove_movie_from_list 1 17473
delete_movie_list 1

# Movie details tests
get_movie_details 17473

echo "All tests passed successfully!"