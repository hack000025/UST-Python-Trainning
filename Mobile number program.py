#!/usr/bin/env python
# coding: utf-8

# In[1]:


# to check whether the given number is valid mobile number or not 
import re
n = input("Enter number")
#[7-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] or \d{9}
m = re.fullmatch("[7-9]\d{9}",n)
if m!= None:
    print("Valid Mobile number")
else:
    print("invalid Mobile number")


# In[ ]:





# In[ ]:




