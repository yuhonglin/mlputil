# -*- coding: utf-8 -*-
"""
  some utility function of plotting based on matplotlib 
"""
# Author: Honglin Yu <yuhonglin1986@gmail.com>
# License: BSD 3 clause

from matplotlib import axes
import numpy as np

 #################
 # stackbar plot #
 #################
def _stack_bar(self, y, colorList=['r', 'g', 'b'], norm=False,  yweight=None):
    """make _stackbar plot
    
    Arguments:
    - `y`: list of equal-size list (array)
    - `yweight`: weight on each y. if None, yweight = np.ones(len(y[0]))
    - `norm`: whether to normalize the bar plot
    - `colorList`: the colors of the bars (used circularly)
    """

    length = len(y[0])
    X = np.arange(length)
    
    if yweight == None:
        yweight = np.ones(length)
    else:
        if norm != True:
            raise ValueError('should not use "yweight" when "norm" is not True')
    
    normList = None
    if norm == True:
        normList = np.zeros(length)
        for i, yy in enumerate(y):
            normList = normList + np.array(yy)*float(yweight[i])
    else:
        normList = np.ones(length)


    bottom = np.zeros(length)
    for i, yy in enumerate(y):
        tmp = np.array(yy)/normList*float(yweight[i])
        self.bar(X, tmp, bottom=bottom, color=colorList[i%len(colorList)])
        bottom = bottom + tmp

    if norm == True:
        self.set_ylim([0,1])
        
axes.Subplot.stack_bar = _stack_bar


  ####################
  # range annotation #
  ####################
def _annotate_xrange(self, boundaries, ypos, text, color='r', linewidth=1, fontsize=23):
    """add range annotations
    
    Arguments:
    - `boundaries`: [left x value, right x value]
    - `text`: the text of annoation
    - `ypos`: y postion of the annotation
    """
    maxY, minY = self.get_ylim()

    self.plot([boundaries[0],boundaries[0]], [0, ypos], linewidth=linewidth, color=color)
    self.plot([boundaries[1],boundaries[1]], [0, ypos], linewidth=linewidth, color=color)
    
    self.annotate(text, xy=(boundaries[0], ypos), color=color, xytext=((boundaries[0]+boundaries[1])/2.0, ypos), xycoords='data', textcoords='data', 
                arrowprops=dict(width=1,color=color),horizontalalignment='center',verticalalignment='center', fontsize=fontsize)

    self.annotate(text, xy=(boundaries[1], ypos), color=color, xytext=((boundaries[0]+boundaries[1])/2.0, ypos), xycoords='data', textcoords='data', 
                arrowprops=dict(width=1,color=color),horizontalalignment='center',verticalalignment='center', fontsize=fontsize, alpha=0.0)
    
axes.Subplot.annotate_xrange = _annotate_xrange
