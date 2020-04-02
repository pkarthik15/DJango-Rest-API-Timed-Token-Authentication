from django.db import models

# Create your models here.
class User(models.Model):

    def upload_dir_profile_image(self, filename):
        path = 'account/photo/{}'.format(filename)
        return path
    
    def upload_dir_resume(self, filename):
        path = 'account/profile/{}'.format(filename)
        return path

    def __str__(self):
        return '{} - {}'.format(self.user_id, self.name)

    user_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    rating = models.FloatField()
    profile_image = models.ImageField(upload_to = upload_dir_profile_image, blank = True, null = True)
    resume = models.FileField(upload_to = upload_dir_resume, blank = True, null = True)


