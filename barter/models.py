from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
  
    
class XchangeStore(models.Model):
    main_title = models.CharField(max_length=250)
    main_category = models.CharField(max_length=200, db_index=True)
    category = models.CharField(max_length=200, db_index=True)
    country = models.CharField(max_length=100, db_index=True)
    region = models.CharField(max_length=150, db_index=True)
    sub_region = models.CharField(max_length=150, db_index=True)
    pub_date = models.DateTimeField('date published')
    from_email = models.EmailField(null=True, blank=True)
    phone_num = models.CharField(max_length=100)
    is_international = models.BooleanField(db_index=True, default=False)
    active = models.BooleanField(db_index=True, default=True)
    desc = models.TextField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    image_url_vendor = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)
    
    
class Currency(models.Model):
    country = models.CharField(max_length=100, db_index=True)
    currency = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=50, db_index=True)
    symbol = models.CharField(max_length=50, db_index=True)
    desc = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)
    
    
    
    