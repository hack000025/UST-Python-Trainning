#!/usr/bin/env python
# coding: utf-8

# In[2]:


#fullmatch()

import re 
s = input("Enter pattern to check")
m = re.fullmatch(s,"ababab")
if m!=None:
    print("Full string is matched")
else:
    print("Full string not matched")


# In[ ]:





# In[ ]:




