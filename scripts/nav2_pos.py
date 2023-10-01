#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by AutomaticAddison.com
 
import time  # Time library
import os
from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2
from ament_index_python.packages import get_package_share_directory
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult # Helper module
import copy
import tkinter as tk
import speech_recognition as sr
from threading import *
import queue
from PIL import Image, ImageTk

bringup_dir = get_package_share_directory('r2d2')
'''
Navigates a robot from an initial pose to a goal pose.
'''
q = queue.Queue()

class Location():
  def __init__(self, posx, posy, posz):
    self.goal_pose = PoseStamped()
    self.goal_pose.header.frame_id = 'map'
    self.goal_pose.pose.position.x = posx
    self.goal_pose.pose.position.y = posy
    self.goal_pose.pose.position.z = posz
    self.goal_pose.pose.orientation.x = 0.0
    self.goal_pose.pose.orientation.y = 0.0
    self.goal_pose.pose.orientation.z = 0.0
    self.goal_pose.pose.orientation.w = 1.0

locations = {"CnC lab": Location(3.0, -2.0, 0.00447),
            "3d printing lab":Location(6.0, -1.0, 0.00447),
            }

class PageManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("R2D2 Interface")
        self.geometry("800x480")
        self.start_voice_assistant()  # Start the voice assistant in the background
        # Create a container frame to hold the pages
        self.container = tk.Frame(self)
        self.container.pack(pady=0, padx=0, expand=True)
        self.recognizer = sr.Recognizer()
        self.start_app = Thread(target=self.ros_nav, args=(q,))
        self.start_app.start()
        
        # Dictionary to store all pages
        self.pages = {}
        
        # Initialize the pages
        for PageClass in (Page1, Page2, Page3):
            page_name = PageClass.__name__
            page = PageClass(self.container, self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        self.show_page("Page1")
    
    def show_page(self, page_name):
        # Show the requested page
        page = self.pages.get(page_name)
        if page:
            page.tkraise()
    
    def start_voice_assistant(self):
      assistant = VoiceAssistant(self)
      background_listener = Thread(target=assistant.listen_for_keyword)
      background_listener.start()

    def ros_nav(self, c):
      rclpy.init()
      
    
      # Launch the ROS 2 Navigation Stack
      navigator = BasicNavigator()
    
      #Set the robot's initial pose if necessary
      #initial_pose = PoseStamped()
      #initial_pose.header.frame_id = 'map'
      #initial_pose.header.stamp = navigator.get_clock().now().to_msg()
      #initial_pose.pose.position.x = 0.0
      #initial_pose.pose.position.y = 0.0
      #initial_pose.pose.position.z = 0.0
      #initial_pose.pose.orientation.x = 0.0
      #initial_pose.pose.orientation.y = 0.0
      #initial_pose.pose.orientation.z = 0.0
      #initial_pose.pose.orientation.w = 1.0
      #navigator.setInitialPose(initial_pose)
    
      # Activate navigation, if not autostarted. This should be called after setInitialPose()
      # or this will initialize at the origin of the map and update the costmap with bogus readings.
      # If autostart, you should `waitUntilNav2Active()` instead.
      # navigator.lifecycleStartup()
    
      # Wait for navigation to fully activate. Use this line if autostart is set to true.
      navigator.waitUntilNav2Active()
    
      # If desired, you can change or load the map as well
      # navigator.changeMap('/path/to/map.yaml')
    
      # You may use the navigator to clear or obtain costmaps
      # navigator.clearAllCostmaps()  # also have clearLocalCostmap() and clearGlobalCostmap()
      # global_costmap = navigator.getGlobalCostmap()
      # local_costmap = navigator.getLocalCostmap()
    
      # Set the robot's goal pose
      goal_pose = PoseStamped()
      goal_pose.header.frame_id = 'map'
      goal_pose.header.stamp = navigator.get_clock().now().to_msg()
      goal_pose.pose.position.x = 10.0
      goal_pose.pose.position.y = 2.0
      goal_pose.pose.position.z = 0.0
      goal_pose.pose.orientation.x = 0.0
      goal_pose.pose.orientation.y = 0.0
      goal_pose.pose.orientation.z = 0.0
      goal_pose.pose.orientation.w = 1.0
      a = 0
      pause_at_goal = False
      #q.put(goal_pose)
      while True:
        try:
          goal_pose = c.get(block=False)
          goal_pose.header.stamp = navigator.get_clock().now().to_msg()
          navigator.cancelTask()
          pause_at_goal = True
          navigator.goToPose(goal_pose)
          continue
        except:
          pass
        # Do something depending on the return code
        if navigator.isTaskComplete():
            print('Goal succeeded!')
            if pause_at_goal:
              print("pausing")
              time.sleep(10)
              pause_at_goal = False
              a ^= 1
            if a == 0:
              goal_pose.header.stamp = navigator.get_clock().now().to_msg()
              goal_pose.pose.position.x = 0.0
              goal_pose.pose.position.y = -7.0
              goal_pose.pose.position.z = 0.0
              goal_pose.pose.orientation.x = 0.0
              goal_pose.pose.orientation.y = 0.0
              goal_pose.pose.orientation.z = 0.0
              goal_pose.pose.orientation.w = 1.0
            elif a == 1:
              goal_pose.header.stamp = navigator.get_clock().now().to_msg()
              goal_pose.pose.position.x = 10.0
              goal_pose.pose.position.y = 3.0
              goal_pose.pose.position.z = 0.0
              goal_pose.pose.orientation.x = 0.0
              goal_pose.pose.orientation.y = 0.0
              goal_pose.pose.orientation.z = 0.0
              goal_pose.pose.orientation.w = 1.0
            a ^= 1
            navigator.goToPose(goal_pose)
        #result = navigator.getResult()
        #if result == TaskResult.CANCELED:
        #    print('Goal was canceled!')
        #elif result == TaskResult.FAILED:
        #    print('Goal failed!')
        #else:
        #    print('Goal has an invalid return status!')
    
      # Shut down the ROS 2 Navigation Stack
      navigator.lifecycleShutdown()

class PageFeatures(tk.Frame):
  def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.tk = controller.tk
        
  def show(self):
      self.tkraise()
  
  def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y

  def dragging(self, event):
      dx = event.x - self.last_x
      dy = event.y - self.last_y

      self.zoom_factor += dy * 0.01  # Adjust zoom factor based on vertical movement

      if self.zoom_factor < 0.5:
          self.zoom_factor = 0.5
      elif self.zoom_factor > 2.0:
          self.zoom_factor = 2.0

      self.image = self.image.resize((int(200 * self.zoom_factor), int(200 * self.zoom_factor)))
      self.image_photo = ImageTk.PhotoImage(self.image)
      self.image_label.config(image=self.image_photo)

      self.last_x = event.x
      self.last_y = event.y

  def stop_drag(self, event):
      self.last_x = 0
      self.last_y = 0

  def change_page(self, page_name):
        self.controller.after(0, self.controller.show_page, page_name)

  def multi_action(self, location, page):
    end_goal = copy.deepcopy(location.goal_pose)
    q.put(end_goal)
    self.change_page(page)

    
class Page1(PageFeatures):
  def __init__(self, parent, controller):
    PageFeatures.__init__(self, parent, controller)
    self.label = tk.Label(self, text="Home Page")
    self.label.pack(pady=50, padx=100)
    
    self.text_button_1 = tk.Label(self, text="Looking for somewhere?", font=("Helvetica", 16, "bold"), relief="raised", bd=5, padx=50, pady=50, bg="lightblue")
    self.text_button_1.bind("<Button-1>", lambda event: self.change_page("Page2"))
    self.text_button_1.pack()

    self.text_button_2 = tk.Label(self, text="Are you lost?", font=("Helvetica", 16, "bold"), relief="raised", bd=5, padx=50, pady=50, bg="lightgreen")
    self.text_button_2.bind("<Button-1>", lambda event: self.change_page("Page3"))  # Change the command to switchToPage3
    self.text_button_2.pack()

class Page2(PageFeatures):
  def __init__(self, parent, controller):
    PageFeatures.__init__(self, parent, controller)
    # Create widgets for page 2
    self.label = tk.Label(self, text="Mall Map")
    self.label.pack(pady=50)
            # Load the original image
    self.image = Image.open(os.path.join(bringup_dir, 'maps', 'New_ob.pgm'))
    self.image = self.image.resize((200, 200))  # Resize for display
    self.image_photo = ImageTk.PhotoImage(self.image)

    # Create a label with the PhotoImage
    self.image_label = tk.Label(self, image=self.image_photo)
    self.image_label.pack()
    self.location_button1 = tk.Label(self, text="Go to CnC Lab", font=("Helvetica", 16, "bold"), relief="raised", bd=5, padx=5, pady=5, bg="lightblue")
    self.location_button1.bind("<Button-1>", lambda event: self.multi_action(locations["CnC lab"], "Page1"))
    self.location_button1.pack()
    self.location_button2 = tk.Label(self, text="Go to 3d printing Lab", font=("Helvetica", 16, "bold"), relief="raised", bd=5, padx=5, pady=5, bg="lightblue")
    self.location_button2.bind("<Button-1>", lambda event: self.multi_action(locations["3d printing lab"], "Page1"))
    self.location_button2.pack()
    self.return_button = tk.Label(self, text="Go Back to Main Page", font=("Helvetica", 16, "bold"), relief="raised", bd=5, padx=5, pady=5, bg="lightblue")
    self.return_button.bind("<Button-1>", lambda event: self.change_page("Page1"))
    self.return_button.pack()

    # Bind mouse events
    self.image_label.bind("<Button-1>", self.start_drag)
    self.image_label.bind("<B1-Motion>", self.dragging)
    self.image_label.bind("<ButtonRelease-1>", self.stop_drag)

    self.last_x = 0
    self.last_y = 0
    self.zoom_factor = 1.0  # Initial zoom factor


class Page3(PageFeatures):
  def __init__(self, parent, controller):
    PageFeatures.__init__(self, parent, controller)
    # Create widgets for page 3
    self.label = tk.Label(self, text="Notifying mall staff...")
    self.label.pack(pady=50)

    self.text_button = tk.Label(self, text="Go Back to Main Page", font=("Helvetica", 16, "bold"), relief="raised", bd=5, padx=50, pady=50, bg="lightgreen")
    self.text_button.bind("<Button-1>", lambda event: self.change_page("Page1"))
    self.text_button.pack()

def main():
  app = PageManager()
  while True:
    app.update_idletasks()
    app.update()
  exit(0)
  

if __name__ == '__main__':
  main()