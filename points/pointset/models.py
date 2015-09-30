from django.db import models


class PointSet(models.Model):
    user = models.ForeignKey('auth.User')
    given_by = models.ForeignKey('auth.User', related_name="given_by")
    point_count = models.PositiveIntegerField()
    description = models.CharField(max_length=30)

    assigned_datetime = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return "{0}: {1}".format(self.user.first_name, self.point_count)