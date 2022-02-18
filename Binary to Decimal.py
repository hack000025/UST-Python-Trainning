#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math


# In[2]:


import random


# In[15]:


num = int(input("Enter any binary number"))
sum = 0
i = 0
while num!=0:
    rem = num%10
    sum = sum+rem*pow(2,i)
    num = int(num/10)
    i = i+1
    print("Decimal number sum",sum)


# In[ ]:




