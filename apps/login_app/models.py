# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def ValidateUserInfo(self, PostData):
        results = {"status": True, 'errors': [] }
        if len(PostData['first_name']) < 2:
            results['errors'].append("first name must be 3 or more characters")
        if not (PostData['first_name']).isalpha():
            results['errors'].append("first name must be alphabetic characters")
        if len(PostData['last_name']) < 2:
            results['errors'].append("last name must be 3 or more characters")
        if not (PostData['last_name']).isalpha():
            results['errors'].append("last name must be alphabetic characters")
        regexResult = re.search(r'\w+@\w+',PostData['email'])
        if not regexResult:
            results['errors'].append("Email is not valid")

        if len(PostData['password']) < 5:
            results['errors'].append("Passwords must be 5 or more characters")
        if PostData['password'] != PostData['passwordc']:
            results['errors'].append("Passwords do not match")
        matchingEmailCount = len( self.filter(email = PostData['email'] ) )
        if (0 < matchingEmailCount):
            results['errors'].append("a user with that email already exists")
        AreThereErrors = (0 == len(results['errors'] ) )
        results['status'] = AreThereErrors
        return results;
    def Creator(self, PostData):
        tempstr = PostData['password']
        hashedPw = bcrypt.hashpw(tempstr.encode(), bcrypt.gensalt())
        print "Hashed Value:" , hashedPw , '%'*30
        user = User.objects.create( first_name=PostData['first_name'],  last_name= PostData['last_name'], email = PostData['email'], password = hashedPw )
        user.save()
        return self;
    def logVal(self, PostData):
        results = {"status": False, 'errors': [], 'user' : None }
        ThisUser = self.filter(email = PostData['email'] ).first()
        if (None == ThisUser):
            results['errors'].append('There is no user found with email {}'.format(PostData['email']) )
        else:
            print "db  @:", ThisUser.email, "  pw:", ThisUser.password
            print "Web @:", PostData['email'], "  pw:", PostData['password']
            incomingpw = PostData['password']
            dbpw = ThisUser.password
            if bcrypt.checkpw(incomingpw.encode(), dbpw.decode() ):
                print "user Is Logged In", '$'*50
                results['status'] = True
                results['user'] = ThisUser
            else:
                print "password not allowd", '$'*50
                results['status'] = False
        return results;


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
