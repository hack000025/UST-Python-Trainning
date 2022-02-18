#!/usr/bin/env python
# coding: utf-8

# In[2]:


# match()

import re 
s = input("enter pattern to check :")
m = re.match(s,"abcxyzabcabdef")
if m!=None:
   print("Match is available at the beginning of the sting ")
   print("Start index :",m.start(),"and End index :",m.end())
else:
   print("Match is not available at the beginning of the string")


# In[ ]:




