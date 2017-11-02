#!/usr/bin/python

# Brett Kromkamp (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014

from node import Node
import re

(_ROOT, _DEPTH, _BREADTH) = range(3)
ROOT = 'root'

class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier, parent)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print "\t"*depth, "{0}".format(identifier)

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call
      
    def print_to_file(self, file, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth > _ROOT:
            file.write("\t"*(depth-1) + "{0}\n".format(identifier))

        depth += 1
        for child in children:
            self.print_to_file(file, child, depth)  # recursive call
              
      
    def get_first_third_level_leaves(self, identifier, leaves, depth=_ROOT):
        children = self[identifier].children
        
        if depth>1:
            if len(children)==0:
                leaves.append(identifier)
            else:
                children = children[:1]
            
        depth += 1
        
        for child in children:
            self.get_first_third_level_leaves(child, leaves, depth)  # recursive call
        
        return leaves
        
    def get_branch(self, identifier, leaves, depth=_ROOT):
        children = self[identifier].children

        if len(children) == 0:
            leaves.append(identifier)
        elif re.match("^\d+[\.)-]* ", children[0]) is not None: # if children are a numerated list then get only first
            children = children[:1]
             
        depth += 1
        for child in children:
            self.get_branch(child, leaves, depth)  # recursive call
            
        return leaves
        
    def get_tagged_leaves(self, identifier, leaves, tag, depth=_ROOT, is_tagged=False):
        children = self[identifier].children

        if tag in identifier:
            is_tagged = True
        if is_tagged:
            if len(children) == 0:
                leaves.append(identifier)
            elif re.match("^\d+[\.)-]* ", children[0]) is not None: # if children are a numerated list then get only first
                children = children[:1]
 
        depth += 1
        for child in children:
            self.get_tagged_leaves(child, leaves, tag, depth, is_tagged)  # recursive call
            
        return leaves
        
        
    def traverse(self, identifier, mode=_DEPTH, get_leaves=False):
        # Python generator. Loosly based on an algorithm from 
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett, 
        # and Brian J. Reiser, page 239-241
        # yield identifier
        queue = self[identifier].children
        while queue:
            if get_leaves:
                if len(self[queue[0]].children)==0:
                    yield queue[0]
            else:
                yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def dump_to_file(self, filename):
        f = open(filename, 'w')
        self.print_to_file(f, ROOT)
        f.truncate()
        f.close()
        
    def replace_node(self, old_identifier, new_identifier):
        old_node = self[old_identifier]
        parent_node = self[old_node.parent]
        new_node = Node(new_identifier)
        parent_node.replace_child(old_identifier, new_identifier)
        del self[old_identifier]
        self[new_identifier] = new_node
        
    def remove_node(self, key):
        parent_node = self[self[key].parent]
        parent_node.delete_child(key)
        del self[key]

    def __getitem__(self, key):
        if key not in self.__nodes:
            return None
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item
        
    def __delitem__(self, key):
        del self.__nodes[key]
