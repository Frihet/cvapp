from django.db import models
import datetime
import django.contrib.auth.models
from django.utils import timezone

YEAR_CHOICES = [(None,'Year')]
for r in range(1969, (datetime.datetime.now().year+1)):
	YEAR_CHOICES.append((r,r))
	
MONTH_CHOICES = (
	(0, 'Month'),
	(1, 'Jan'),
	(2, 'Feb'),
	(3, 'Mar'),
	(4, 'Apr'),
	(5, 'Mai'),
	(6, 'Jun'),
	(7, 'Jul'),
	(8, 'Aug'),
	(9, 'Sep'),
	(10, 'Okt'),
	(11, 'Nov'),
	(12, 'Des'),
)

# Create your models here.
class Person(models.Model):
	name = models.CharField("Name*", max_length=50)
	title = models.CharField("Job title", max_length=60, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	mail = models.EmailField("E-mail*")
	photo = models.URLField("Photo-URL", null=True, blank=True)
	image = models.ImageField(upload_to="photos", null=True, blank=True)
	birthdate = models.DateField("Date of birth (yyyy-mm-dd)", null=True, blank=True)
	
	def __unicode__(self):
		return self.name
		
	def save(self, *args, **kwargs):
		
		super(Person, self).save(*args, **kwargs)
		
		# If there are less than 4 existing CVs, create 4 new CVs for the person.
		if self.cv_set.count() < 4:
			for a in range(1, 5-self.cv_set.count()):
				c = Cv(tags = 'Empty CV', person = self)
				c.save()
				
class Technology(models.Model):
	person = models.ForeignKey(Person)
	title = models.CharField(max_length=50, null=True, blank=True)
	title_en = models.CharField(max_length=50, null=True, blank=True)
	data = models.TextField("Data (separate with comma)", null=True, blank=True)
	data_en = models.TextField(null=True, blank=True)
	def data_as_list(self):
		return self.data.split(',')
	def __unicode__(self):
		if self.title != "":
			return self.title
		else:
			return self.title_en
	
class Experience(models.Model):

	person = models.ForeignKey(Person)
	
	title = models.CharField(max_length=50, null=True, blank=True)
	title_en = models.CharField(max_length=50, null=True, blank=True)
	
	from_year = models.IntegerField('From year*', max_length=4, choices=YEAR_CHOICES, default=0)
	from_month = models.IntegerField('From month', max_length=2, choices=MONTH_CHOICES, default=0, null=True, blank=True)
	to_year = models.IntegerField('To year', max_length=4, choices=YEAR_CHOICES, default=0, null=True, blank=True)
	to_month = models.IntegerField('To month', max_length=2, choices=MONTH_CHOICES, default=0, null=True, blank=True)
	
	company = models.CharField("Client company, Project title", max_length=140, null=True, blank=True)
	company_en = models.CharField(max_length=140, null=True, blank=True)
	
	description = models.TextField(null=True, blank=True)
	description_en = models.TextField(null=True, blank=True)
	
	techs = models.CharField(max_length=140, null=True, blank=True)
	
	def from_ym(self):
		if self.to_year:
			ym = self.to_year*100
			if self.to_month:
				ym += self.to_month
		else:
			ym = self.from_year*100
			if self.from_month:
				ym += self.from_month
		return  ym
	
	def from_monthname(self):
		return MONTH_CHOICES[self.from_month][1] # Problem with languages :( Sigh, I guess we'll use Norwegian first?
	def to_monthname(self):
		return MONTH_CHOICES[self.to_month][1]
	
	def __unicode__(self):
		if self.title is not None:
			t = self.title
		elif self.title_en is not None:
			t = self.title_en
		else:
			t = "No title"
		return "%s, %s, %s" % (t, self.company, self.from_year)

class Workplace(models.Model):

	person = models.ForeignKey(Person)
	
	title = models.CharField(max_length=50, null=True, blank=True)
	title_en = models.CharField(max_length=50, null=True, blank=True)
	
	from_year = models.IntegerField('From year*', max_length=4, choices=YEAR_CHOICES, default=0)
	from_month = models.IntegerField('From month', max_length=2, choices=MONTH_CHOICES, default=0, null=True, blank=True)
	to_year = models.IntegerField('To year', max_length=4, choices=YEAR_CHOICES, default=0, null=True, blank=True)
	to_month = models.IntegerField('To month', max_length=2, choices=MONTH_CHOICES, default=0, null=True, blank=True)
	
	company = models.CharField(max_length=140, null=True, blank=True)
	company_en = models.CharField(max_length=140, null=True, blank=True)
	
	description = models.TextField(null=True, blank=True)
	description_en = models.TextField(null=True, blank=True)
	
	def from_ym(self):
		if self.to_year:
			ym = self.to_year*100
			if self.to_month:
				ym += self.to_month
		else:
			ym = self.from_year*100
			if self.from_month:
				ym += self.from_month
		return  ym
	
	def from_monthname(self):
		return MONTH_CHOICES[self.from_month][1] # Problem with languages :( Sigh, I guess we'll use Norwegian first?
	def to_monthname(self):
		return MONTH_CHOICES[self.to_month][1]
	
	def __unicode__(self):
		return self.title + ", " + self.company
	
class Education(models.Model):

	person = models.ForeignKey(Person)
	
	title = models.CharField(max_length=50, null=True, blank=True)
	title_en = models.CharField(max_length=50, null=True, blank=True)
	
	from_year = models.IntegerField('From year*', max_length=4, choices=YEAR_CHOICES, default=0)
	from_month = models.IntegerField('From month', max_length=2, choices=MONTH_CHOICES, default=0, null=True, blank=True)
	to_year = models.IntegerField('To year', max_length=4, choices=YEAR_CHOICES, default=0, null=True, blank=True)
	to_month = models.IntegerField('To month', max_length=2, choices=MONTH_CHOICES, default=0, null=True, blank=True)
	
	school = models.CharField(max_length=140, null=True, blank=True)
	school_en = models.CharField(max_length=140, null=True, blank=True)
	
	description = models.TextField(null=True, blank=True)
	description_en = models.TextField(null=True, blank=True)
	
	def from_ym(self):
		if self.to_year:
			ym = self.to_year*100
			if self.to_month:
				ym += self.to_month
		else:
			ym = self.from_year*100
			if self.from_month:
				ym += self.from_month
		return  ym
	
	def from_monthname(self):
		return MONTH_CHOICES[self.from_month][1] # Problem with languages :( Sigh, I guess we'll use Norwegian first?
	def to_monthname(self):
		return MONTH_CHOICES[self.to_month][1]
	
	def __unicode__(self):
		return self.title + ", " + self.school
	
class Other(models.Model):

	person = models.ForeignKey(Person)
	
	title = models.CharField(max_length=50, null=True, blank=True)
	title_en = models.CharField(max_length=50, null=True, blank=True)
	
	data = models.TextField(null=True, blank=True)
	data_en = models.TextField(null=True, blank=True)
	
	def data_as_list(self):
		return self.data.split('\n')
		
	def __unicode__(self):
		return self.title

class Cv(models.Model):

	person = models.ForeignKey(Person)
	
	last_edited = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	
	tags = models.CharField(max_length=50)
	
	title = models.CharField(max_length=50, null=True, blank=True)
	title_en = models.CharField(max_length=50, null=True, blank=True)
	
	profile = models.TextField(null=True, blank=True)
	profile_en = models.TextField(null=True, blank=True)
	
	technology = models.ManyToManyField(Technology, null=True, blank=True)
	experience = models.ManyToManyField(Experience, null=True, blank=True)
	workplace = models.ManyToManyField(Workplace, null=True, blank=True)
	education = models.ManyToManyField(Education, null=True, blank=True)
	other = models.ManyToManyField(Other, null=True, blank=True)
	
	def is_recent(self):
		return self.last_edited >= timezone.now() - datetime.timedelta(days=60)
		
	is_recent.admin_order_field = 'last_edited'
	is_recent.boolean = True
	is_recent.short_description = 'Less than two months old'
		
	def __unicode__(self):
		return self.person.name + ", " + self.tags

	def save(self, *args, **kwargs):
		
		# If the tags is "Empty CV", then set it to "Title"
		if self.tags == "Empty CV" and self.title is not None:
			self.tags = self.title
			
		super(Cv, self).save(*args, **kwargs)