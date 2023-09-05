from django.db import models


class Contact(models.Model):
    username=models.CharField(max_length=500)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=122)
    phoneno=models.CharField(max_length=12)
    date=models.DateField()
    def __str__(self):
        return self.name+" "+self.email
# Create your models here.
class Postpdf(models.Model):
    pdf = models.FileField(upload_to = 'files/')
    # tid = models.ForeignKey(Contact, default=None, on_delete=models.CASCADE)

class Class(models.Model):
    name=models.CharField(max_length=500)
    rno=models.CharField(max_length=12)
    tid = models.ForeignKey(Contact, default=None, on_delete=models.CASCADE)
    mark=models.IntegerField()
    smark=models.IntegerField()
    def __str__(self):
        return self.rno
    