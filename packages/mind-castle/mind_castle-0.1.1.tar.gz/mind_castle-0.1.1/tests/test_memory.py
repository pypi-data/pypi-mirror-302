from memory_secret_store import MemorySecretStore


def test_put_secret():
    secret_store = MemorySecretStore()
    secret_store.put_secret("some_secret_key", "some_secret_value")

    assert secret_store.secrets["some_secret_key"] == "some_secret_value"


def test_get_secret():
    secret_store = MemorySecretStore()
    secret_store.put_secret("some_secret_key", "some_secret_value")

    assert secret_store.get_secret("some_secret_key") == "some_secret_value"
