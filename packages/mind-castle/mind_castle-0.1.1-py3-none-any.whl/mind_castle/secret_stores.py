import json
import os
import boto3
from enum import Enum
from .secret_store import SecretStore
from typing import Optional


# If you add a secret store implementation here, make sure to add it to
# the SecretStoreType enum and TYPE_STORE_MAP dictionary at the bottom of this file


class MemorySecretStore(SecretStore):
    '''
    An in-memory secret store.
    This is not persistent and will be lost when the application is restarted.
    Use only for testing or development.
    '''

    store_type = "mem"

    def __init__(self):
        self.secrets = {}

    def get_secret(self, key: str, default: str = None) -> Optional[str]:
        return self.secrets.get(key, default)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        self.secrets[key] = value
        return {"secret_type": self.store_type, "key": key}


class JsonSecretStore(SecretStore):
    store_type = "json"
    filename = "secrets.json"

    def __init__(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("{}")

    def get_secret(self, key: str, default: str = None) -> Optional[str]:
        with open(self.filename, "r") as f:
            secrets = json.load(f)
        return secrets.get(key, default)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        with open(self.filename, "r") as f:
            secrets = json.load(f)
            secrets[key] = value

        with open(self.filename, "w") as f:
            json.dump(secrets, f)
        return {"secret_type": self.store_type, "key": key}


class AWSSecretsManagerSecretStore(SecretStore):
    '''
    Uses AWS Secrets Manager to store secrets.
    This assumes you have credentials in the environment or in the default AWS credentials file.
    '''
    store_type = "awssecretsmanager"

    def __init__(self):
        # TODO: Use this region param as a test for how to pass args to a secret store init
        self.client = boto3.client('secretsmanager', region_name='us-east-2')

    def get_secret(self, key: str, default: str = None) -> Optional[str]:
        response = self.client.get_secret_value(SecretId=key)
        return response.get("SecretString", default)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        # Response is always a success. This throws an exception if it fails
        response = self.client.create_secret(
            Name=key,
            ClientRequestToken=key,
            # Description='string',
            # KmsKeyId='string',
            # SecretBinary=b'bytes',
            SecretString=value,
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            # AddReplicaRegions=[
            #     {
            #         'Region': 'string',
            #         'KmsKeyId': 'string'
            #     },
            # ],
            # ForceOverwriteReplicaSecret=True|False
        )
        return {"secret_type": self.store_type, "key": key, "arn": response.get("ARN")}


class SecretStoreType(str, Enum):
    '''List of supported secret store types'''
    MEMORY = MemorySecretStore.store_type
    JSON = JsonSecretStore.store_type
    AWS_SECRETS_MANAGER = AWSSecretsManagerSecretStore.store_type


# Map of secret store types to their implementations
TYPE_STORE_MAP = {
    SecretStoreType.MEMORY: MemorySecretStore,
    SecretStoreType.JSON: JsonSecretStore,
    SecretStoreType.AWS_SECRETS_MANAGER: AWSSecretsManagerSecretStore
}


def get_secret_store(secret_type: SecretStoreType) -> SecretStore:
    '''Instantiates and returns a SecretStore implementation with the given type.'''

    store_class = TYPE_STORE_MAP.get(secret_type)
    if store_class is None:
        raise ValueError(f"Unknown secret store type '{secret_type}'")
    return store_class()
