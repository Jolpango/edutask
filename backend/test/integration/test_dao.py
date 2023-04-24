"""Test functions for dao.py
"""
import pytest
import pymongo
import unittest.mock as mock

from src.util.dao import DAO

def raise_exception(data):
    raise Exception()

#Arrange
@pytest.fixture
@mock.patch("src.util.dao.getValidator", autospec = True)
def sut(mocked_validator):
    """Sets up DAO
    """
    collection_name = "test_collection"
    json_string = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["test_string", "test_bool", "test_array"],
            "properties": {
                "test_string": {
                    "bsonType": "string",
                    "description": "test string req",
                },
                "test_bool": {
                    "bsonType": "bool",
                    "description": "test bool"
                },
                "test_array": {
                    "bsonType": "array",
                    "description": "test array",
                    "uniqueItems": True,
                    "items": {
                        "bsonType": "string"
                    }
                }
            }
        }
    }
    mocked_validator.return_value = json_string
    system_under_test = DAO(collection_name)
    system_under_test.drop()
    system_under_test = DAO(collection_name)
    return system_under_test


#Arrange
@pytest.fixture
@mock.patch("src.util.dao.getValidator", autospec = True)
def broken_sut(mocked_validator):
    """Sets up DAO
    """
    collection_name = "test_collection"
    collection_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["test_string", "test_bool", "test_array"],
            "properties": {
                "test_string": {
                    "bsonType": "string",
                    "description": "test string req",
                },
                "test_bool": {
                    "bsonType": "bool",
                    "description": "test bool"
                },
                "test_array": {
                    "bsonType": "array",
                    "description": "test array",
                    "uniqueItems": True,
                    "items": {
                        "bsonType": "string"
                    }
                }
            }
        }
    }
    mocked_validator.return_value = collection_schema
    system_under_test = DAO(collection_name)
    system_under_test.drop()
    system_under_test = DAO(collection_name)
    system_under_test.collection.insert_one = raise_exception
    return system_under_test


def test_required_complies_unique_operational(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    result = sut.create({"test_string": "test", "test_bool": True, "test_array": [ "test", "test2" ]
})
    assert result["test_string"] == "test"
    assert result["test_bool"] is True
    assert result["test_array"][0] == "test"
    assert result["test_array"][1] == "test2"
    sut.drop()


def test_required_complies_unique_operational_duplicates(sut):
    """
    Args:
        sut (DAO): Database connection
    """

    with pytest.raises(pymongo.errors.WriteError) as _e:
        _ = sut.create({
        "test_string": "test",
        "test_bool": True,
        "test_array": [ "test", "test" ]
        })
    sut.drop()


def test_no_properties(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    with pytest.raises(pymongo.errors.WriteError) as _e:
        _ = sut.create({})
    sut.drop()


def test_one_property(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    with pytest.raises(pymongo.errors.WriteError) as _e:
        _ = sut.create({"test_string": "test"})
    sut.drop()


def test_extra_proprties(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    result = sut.create({"test_string": "test", "test_bool": True, "test_more": 33, "test_array": ["5"]})
    assert result["test_string"] == "test"
    assert result["test_bool"] is True
    assert result["test_array"][0] == "5"
    sut.drop()


def test_wrong_type_bool(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    with pytest.raises(pymongo.errors.WriteError) as _e:
        _ = sut.create({"test_string": "test", "test_bool": 55, "test_array": ["5"]})
    sut.drop()


def test_wrong_type_string(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    with pytest.raises(pymongo.errors.WriteError) as _e:
        _ = sut.create({"test_string": 55,"test_bool": True, "test_array": ["5"]})
    sut.drop()


def test_wrong_type_both(sut):
    """
    Args:
        sut (DAO): Database connection
    """
    with pytest.raises(pymongo.errors.WriteError) as _e:
        _ = sut.create({"test_string": 55, "test_bool": 55, "test_array": [5]})
    sut.drop()

def test_broken_database(broken_sut):
    """

    Args:
        broken_sut (DAO): Database connection(mocked to raise exception)
    """
    with pytest.raises(Exception) as _e:
        broken_sut.create({"asdasd":"asdasd"})
