from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.template.defaultfilters import default
from django.db.models.signals import post_save


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	
	is_seller    			= models.BooleanField(default=False)
	firstname    			= models.CharField(max_length=30, default='vendeur')
	lastname    			= models.CharField(max_length=30, default='vendeur')
	addressseller  			= models.CharField(max_length=30, default='adresse vendeur')
	telephone       		= models.CharField(max_length=30, default='7777777777')
	shopname        		= models.CharField(max_length=30, default='boutique vendeur')


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def fullname(self):
		return self.firstname + ' ' + self.lastname


	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


#Creaion de la classe AccountProfil pour la modification de sn profil

class Profil(models.Model):
	account = models.OneToOneField(Account, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='profile_image', default='default.png')


	def __str__(self):
		return self.user.username















