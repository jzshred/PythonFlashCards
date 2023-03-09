# PythonFlashCards

### Test your Python knowledge through Q&amp;A sessions

The user chooses a Python subject and will be asked questions about methods for that particular subject. After completing the subject Q&A session, the user's accuracy rate will be displayed. Accuracy is measured by number of correct answers divided by total number of questions. Once the Q&A session has ended, the user may choose another subject.

### Instructions

You can clone this repository locally and start working on the project. The main files are:
- _qa.py_: script the user runs to start the Q&A session.
- _flashcards.py_: contains the class for handling the Q&A session.
- _test_flashcards.py_: tests to check that the methods in _flashcards.py_ run correctly.
- _subject.py_: contains the class for holding questions and answers from a particular subject.
- _test_subject.py_: tests to check that the methods in _subject.py_ run correctly. 

All testing requires __pytest__ version 7.2.1 or above.

There is a folder named _subjects_, which contains a _questions_ and an _answers_ text file for every Python subject included in this project.

To add a question and its answer, simply add them in the corresponding text files.

To add a subject, create two text files in the _subjects_ folder with the subject name followed by _questions_ and _answers_. Example: new_subject_questions.txt and new_subject_answers.txt. Then, add the subject title in the subjects list included in the constructor of the Flashcard class found in _flashcards.py_.

To clone the repository:<br>
git clone https://github.com/jzshred/PythonFlashCards.git

To install pytest:<br>
pip install pytest

### Contributing

Please read the CONTRIBUTING.md file.
