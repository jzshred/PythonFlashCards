# PythonFlashCards

### Test your Python knowledge through Q&amp;A sessions

The user chooses a Python subject and will be asked questions about methods for that particular subject. After completing the subject Q&A session, the user's accuracy rate will be displayed. Accuracy is measured by number of correct answers divided by total number of questions. Once the Q&A session has ended, the user may choose another subject.

### Instructions

You can clone this repository locally and start working on the project. The main files are located in the _src_ folder:
- _qa.py_: script the user runs to start the Q&A session.
- _flashcards.py_: contains the class for handling the Q&A session.
- _subject.py_: contains the class for holding questions and answers from a particular subject.
- _random_subject.py_: contains the class for holding questions and answers from random subjects.
- _scorecard.py_: contains the class for holding scores for Q&A sessions.

All tests are located in the _tests_ folder:
- _test_flashcards.py_: tests to check that the methods in _flashcards.py_ run correctly.
- _test_subject.py_: tests to check that the methods in _subject.py_ run correctly. 
- _test_random_subject.py_: tests to check that the methods in _random_subject.py_ run correctly.
- _test_scorecard.py_: tests to check that the methods in _scorecard.py_ run correctly.

Testing requires __pytest__ version 7.2.1 or above, __pytest-cov__ version 4.0.0 or above,
and __pytest-mock__ version 3.10.0 or above.

There is a folder named _subjects_, which contains a _questions_ text file and an _answers_ text file for every Python subject included in this project.

To clone the repository:<br>
- git clone https://github.com/jzshred/PythonFlashCards.git

To install the required packages for testing:<br>
- pip install pytest<br>
- pip install pytest-cov<br>
- pip install pytest-mock

### Contributing

Please read the CONTRIBUTING.md file.
