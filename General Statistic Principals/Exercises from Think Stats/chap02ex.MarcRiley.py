#!/usr/bin/env python
# coding: utf-8

# # Examples and Exercises from Think Stats, 2nd Edition
# 
# http://thinkstats2.com
# 
# Copyright 2016 Allen B. Downey
# 
# MIT License: https://opensource.org/licenses/MIT
# 

# In[3]:


from __future__ import print_function, division

get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np

import nsfg
import first


# Given a list of values, there are several ways to count the frequency of each value.

# In[4]:


t = [1, 2, 2, 3, 5]


# You can use a Python dictionary:

# In[5]:


hist = {}
for x in t:
    hist[x] = hist.get(x, 0) + 1
    
hist


# You can use a `Counter` (which is a dictionary with additional methods):

# In[6]:


from collections import Counter
counter = Counter(t)
counter


# Or you can use the `Hist` object provided by `thinkstats2`:

# In[7]:


import thinkstats2
hist = thinkstats2.Hist([1, 2, 2, 3, 5])
hist


# `Hist` provides `Freq`, which looks up the frequency of a value.

# In[8]:


hist.Freq(2)


# You can also use the bracket operator, which does the same thing.

# In[9]:


hist[2]


# If the value does not appear, it has frequency 0.

# In[10]:


hist[4]


# The `Values` method returns the values:

# In[11]:


hist.Values()


# So you can iterate the values and their frequencies like this:

# In[12]:


for val in sorted(hist.Values()):
    print(val, hist[val])


# Or you can use the `Items` method:

# In[13]:


for val, freq in hist.Items():
     print(val, freq)


# `thinkplot` is a wrapper for `matplotlib` that provides functions that work with the objects in `thinkstats2`.
# 
# For example `Hist` plots the values and their frequencies as a bar graph.
# 
# `Config` takes parameters that label the x and y axes, among other things.

# In[14]:


import thinkplot
thinkplot.Hist(hist)
thinkplot.Config(xlabel='value', ylabel='frequency')


# As an example, I'll replicate some of the figures from the book.
# 
# First, I'll load the data from the pregnancy file and select the records for live births.

# In[15]:


preg = nsfg.ReadFemPreg()
live = preg[preg.outcome == 1]


# Here's the histogram of birth weights in pounds.  Notice that `Hist` works with anything iterable, including a Pandas Series.  The `label` attribute appears in the legend when you plot the `Hist`. 

# In[16]:


hist = thinkstats2.Hist(live.birthwgt_lb, label='birthwgt_lb')
thinkplot.Hist(hist)
thinkplot.Config(xlabel='Birth weight (pounds)', ylabel='Count')


# Before plotting the ages, I'll apply `floor` to round down:

# In[17]:


ages = np.floor(live.agepreg)


# In[18]:


hist = thinkstats2.Hist(ages, label='agepreg')
thinkplot.Hist(hist)
thinkplot.Config(xlabel='years', ylabel='Count')


# As an exercise, plot the histogram of pregnancy lengths (column `prglngth`).

# In[19]:


# Solution goes here


# `Hist` provides smallest, which select the lowest values and their frequencies.

# In[20]:


for weeks, freq in hist.Smallest(10):
    print(weeks, freq)


# Use `Largest` to display the longest pregnancy lengths.

# In[21]:


# Solution goes here


# From live births, we can select first babies and others using `birthord`, then compute histograms of pregnancy length for the two groups.

# In[22]:


firsts = live[live.birthord == 1]
others = live[live.birthord != 1]

first_hist = thinkstats2.Hist(firsts.prglngth, label='first')
other_hist = thinkstats2.Hist(others.prglngth, label='other')


# We can use `width` and `align` to plot two histograms side-by-side.

# In[23]:


width = 0.45
thinkplot.PrePlot(2)
thinkplot.Hist(first_hist, align='right', width=width)
thinkplot.Hist(other_hist, align='left', width=width)
thinkplot.Config(xlabel='weeks', ylabel='Count', xlim=[27, 46])


# `Series` provides methods to compute summary statistics:

# In[24]:


mean = live.prglngth.mean()
var = live.prglngth.var()
std = live.prglngth.std()


# Here are the mean and standard deviation:

# In[25]:


mean, std


# As an exercise, confirm that `std` is the square root of `var`:

# In[26]:


# Solution goes here


# Here's are the mean pregnancy lengths for first babies and others:

# In[27]:


firsts.prglngth.mean(), others.prglngth.mean()


# And here's the difference (in weeks):

# In[28]:


firsts.prglngth.mean() - others.prglngth.mean()


# This functon computes the Cohen effect size, which is the difference in means expressed in number of standard deviations:

# In[29]:


def CohenEffectSize(group1, group2):
    """Computes Cohen's effect size for two groups.
    
    group1: Series or DataFrame
    group2: Series or DataFrame
    
    returns: float if the arguments are Series;
             Series if the arguments are DataFrames
    """
    diff = group1.mean() - group2.mean()

    var1 = group1.var()
    var2 = group2.var()
    n1, n2 = len(group1), len(group2)

    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d


# Compute the Cohen effect size for the difference in pregnancy length for first babies and others.

# In[30]:


CohenEffectSize(firsts.prglngth, others.prglngth)


# ## Exercises

# Using the variable `totalwgt_lb`, investigate whether first babies are lighter or heavier than others. 
# 
# Compute Cohen’s effect size to quantify the difference between the groups.  How does it compare to the difference in pregnancy length?

# In[31]:


firsts.totalwgt_lb.mean()>others.totalwgt_lb.mean()


# In[32]:


CohenEffectSize(firsts.totalwgt_lb, others.totalwgt_lb)


# For the next few exercises, we'll load the respondent file:

# In[33]:


resp = nsfg.ReadFemResp()


# Make a histogram of <tt>totincr</tt> the total income for the respondent's family.  To interpret the codes see the [codebook](http://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=FEM&section=R&subSec=7876&srtLabel=607543).

# In[35]:


hist = thinkstats2.Hist(resp.totincr)
thinkplot.Hist(hist)
thinkplot.Config(xlabel='total income', ylabel='Count')


# Make a histogram of <tt>age_r</tt>, the respondent's age at the time of interview.

# In[37]:


hist = thinkstats2.Hist(resp.ager)
thinkplot.Hist(hist)
thinkplot.Config(xlabel='Age', ylabel='Count')


# Make a histogram of <tt>numfmhh</tt>, the number of people in the respondent's household.

# In[39]:


hist = thinkstats2.Hist(resp.numfmhh)
thinkplot.Hist(hist)
thinkplot.Config(xlabel='Ammount of people', ylabel='Count')


# Make a histogram of <tt>parity</tt>, the number of children borne by the respondent.  How would you describe this distribution?

# In[40]:


hist = thinkstats2.Hist(resp.parity)
thinkplot.Hist(hist)
thinkplot.Config(xlabel='Number of Children', ylabel='Count')


# Use Hist.Largest to find the largest values of <tt>parity</tt>.

# In[48]:


hist.Largest()


# Let's investigate whether people with higher income have higher parity.  Keep in mind that in this study, we are observing different people at different times during their lives, so this data is not the best choice for answering this question.  But for now let's take it at face value.
# 
# Use <tt>totincr</tt> to select the respondents with the highest income (level 14).  Plot the histogram of <tt>parity</tt> for just the high income respondents.

# In[61]:


more_money=[resp.totincr==14]
hist = thinkstats2.Hist(resp.totincr)
thinkplot.Hist(hist, label='parity')
thinkplot.Config(xlabel='parity', ylabel='Count')


# Find the largest parities for high income respondents.

# In[50]:


hist.Largest()


# Compare the mean <tt>parity</tt> for high income respondents and others.

# In[62]:


less_money=[resp.totincr<14]
less_money.parity.mean(), more_money.parity.mean()


# Compute the Cohen effect size for this difference.  How does it compare with the difference in pregnancy length for first babies and others?

# In[63]:


CohenEffectSize(more_money.parity, less_money.parity)


# In[ ]:


#2-1 answer: using the information found on page 21 the frequency at which the majority of first babies are born are within 2-3 weeks of 28.6 weeks. Meaning first babies arrive as normal. 

