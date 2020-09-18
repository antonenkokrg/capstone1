This application created to help you find your online trainer, coach.  


## For run application you need to do this steps:

1. Clone git repository
2. in folder run command python3 -m venv venv
3. . venv/bin/activate
4. pip install -r requirements.txt
5. crearedb capstone1
5. python seed.py
6. flask run


## Routes:

### /login
  
    Login page, verify login and password, redirect to home page

### /registration 

    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form. 

### /logout

	Delete user from session, and redirect to login page


### Get /

    Home page showes all trainers limited by 21 on page

### POST,GET /training

    Form for adding new training. Only trainer can see that page

### DELETE /trainings/<training_id>
    Delete training from database

### GET /users/<user_id>
    Show page with user information and booked trainings, if user is trainer show hiw trainings and all info about trainer 

### GET users/<user_id>/trainings
    Show all booked training by user

### GET /trainings
    List of available trainings

### GET trainings/<training_id>
    Information about training, add people who will attend 

### POST trainigs/<training_id>/
    book trainig
