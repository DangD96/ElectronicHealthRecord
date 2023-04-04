# CS50W Final Project: Mini Electronic Health Record (EHR)

# Distinctiveness and Complexity

## Distinctiveness

The previous projects in this course were search engines, wikis, social networks, mail clients, and e-commerce sites. My web application is different because it's a platform for keeping track of electronic patient health data; the patient's electronic health record. This is a system where users (doctors) can log in to document information on their patients and send messages to them as well.

## Complexity

All of the previous projects in this course had some sort of core concept that was introduced. They were:

### Search

- Working with forms using the HTTP POST method.

### Wiki

Same as above, plus
- Django views and templates.

### Commerce

Same as above, plus
- Django models.

### Mail

Same as above, plus
- Use of Javascript for client-side interaction.
- AJAX requests to API endpoints.

### Network

Same as above, plus
- Use of Pagination.

In order to make my web application more complex, I need to leverage all of the concepts used previously, and then some. So in addition to implementing all of the concepts listed above, my web application:

- Implements sorting on the patient list.
- Implements user preferences by saving the logged in user's sort method for their patient list.
- Implements views within views. I use Django to serve a parent view and then use JavaScript to switch between child views within that parent view.
- Sends emails. Regarding emails, the original plan was to send actual emails [using Gmail's SMTP port](https://data-flair.training/blogs/django-send-email/), but apparently, Google had [other plans](https://support.google.com/accounts/answer/6010255?hl=en). So instead of scrapping this effort, I opted to send the email using Django's email [console backend](https://docs.djangoproject.com/en/4.1/topics/email/#console-backend). The email is output to the console, but at least it's better than nothing.

# Project Documentation

## Assumptions

- Users of this application (Doctors) will have been given their login credentials ahead of time. Since personal health information is highly regulated in real life, I won't be implementing registration functionality. See the Users section below for users to test with.
- If a doctor is creating an entry for a new patient, they're responsible for that patient.

## Users

- Admin User
    - Username: admin
    - Password: admin
    - Email: admin@email.com

- Doctor User
    - Username: md1
    - Password: harvardtest1

- Doctor User
    - Username: md2
    - Password: harvardtest2

## Files

### layout.html

- Defines the main nav bar of the application as well as its options.
- Available options change depending on whether logged in user is a doctor or not.

### index.html

- Defines the layout for the patient list table.
- Defines buttons to change the order of the patient list table.
- Displays appropriate messages if the signed in user is not a doctor or does not have any patients they're currently responsible for.
- Defines links for pagination.

### login.html

- Defines the form used to log into the application.

### new_pat.html

- Defines the form used to create a new patient record.

### patient_chart.html

- Defines the parent view to be used to display information about the patient that's currently open.
- Contains its own nav bar. This allows the user to switch between the two main views defined within the patient's workspace.
    - One view to display a patient's active medications, if they exist, and to add to that medication list.
    - One view to send a message (email) to the patient.

### models.py

- Defines the models used in this web application: Patient, Doctor, Medication, and Message.

### admin.py

- Registers the models noted above.

### urls.py (app-level)

- Defines the various URL patterns for the ehr application that Django will use to call the various view functions and APIs. Summaries of these functions will be provided in the views.py section.

### views.py

#### View Functions

- The `index` function handles saving and processing the doctor's sort method, pagination, and tracks if the logged in user isn't a doctor.
- The `login_view` function tries to log the user in and displays errors if unsuccessful.
- The `logout_view` function logs the user out.
- The `patient_view` function gets the appropriate Patient object from the database and passes that information to the template.
- The `new_patient` function displays an empty form if called via GET. It creates a new Patient object if called via POST. This function also displays an error if a user that's not a doctor tries to access it.

#### APIs

##### GET

- The `get_sort_method` API returns the sort preference of the Doctor that called it. Returns an error if called by something other than GET.
- The `get_patient_meds` API returns all of a given patient's active medications. Returns an error if called by something other than GET. Also returns an error if a user that's not a doctor tries to call it.

##### POST/PUT

- The `set_sort_method` API updates a Doctor object's sort_preference attribute with a sort preference. Returns an error if called by something other than PUT.
- The `save_patient_meds` API saves a new medication to a given patient's list of active medications. Returns an error if called by something other than POST.
- The `send_email` API uses Django's email console backend to output an email to the console. Returns an error if called by something other than POST.

### styles.css

- Contains some additional CSS to make the web application more interactive and visually appealing.

### ehr.js

- Adds event listeners to the rows of the patient list table as well as the sort buttons. Also calls the `highlightSortMethod` function so the front end will display the user's sort preference.
- The `highlightRow` function fires when a patient list row is moused over. It changes the color of the row so it's easier to tell where the user is.
- The `setSortMethod` function fires after the user clicks one of the sort buttons. It makes an AJAX call to the /sort endpoint, which corresponds to the `set_sort_method` API.
- The `highlightSortMethod` function makes an AJAX call to the /preference endpoint, which corresponds to the `get_sort_method` API.
- The `getCookie` function just returns a CSRF token to be used when making POST or PUT requests to the APIs.

### patientView.js

- Adds event listeners to the Meds and Message buttons. Also calls the `loadMedsView` function so we default to showing the meds view first.
- The `loadMedsView` function makes a call to the asynchronous `getPatientMeds` function. Once the promise from `getPatientMeds` is resolved, `loadMedsView` takes the meds it received and displays them.
- The `getPatientMeds` asynchronous function gets a particular patient's active medications via an AJAX call to the /get_meds/id endpoint, which corresponds to the `get_patient_meds` API.
- The `loadMessageView` function displays the form used to send a message (email) to the patient.

# Specifications

- Access
    - If you're not logged in, the main nav bar should only show the name of the application: Health.
    - If you log in as a user that's not a doctor, you'll get a message saying that only doctors may view patients. The only option in the nav bar that you get is to log out.
    - If you log in as a doctor, you get all the options in the nav bar.

- Index Page
    - If you log in as a doctor and don't have any patients at the moment, no patient list is displayed. An appropriate message is displayed instead.
    - If you log in as a doctor and have patients under your care, they'll be displayed in the patient list table.
    - Each row will contain a patient's ID, a photo if it exists, their first and last names, and their age.
    - Mousing over each row will highlight it green.

- Sorting
    - Your user's preferred sort method will be highlighted in a cyan color.
    - Choosing a different sort option will make the patient list update to match that sorting method.
    - If you choose a sort option, log out, and log back in, the patient list will have remembered your choice.

- Pagination
    - By default, only 5 patients display at a time.

- New Patient
    - The New Patient option in the main nav bar takes you to a form where you can create a new patient record.
    - The form asks for a first name, last name, age, email, and photo. Email and photo are both optional.
    - Once you create a new patient, you'll be redirected back to the index page and your patient will be added to the patient list.

- Patient Chart
    - Clicking on the patient's ID will take you into their chart.
    - The patient's info is displayed in a sidebar.
    - All patients will have a 'Medications' activity button. If a patient also has an email on file, their chart will also have a 'Message' button.
    - Clicking on the Medications and Message buttons will let you switch between their corresponding views.

- Medications
    - If the patient has no active medications, there will be an appropriate message.
    - You can add a new medication using the Add Medications form. 
    - If you try to add a med that already exists for a patient, you'll get an error.

- Message
    - Use the Contact Patient form to compose an email to your patient.
    - After clicking Send, the email that would be sent will appear in the console.

# How to Run

To run, simply cd into the 'finalProject/mysite' directory and call `python manage.py runserver`. If that doesn't work, then try `python3 manage.py runserver`.

# Build

If you choose to create your own doctor for testing:

1. Navigate to the /admin route of the web application.
2. Log in as admin/admin.
3. Find the User model and create a new User object. Save the object.
4. Find the Doctor model and create a new Doctor object, making sure to link your Doctor object to the User object you created in step 3. Save the Doctor object.
5. Log out.
