from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
# import magic

ext_validator = FileExtensionValidator(['png','jpg','jpeg'])

# def validate_file_mime_type(file):
#     accept = ['image/png','image/jpeg','image/jpg']
#     file_mime_type =magic.from_buffer(file.read(1024),mime=True)
#     print(file_mime_type)
#     if file_mime_type not in accept:
#         raise ValidationError(" unsupported file type")
    


class Post(models.Model):
    title = models.CharField(max_length=50)
    image_post = models.ImageField(upload_to='Image_blog', blank=False, validators=[ext_validator])
    content= models.TextField()
    date_posted= models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User,blank=True, related_name="post_like")


    def __str__(self) :
        return self.title
    
    def save(self, *args, **Kwargs):
        super(Post,self).save(*args,**Kwargs)

    @property
    def like_count(self):
        return self.liked.count()

  
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={ 
                                             "pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="Comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE, default=True ,db_constraint=False, null=False)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return   '%s' % (self.name)  
    

    def save(self, *args, **Kwargs):
        super(Comment,self).save(*args,**Kwargs)