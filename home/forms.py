from django import forms

from .models import Comment,Post


class CreatePost(forms.ModelForm):
     class Meta:
          model = Post
       
          fields = ['title','image_post','content']
          
          widgets = {
            'image_post': forms.FileInput(attrs={'accept':'.png,.jpeg,jpg',}),
            
         }

class CommentForm (forms.ModelForm):
    class Meta:
          model = Comment
          fields = [ 'body']
          
          widgets = {
              'body': forms.TextInput(attrs={'class':'form-control'}),
              
          }