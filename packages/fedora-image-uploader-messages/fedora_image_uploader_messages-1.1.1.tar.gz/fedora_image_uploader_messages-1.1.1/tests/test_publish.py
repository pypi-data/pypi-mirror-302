# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from fedora_image_uploader_messages import (
    AwsPublishedV1,
    AzurePublishedV1,
    ContainerPublishedV1,
)


def test_aws_schema():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {
        "architecture": "x86_64",
        "compose_id": "Fedora-40-20240501.n.0",
        "image_name": "Fedora-Cloud-AmazonEC2",
        "regions": {
            "us-east-2": "ami-123",
            "us-west-1": "ami-321",
        },
        "release": 40,
        "subvariant": "Cloud_Base",
    }
    message = AwsPublishedV1(body=body)
    message.validate()


def test_aws_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    body = {
        "architecture": "x86_64",
        "compose_id": "Fedora-40-20240501.n.0",
        "image_name": "Fedora-Cloud-AmazonEC2",
        "regions": {
            "us-east-2": "ami-123",
            "us-west-1": "ami-321",
        },
        "release": 40,
        "subvariant": "Cloud_Base",
    }
    for key in body:
        missing_body = body.copy()
        del missing_body[key]
        message = AwsPublishedV1(body=missing_body)
        with pytest.raises(ValidationError):
            message.validate()


def test_aws_display():
    """Assert the human-readable version is as expected."""
    body = {
        "architecture": "x86_64",
        "compose_id": "Fedora-40-20240501.n.0",
        "image_name": "Fedora-Cloud-AmazonEC2",
        "regions": {
            "us-east-2": "ami-123",
            "us-west-1": "ami-321",
        },
        "release": 40,
        "subvariant": "Cloud_Base",
    }
    message = AwsPublishedV1(body=body)
    message.validate()

    assert message.summary == (
        "fedora-image-uploader published AWS images from compose Fedora-40-20240501.n.0"
        " as Fedora-Cloud-AmazonEC2 in 2 regions"
    )
    assert str(message) == (
        """A new image has been published to Amazon Web Services:

\tArchitecture: x86_64
\tCompose ID: Fedora-40-20240501.n.0
\tImage Name: Fedora-Cloud-AmazonEC2
\tRegions: us-east-2 as ami-123, us-west-1 as ami-321
"""
    )


def test_azure_schema():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {
        "architecture": "x86_64",
        "compose_id": "Fedora-40-20240501.n.0",
        "image_definition_name": "Fedora-Cloud-40-x64",
        "image_version_name": "40.20240501.0",
        "image_resource_id": (
            "/CommunityGalleries/Fedora-5e266ba4-2250-406d-adad-5d73860d958f/Images"
            "/Fedora-Cloud-40-x64/Versions/40.20240501.0"
        ),
        "regions": ["eastus", "eastus2", "centralus"],
        "release": 40,
        "subvariant": "Cloud_Base",
    }
    message = AzurePublishedV1(body=body)
    message.validate()


def test_azure_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    body = {
        "architecture": "x86_64",
        "compose_id": "Fedora-40-20240501.n.0",
        "image_definition_name": "Fedora-Cloud-40-x64",
        "image_version_name": "40.20240501.0",
        "image_resource_id": (
            "/CommunityGalleries/Fedora-5e266ba4-2250-406d-adad-5d73860d958f/Images"
            "/Fedora-Cloud-40-x64/Versions/40.20240501.0"
        ),
        "regions": ["eastus", "eastus2", "centralus"],
        "release": 40,
        "subvariant": "Cloud_Base",
    }
    for key in body:
        missing_body = body.copy()
        del missing_body[key]
        message = AzurePublishedV1(body=missing_body)
        with pytest.raises(ValidationError):
            message.validate()


def test_azure_str():
    """Assert __str__ and the summary property produce a useful messages."""
    body = {
        "architecture": "x86_64",
        "compose_id": "Fedora-40-20240501.n.0",
        "image_definition_name": "Fedora-Cloud-40-x64",
        "image_version_name": "40.20240501.0",
        "image_resource_id": (
            "/CommunityGalleries/Fedora-5e266ba4-2250-406d-adad-5d73860d958f/Images"
            "/Fedora-Cloud-40-x64/Versions/40.20240501.0"
        ),
        "regions": ["eastus", "eastus2", "centralus"],
        "release": 40,
        "subvariant": "Cloud_Base",
    }

    expected_summary = (
        "fedora-image-uploader published Azure image from compose Fedora-40-20240501.n.0 as "
        "version 40.20240501.0 to Fedora-Cloud-40-x64"
    )
    expected_str = (
        "A new image has been published to the Azure image gallery:\n\n"
        "\tArchitecture: x86_64\n"
        "\tCompose ID: Fedora-40-20240501.n.0\n"
        "\tImage Definition Name: Fedora-Cloud-40-x64\n"
        "\tImage Version Name: 40.20240501.0\n"
        "\tImage Resource ID: /CommunityGalleries/Fedora-5e266ba4-2250-406d-adad-5d73860d958f/"
        "Images/Fedora-Cloud-40-x64/Versions/40.20240501.0\n"
        "\tRegions: eastus, eastus2, centralus\n"
    )
    message = AzurePublishedV1(body=body)
    message.validate()

    assert expected_summary == message.summary
    assert expected_str == str(message)


def test_container_str():
    """Assert the container summary is correct."""
    body = {
        "architectures": ["x86_64", "ppc64le", "aarch64", "s390x"],
        "compose_id": "Fedora-40-20240501.n.0",
        "registries": ["quay.io/fedora", "registry.fedoraproject.org"],
        "repository": "fedora",
        "tags": ["40", "latest"],
    }

    expected_summary = (
        "fedora-image-uploader published container manifest from compose Fedora-40-20240501.n.0 "
        "to quay.io/fedora, registry.fedoraproject.org."
    )
    expected_str = (
        "A new container manifest has been published:\n\n"
        "\tCompose ID: Fedora-40-20240501.n.0\n"
        "\tRegistries: quay.io/fedora, registry.fedoraproject.org\n"
        "\tRepository: fedora\n"
        "\tTags: 40, latest\n"
        "\tArchitectures: x86_64, ppc64le, aarch64, s390x\n"
    )

    message = ContainerPublishedV1(body=body)
    assert expected_summary == message.summary
    assert expected_str == str(message)
