from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Challenge(models.Model):

    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    task_description = models.TextField()
    ex_input = models.TextField(null=True, blank=True)
    ex_output = models.TextField(null=True, blank=True)

    def was_lurked_by(self, user):
        try:
            Lurk.objects.get(user = user, \
                    challenge=self)
            return True
        except Lurk.DoesNotExist:
            return False

    def __unicode__(self):
        return "#%d %s" % (self.id, self.title)


class Solution(models.Model):

    challenge = models.ForeignKey(Challenge)
    created_by = models.ForeignKey(User)
    code = models.TextField()


class Lurk(models.Model):

    challenge = models.ForeignKey(Challenge)
    user = models.ForeignKey(User)



