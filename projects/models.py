from django.db import models


class Project(models.Model):
    name = models.CharField('Project name', max_length=100, unique=True)
    author = models.ForeignKey('users.Profile', verbose_name='Projects authors', blank=True, null=True, on_delete=models.CASCADE, editable=False)
    tags = models.ManyToManyField('Tag', verbose_name='Project technologies', blank=True)
    image = models.ImageField(upload_to='photos', verbose_name='Project photo', blank=True, null=True)
    description = models.TextField('Project description', blank=True, null=True)
    likes_counter = models.IntegerField('Project likes', blank=True, null=True)
    likes_ratio = models.FloatField('Project likes ratio', blank=True, null=True)
    source_link = models.CharField('Project source link', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):

    choices = [
        ('up', 'vote up'),
        ('down', 'vote down')
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    text = models.TextField()
    vote = models.CharField(choices=choices, max_length=100)


class Tag(models.Model):

    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag
