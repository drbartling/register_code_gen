import pytest
from pydantic.dataclasses import dataclass

from templating import Template


def test_template_matches_string_template_interface():
    # Except all variables must be wraped in curly braces
    t = Template("${who} likes ${what}")
    result = t.substitute(who="tim", what="kung pao")
    assert "tim likes kung pao" == result

    d = {"who": "tim"}
    result = Template("Give ${who} $$100").substitute(d)
    assert "Give tim $100" == result

    with pytest.raises(KeyError):
        result = t.substitute(d)

    result = t.safe_substitute(d)
    assert "tim likes ${what}" == result


def test_template_allows_periods_and_flattens_dictionaries():
    t = Template("Hello Mr. ${name.last}, ${name.first}")
    d = {"name": {"first": "Charles", "last": "Dickens"}}
    result = t.substitute(d)
    expected = "Hello Mr. Dickens, Charles"
    assert expected == result


def test_we_also_flatten_key_word_args():
    t = Template("Hello Mr. ${name.last}, ${name.first}")
    result = t.substitute(name={"first": "Charles", "last": "Dickens"})
    expected = "Hello Mr. Dickens, Charles"
    assert expected == result


def test_we_merge_dict_with_kwargs():
    t = Template("Hello Mr. ${name.last}, ${name.first}")
    d = {"name": {"first": "Charles"}}
    result = t.substitute(d, name={"last": "Dickens"})
    expected = "Hello Mr. Dickens, Charles"
    assert expected == result


def test_we_can_access_object_attributes():
    t = Template("Hello, ${person.name}")
    p = Person()
    result = t.substitute(person=p)
    expected = "Hello, Bob"
    assert expected == result


@dataclass
class Person:
    name: str = "Bob"
