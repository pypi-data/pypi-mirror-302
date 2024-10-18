from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
    EXCLUDE,
)


class GlobalSchema(Schema):
    """
    Schema for global parameters applicable to messages.

    Fields:
        sender (str): The sender's identifier (max length: 11).
        dlr (str): Delivery report option ("yes" or "no").
        dlr_url (str): URL for delivery reports.
        dlr_level (int): Level of delivery report (1-3).
        dlr_method (str): HTTP method for delivery report ("GET" or "POST").
    """

    sender = fields.Str(validate=validate.Length(max=11), required=True)
    dlr = fields.Str(validate=validate.OneOf(["yes", "no"]))
    dlr_url = fields.Url()
    dlr_level = fields.Int(validate=validate.Range(min=1, max=3))
    dlr_method = fields.Str(validate=validate.OneOf(["GET", "POST"]))

    @validates_schema
    def validate_dlr(self, data, **kwargs):
        """
        Validates the delivery report settings.

        Raises:
            ValidationError: If 'dlr' is 'yes' and 'dlr_url' is not provided,
                             or if 'dlr_level' is set but 'dlr_url' is missing.
        """
        if data.get("dlr") == "yes" and not data.get("dlr_url"):
            raise ValidationError("dlr_url is required", field_name="dlr_url")

        if data.get("dlr_level") and not data.get("dlr_url"):
            raise ValidationError({"dlr_url": ["Missing data for required field."]})


class ConfigSchema(Schema):
    """
    Schema for configuration parameters.

    Fields:
        errback_url (str): URL for error handling.
        callback_url (str): URL for callback handling.
        schedule_at (datetime): Scheduled time for sending the message.
    """

    errback_url = fields.Url()
    callback_url = fields.Url()
    schedule_at = fields.DateTime()


class MessageSchema(GlobalSchema):
    """
    Schema for individual messages.

    Fields:
        to (str): Recipient's phone number (validated format).
        content (str): Message content (max length: 1500).
    """

    to = fields.Str(
        validate=validate.Regexp("^[0-9]\d{5,14}$", error="Not a valid phone format"),
        required=True,
    )
    content = fields.Str(
        validate=validate.Length(max=1500),
        required=True,
    )


class TwillioSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        fields = ("to", "sender", "content")

    to = fields.Str(
        validate=validate.Regexp("^\+[0-9]\d{5,14}$", error="Not a valid phone format"),
        required=True,
    )
    sender = fields.Str(
        data_key="from_",
        validate=validate.Length(max=11),
        required=True,
    )
    content = fields.Str(
        data_key="body",
        validate=validate.Length(max=1500),
        required=True,
    )


class BatchMessageSchema(MessageSchema):
    """
    Schema for batch messages.

    Fields:
        to (list[str]): List of recipient phone numbers (validated format).
        content (str): Message content (inherited from MessageSchema).
    """

    class Meta:
        fields = ("to", "content")

    to = fields.List(
        fields.Str(
            validate=validate.Regexp(
                "^[0-9]\d{5,14}$", error="Not all phone numbers are in valid format"
            )
        ),
        required=True,
    )


class BatchMessage(Schema):
    """
    Schema for a batch of messages.

    Fields:
        messages (list[BatchMessageSchema]): List of messages to send.
        globals (GlobalSchema): Global parameters for the messages.
        configs (ConfigSchema): Configuration settings for the messages.
    """

    messages = fields.Nested(BatchMessageSchema, many=True)
    globals = fields.Nested(GlobalSchema)
    configs = fields.Nested(ConfigSchema)
