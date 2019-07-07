from django import template

register = template.Library()

def file_name_only(value):
	print("jj",value)
	li = value.split('/')
	return li[-1]

register.filter('file_name_only',file_name_only)