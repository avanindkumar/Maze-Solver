from tkinter import font
import cv2
import numpy as np
import threading
import colorsys
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import colorsys
import time

# image changing in frame nad mouse event

#class definition
class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

imagelist=["images/bottom.jpeg","images/default_background.png","images/default_title.jpg","images/mid.jpg","images/title.jpg","images/transition.jpg"]
img=None
loc=None
w=0
h=0
rw =2
count = 0
start = Point()
end = Point()
found = False
done_solving=False
algo_running=False

dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
#functions
def re_renderTk():
    global img
    cv2.imwrite("solved.png",img)
    imgTk=Image.fromarray(img)
    imgTk = ImageTk.PhotoImage(imgTk)
    imageRender.configure(image=imgTk)
    imageRender.image = imgTk
    

def DIJKSTRA():
    print("dijkstra")
    
def ASTAR():
    print("a star") 
       
def BFS():
    global img, h,w,dir4,found,done_solving,algo_running,start,end
    s=start
    e=end
    print("BFS called",s.x,e.x)
    algo_running=True
    const = 2
    q = []
    v = [ [0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    nodecount=1
    q.append(s)    
    v[s.y][s.x] = 1
    while len(q) > 0:
        p = q.pop(0)
        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                q.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1
                img[cell.y][cell.x] = list(reversed([i*255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x]/const, 1, 1)]))
                parent[cell.y][cell.x] = p

                if cell == e:
                    found = True
                    del q[:]
                    break
                    
    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()
        for p in path:
            img[p.y][p.x] = [255,0,0]
        print("path found")
        algo_running=False
        done_solving=True;
        re_renderTk()
    else:
        print("path not found")
        done_solving=True;
        algo_running=False
        re_renderTk()
    
def DFS():
    global img, h,w,dir4,found,done_solving,algo_running,start,end
    s=start
    e=end
    print("DFS called")
    algo_running=True
    const = 2
    q = []
    v = [ [0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]
    nodecount=1    
    q.insert(0,s)
    v[s.y][s.x] = 1
    while len(q) > 0:
        p = q.pop(0)
        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)): 
                q.insert(0,cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1
                img[cell.y][cell.x] = list(reversed([i*255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x]/const, 1, 1)]))
                parent[cell.y][cell.x] = p

                if cell == e:
                    found = True
                    del q[:]
                    break
                    
    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()
        for p in path:
            img[p.y][p.x] = [255,0,0]
        print("path found")
        algo_running=False
        done_solving=True;
        re_renderTk()
    else:
        print("path not found")
        done_solving=True;
        algo_running=False
        re_renderTk()
        

def disp():
    global img,found,new_image
    # cv2.namedWindow("MouseEvent")
    # # cv2.imshow("MouseEvent",img)
    # cv2.setMouseCallback('MouseEvent', mouse_event)
    while done_solving!=True:
        new_image=Image.fromarray(img)
        new_image=ImageTk.PhotoImage(new_image)
        imageRender.configure(image=new_image)
        imageRender.image = new_image
        # cv2.imshow('MouseEvent', img)
        # cv2.waitKey(1)
    # cv2.waitKey(3000)
    # if done_solving==True:
    #     cv2.destroyWindow('MouseEvent')

def mouse_event(event, pX, pY, flags, params):
    global img, start, end, count
    if event == cv2.EVENT_LBUTTONUP:
        if count == 0:
            cv2.rectangle(img, (pX-rw, pY-rw), (pX+rw, pY+rw), (0,0,255), -1)
            start = Point(pX, pY)
            print("start = ", start.x, start.y)
            count+=1
        elif count == 1:
            cv2.rectangle(img, (pX-rw, pY-rw), (pX+rw, pY+rw), (0,200,50), -1)
            end = Point(pX, pY)
            print("end = ", end.x, end.y)
            count+=1


def mouse_event_handler():
    global start,end,img,loc,h,w
    img=cv2.imread(loc,cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w = img.shape[:2]
    # t = threading.Thread(target=BFS, args=(start, end))
    # t.daemon = True
    # t2 = threading.Thread(target=disp, args=())
    # t2.daemon = True
    while count<2:
        pass
        BFS(start, end)
    # re_renderTk()


def open_img():
    global start,end,img,loc,h,w
    loc = filedialog.askopenfilename()
    imgTk = Image.open(loc)
    imgTk = ImageTk.PhotoImage(imgTk)
    imageRender.configure(image=imgTk)
    imageRender.image = imgTk
    img=cv2.imread(loc,cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w = img.shape[:2]



def mouse(e):
    global count,start,end
    if(count==0):
        print("Start: ",(e.x),str(e.y))
        start = Point(e.x,e.y)
        status_start_label.config(text=f"Start: X={start.x}, Y={start.y}")
        count+=1
    elif(count==1):
        print("End: ",str(e.x),str(e.y))
        end = Point(e.x,e.y)
        status_end_label.config(text=f"End: X={end.x}, Y={end.y}")
        count+=1


def event_raise():
    global done_solving
    while done_solving!=True:
        imageRender.event_generate("<<event1>>", when="tail", state=123)
        time.sleep(0.2)
        

def update_frame_image(e):

    global img,algo_running
    if(algo_running==False):
        pass
    else:
        imgTk=Image.fromarray(img)
        imgTk = ImageTk.PhotoImage(imgTk)
        imageRender.configure(image=imgTk)
        imageRender.image = imgTk

def clear_location():
    global start,end,count
    start.x=0
    start.y=0
    end.x=0
    end.y=0
    count=0
    status_start_label.config(text=f"Start: X={start.x}, Y={start.y}")
    status_end_label.config(text=f"End: X={end.x}, Y={end.y}")

def run_algo(algo_name):
    if(algo_name=="dfs"):
        thd2 = threading.Thread(target=DFS) 
        thd2.start()

    if(algo_name=="bfs"):
        thd2 = threading.Thread(target=BFS) 
        thd2.start()
    if(algo_name=="astar"):
        thd2 = threading.Thread(target=ASTAR) 
        thd2.start()
    if(algo_name=="dijkstra"):
        thd2 = threading.Thread(target=DIJKSTRA) 
        thd2.start()
        
def clear_image():
    global start,end,img,loc,h,w,count,done_solving,found
    img=None
    loc=None
    h=0
    w=0
    done_solving=False
    found=False
    imageRender.configure(image='')
    clear_location()
    
    

    


window=Tk()
window.state('zoomed')
window.title('Maze Solver')


varimage = StringVar()
inputimage = StringVar()



TopFrame = Frame(window,bg="#009be5", bd=0)
TopFrame.pack(side=TOP, fill=X)
title= Label(TopFrame, font=("Bold", 32,),text="Maze Solver",bg="#009be5",fg="white")
title.pack()


MidFrame = Frame(window,bg="#63ccff")
MidFrame.pack(side=TOP, fill="both", expand=True)

MidFrameLeft = Frame(MidFrame,bg="#63ccff",width=300,height=300,highlightthickness=4,highlightbackground="red")
MidFrameLeft.pack(side=LEFT, fill="both",anchor="nw",expand=True)
MidFrameRight = Frame(MidFrame,bg="#63ccff",width=300,height=300,highlightthickness=4,highlightbackground="red")
MidFrameRight.pack(side=RIGHT, fill="y",anchor="ne")



BottomFrame = Frame(window, bg="#006db3", bd=0)
BottomFrame.pack(side=BOTTOM, fill=X)

canvas = Canvas(MidFrameLeft,bg="#63ccff",bd=-2)
v_scrollbar = Scrollbar(MidFrameLeft, orient="vertical", command=canvas.yview)
h_scrollbar =Scrollbar(MidFrameLeft,orient=HORIZONTAL,command=canvas.xview)

scrollable_frame = Frame(canvas)
scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(xscrollcommand=h_scrollbar.set)
canvas.configure(yscrollcommand=v_scrollbar.set)

h_scrollbar.pack(side=BOTTOM,fill=X)
v_scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

imageRender = Label(scrollable_frame,bg="#63ccff")
imageRender.pack()
imageRender.bind("<Button-1>",mouse)
imageRender.bind("<<event1>>", update_frame_image)

status_start_label=Label(MidFrameRight,font=("Bold",11,),text=f"Start: X={start.x}, Y={start.y}",width=20,bg="#63ccff",)
status_start_label.grid(row=0,column=0,pady=5)
status_end_label=Label(MidFrameRight,font=("Bold",11,),text=f"End: X={end.x}, Y={end.y}",width=20,bg="#63ccff",)
status_end_label.grid(row=1,column=0,pady=5)
status_location_clear_button=Button(MidFrameRight,text="Clear Location",width=15,bg="#ec97f9",command=clear_location)
status_location_clear_button.grid(row=1,column=1,)
status_location_clear_button=Button(MidFrameRight,text="Clear Image",width=15,bg="#ec97f9",command=clear_image)
status_location_clear_button.grid(row=5,column=1,pady=10)


thd = threading.Thread(target=event_raise) 
thd.daemon = True
thd.start()






open_image_button = Button(BottomFrame, text='Open Image',bg="#ec97f9", command=lambda: open_img())
open_image_button.grid(row=0, column=0, padx=30,sticky="nsew")
dfs_algo_button = Button(BottomFrame, text='DFS Search', bg="#ec97f9",command=lambda:run_algo("dfs"))
dfs_algo_button.grid(row=0, column=1, padx=30,sticky="nsew")
bfs_algo_button = Button(BottomFrame, text='BFS Search', bg="#ec97f9",command=lambda:run_algo("bfs"))
bfs_algo_button.grid(row=0, column=2, padx=30,sticky="nsew")
astar_algo_button = Button(BottomFrame, text='A* Search', bg="#ec97f9",command=lambda:run_algo("astar"))
astar_algo_button.grid(row=0, column=3, padx=30,sticky="nsew")
dijkstra_algo_button = Button(BottomFrame, text='Dijkstra Search', bg="#ec97f9",command=lambda:run_algo("dijkstra"))
dijkstra_algo_button.grid(row=0, column=4, padx=30,sticky="nsew")


window.mainloop()

