import pytest
from random import randrange
from random_subject import RandomSubject
from subject import Subject


def test_randrange():
    assert randrange(4) in range(4)


@pytest.fixture()
def random_subject():
    return RandomSubject(["subjects/test_subject"], 3)


def test_init(mocker):
    subjects = ["subjects/test_subject"]
    total_questions = 3
    mock_set_random_qa = mocker.patch.object(RandomSubject, '_set_random_qa', autospec=True)
    random_subject = RandomSubject(subjects, total_questions)
    assert random_subject.questions == []
    assert random_subject.answers == []
    assert random_subject._chosen_subject is None
    assert random_subject._subject_qa is None
    assert random_subject._random_question_number is None
    mock_set_random_qa.assert_called_once_with(random_subject, subjects, total_questions)


def test_set_random_subject(random_subject):
    assert random_subject._chosen_subject == "subjects/test_subject"


def test_set_subject_qa(random_subject):
    assert isinstance(random_subject._subject_qa, Subject)


def test_set_random_question_number(random_subject):
    assert random_subject._random_question_number in range(len(random_subject._subject_qa.questions))


def test_set_random_question(random_subject):
    assert random_subject.questions[0] in random_subject._subject_qa.questions


def test_set_random_answer(random_subject):
    assert random_subject.answers[0] in random_subject._subject_qa.answers


def test_set_random_qa(random_subject):
    assert len(random_subject.questions) == 3
    assert len(random_subject.answers) == 3
