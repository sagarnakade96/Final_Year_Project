
from django.db import models
from blogAdmin.choices import ModerationStates


class TimestampModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, db_column="created_on")
    updated_on = models.DateTimeField(auto_now=True, db_column="updated_on")

    class Meta:
        get_latest_by = "updated_on"
        ordering = (
            "-updated_on",
            "-created_on",
        )
        abstract = True

class ModerationModel(models.Model):
    """ModerationModel
    An abstract base class model that provides self-managed "status" fields.
    """

    status = models.CharField(
        max_length=3,
        choices=ModerationStates.choices,
        default=ModerationStates.UNDER_REVIEW,
    )

    class Meta:
        abstract = True