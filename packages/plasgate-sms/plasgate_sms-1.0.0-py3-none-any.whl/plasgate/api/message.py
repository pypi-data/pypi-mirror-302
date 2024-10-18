import os
import requests
from typing import TypeVar, Dict, Any
from abc import ABC, abstractmethod
from marshmallow import ValidationError

from .schema import BatchMessage, MessageSchema, TwillioSchema

Self = TypeVar("Self", bound="BaseClient")


def get_message(err: Dict[str, Any]) -> str:
    """
    Extracts an error message from the provided error dictionary.

    Args:
        err (Dict[str, Any]): The error dictionary returned from a request.

    Returns:
        str: A descriptive error message or a default message for unexpected errors.
    """
    try:
        if err.get("messages"):
            return list(
                list(list(list(err.values())[0].values())[0].values())[0].values()
            )[0][0]
        return list(list(err.values())[0].values())[0][0]
    except AttributeError:
        return list(err.values())[0][0]
    except Exception:
        return "Unexpected error"


class BaseClient(ABC):
    """
    Abstract base class for clients that can create resources.
    """

    @abstractmethod
    def create(self):
        """Creates a resource. This method should be implemented in subclasses."""
        pass


class Plasgate(ABC):
    """
    Base class for Plasgate clients, handling common request setup.
    """

    bundle: bool | str = False
    params: Dict[str, Any] = {}
    payload: Dict[str, Any] = {}
    headers: Dict[str, str] = {"Content-Type": "application/json", "x-secret": None}

    def _set_private(self, private: str) -> None:
        """Sets the private key in parameters."""
        self.params["private_key"] = private

    def _set_secret(self, secret: str) -> None:
        """Sets the secret key in headers."""
        self.headers["x-secret"] = secret

    def __init__(self, username: str, password: str, verify: bool) -> None:
        """Initializes the Plasgate client with username and password."""
        self.bundle = (
            os.path.join(os.path.dirname(__file__), "bundle.crt")
            if verify is True
            else self.bundle
        )
        self._set_secret(password)
        self._set_private(username)

    def get_bundle(self):
        resp = requests.get(
            "https://cloudapi.plasgate.com/sms/public/certificates",
            headers=self.headers,
            params=self.params,
            verify=False,
        )

        with open(self.bundle, "w") as writer:
            writer.write(resp.content.decode("utf-8"))

    def request(self) -> Dict[str, Any]:
        """Sends a POST request to the Plasgate API and returns the response JSON."""
        try:
            resp = requests.post(
                self.base_url,
                json=self.payload,
                headers=self.headers,
                params=self.params,
                verify=self.bundle,
            )
            resp.raise_for_status()

            return resp.json()

        except (requests.exceptions.SSLError, OSError) as err:
            if self.bundle is False:
                raise err

            self.get_bundle()

            self.request()

        except requests.HTTPError as err:
            raise err

    @abstractmethod
    def send(self):
        """Sends a message. This method should be implemented in subclasses."""
        pass


class PlasgateBatchSend(Plasgate):
    """
    Client for sending batch messages through Plasgate.
    """

    base_url = "https://cloudapi.plasgate.com/rest/batch-send"

    def send(self, payload: dict, global_: dict = {}, config: dict = {}) -> None:
        """
        Sends a batch message after validating the payload.

        Args:
            payload (dict): The payload for the batch message.
            global_ (dict, optional): Global parameters for the message.
            config (dict, optional): Configuration options for the message.

        Raises:
            ValueError: If the payload is invalid.
        """
        schema = BatchMessage()
        err = schema.validate({**payload, **global_, **config})

        if err:
            message = get_message(err)
            raise ValueError(message)

        self.payload = schema.dump({**payload, **global_, **config})
        self.request()


class PlasgateSingleSend(Plasgate):
    """
    Client for sending single messages through Plasgate.
    """

    base_url = "https://cloudapi.plasgate.com/rest/send"

    def send(self, payload: dict) -> None:
        """
        Sends a single message.

        Args:
            payload (dict): The payload for the message.
        """

        schema = MessageSchema()
        err = schema.validate(payload)

        if err:
            message = get_message(err)
            raise ValueError(message)

        self.payload = payload

        self.request()


class TwilioClient(Plasgate):
    """
    Client for sending messages using the Twilio API.
    """

    base_url = "https://cloudapi.plasgate.com/rest/send"

    def __init__(self, username: str = None, password: str = None, **kwargs) -> None:
        """Initializes the Twilio client with username and password."""
        super().__init__(username, password, False)

    def send(self, payload):

        try:
            schema = TwillioSchema()
            self.payload = schema.load(payload)
        except ValidationError as err:
            raise ValueError(get_message(err.messages))

        self.request()


class PlasgateClient(ABC):
    """
    Client for sending messages through the Plasgate API.
    """

    _strategy: Plasgate = None

    def __init__(
        self, private: str, secret: str, batch: bool = False, verify: bool = False
    ) -> None:
        """Initializes the Plasgate client with private and secret keys."""
        self.secret = secret
        self.private = private
        self._strategy = (
            PlasgateBatchSend(self.private, self.secret, verify=verify)
            if batch
            else PlasgateSingleSend(self.private, self.secret, verify=verify)
        )

    @property
    def messages(self):
        """Returns the current client instance."""
        return self

    def create(self, **payload: Any) -> None:
        """
        Creates and sends a message using the specified payload.

        Args:
            **payload: The parameters for the message.
        """

        self._strategy = (
            TwilioClient(self.private, self.secret)
            if "from_" in payload
            else self._strategy
        )

        return self._strategy.send(payload)
