from django.db import models
from django.contrib.auth.models import User, AbstractUser
from mimetypes import guess_type

#custom user model
class User(AbstractUser):
    is_teacher = models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)

#post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_of_replies = 0

    def __str__(self):
    
        return self.title + "\n" + self.description

#reply model
class Reply(models.Model):
    post = models.ForeignKey(Post, related_name="replies", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username + "\n" + self.description

#file model    
class File(models.Model):
    file = models.FileField(upload_to="gen/")
    post = models.ForeignKey(Post, related_name="files", on_delete=models.CASCADE)

    #this function converts file types into a string
    #to determine appropriate file tags
    def gethtml(file):
        type_tuple = guess_type(file.file.url, strict=True)
        if (type_tuple[0]).__contains__("image"):
            return "image"
        elif (type_tuple[0]).__contains__("video"):
            return "video"
        elif (type_tuple[0]).__contains__("text"):
            return "text"
        elif (type_tuple[0]).__contains__("application"):
            return "application"
        elif (type_tuple[0]).__contains__("msword"):
            return "msword"
        elif (type_tuple[0]).__contains__("vnd.openxmlformats-officedocument.wordprocessingml.document"):
            return "document"

#subject model
class Subject(models.Model):
    teacher = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

#question model
class Question(models.Model):
    subject = models.ForeignKey(Subject, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField('Question', max_length=255, blank=True)

    def __str__(self):
        return self.text

#answer model
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)

#score model
class Score(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)
    value = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=0)

    def __str__(self):
        return str(self.user) + "'s score on " + str(self.subject.title)



