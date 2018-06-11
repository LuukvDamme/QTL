#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  4 17:05:19 2018

@author: luuk

script to run a t.test on marker files
requires a file with markers and a file with values
output is a file with either H0/H1 or both
"""
from scipy.stats import stats
import numpy as np

def main():
    Values=ReadFile("CvixLerC9.loc", "CvixLerC9.qua")
    tTest(Values)
    
    
#Method creates 3 lists out of 2 files containing 
#headers, a/b's and the values
#the a/b's in infolist are +1 on the index 0 is empty
def ReadFile(a,b):
    
    file1=open(a,"r")
    file2=open(b,"r")  
    
    #create values that will be used
    i=0
    o=0
    head=""
    info=""     
    headlist=[]
    infolist=[]   
    
    #make usefull lists out of first file
    for line in file1:
        if line==("\n"):
            i=i+1
        if i==2:
            if "(a,b)" in line:
                head=line
                head=head.replace("\n","")
                headlist.append(head)
                if o!=0:
                    info=info.replace("\n","")
                    info=info.replace(" ","")
                    infolist.append(info)
                    info=""
            else:
                o=1
                info=info.replace("\n","")
                info=info.replace(" ","")
                info+=line
                
    info=info.replace("\n","")
    info=info.replace(" ","")
    infolist.append(info)
  

    #create values that will be used
    i=0
    valuelist=[]
    
    #make usefull list out of second file
    for line in file2:
        line=line.replace("\n","")
        if line[0].isdigit():
            line=line.split("\t")
            valuelist.append(line[1])
            
    file1.close
    file2.close
    return headlist, infolist, valuelist


#Method loops overe the headerlist and takes the corresponding values and a/b's
#it ignores when a value is -
#this data is converted into an array of a and an array of b
#this is used in a t.test writing to the file can be turned on/off depending on the interest of the research
def tTest(ReadList):
    headerlist=ReadList[0]
    infolist=ReadList[1]
    valuelist=ReadList[2]
    alist=[]
    blist=[]
    index=1
    letterIndex=0
    Results=open("H1Results.txt","a")
    
    for header in headerlist:
        info=infolist[index]
        for letter in info:
            
            if letter=="a":
                a=valuelist[letterIndex]
                if a=="-": 
                    a=0
                    letterIndex=letterIndex+1
                else:
                    a=float(a)
                    alist.append(a)
                    letterIndex=letterIndex+1
                    
            if letter=="b":
                b=valuelist[letterIndex]
                if b=="-":
                    b=0
                    letterIndex=letterIndex+1
                else:    
                    b=float(b)
                    blist.append(b)
                    letterIndex=letterIndex+1
                    
            if letter=="-":
                letterIndex=letterIndex+1

        aarray = np.asarray(alist).astype(np.float)
        barray = np.asarray(blist).astype(np.float)
        
        t, p = stats.ttest_ind(aarray,barray)
        """
        if float(p)>0.05:        
            Results.write(header)   
            Results.write("\n")            
            Results.write(" P-value= ")
            Results.write(str(p))
            Results.write(" H0=True")
            Results.write("\n")
            Results.write("\n")
        """   
        if float(p)<0.05:        
            Results.write(header)   
            Results.write("\n")            
            Results.write(" P-value= ")
            Results.write(str(p))
            Results.write(" H1=True")
            Results.write("\n")
            Results.write("\n")
        
        letterIndex=0
        index=index+1
        alist=[]
        blist=[]

    Results.close
    
    
main()