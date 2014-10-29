# -*- coding: utf-8 -*-
"""
  some utility function of plotting based on matplotlib 
"""
# Author: Honglin Yu <yuhonglin1986@gmail.com>
# License: BSD 3 clause

from matplotlib import axes
import numpy as np
from matplotlib.pyplot import setp

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


 ##############################
 # hist with frequency logged #
 ##############################
def _loghist(self, y, bins=20, logx=False):
    """ first bin the values in y by their rank in y, then boxplot the data in each bin
    
    Arguments:
    - `y`: the data
    - `bins`: 
    """

    if logx == True:
        y = np.log10(np.array(y)+1)
    
    frequencies, boundaries = np.histogram(y, bins=bins)

    X = []
    for i in range(0, len(boundaries)-1):
        X.append( (boundaries[i+1]+boundaries[i])/2.0 )

    frequencies = np.log10(frequencies+1)
        
    self.bar( X, frequencies, width=(X[1]-X[0])*.9 )

    yticks = range(1, int(max(frequencies))+2)
    self.set_yticks(yticks)
    self.set_yticklabels(['$10^%d$' % x for x in yticks])

    if logx == True:
        xticks = range(int(min(y)), int(max(y))+2)
        self.set_xticks(xticks)
        self.set_xticklabels(['$10^%d$' % x for x in xticks])
        
axes.Subplot.loghist = _loghist


 #################
 # group boxplot #
 #################
def _gboxplot(self, groupname_data, colorList=['DarkGreen', 'DarkRed', 'tan', 'pink'],
              legend = None, legendparam=None, groupOrder=None, linewidth = 3, boxWidth = .9, boxDist = .1,
              groupDist = 3, pivotPos = 0):

    if groupOrder == None:
        groupOrder = sorted(groupname_data.keys())

    numBoxInGroup = len(groupname_data.itervalues().next())

    Y = []
    positions = []
    widths = []

    xticks = []

    self.hold(True)

    pivotPos = 0
    
    for groupIdx, groupName in enumerate(groupOrder):
        Y.extend( groupname_data[groupName] )
        positions.extend([pivotPos + x*(boxDist+boxWidth) + groupIdx*groupDist for x in range(numBoxInGroup)])
        xticks.append(np.mean([pivotPos + x*(boxDist+boxWidth) + groupIdx*groupDist for x in range(numBoxInGroup)]))
        widths.extend([boxWidth]*numBoxInGroup)

    bp = self.boxplot(Y, positions=positions, widths=widths)

    print bp
    print bp['boxes']
    print bp['whiskers']
    
    # set colors
    for j in range(len(groupname_data)):
        for i in range(numBoxInGroup):
             setp(bp['boxes'][j*numBoxInGroup+i], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['caps'][j*numBoxInGroup*2+i*2], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['caps'][j*numBoxInGroup*2+i*2+1], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['whiskers'][j*numBoxInGroup*2+i*2], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['whiskers'][j*numBoxInGroup*2+i*2+1], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['fliers'][j*numBoxInGroup*2+i*2], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['fliers'][j*numBoxInGroup*2+i*2+1], color=colorList[i%len(colorList)], linewidth=linewidth)
             setp(bp['medians'][j*numBoxInGroup+i], color=colorList[i%len(colorList)], linewidth=linewidth)


    # add group names
    self.set_xticks(xticks)
    self.set_xticklabels(groupOrder)
    

             
    if legend != None:
        tmp = []
        for i in range(numBoxInGroup):
            h, = self.plot([1,1], color=colorList[i%len(colorList)], linewidth=linewidth)
            tmp.append(h)

        self.legend(tmp, legend, **legendparam)
            
        for h in tmp:
            h.set_visible(False)
            
axes.Subplot.gboxplot = _gboxplot
