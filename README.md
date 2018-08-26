# Installation and instructions for the API and Moodle plugin

Moodle plugin: https://github.com/jstavanja/quiz-biometrics-plugin.

## Installation and setup of Django API and backend
First, clone the git repository https://github.com/jstavanja/quiz-biometrics-api onto your machine.

You need to already have Docker installed on your computer along with docker compose.
Then run these commands:

```bash
docker-compose build
run docker-compose run web python manage.py migrate
run docker-compose run web python manage.py createsuperuser
```
After the createsuperuser command, enter user credentials for the super user that you wish to use.

Then to run everything, type:
```bash
docker-compose up
```

You should now have a working backend API system.

To access the default Django dashboard which should be disabled in the production environment for everyone but the superuser, go to localhost:8000/admin. If you wish to acces the custom dashboard, that will be used for professors go to localhost:8000/dash/quiz.

## Instructions for the instructor (api)

### Architecture idea
User's data can be stored for different test types. The test types differ in the keystroke data the students have to input during the test. You can set the input text they have to type and the amount of times they need to repeat the text.

### How to create a Quiz with a Keystroke test type assigned to it
For that you need to create a keystroke test type at /dash/keystroke_test/add. Then you need to create a Course to which you will assign a certain keystroke test type (each course in moodle will have one keystroke test type). You can do that at /dash/course/add. At the course list you will be able to see all the courses you have created. Each course can have a quiz, which gets it's unique ID, so when you are testing the authenticity of your students, you can know at which moodle quiz a test happened. You can create a quiz when you view a course in your course list and click add quiz to this course. When you click on a quiz on the course's quiz list, you will be able to see all the results from the students taking the quiz test. On the same page, the Quiz's ID will be displayed in the top right corner of the page and is also the ID you need to enter, when adding the question in the Moodle quiz editing section.

## Installation of the moodle plugin
Clone the git repository https://github.com/jstavanja/quiz-biometrics-plugin to your disk and put the files inside the root folder of the Moodle installation and install the Moodle plugin in the administration dashboard as any other question type plugin.

## Instructions for the moodle plugin
First, go inside the api project and go into the folder forms, and serve it with a server on port 1337 (or change both this port and the port in the Moodle plugin as well). I found the easiest way for testing and development to be running this python module:
```bash
python -m SimpleHTTPServer 1337
```
This will provide all the forms and static files for the forms that the students will be using.

To add a registration question to a quiz, make a quiz and add a question with the type keystrokerecorder (has to be renamed in the future to something like biometricsquestion).

DEV PHASE: in the current phase, you can edit the moodle quiz ID you wish to use in the forms parameter *Quiz ID from the dashboard*. Security for random people to not be able to access other people's forms still needs to be implemented.

After you set the correct ID to that variable (you may possibly need to clean the Moodle caches at admin/purgecaches.php) you should be able to create registration and test questions.

When creating a question in a quiz, in the title of the question, put only:
  - "registration" -> if you wish to add a first time registration form into a question (that will add a students unique id from moodle to the backend database and save his real typing patterns and face photo). use this only once.

  - "test" -> if you wish to add a test, which compares the newly sent data with the original data set at the registration. all this data gets sent to the api, gets compared and is stored for the instructor to check.
