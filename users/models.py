from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic 

# ext_validator = FileExtensionValidator(['png','jpg','jpeg'])

# def validate_file_mime_type(file):
#     accept = ['image/png','image/jpeg','image/jpg']
#     file_mime_type =magic.from_buffer(file.read(1024),mime=True)
#     print(file_mime_type)
#     if file_mime_type not in accept:
#         raise ValidationError(" unsupported file type")
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **Kwargs):
        super(Profile,self).save(*args,**Kwargs)

        # img = Image.open(self.image.path)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
