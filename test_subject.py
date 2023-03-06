import pytest
from subject import Subject


@pytest.fixture()
def subject():
    return Subject("subjects/test_subject")


def test_set_questions(subject):
    assert subject.questions == ["question 1\n", "question 2\n", "question 3\n"]


def test_set_answers(subject):
    assert subject.answers == ["answer 1\n", "answer 2\n", "answer 3\n"]
