from django.db import models

class ModerationStates(models.TextChoices):
    APPROVED = "AP", "Approved"
    REJECTED = "RJ","REJECTED"
    UNDER_REVIEW = "UR", "Under review"
    MARKED_SPAM = "MS", "Marked Spam"
    DELETED  = "DL", "DELETED"

class PostTypes(models.TextChoices):
    PUBLIC = "PU", "Public"
    USER = "US", "User"
    ADMIN = "AD", "Admin"

class WelcomeTypes(models.TextChoices):
    I_AM_USER = "hey, there I am using blog portal"
