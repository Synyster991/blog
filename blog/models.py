from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} by {}".format(self.title, self.user)
    
    def summary(self):
        return "{}".format(self.body[:100])


class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "{} ({}) - {}".format(self.body[:20], self.post.title, self.user)


class Announcements(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.title, self.body[:20])

    def summary(self):
        return "{}".format(self.body[:100])


class Members(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} ({})".format(self.user.last_name, self.user.first_name, self.user)
 