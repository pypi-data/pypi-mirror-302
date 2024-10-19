import abc
import os
import typing as t
from dataclasses import dataclass, field

import hvac
from hvac.api.auth_methods import Kubernetes


class BaseStorage(abc.ABC):
    name: str
    available: bool

    @property
    @abc.abstractmethod
    def enabled(self) -> bool:
        pass

    @abc.abstractmethod
    def get_secret(self, name: str, fallback_value: t.Any = None) -> t.Any:
        pass


KV_VERSION1 = "v1"
KV_VERSION2 = "v2"

SUPPORT_KV_VERSIONS = (KV_VERSION1, KV_VERSION2)


@dataclass
class VaultStorage(BaseStorage):
    host: str
    namespace: str
    role: str
    kv_version: str = KV_VERSION1

    name: str = "vault_storage"
    available: bool = True
    ssl_verify: bool = False

    auth_mount_point: str = "kubernetes"
    auth_token_path: str = "/var/run/secrets/kubernetes.io/serviceaccount/token"

    secrets: t.Dict[str, t.Any] = field(init=False, repr=False)

    def __post_init__(self):
        if not self.enabled:
            self.secrets = {}
        else:
            self.secrets = self._get_secrets()

    @property
    def enabled(self) -> bool:
        return bool(self.available and self.host and self.auth_token_path and self.namespace)

    def _get_client_token(self, client: hvac.Client) -> str:
        with open(self.auth_token_path) as f:
            sa_token = f.read()

        auth_info = Kubernetes(client.adapter).login(
            role=self.role, jwt=sa_token, mount_point=self.auth_mount_point
        )

        client_token = auth_info.get("auth", {}).get("client_token")
        if not client_token:
            raise ValueError("Not found vault token.")

        return str(client_token)

    def _parse_secrets(self, raw_data: t.Dict[t.Any, t.Any]) -> t.Any:
        if self.kv_version == KV_VERSION1:
            return raw_data.get("data", {})
        elif self.kv_version == KV_VERSION2:
            return raw_data.get("data", {}).get("data", {})

        raise ValueError(f"Not valifd kv version: '{self.kv_version}'")

    def _get_secrets(self):
        client = hvac.Client(url=self.host, verify=self.ssl_verify)
        client.token = self._get_client_token(client)
        return self._parse_secrets(client.read(self.namespace))

    def get_secret(self, name: str, fallback_value: t.Any = None) -> t.Any:
        return self.secrets.get(name) or fallback_value


@dataclass
class ENVStorage(BaseStorage):
    name: str = "env_storage"
    available: bool = True

    @property
    def enabled(self) -> bool:
        return bool(self.available)

    def get_secret(self, name: str, fallback_value: t.Any = None) -> t.Any:
        return os.getenv(name, fallback_value)
