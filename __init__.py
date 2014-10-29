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

 ###############
 # bin boxplot #
 ###############
def _rankbin_boxplot(self, y, bins=20, yscale='normal', reverse=True):
    """ first bin the values in y by their rank in y, then boxplot the data in each bin
    
    Arguments:
    - `y`: the data
    - `bins`: integer, number of rankbin
    - `reverse`:
    """
    if yscale not in ('normal', 'log'):
        return

    # first rank the data
    if yscale == 'normal':
        sortedy = sorted(y, reverse=reverse)
    else:
        sortedy = [np.log10(x+1) for x in sorted(y, reverse=reverse)]

    numDataInEachBin = int(len(y)/bins)

    Y = []

    for i in range(0, bins-1):
        Y.append(sortedy[i*numDataInEachBin:(i+1)*numDataInEachBin])

    Y.append(sortedy[(bins-1)*numDataInEachBin:])
        
    self.boxplot(Y)

    if yscale == 'log':
        yticks = range(1, int(max(sortedy))+2)
        self.set_yticks(yticks)
        self.set_yticklabels(['$10^%d$' % x for x in yticks])
    
axes.Subplot.rankbin_boxplot = _rankbin_boxplot
