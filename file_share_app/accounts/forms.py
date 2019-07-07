from django import forms  
from accounts.models import Filedb
# class StudentForm(forms.ModelForm):
# 	# user = forms.CharField(label="Enter user name",max_length=50)
# 	title  = forms.CharField(label="title", max_length = 10)
# 	author  = forms.CharField(label="title", max_length = 10)
# 	file   = forms.FileField(label="file upload") # for creating file input  
# 	description  = forms.CharField(label="description", max_length = 10)
#     cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)

	
# 	class Meta:
# 		model = Filedb
# 		fields = ['title','description','file']



class StudentForm(forms.ModelForm):
    class Meta:
        model = Filedb
        fields = ('title',  'file', 'cover', 'description')
