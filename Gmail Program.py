#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Gmail

import re
n = input("Enter you Gmail id")

m=re.fullmatch("\w[a-zA-Z0-9_.]*@gmail[.]com",n)
if m!=None:
    print("valid mail id ")
else:
    print("invalid mail id")


# In[ ]:





# In[ ]:




