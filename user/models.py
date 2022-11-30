from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=32,
        unique=True,
        help_text=_(
            "Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    def __str__(self):
        return self.username.__str__()


class Call(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    # Millisecond may kill my database performance so i put sec unit
    duration = models.FloatField(validators=[MinValueValidator(0.0)], help_text=_("Second"))

    @staticmethod
    def milli_to_second(val) -> float:
        """
        Convert Millisecond to seconds
        """
        try:
            return val / 1000
        except ZeroDivisionError | TypeError:
            return 0.0
