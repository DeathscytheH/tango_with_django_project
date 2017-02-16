from django.db import models


# Create your models here.

class Category(models.Model):
    """docstring for Category.
    Category model for db
    """
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        """docstring for Meta."""
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    """docstring for Page.
    Page model for db
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
