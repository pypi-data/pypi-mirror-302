# SPDX-FileCopyrightText: 2024 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from fedora_messaging import message

SCHEMA_URL = "http://fedoraproject.org/message-schema/"


class _PublishedV1(message.Message):
    """
    Base class that just defines a base topic and common properties.

    This message class should never be used to send a message, use a sub-class.
    """

    topic = ".".join(["fedora_image_uploader", "published", "v1"])

    @property
    def app_name(self):
        return "fedora-image-uploader"


class AwsPublishedV1(_PublishedV1):
    """Published when an AWS AMI is created from an image."""

    topic = ".".join([_PublishedV1.topic, "aws"])
    body_schema = {
        "id": f"{SCHEMA_URL}/v1/{'.'.join([_PublishedV1.topic, 'aws'])}",
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "description": (
            "Schema for messages sent by fedora-image-uploader when a "
            "new Amazon Web Services image is published."
        ),
        "type": "object",
        "properties": {
            "architecture": {
                "type": "string",
                "description": "The machine architecture of the image (x86_64, aarch64, etc).",
            },
            "compose_id": {
                "type": "string",
                "description": "The compose ID this image was created from.",
            },
            "image_name": {
                "type": "string",
                "description": "The name of the AMI.",
            },
            "regions": {
                "type": "object",
                "description": (
                    "A map of regions to AMI IDs. The object keys are the AWS region and "
                    "the value is the AMI ID."
                ),
            },
            "release": {
                "type": "integer",
                "description": "The release number associated with the image.",
            },
            "subvariant": {
                "type": "string",
                "description": "The subvariant of the image (e.g. Cloud_Base).",
            },
        },
        "required": [
            "architecture",
            "compose_id",
            "image_name",
            "regions",
            "release",
            "subvariant",
        ],
    }

    @property
    def summary(self):
        return (
            f"{self.app_name} published AWS images from compose {self.body['compose_id']} as "
            f"{self.body['image_name']} in {len(self.body['regions'])} regions"
        )

    def __str__(self):
        regions_and_ids = [f"{region} as {id}" for region, id in self.body["regions"].items()]
        return (
            "A new image has been published to Amazon Web Services:\n\n"
            f"\tArchitecture: {self.body['architecture']}\n"
            f"\tCompose ID: {self.body['compose_id']}\n"
            f"\tImage Name: {self.body['image_name']}\n"
            f"\tRegions: {', '.join(regions_and_ids)}\n"
        )


class AzurePublishedV1(_PublishedV1):
    """
    Published when an image is uploaded to the Azure image gallery.
    """

    topic = ".".join([_PublishedV1.topic, "azure"])
    body_schema = {
        "id": f"{SCHEMA_URL}/v1/{'.'.join([_PublishedV1.topic, 'azure'])}",
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "description": (
            "Schema for messages sent by fedora-image-uploader when a "
            "new Azure image is published."
        ),
        "type": "object",
        "properties": {
            "architecture": {
                "type": "string",
                "description": "The machine architecture of the image (x86_64, aarch64, etc).",
            },
            "compose_id": {
                "type": "string",
                "description": "The compose ID this image was created from.",
            },
            "image_definition_name": {
                "type": "string",
                "description": "The name of the image collection within the Azure gallery.",
            },
            "image_version_name": {
                "type": "string",
                "description": (
                    "The image version name which uniquely identifies it "
                    "in the image definition."
                ),
            },
            "image_resource_id": {
                "type": "string",
                "description": (
                    "The Azure resource ID of the image which can be used to "
                    "provision a virtual machine."
                ),
            },
            "regions": {
                "type": "array",
                "description": (
                    "The regions to which the image was replicated; virtual machines using this "
                    "image must be launched in one of these regions."
                ),
                "items": {"type": "string"},
            },
            "release": {
                "type": "integer",
                "description": "The release number associated with the image.",
            },
            "subvariant": {
                "type": "string",
                "description": "The subvariant of the image (e.g. Cloud_Base).",
            },
        },
        "required": [
            "architecture",
            "compose_id",
            "image_definition_name",
            "image_version_name",
            "image_resource_id",
            "regions",
            "release",
            "subvariant",
        ],
    }

    @property
    def summary(self):
        return (
            f"{self.app_name} published Azure image from compose {self.body['compose_id']} as "
            f"version {self.body['image_version_name']} to {self.body['image_definition_name']}"
        )

    def __str__(self):
        return (
            "A new image has been published to the Azure image gallery:\n\n"
            f"\tArchitecture: {self.body['architecture']}\n"
            f"\tCompose ID: {self.body['compose_id']}\n"
            f"\tImage Definition Name: {self.body['image_definition_name']}\n"
            f"\tImage Version Name: {self.body['image_version_name']}\n"
            f"\tImage Resource ID: {self.body['image_resource_id']}\n"
            f"\tRegions: {', '.join(self.body['regions'])}\n"
        )


class ContainerPublishedV1(_PublishedV1):
    """Published when a new image manifest is pushed."""

    topic = ".".join([_PublishedV1.topic, "container"])
    body_schema = {
        "id": f"{SCHEMA_URL}/v1/{'.'.join([_PublishedV1.topic, 'container'])}",
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "description": (
            "Schema for messages sent by fedora-image-uploader when a new "
            "container manifest is uploaded."
        ),
        "type": "object",
        "properties": {
            "architectures": {
                "type": "array",
                "description": "The machine architectures of the images (x86_64, aarch64, etc).",
                "items": {"type": "string"},
            },
            "compose_id": {
                "type": "string",
                "description": "The compose ID this image was created from.",
            },
            "registries": {
                "type": "array",
                "items": {"type": "string"},
                "description": "The registries where the container was published.",
            },
            "release": {
                "type": "integer",
                "description": "The release number associated with the image.",
            },
            "repository": {
                "type": "string",
                "description": "The repository where the container was published.",
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "The names under which the manifest was published (e.g. '40', 'latest')"
                ),
            },
        },
        "required": ["architectures", "compose_id", "registries", "release", "repository", "tags"],
    }

    @property
    def containers(self):
        """List of containers affected by the action that generated this message."""
        containers = []
        for registry in self.body["registries"]:
            for tag in self.body["tags"]:
                containers.append(f"{registry}/{self.body['repository']}:{tag}")
        return containers

    @property
    def summary(self):
        return (
            f"{self.app_name} published container manifest from compose {self.body['compose_id']} "
            f"to {', '.join(self.body['registries'])}."
        )

    def __str__(self):
        return (
            "A new container manifest has been published:\n\n"
            f"\tCompose ID: {self.body['compose_id']}\n"
            f"\tRegistries: {', '.join(self.body['registries'])}\n"
            f"\tRepository: {self.body['repository']}\n"
            f"\tTags: {', '.join(self.body['tags'])}\n"
            f"\tArchitectures: {', '.join(self.body['architectures'])}\n"
        )
