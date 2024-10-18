from plasgate.api.message import TwilioClient, PlasgateClient


class Client:
    """
    A unified client for sending messages using either Twilio or Plasgate.

    Attributes:
        http_client (str): The type of HTTP client being used ("twilio" or "plasgate").
        batch_sending (bool): Indicates whether to use batch sending for messages.
        private (str): The private key for authentication.
        secret (str): The secret key for authentication.
        kwargs (dict): Additional arguments passed during initialization.
    """

    http_client = None
    batch_sending = False

    def __init__(self, private: str, secret: str, **kwargs) -> None:
        """
        Initializes the Client with the provided credentials and options.

        Args:
            private (str): The private key for authentication.
            secret (str): The secret key for authentication.
            **kwargs: Additional arguments for client configuration.
                       Must include "from_" for Twilio integration if using Twilio.
        """
        self.kwargs = kwargs
        self.secret = secret
        self.private = private
        self.verify = self.kwargs.pop("verify", False)
        self.batch_sending = self.kwargs.pop("batch_sending", False)
        self.http_client = "twilio" if self.kwargs else "plasgate"

    @property
    def messages(self):
        """
        Returns the appropriate message client instance based on the selected HTTP client.

        Returns:
            TwilioClient or PlasgateClient: The message client configured with the provided credentials.
        """

        return (
            TwilioClient(self.private, self.secret, **self.kwargs)
            if self.http_client == "twilio"
            else PlasgateClient(
                self.private, self.secret, batch=self.batch_sending, verify=self.verify
            )
        )
