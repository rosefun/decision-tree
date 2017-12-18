#python实现决策树2

from math import log
import operator

def calShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVect in dataSet:
        currentLabel = featVect[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = labelCounts[key] / numEntries
        shannonEnt -= prob * math.log(prob, 2)
    return  shannonEnt
    
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
    
def createDataSet():
    dataSet = [['youth', 'no', 'no', 'just so-so', 'no'],
               ['youth', 'no', 'no', 'good', 'no'],
               ['youth', 'yes', 'no', 'good', 'yes'],
               ['youth', 'yes', 'yes', 'just so-so', 'yes'],
               ['youth', 'no', 'no', 'just so-so', 'no'],
               ['midlife', 'no', 'no', 'just so-so', 'no'],
               ['midlife', 'no', 'no', 'good', 'no'],
               ['midlife', 'yes', 'yes', 'good', 'yes'],
               ['midlife', 'no', 'yes', 'great', 'yes'],
               ['midlife', 'no', 'yes', 'great', 'yes'],
               ['geriatric', 'no', 'yes', 'great', 'yes'],
               ['geriatric', 'no', 'yes', 'good', 'yes'],
               ['geriatric', 'yes', 'no', 'good', 'yes'],
               ['geriatric', 'yes', 'no', 'great', 'yes'],
               ['geriatric', 'no', 'no', 'just so-so', 'no']]
    labels = ['age', 'work', 'house', 'credit']
    return dataSet, labels
    
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueValue = set(featList)
        newEntropy = 0.0
        for value in uniqueValue:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / len(dataSet)
            newEntropy += prob * calShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
    
    
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
    
    
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    # 训练集所有实例属于同一类
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 训练集的所有特征使用完毕，当前无特征可用
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree
    
    
    
# myDat, labels = createDataSet()
# myTree = createTree(myDat, labels)
# print(myTree)



# import sys
# from tree import *
 
# reload(sys)
# sys.setdefaultencoding('utf-8')
# from pylab import *
 
# mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
# mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
# ##################################
 
# # 测试决策树的构建
# # myDat, labels = createDataSet()
# # myTree = createTree(myDat, labels)
# # 绘制决策树
# import treePlotter
# treePlotter.createPlot(myTree)


# import matplotlib.pyplot as plt
 
# # 定义文本框和箭头格式
# decisionNode = dict(boxstyle="round4", color='#3366FF')  #定义判断结点形态
# leafNode = dict(boxstyle="circle", color='#FF6633')  #定义叶结点形态
# arrow_args = dict(arrowstyle="<-", color='g')  #定义箭头
 
# #绘制带箭头的注释
# def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    # createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            # xytext=centerPt, textcoords='axes fraction',
                            # va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
 
 
# #计算叶结点数
# def getNumLeafs(myTree):
    # numLeafs = 0
    # firstStr = myTree.keys()[0]
    # secondDict = myTree[firstStr]
    # for key in secondDict.keys():
        # if type(secondDict[key]).__name__ == 'dict':
            # numLeafs += getNumLeafs(secondDict[key])
        # else:
            # numLeafs += 1
    # return numLeafs
 
 
# #计算树的层数
# def getTreeDepth(myTree):
    # maxDepth = 0
    # firstStr = myTree.keys()[0]
    # secondDict = myTree[firstStr]
    # for key in secondDict.keys():
        # if type(secondDict[key]).__name__ == 'dict':
            # thisDepth = 1 + getTreeDepth(secondDict[key])
        # else:
            # thisDepth = 1
        # if thisDepth > maxDepth:
            # maxDepth = thisDepth
    # return maxDepth
 
 
# #在父子结点间填充文本信息
# def plotMidText(cntrPt, parentPt, txtString):
    # xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    # yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    # createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)
 
 
# def plotTree(myTree, parentPt, nodeTxt):
    # numLeafs = getNumLeafs(myTree)
    # depth = getTreeDepth(myTree)
    # firstStr = myTree.keys()[0]
    # cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    # plotMidText(cntrPt, parentPt, nodeTxt)  #在父子结点间填充文本信息
    # plotNode(firstStr, cntrPt, parentPt, decisionNode)  #绘制带箭头的注释
    # secondDict = myTree[firstStr]
    # plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    # for key in secondDict.keys():
        # if type(secondDict[key]).__name__ == 'dict':
            # plotTree(secondDict[key], cntrPt, str(key))
        # else:
            # plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            # plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            # plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    # plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
 
 
# def createPlot(inTree):
    # fig = plt.figure(1, facecolor='white')
    # fig.clf()
    # axprops = dict(xticks=[], yticks=[])
    # createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    # plotTree.totalW = float(getNumLeafs(inTree))
    # plotTree.totalD = float(getTreeDepth(inTree))
    # plotTree.xOff = -0.5 / plotTree.totalW;
    # plotTree.yOff = 1.0;
    # plotTree(inTree, (0.5, 1.0), '')
    # plt.show()
    
    
    
import sys
# # from tree import *
 
# reload(sys)

# sys.setdefaultencoding('utf-8')

import importlib
importlib.reload(sys)
from pylab import *
 
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
##################################
 
# 测试决策树的构建
myDat, labels = createDataSet()
myTree = createTree(myDat, labels)
# 绘制决策树
import treePlotter
treePlotter.createPlot(myTree)