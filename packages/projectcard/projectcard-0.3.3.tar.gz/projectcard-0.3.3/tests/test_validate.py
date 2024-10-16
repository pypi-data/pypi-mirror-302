"""Tests for the projectcard.validate module."""

import pytest

from projectcard import ProjectCard
from projectcard.errors import ProjectCardValidationError, PycodeError
from projectcard.logger import CardLogger
from projectcard.validate import validate_card


def test_update_dict_with_schema_defaults():
    from projectcard.validate import update_dict_with_schema_defaults

    # Test case 1: Missing required property with default value
    data = {}
    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "default": "John Doe",
            },
            "age": {
                "type": "integer",
                "default": 30,
            },
        },
        "required": ["name"],
    }
    expected_result = {
        "name": "John Doe",
    }
    assert update_dict_with_schema_defaults(data, schema) == expected_result

    # Test case 2: Required property already present
    data = {
        "name": "Jane Smith",
    }
    expected_result = {
        "name": "Jane Smith",
    }
    assert update_dict_with_schema_defaults(data, schema) == expected_result

    # Test case 3: Nested properties with default values
    data = {
        "person": {
            "name": "Alice",
        },
    }
    schema = {
        "type": "object",
        "properties": {
            "person": {
                "type": "object",
                "required": ["name", "age"],
                "properties": {
                    "name": {
                        "type": "string",
                        "default": "John Doe",
                    },
                    "age": {
                        "type": "integer",
                        "default": 30,
                    },
                },
            },
        },
    }
    expected_result = {
        "person": {
            "name": "Alice",
            "age": 30,
        },
    }
    assert update_dict_with_schema_defaults(data, schema) == expected_result

    # Test case 4: List items with default values
    data = {
        "people": [
            {
                "name": "Bob",
            },
            {
                "name": "Charlie",
                "age": 25,
            },
            {},
        ],
    }
    schema = {
        "type": "object",
        "properties": {
            "people": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "age"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "default": "John Doe",
                        },
                        "age": {
                            "type": "integer",
                            "default": 30,
                        },
                    },
                },
            },
        },
    }
    expected_result = {
        "people": [
            {
                "name": "Bob",
                "age": 30,
            },
            {
                "name": "Charlie",
                "age": 25,
            },
            {
                "name": "John Doe",
                "age": 30,
            },
        ],
    }

    assert update_dict_with_schema_defaults(data, schema) == expected_result


def test_update_project_card_with_defaults():
    from projectcard.projectcard import ProjectCard

    project_card_data = {
        "project": "Delete Transit",
        "transit_service_deletion": {"service": {"trip_properties": {"trip_id": ["trip_1"]}}},
    }
    card = ProjectCard(project_card_data)
    CardLogger.debug(f"card:\n{card}")
    assert card.transit_service_deletion["clean_shapes"] is False


def test_good_pycode_(request):
    """Make sure bad pycode syntax will raise an error."""
    CardLogger.info(f"--Starting: {request.node.name}")

    _pycode = "roadway_net.links_df.loc[roadway_net.links_df['lanes'] == 5, 'lanes'] = 12"
    project_data = {
        "project": "Test Project",
        "self_obj_type": "RoadwayNetwork",
        "pycode": _pycode,
    }
    project_card = ProjectCard(project_data)
    valid = project_card.validate()
    assert valid


def test_bad_pycode_(request):
    """Make sure bad pycode syntax will raise an error."""
    CardLogger.info(f"--Starting: {request.node.name}")

    _pycode = "roadway_net.links_df.loc[[roadway_net.links_df['lanes'] == 5, 'lanes'] = 12"
    project_data = {
        "project": "Test Project",
        "self_obj_type": "RoadwayNetwork",
        "pycode": _pycode,
    }
    project_card = ProjectCard(project_data)
    with pytest.raises(PycodeError):
        valid = project_card.validate()
