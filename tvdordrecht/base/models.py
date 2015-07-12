from django.db import models


class Base(TimeStampedModel):
    """Base model for standard functionality.
    """
    created = models.DateTimeField(
        "publicatie datum",
        blank=True,
        null=True,
        ) # auto_now_add=True
    created_by = models.ForeignKey(
        User,
        verbose_name="Eigenaar",
        blank=True,
        null=True,
        editable=False,
        related_name="agenda_owner",
        on_delete=models.SET_NULL,
        )
    last_modified = models.DateTimeField(
        "laatst bewerkt",
        blank=True,
        null=True,
        editable=False,
        auto_now=True,
        )
    last_modified_by = models.ForeignKey(
        User,
        verbose_name="Laatst bewerkt door",
        blank=True,
        null=True,
        editable=False,
        related_name="agenda_last_modified_by",
        on_delete=models.SET_NULL,
        )

    def save(self):
        if self.all_day:
            self.start_time = None
            self.end_time = None
            if self.start_date == self.end_date:
                self.end_date = None
        # if not self.id:
        #     self.created_by = threadlocals.get_current_user()
        #     self.pub_date = datetime.datetime.now()
        # self.last_modified_by = threadlocals.get_current_user()
        super(Agenda, self).save()
