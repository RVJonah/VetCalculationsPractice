My project is titled the Veterinary Calculation Practice. It is born out of a question that was asked of me at work by a student veterinary nurse
during her training. She was struggling with the mathematical calculations involved in her exams and asked if I would be able to write a program
to generate questions for her to answer as her text book only provided 5 or 6 examples.
The premise of the project is that it has 3 main activities:
1. To teach the user how the calculations:
    This is performed by having teach me pages where the layout of the page will be standard across the website where randomly generated patient/treatment
information is displayed on the right half of the screen and the important details that must be noted in each area pointed out by text on the left side of the screen
Below these boxes will be step by step instructions explaining how the answer can be achieved and giving the necessary formulae required to calculate the answer with
the details of the example filled in to the demonstrate the example.

2. To quiz the user with single questions:
    In the quiz me section single questions will be randomly generated via python class objects on the server and displayed in the user. The user will have the options
of having some help via the 'help me' button which will reveal the relevant formulae for the task but not provide the full workings. Should the user be completely stuck they
will still have the option of the 'show answer' button which will reveal the whole answer but the student will not longer be able to submit an answer until they have
requested a fresh question from the server.

3. To test the user on all the calcuation areas available on the site via a user login:
    The user will first need to register with the site, providing details such as their name email address and college. An email will be sent to the user confirming
registration is successful however this functionality will be removed for submission to protect the email password. These details will be stored in the database
ensuring that the inputs cannot corrupt or drop and data in the database and the passwords will only be stored as hashes of the original password. Once registered the
user can then proceed to take tests on any of the areas of the site. The test area will provide 10 questions on the selected area or can provide randomly generated
questions that may be drawn from any of the areas. The answers to the questions will be stored in a table on the server database. The question data will be passed from
the server as a 10 question JSON object which will then be accessed using javascript to display the question data to user in the correct order with the ability to
move through the questions in both directions and eventually submit the answers back to the server as another JSON dictionary. The answers will then be compared to the
answers stored in the table and the result of the test will be stored as a percentage in a further table. The table will the be reset to all values being null before any
new questions will be sent to the user. The result of the test plus the number of unanswered questions will be displayed to the user with the option to retry the test or
try another test.

The my account page will be displayed on login and will allow the user to change their password and/or their email address should they so wish. Also displayed will be a
table showing the current highest score for any of the tests that have been taken and also the number of times the user has taken each of the tests.
