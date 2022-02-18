#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Modules


# In[1]:


#Impoortance of modules
#1.we known that Functions concept is used for performing some operations and provides code Re-usability.
#2.Functions concept provides code Re-usability within the same program and unable to provide code Re-usabilty across the programs.
#3.In order to provide code Re-usability across the programs,we must use the concept of modules.


# In[ ]:


#definition of module
A module is a collection of variables,functions and classes.


# In[ ]:


#Types of modules
1.Pre-defined modules or Built-in-modules.
2.programmer -defined modules or user -defined modules


# In[2]:


#example of pre-defined module


# In[4]:


import calendar
print(calendar.month(2022,2))


# In[5]:


from calendar import month
print(month(1997,10))


# In[6]:


import random             #OTP
print(random.randint(100,999))


# In[7]:


from random import randint as r     #OTP
print(r(1000,9999))


# In[ ]:


#Approches to re-use the modules.They are
1.by using import modulename
2.by using from modulename import members


# In[ ]:


#syntaxes for importing modules
1.import modulename
2.import module1,module2
3.import module1 as m1
4.import module1 as m1,module2 as m2
5.from module import member
6.from module import member1,member2,member3
7.from module import member1 as x
8.from module import *


# In[8]:


#Datetime module
1.date have 3 fields---->Year,month,day
2.time have 4 fields----->Hours,minutes,seconds and microseconds


# In[9]:


#To retrive current date and time
import datetime
res=datetime.datetime.now()
print(res)


# In[10]:


#To create date object
import datetime
res1=datetime.datetime(2022,2,16,12,30,30,45)
print(res1)


# In[1]:


import datetime
cd=datetime.datetime.now()
res=cd.strftime('%y')
print("shortform of year:",res)
res=cd.strftime('%Y')
print("fullform of year:",res)
res=cd.strftime('%b')
print("shortform of month:",res)
res=cd.strftime('%B')
print("fullform of year:",res)
res=cd.strftime('%a')
print("shortform of day:",res)
res=cd.strftime('%A')
print("fullform of day:",res)
res=cd.strftime('%H')
print("Hours in 24hrs format:",res)
res=cd.strftime('%I')
print("Hours in 12hrs format:",res)
res=cd.strftime('%p')
print("AM/PM:",res)
res=cd.strftime('%M')
print("mintues:",res)
res=cd.strftime('%S')
print("seconds:",res)
res=cd.strftime('%f')
print("microseconds:",res)
res=cd.strftime('%j')
print("Day number of year:",res)
res=cd.strftime('%x')
print("local date:",res)
res=cd.strftime('%X')
print("local time:",res)







# In[2]:


#TO check the min and max values of time in a day
print('Earliest:',datetime.time.min)
print('Latest:',datetime.time.max)
print('Resolution:',datetime.time.resolution)


# In[3]:


#To check the min and max values of date in a year
print('Earliest:',datetime.date.min)
print('Latest:',datetime.date.max)
print('Resolution:',datetime.date.resolution)


# In[ ]:


#timeit module will measure exection in seconds.timeit module is used to know how long your code is taking to run.


# In[19]:


#timeit module
import timeit 
timeit.timeit('" _".join(str(n)for n in range(100))',number=1000)


# In[20]:


#random module


# In[21]:


import random as r
r.randrange(10,20)


# In[23]:


r.randint(1000,9999)


# In[24]:


r.random()


# In[25]:


r.uniform(1,2)


# In[26]:


list=['hello','bye','hi','smile']
print(r.choice(list))


# In[31]:


list=['bhavani','guru','kiran','aruna','maya']
r.shuffle(list)
print(list)


# In[32]:


list=['bhavani','guru','kiran','aruna','maya']
r.sample(list,3)


# In[ ]:


#math module


# In[1]:


from math import*
print(sqrt(4))
print(ceil(5.7))    #always will give least value
print(floor(5.7))   #always will give highest value
print(log(9))
print(sin(60))
print(tan(90))
print(round(5.7))
print(pow(3,3))


# In[2]:


#constants
print(pi)
print(e)

