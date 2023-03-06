import pytest
from random import randrange
from random_subject import RandomSubject
from subject import Subject


def test_randrange():
    assert randrange(4) in range(4)


@pytest.fixture()
def random_subject():
    return RandomSubject(["subjects/test_subject"], 3)


def test_choose_random_subject(random_subject):
    assert random_subject._RandomSubject__chosen_subject == "subjects/test_subject"


def test_build_subject_qa(random_subject):
    assert isinstance(random_subject._RandomSubject__subject_qa, Subject)


def test_choose_random_question_number(random_subject):
    assert random_subject._RandomSubject__random_question_number \
           in range(len(random_subject._RandomSubject__subject_qa.questions))


def test_add_random_question(random_subject):
    assert random_subject.questions[0] in random_subject._RandomSubject__subject_qa.questions


def test_add_random_answer(random_subject):
    assert random_subject.answers[0] in random_subject._RandomSubject__subject_qa.answers


def test_build_random_qa(random_subject):
    assert len(random_subject.questions) == 3
    assert len(random_subject.answers) == 3
