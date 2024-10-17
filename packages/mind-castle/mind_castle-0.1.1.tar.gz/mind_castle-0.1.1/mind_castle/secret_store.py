from typing import Optional
import uuid


class SecretStore():
    '''This is an abstract class that defines the interface for a secret store.'''

    def get_secret(self, key: str, default: str = None) -> Optional[str]:
        raise NotImplementedError()

    def put_secret(self, value: str) -> dict:
        raise NotImplementedError()

    def get_secret_key(self) -> str:
        '''
        Generates a key based on this machine's hardware and the time.
        https://docs.python.org/3/library/uuid.html#uuid.uuid1
        '''

        return str(uuid.uuid1())
