
# coding: utf-8

# In[ ]:


#State Class
from collections import deque
N = 3
possible_changes = ((0,1),(0,2),(1,0),(2,0),(1,1))

class State():
    #Initally.All 3 missionaries and cannibals are in one side.
    #The goal is to have all of them on the other side
    
    def __init__(self, prev = None,m=None,c=None):
        if prev == None:
            self.missionaries = N
            self.cannibals = N
            self.river_crossed = False
            self.level = 0
        else:
            self.missionaries = m
            self.cannibals = c
            self.river_crossed = not prev.river_crossed
            self.level = prev.level + 1
            
        self.next_states = []
        self.parent = prev
        
    def __str__(self):
        return str("{} {} {}".format(self.missionaries,self.cannibals,self.river_crossed))
    def game_over(self):
        if self.missionaries < self.cannibals and self.missionaries > 0:
            return True
        elif N - self.missionaries < N -self.cannibals and self.missionaries <3 :
            return True
        return False
    
    def check_invalid(self,m,c):
        if m < 0 or c < 0:
            return True
        elif m > 3 or c > 3:
            return True
        itr = self
        while(itr!= None):
            if itr.missionaries == m and itr.cannibals == c and itr.river_crossed != self.river_crossed:
                return True
            itr = itr.parent
        return False
        
    def explore(self):
        if self.missionaries == 0 and self.cannibals == 0:

            a = self
            while(a!=None):
                a = a.parent
        elif self.game_over() == True:
            pass
        else:

            for i,j in possible_changes:
                if self.river_crossed == True:
                    if i > N - self.missionaries or j > N- self.cannibals:
                        continue
                else:
                    if i >  self.missionaries or j > self.cannibals:
                        continue

                m = self.missionaries - (-1)**self.river_crossed * i
                c = self.cannibals - (-1)**self.river_crossed * j
                if self.check_invalid(m,c)!= True:
                    child = State(self,m,c)
                    #if child.game_over()!= True:
                    self.next_states.append(child)

    def recursive_traverse(self):
        if len(self.next_states )==0:
            return self.__str__()
        else:
            str = ""
            for i in self.next_states:
                str = str + "," + i.recursive_traverse()
            str=str[1:]
            return "("+str+")"+self.__str__()

# In[ ]:


a = State()
queue = deque([a])
while len(queue) != 0 :
    current = queue.popleft()
    current.explore()
    queue.extend(current.next_states)

from ete2 import Tree, faces, AttrFace, TreeStyle

def my_layout(node):
  # Add name label to all nodes
  faces.add_face_to_node(AttrFace("name"), node, column=0, position="branch-right")

ts = TreeStyle()
ts.show_leaf_name = False
ts.layout_fn = my_layout

print(a)

t = Tree("((B,(E,(A,G)M1_t1)M_1_t2)M2_t3,(C,D)M2_t1)M2_t2;", format=8)

str = a.recursive_traverse()+";"
t = Tree(str,format=8)
t.show(tree_style=ts)