from django.db import models

from src.common.models.abstract import AbstractOrgDetails


class Branch(AbstractOrgDetails):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "branch"
