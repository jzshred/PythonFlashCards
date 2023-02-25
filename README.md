# PythonFlashCards

### Test your Python knowledge through Q&amp;A sessions

The user chooses a Python subject and will be asked questions about methods for that particular subject. After completing the subject Q&A session, the user's accuracy rate will be displayed. Accuracy is measured by number of correct answers divided by total number of questions. Once the Q&A session has ended, the user may choose another subject.

### Installation

You can clone this repository locally and start editing the _flashcards.py_ file. There are 3 main files in this project:
- _qa.py_: this is the script the user would run to start the Q&A session.
- _flashcards.py_: contains the code for generating the Q&A session.
- _test_flashcards.py_: contains the tests to check that the methods in _flashcards.py_ run correctly. Requires __pytest__ version 7.2.1 or above.

There is a folder named _subjects_, which contains a _questions_ and an _answers_ text file for every Python subject included in this project. To add a question and its answer, simply add them in the corresponding text files.

To clone the repository:
git clone https://github.com/jzshred/PythonFlashCards.git

To install pytest:
pip install pytest

### Contributing

Please read the CONTRIBUTING.md file.
