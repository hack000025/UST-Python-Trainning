#!/usr/bin/env python
# coding: utf-8

# In[17]:


import re
pattern = '^a...s$'
test_string = 'abyss'

n = str(input("Enter your string with the length of five"))
result = re.match(pattern,test_string)

if result:
  print("Search successful.",result)
else:
  print("Search unsuccessful.",result) 


# In[ ]:




