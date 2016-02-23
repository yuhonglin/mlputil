# -*- coding: utf-8 -*-
"""
  some utility function of plotting based on matplotlib 
"""
# Author: Honglin Yu <yuhonglin1986@gmail.com>
# License: BSD 3 clause

from matplotlib import axes, figure
import numpy as np
from matplotlib.pyplot import setp
from matplotlib.colors import LogNorm

 #################
 # stackbar plot #
 #################
def _stack_bar(self, y, colorList=['r', 'g', 'b'], norm=False,  yweight=None, alpha=1.0):
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

    if not hasattr(alpha, '__iter__'):
        alpha = [alpha for x in range(len(y))]
        

    bottom = np.zeros(length)
    for i, yy in enumerate(y):
        tmp = np.array(yy)/normList*float(yweight[i])
        self.bar(X, tmp, bottom=bottom, color=colorList[i%len(colorList)], alpha=alpha[i])
        bottom = bottom + tmp

    if norm == True:
        self.set_ylim([0,1])
        
axes.Subplot.stack_bar = _stack_bar


  ####################
  # range annotation #
  ####################
def _annotate_xrange(self, boundaries, ypos, text, color='r', linewidth=1, fontsize=23, boundarysize=[0.0, 1.0]):
    """add range annotations
    
    Arguments:
    - `boundaries`: [left x value, right x value]
    - `text`: the text of annoation
    - `ypos`: y postion of the annotation
    """
    maxY, minY = self.get_ylim()

    self.plot([boundaries[0],boundaries[0]], [0+ypos*boundarysize[0], ypos*boundarysize[1]], linewidth=linewidth, color=color)
    self.plot([boundaries[1],boundaries[1]], [0+ypos*boundarysize[0], ypos*boundarysize[1]], linewidth=linewidth, color=color)
    
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
    self.set_yticklabels(['$10^{%d}$' % x for x in yticks])

    if logx == True:
        xticks = range(int(min(y)), int(max(y))+2)
        self.set_xticks(xticks)
        self.set_xticklabels(['$10^{%d}$' % x for x in xticks])
        
axes.Subplot.loghist = _loghist


 #################
 # group boxplot #
 #################
def _gboxplot(self, groupname_data, colorList=['DarkGreen', 'DarkRed', 'tan', 'pink'],
              legend = None, legendparam={}, groupOrder=None, linewidth = 3, boxWidth = .9, boxDist = .1,
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


 #############
 # grid hist #
 #############
def _gridhist(self, data, bins=50,  firstIndexOrder=None, secondIndexOrder=None, axisOff=True):
    """grid hist: histogram of data that can be indexed in 2 ways
    
    Arguments:
    - `data`: a dictionary of the form {(index1, index2) : [data], ...}
    - `bins`:
    - `firstIndexOrder` : the order of first index in plotting, if none, will use lexical order
    - `secondIndexOrder` : the order of second index in plotting, if none, will use lexical order
    - 'axisOff` : whether turn off the axes
    """

    if type(bins) == int:
        tmp = bins
        bins = {}
        for x in data.iterkeys():
            bins[x] = tmp

    # self.subplots_adjust(left=0.1,top=0.9,bottom=0.02,right=0.98,wspace=0.1,hspace=0.1)
            
    # determine the order
    if firstIndexOrder == None:
        firstIndexOrder = sorted( set(map(lambda x: x[0], data.keys())) )
    if secondIndexOrder == None:
        secondIndexOrder = sorted( set(map(lambda x: x[1], data.keys())) )

    for i, firstIndex in enumerate(firstIndexOrder):
        for j, secondIndex in enumerate(secondIndexOrder):
            ax = self.add_subplot( len(firstIndexOrder), len(secondIndexOrder), i*len(secondIndexOrder)+ j + 1 )
            ax.hist(data[(firstIndex, secondIndex)], bins=bins[(firstIndex, secondIndex)])

            if axisOff == True:
                ax.set_xticklabels('')
                ax.set_yticklabels('')

            if j == 0:
                ax.set_ylabel(firstIndex)
            if i == 0:
                ax.set_title(secondIndex)
                
figure.Figure.gridhist = _gridhist


 ###############
 # grid hist2d #
 ###############
def _gridhist2d(self, data, bins=50, norm=LogNorm(), firstIndexOrder=None, secondIndexOrder=None, axisOff=True, histparam={}, fontsize=10):
    """a 2d version of "gridhist"
    
    Arguments:
    - `data`:
    - `firstIndexOrder`:
    - `secondIndexOrder`:
    - `axisOff`:
    """

    if type(bins) == int:
        tmp = bins
        bins = {}
        for x in data.iterkeys():
            bins[x] = tmp

    # determine the order
    if firstIndexOrder == None:
        firstIndexOrder = sorted( set(map(lambda x: x[0], data.keys())) )
    if secondIndexOrder == None:
        secondIndexOrder = sorted( set(map(lambda x: x[1], data.keys())) )

    for i, firstIndex in enumerate(firstIndexOrder):
        for j, secondIndex in enumerate(secondIndexOrder):
            ax = self.add_subplot( len(firstIndexOrder), len(secondIndexOrder), i*len(secondIndexOrder)+ j + 1 )
            h2 = ax.hist2d(data[(firstIndex, secondIndex)][0], data[(firstIndex, secondIndex)][1], bins=bins[(firstIndex, secondIndex)], norm=norm, **histparam)
            
            if axisOff == True:
                ax.set_xticklabels('')
                ax.set_yticklabels('')

            if j == 0:
                ax.set_ylabel(firstIndex)
            if i == 0:
                ax.set_title(secondIndex)

            # self.colorbar(h2, ax=ax)
            cb = self.colorbar(h2[-1], ax=ax)
            cb.ax.tick_params(labelsize=fontsize) 

            for item in (ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(fontsize)
                
figure.Figure.gridhist2d = _gridhist2d


  #################
  # general grid  #
  #################
def _grid(self, data, plotfunc, firstIndexOrder=None, secondIndexOrder=None, axisOff=True):
    """ the general grid function
    
    Arguments:
    - `self`: a figure object
    - `data`:
    - `plotfunc`:
    """

    # determine the order
    if firstIndexOrder == None:
        firstIndexOrder = sorted( set(map(lambda x: x[0], data.keys())) )
    if secondIndexOrder == None:
        secondIndexOrder = sorted( set(map(lambda x: x[1], data.keys())) )

    for i, firstIndex in enumerate(firstIndexOrder):
        for j, secondIndex in enumerate(secondIndexOrder):
            ax = self.add_subplot( len(firstIndexOrder), len(secondIndexOrder), i*len(secondIndexOrder)+ j + 1 )

            if (firstIndex, secondIndex) in data:
                plotfunc(ax, data[(firstIndex, secondIndex)], (firstIndex, secondIndex))

figure.Figure.grid = _grid


  ##################
  # transformation #
  ##################
def _toArray(self, scale='rgb'):
    """ to numpy array
    reference: http://www.icare.univ-lille1.fr/wiki/index.php/How_to_convert_a_matplotlib_figure_to_a_numpy_array_or_a_PIL_image
    Arguments:
    - `self`: an figure object
    """

    scale = scale.lower()
    
    if scale not in ('rgb', 'grey', 'gray'):
        raise('unknown scale, should be one of (\'rgb\', \'grey\', \'gray\')')

    self.canvas.draw()

    w, h = self.canvas.get_width_height()
    buf = np.fromstring( self.canvas.tostring_argb(), dtype=np.uint8, sep='' )
    
    buf.shape = (h, w, 4) # the order of 'h' and 'w' in original code is wrong

    buf = np.roll ( buf, 3, axis = 2 )
    
    if scale == 'rgb':
        return buf
    else:
        return 0.299*buf[:,:,0] + 0.587*buf[:,:,1] + 0.114*buf[:,:,2] 
        
        
figure.Figure.toarray = _toArray
        
        
