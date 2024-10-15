# coding: utf-8

"""
    Regula Face SDK Web API

    <a href=\"https://regulaforensics.com/products/face-recognition-sdk/  \" target=\"_blank\">Regula Face SDK</a> is a cross-platform biometric verification solution for a digital identity verification process and image quality assurance. The SDK enables convenient and reliable face capture on the client side (mobile, web, and desktop) and further processing on the client or server side.   The Face SDK includes the following features:  * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#face-detection\" target=\"_blank\">Face detection and image quality assessment</a> * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#face-comparison-11\" target=\"_blank\">Face match (1:1)</a> * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#face-identification-1n\" target=\"_blank\">Face search (1:N)</a> * <a href=\"https://docs.regulaforensics.com/develop/face-sdk/overview/introduction/#liveness-assessment\" target=\"_blank\">Liveness detection</a>  Here is the <a href=\"https://github.com/regulaforensics/FaceSDK-web-openapi  \" target=\"_blank\">OpenAPI specification on GitHub</a>.   ### Clients * [JavaScript](https://github.com/regulaforensics/FaceSDK-web-js-client) client for the browser and node.js based on axios * [Java](https://github.com/regulaforensics/FaceSDK-web-java-client) client compatible with jvm and android * [Python](https://github.com/regulaforensics/FaceSDK-web-python-client) 3.5+ client * [C#](https://github.com/regulaforensics/FaceSDK-web-csharp-client) client for .NET & .NET Core   # noqa: E501

    The version of the OpenAPI document: 6.2.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from regula.facesdk.webclient.gen.configuration import Configuration


class PersonFields(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'name': 'str',
        'external_id': 'str',
        'metadata': '{str: (bool, date, datetime, dict, float, int, list, str, none_type)}',
        'groups': '[str]',
        'ttl': 'int, none_type',
    }

    attribute_map = {
        'name': 'name',
        'external_id': 'externalId',
        'metadata': 'metadata',
        'groups': 'groups',
        'ttl': 'ttl',
    }

    def __init__(self, name=None, external_id=None, metadata=None, groups=None, ttl=None, local_vars_configuration=None):  # noqa: E501
        """PersonFields - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._external_id = None
        self._metadata = None
        self._groups = None
        self._ttl = None
        self.discriminator = None

        self.name = name
        if external_id is not None:
            self.external_id = external_id
        if metadata is not None:
            self.metadata = metadata
        if groups is not None:
            self.groups = groups
        self.ttl = ttl

    @property
    def name(self):
        """Gets the name of this PersonFields.  # noqa: E501

        Person's name.  # noqa: E501

        :return: The name of this PersonFields.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PersonFields.

        Person's name.  # noqa: E501

        :param name: The name of this PersonFields.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def external_id(self):
        """Gets the external_id of this PersonFields.  # noqa: E501

        Person's ID, used for linking search results to an ID in an external system. Can be set when creating a Person, stored in the database, and included in the search to return only Persons with the specified ID. Optional.  # noqa: E501

        :return: The external_id of this PersonFields.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this PersonFields.

        Person's ID, used for linking search results to an ID in an external system. Can be set when creating a Person, stored in the database, and included in the search to return only Persons with the specified ID. Optional.  # noqa: E501

        :param external_id: The external_id of this PersonFields.  # noqa: E501
        :type external_id: str
        """

        self._external_id = external_id

    @property
    def metadata(self):
        """Gets the metadata of this PersonFields.  # noqa: E501

        A free-form object containing person's extended attributes.  # noqa: E501

        :return: The metadata of this PersonFields.  # noqa: E501
        :rtype: {str: (bool, date, datetime, dict, float, int, list, str, none_type)}
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this PersonFields.

        A free-form object containing person's extended attributes.  # noqa: E501

        :param metadata: The metadata of this PersonFields.  # noqa: E501
        :type metadata: {str: (bool, date, datetime, dict, float, int, list, str, none_type)}
        """

        self._metadata = metadata

    @property
    def groups(self):
        """Gets the groups of this PersonFields.  # noqa: E501

        Groups a person should be placed to. If no group is specified in request, a Default group is created and the person is placed to it.  # noqa: E501

        :return: The groups of this PersonFields.  # noqa: E501
        :rtype: [str]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this PersonFields.

        Groups a person should be placed to. If no group is specified in request, a Default group is created and the person is placed to it.  # noqa: E501

        :param groups: The groups of this PersonFields.  # noqa: E501
        :type groups: [str]
        """

        self._groups = groups

    @property
    def ttl(self):
        """Gets the ttl of this PersonFields.  # noqa: E501

        The lifespan of the Person's records, seconds. Optional.  # noqa: E501

        :return: The ttl of this PersonFields.  # noqa: E501
        :rtype: int, none_type
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this PersonFields.

        The lifespan of the Person's records, seconds. Optional.  # noqa: E501

        :param ttl: The ttl of this PersonFields.  # noqa: E501
        :type ttl: int, none_type
        """

        self._ttl = ttl

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PersonFields):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PersonFields):
            return True

        return self.to_dict() != other.to_dict()
