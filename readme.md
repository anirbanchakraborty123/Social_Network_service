# Social Network Rest API using Python-Djnago-Drf

This is a RESTful API for managing social network api with features like pagination, filtering, and Api Rate limiting/throttling.

## Setup Instructions

1. Clone the repository:
   ```
    git clone https://github.com/anirbanchakraborty123/Social_Network_service.git
    cd social_network_api
   ```

2. Create a virtual environment:
   ```
   - python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
      ```
       venv\Scripts\activate
      ```
  
   - On macOS and Linux:
     ```
       source venv/bin/activate
     ```
  
4. Install dependencies:
```
   - pip install -r requirements.txt
```

5. Apply migrations:
```
   - python manage.py migrate
```

6. Start the development server:
```
   - python manage.py runserver
```

## Alternative way to run the project in local using docker build

    1. Build and run the Docker containers:
        ```bash
        docker-compose up --build
        ```

    2. Apply migrations:
        ```bash
        docker-compose run web python manage.py migrate
        ```

    3. Create a superuser:
        ```bash
        docker-compose run web python manage.py createsuperuser
        ```

7. The API's will be accessible at 'http://localhost:8000/api/v1/' with mandatory JWT bearer access_token Authentication Header.
```
   - You can get new access_token using login creds-(username,passsowrd) on below apis
   - Get new access_token 'POST api/v1/login/'
      - payload={
        email,password
      }
      - response={
        access_token,refresh_token
      }
   - Refresh expired access_token by passing refresh_token to 'POST api/v1/token/refresh/'
     - payload={
        refresh_token
     }
     - response={
        access_token,refresh_token
     }
  ```  
### Swagger OPEN API Documentation:

   You can view swagger api document of all available Rest apis:
   - You can test them after authentication:
     ```
   - http://127.0.0.1:8000/api/v1/schema/swagger-ui/
     ```
```
## API Endpoints

### User Authentication

- **Signup:** `POST api/v1/signup/`
- **Login:** `POST api/v1//login/`

### User Search

- **Search Users:** `GET /api/v1/search/?q=<keyword>`

### Friend Requests

- **Send Friend Request:** `POST /api/v1/friend-request/send/<user_id>/`
- **Respond to Friend Request:** `POST /api/v1/friend-request/<request_id>/<action>/`

### List Friends and Requests

- **List Friends:** `GET /api/v1/friends/`
- **List Pending Requests:** `GET /api/v1/friend-requests/pending/`

## Postman Collection

Imported the provided Postman collection `Social Network API.postman_collection.json` to quickly test the API endpoints.
