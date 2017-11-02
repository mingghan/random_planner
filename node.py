#!/usr/bin/python

# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

class Node:
    def __init__(self, identifier, parent=""):
        self.__identifier = identifier
        self.__children = []
        self.__parent = parent

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children
        
    @property
    def parent(self):
    	return self.__parent

    def add_child(self, identifier):
        self.__children.append(identifier)
        #self.__parent = self.identifier
        
    def delete_child(self, identifier):
    	self.__children.remove(identifier)
    	
    def replace_child(self, old_child, new_child):
    	self.__children = [new_child if x == old_child else x for x in self.__children]
