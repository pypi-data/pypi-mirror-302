#!/usr/bin/env python
# coding: utf-8

# # KOMO-3: Manipulation Modelling & Execution
# 
# The discussed components (KOMO, BotOp, NLP_Solver, RRT) provide basic ingredients for manipulation planning and execution. This tutorial is about how to practically use these in typical manipulation settings.
# 
# The first focus is on *manipulation modelling*. While KOMO provides a very powerful abstract framework to define all kinds of constraints, here we discuss what are concrete useful constraints for typical actions, e.g., picking and placing a box, or capsule. The *ManipulationModelling* class is meant to translate between typical actions and the abstract KOMO specification of the corresponding constraints.
# 
# The second focus is on the whole pipeline. We follow a basic sense-plan-act pipeline (not yet a fully integrated reactive framework such as SecMPC). To be more detailed, we assume the following basic steps in each loop:
# * Perception: Update the configuration model to be in sync with the real world - using perception.
# * Discrete decisions (task planning): Decide on discrete next actions, such as which object to pick or place next.
# * Waypoint planning: Model the manipulation constraints for the next few actions and solve them to get a plan for the next few waypoints.
# * Path planning: Create a fine-grained path/trajectory between waypoints, sometimes justing quick interpolation & optimization, sometimes using full fledge path finding (bi-directional RRT).
# * Execution: Sending the path to BotOp for running it on the real system.
# 
# We neglect perception and discrete decision making here.

# ## Manipulation Modelling
# 
# We start with discussing manipulation modelling for standard box/cylinder grasping and placing.

# In[1]:


import robotic as ry
import numpy as np
import random
import time

# this import the local manipulation.py .. to be integrated in robotic..
import manipulation as manip


# A basic configuration with a box and cylinder:

# In[2]:




# ## Integrated Example
# 
# Let's start with an integrated example, where the robot endlessly loops through picking and placing a box on a table.

# In[ ]:


import robotic as ry
import manipulation as manip
import numpy as np
#from importlib import reload
import time
import random


# We define a basic configuration with box on the table:

# In[ ]:


C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/scenarios/pandaSingle.g'))

C.addFrame("box", "table") \
    .setJoint(ry.JT.rigid) \
    .setShape(ry.ST.ssBox, [.15,.06,.06,.005]) \
    .setRelativePosition([-.0,.3-.055,.095]) \
    .setContact(1) \
    .setMass(.1)

C.addFrame("obstacle", "table") \
    .setShape(ry.ST.ssBox, [.06,.15,.06,.005]) \
    .setColor([.1]) \
    .setRelativePosition([-.15,.3-.055,.095]) \
    .setContact(1)

C.delFrame("panda_collCameraWrist")

# for convenience, a few definitions:
qHome = C.getJointState()
gripper = "l_gripper";
palm = "l_palm";
box = "box";
table = "table";
boxSize = C.getFrame(box).getSize()

C.view()




# ### random pushes

# In[ ]:


#from importlib import reload 
#reload(manip)

C.getFrame("l_panda_finger_joint1").setJointState(np.array([.0]))

obj = box
C.getFrame(obj).setRelativePosition([-.0,.3-.055,.095])
C.getFrame(obj).setRelativeQuaternion([1.,0,0,0])

for i in range(30):
     qStart = C.getJointState()

     info = f'push {i}'
     print('===', info)

     M = manip.ManipulationModelling(info)
     M.setup_pick_and_place_waypoints(C, gripper, obj, 1e-1, accumulated_collisions=False)
     helperStart = M.straight_push([1.,2.], obj, gripper, table)
     #random target position
     M.komo.addObjective([2.], ry.FS.position, [obj], ry.OT.eq, 1e1*np.array([[1,0,0],[0,1,0]]), .4*np.random.rand(3) - .2+np.array([.0,.3,.0]))
     M.solve()
     if not M.ret.feasible:
          continue

     M1 = M.sub_motion(0, accumulated_collisions=False)
     M1.retractPush([.0, .15], gripper, .03)
     M1.approachPush([.85, 1.], gripper, .03)
     M1.no_collisions([.15,.85], [obj, "l_finger1"], .02)
     M1.no_collisions([.15,.85], [obj, "l_finger2"], .02)
     M1.no_collisions([.15,.85], [obj, 'l_palm'], .02)
     M1.no_collisions([], [table, "l_finger1"], .0)
     M1.no_collisions([], [table, "l_finger2"], .0)
     M1.solve()
     if not M1.ret.feasible:
          continue

     M2 = M.sub_motion(1, accumulated_collisions=False)
     M2.komo.addObjective([], ry.FS.positionRel, [gripper, helperStart], ry.OT.eq, 1e1*np.array([[1,0,0],[0,0,1]]))
     M2.solve()
     if not M2.ret.feasible:
          continue

     M1.play(C, 1.)
     C.attach(gripper, obj)
     M2.play(C, 1.)
     C.attach(table, obj)

del M


# ## TODOS:
# * Proper execution: BotOp instead of display with C
# * RRTs
# * additional planar motion constraint for in-plane manipulation
# * more typical manipulation constraints: camera_look_at, push_straight, 

# In[ ]:


del C


# In[ ]:




