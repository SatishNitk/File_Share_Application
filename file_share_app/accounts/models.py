from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Filedb(models.Model):
	FILE_CHOICES = (
    ('video','VIDIO'),
    ('audio', 'AUDIO'),
    ('file','FILE'),
    ('pdf','PDF'),
	)

	user = models.ForeignKey(User, on_delete= models.CASCADE)
	title = models.CharField(max_length=50)
	file = models.FileField(upload_to='books/pdfs/')
	description= models.CharField(max_length=6, choices=FILE_CHOICES, default='file')
	cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)


	def __str__(self):
		return self.title
	@property
	def get_username(self):
		return User.get_username()


# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     pdf = models.FileField(upload_to='books/pdfs/')

#     def __str__(self):
#         return self.title

#     def delete(self, *args, **kwargs):
#         self.pdf.delete()
#         self.cover.delete()
#         super().delete(*args, **kwargs)