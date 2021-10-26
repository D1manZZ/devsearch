from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    email = models.EmailField(blank=True, null=True, editable=False)
    short_intro = models.CharField(max_length=70, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('projects.Tag', blank=True)
    social_linkedin = models.CharField(max_length=300, blank=True, null=True)
    social_github = models.CharField(max_length=300, blank=True, null=True)
    social_twitter = models.CharField(max_length=300, blank=True, null=True)
    social_youtube = models.CharField(max_length=300, blank=True, null=True)
    social_website = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        def crop_center(pil_img, crop_width, crop_height):
            img_width, img_height = pil_img.size
            return pil_img.crop(((img_width - crop_width) // 2,
                                 (img_height - crop_height) // 2,
                                 (img_width + crop_width) // 2,
                                 (img_height + crop_height) // 2))

        def crop_max_square(pil_img):
            return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

        super().save()
        if self.image:
            img = Image.open(self.image.path)
            img = crop_max_square(img)
            img.save(self.image.path)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='you_send')
    recipient = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='you_receive')
    text = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['created']
