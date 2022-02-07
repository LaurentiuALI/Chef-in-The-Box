from django.db import models
from jsonfield import JSONField

class File ( models.Model ) :
    path    = models.CharField ( max_length=256 )
    content = JSONField()

    def __str__ ( self ) :
        return self.path + " " + str ( self.content )

# Create your models here.
