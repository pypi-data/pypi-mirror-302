import logging
import sqlalchemy.types as types
import json

from .secret_stores import get_secret_store, SecretStoreType


logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class SecretData(types.TypeDecorator):
    '''A sqlalchemy field type that stores data in a secret store.'''

    impl = types.JSON  # The base data type for this field
    cache_ok = True

    def __init__(self, store_type: SecretStoreType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get an implementation from the store factory
        # based on the given store_type
        self.secret_type = store_type
        self.secret_store = get_secret_store(store_type)

    def process_bind_param(self, value, dialect):
        logger.debug(f"Storing {value} of type {type(value)} as a secret.")
        # This might not be a dict or list, but let's json dump everything to be consistent
        stringValue = json.dumps(value, sort_keys=True)

        store_params = self.secret_store.put_secret(stringValue)
        logger.debug(f"Stored {stringValue} as {store_params}")
        return store_params

    def process_result_value(self, value, dialect):
        if value == {}:
            return {}
        logger.debug(f"Restoring {value} from a secret.")
        secret_type = value.get("secret_type")
        key = value.get("key")
        if secret_type is None:
            raise ValueError(f"Secret data is missing secret_type: {value}")

        # We can't assume the secret type here is the same as 'self.secret_type'
        # because the user may have been using a different secret store type previously
        store = get_secret_store(secret_type) if secret_type != self.secret_type else self.secret_store
        result = store.get_secret(key)
        logger.debug(f"Restored {result} from key {key}")
        if result is None:
            return {}
        return json.loads(result)
