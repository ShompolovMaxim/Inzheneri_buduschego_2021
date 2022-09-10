from tkinter import *
from tkinter import messagebox
from math import *
import webbrowser
import os
from tkinter.ttk import Combobox 
import tkinter.font as tkFont

def del_all():
    global items
    for i in items:
        i.destroy()
    items=[]

def save():
    file=open(name.ent.get()+'.txt','w')
    file.write(status+'\n'+'\n'.join(map(str,settings.setts()))+'\n')
    file.close()
    file=open('saved_names_code123123423.txt','a')
    file.write(name.ent.get()+'\n')
    file.close()
    goto_start()

def chart():
    settings.update()
    if settings.enough():
        settings.calculate()
        if settings.correct():
            try:
                shift=5
                inf.config(text='\n'.join(settings.calculate_extra()))
                settings.pull()
                can.delete('all')
                y=float(settings.y0)
                v=float(settings.v0)
                u=float(settings.alpha)
                tk=(v*sin(u)+((v**2)*(sin(u)**2)+2*g*y)**0.5)/g
                xm=v*cos(u)*tk
                kx=xm/win_width
                ym=y+((v*sin(u))**2)/(g*2)
                ky=((win_height/2-shift)/ym)**(-1)
                k=max(kx,ky)
                x2=0
                y2=win_height//2-int(ym*ky)
                for i in range(0,win_width-1,1):
                    x1=i*k
                    y1=y+tan(u)*x1-g*(x1**2)/(2*(v**2)*(cos(u)**2))
                    y1=int(y1/k)
                    if y1>=0 and x2>=0 and y2>=0:
                        can.create_line(x2,(win_height//2+shift)-y2,i,(win_height//2+shift)-y1,width=2)
                    x2=i
                    y2=y1
            except:
                messagebox.showinfo(message=tr['Impossible to calculate!'], title=tr['Error!'])
        else:
            messagebox.showinfo(message=tr['Impossible to calculate!'], title=tr['Error!'])
    else:
        messagebox.showinfo(message=tr['Not enough data!'], title=tr['Error!'])

def open_theory_file():
    os.system("start "+"Theory_"+leng+".docx")

def show_theory():
    file=open('theory_'+leng+'.txt','r',encoding='utf8')
    s=file.read()
    file.close()
    items[1].destroy()
    items.append(Text(window,wrap=WORD))
    items[-1].insert(1.0,s)
    items[-1].pack(fill=BOTH)

def open_webbrowser():
    try:
        if leng=='rus':
            webbrowser.open('https://ido.tsu.ru/schools/physmat/data/res/virtlab/text/m2_1.html', new=2)
        else:
            webbrowser.open('https://www.matematicus.ru/en/mechanics-and-physics/movement-of-a-body-thrown-at-an-angle-to-the-horizon', new=2)
    except:
        pass

def goto_theory():
    del_all()
    items.append(Button(window,text=tr['Open in file'],command=open_theory_file,width=20))
    items[-1].pack()
    items.append(Button(window,text=tr['Show theory'],command=show_theory,width=20))
    items[-1].pack()
    items.append(Button(window,text=tr['Show in webbrowser'],command=open_webbrowser,width=20))
    items[-1].pack()
    items.append(Button(window,text=tr['Exit'],command=goto_start,width=20))
    items[-1].pack()

def choose_english():
    global tr,leng
    leng='eng'
    tr=dict()
    for i in range(len(eng)):
        tr[eng[i]]=eng[i]
    if items!=[]:
        items[-1]['text']=tr['Exit']

def choose_russian():
    global tr,leng,window
    leng='rus'
    tr=dict()
    for i in range(len(eng)):
        tr[eng[i]]=rus[i]
    if items!=[]:
        items[-1]['text']=tr['Exit']

def goto_language():
    del_all()
    var=IntVar(window) 
    items.append(Radiobutton(window, text='English',variable=var, value=1,command=choose_english,indicatoron=0,width=20))
    items[-1].pack()
    items.append(Radiobutton(window, text='Русский',variable=var, value=2,command=choose_russian,indicatoron=0,width=20))
    items[-1].pack()
    items.append(Button(window,text=tr['Exit'],command=goto_start,width=20))
    items[-1].pack()

def goto_start():
    del_all()
    global settings,status
    status=''
    settings=0
    items.append(Button(window,text=tr['New model'],command=goto_choose_model,width=20))
    items.append(Button(window,text=tr['New model from file'],command=goto_saved,width=20))
    items.append(Button(window,text=tr['Saved model'],command=goto_saved,width=20))
    items.append(Button(window,text=tr['Theory'],command=goto_theory,width=20))
    items.append(Button(window,text=tr['Language'],command=goto_language,width=20))
    items.append(Button(window,text=tr['Exit'],command=window.destroy,width=20))
    for i in items:
        i.pack()

def goto_saved_model():
    try:
        if file_name.ent.get() in lst:
            file=open(file_name.ent.get()+'.txt' ,'r')
            l=list(file.read().split('\n'))
            file.close()
            global settings
            st=l[0]
            l=l[1:]
            for i in range(len(l)):
                try:
                    l[i]=float(l[i])
                except:
                    pass
            if st=='usual':
                settings=mods(l[0],l[1],l[2],l[3],l[4],l[5])
                goto_model()
            elif st=='horizontal':
                settings=mods(l[0],l[1],l[2],l[3],l[4],l[5])
                goto_hormodel()
            elif st=='vertical':
                settings=vertical_mods(l[0],l[1],l[2],l[3])
                goto_vertical_model()
            elif st=='special':
                settings=special_mods(l[0],l[1],l[2],l[3],l[4],l[5],l[6])
                goto_special_model()
        else:
            messagebox.showinfo(message=tr['There is no such model!'], title=tr['Error!'])
    except:
        pass

def go_back():
    if status=='usual':
        goto_model()
    elif status=='horizontal':
        goto_hormodel()
    elif status=='vertical':
        goto_vertical_model()
    elif status=='special':
        goto_special_model()    

def goto_save():
    settings.update()
    if status!='special':
        settings.calculate()
    del_all()
    global name
    name=my_entry(0,0,tr['Module name'],'')
    items.append(Button(window,text=tr['Save'],command=save))
    items[-1].grid(column=2,row=0)
    items.append(Button(window,text=tr['Back'],command=go_back))
    items[-1].grid(column=3,row=0)

def goto_saved():
    del_all()
    file=open('saved_names_code123123423.txt','r')
    global lst,file_name
    lst=file.readlines()
    file.close()
    for i in range(len(lst)):
        lst[i]=lst[i][:-1]
    file_name=my_entry(0,0,tr['Name:'],'')
    items.append(file_name)
    items.append(Button(window,text=tr['Open'],command=goto_saved_model))
    items[-1].grid(column=2,row=0)
    items.append(Button(window,text=tr['Exit'],command=goto_start))
    items[-1].grid(column=3,row=0)

def make_vertical_model():
    settings.update()
    if settings.enough():
        settings.calculate()
        if settings.correct():
            try:
                inf.config(text='\n'.join(settings.calculate_extra()))
                shift=5
                settings.pull()
                can.delete('all')
                can.create_line(20,0,20,(win_height//2+shift),width=2)
            except:
                messagebox.showinfo(message='Impossible to calculate!', title='Error!')
        else:
            messagebox.showinfo(message='Impossible to calculate!', title='Error!')
    else:
        messagebox.showinfo(message='Not enough data!', title='Error!')

def goto_vertical_model():
    global y0,v0,t_fl,ym,can,inf,direc,settings,status
    status='vertical'
    if settings==0:
        settings=vertical_mods()
    del_all()
    y0=my_entry(0,0,tr['Start height (m):'],settings.y0)
    v0=my_entry(0,1,tr['Start speed (m/s):'],settings.v0)
    t_fl=my_entry(0,2,tr['Time of flight (s):'],settings.t_fl)
    ym=my_entry(0,3,tr['Max height (m):'],settings.ym)
    items.append(Label(window,text=tr['The speed is directed:']))
    items[-1].grid(column=2,row=0)
    direc = Combobox(window,values=(' ',tr['up'],tr['down']))
    direc.current(0)
    direc.grid(column=2,row=1)
    items.append(direc)    
    inf=Label(window,text='')
    inf.grid(column=3,row=0,rowspan=4)
    items.append(inf)
    items.append(Button(window,text=tr['Make model'],command=make_vertical_model,width=14))
    items[-1].grid(column=4,row=0)
    items.append(Button(window,text=tr['Save'],command=goto_save,width=14))
    items[-1].grid(column=4,row=1)
    items.append(Button(window,text=tr['Clear'],command=settings.clear,width=14))
    items[-1].grid(column=4,row=2)
    items.append(Button(window,text=tr['Exit'],command=goto_start,width=14))
    items[-1].grid(column=4,row=3)
    can=Canvas(window,width=win_width,height=win_height//2,bg='white')
    can.grid(column=0,row=4,columnspan=30)
    items.append(can)
    if settings.correct():
        make_vertical_model()

def goto_model():
    global y0,v0,alpha,can,t_fl,xm,ym,inf,direc,settings,status
    if status!='horizontal':
        status='usual'
    if settings==0:
        settings=mods()
    del_all()
    y0=my_entry(0,0,tr['Start height (m):'],settings.y0)
    v0=my_entry(0,1,tr['Start speed (m/s):'],settings.v0)
    alpha=my_entry(0,2,tr['Start angle (rad):'],settings.alpha)
    t_fl=my_entry(0,3,tr['Time of flight (s):'],settings.t_fl)
    xm=my_entry(0,4,tr['Distance (m):'],settings.xm)
    ym=my_entry(0,5,tr['Max height (m):'],settings.ym)
    items.append(Label(window,text=tr['The speed is directed:']))
    items[-1].grid(column=2,row=0)
    direc = Combobox(window,values=(' ',tr['up'],tr['down']))
    direc.current(settings.dire)
    direc.grid(column=2,row=1)
    items.append(direc)
    inf=Label(window,text='')
    inf.grid(column=3,row=0,rowspan=6)
    items.append(inf)
    items.append(Button(window,text=tr['Make model'],command=chart,width=14))
    items[-1].grid(column=4,row=0)
    items.append(Button(window,text=tr['Save'],command=goto_save,width=14))
    items[-1].grid(column=4,row=1)
    items.append(Button(window,text=tr['Clear'],command=settings.clear,width=14))
    items[-1].grid(column=4,row=2)
    items.append(Button(window,text=tr['Exit'],command=goto_start,width=14))
    items[-1].grid(column=4,row=3)
    can=Canvas(window,width=win_width,height=win_height//2,bg='white')
    can.grid(column=0,row=6,columnspan=30)
    items.append(can)
    settings.update()
    if settings.correct():
        chart()

def goto_hormodel():
    goto_model()
    global status
    status='horizontal'
    settings.alpha=pi/2
    alpha.pull('0')
    alpha.ent['state']=DISABLED
    direc.current(1)
    direc['state']=DISABLED

def make_special_model():
    settings.update()
    if settings.correct():
        try:
            shift=5
            can.delete('all')
            x=0
            y=settings.y0+eval(str(settings.R).replace('^','**'))
            vx=settings.v0*cos(settings.alpha)
            vy=settings.v0*sin(settings.alpha)
            R=eval(str(settings.R).replace('^','**'))
            Ra=118000*R/(64*10**5)
            xmx=0
            ymx=y
            xmn=0
            ymn=y
            g1=G*eval(str(settings.M).replace('^','**'))/(x**2+y**2)
            if settings.v0>=(g*R**2/y)**0.5:
                dt=10000000/y
            else:
                dt=(vy+(vy**2+2*g1*settings.y0)**0.5)/g1/1000
                if dt==0:
                    dt=0.01   
            if settings.k!=0:
                ka=(Ra-((x**2+y**2)**0.5-R))/Ra
                dt=min(1/(settings.k*ka*1000),dt)
            f=0
            k=0
            h_max=0
            h_min=y
            v_max=settings.v0
            v_min=settings.v0
            coor=list()
            coor.append(tuple([x,y]))
            x0=x
            while x**2+y**2>=eval(str(settings.R).replace('^','**'))**2 and (settings.k!=0 or f<2) and k<20000:
                if x>xmx:
                    xmx=x
                if x<xmn:
                    xmn=x
                if y>ymx:
                    ymx=y
                if y<ymn:
                    ymn=y
                if x*x0<0:
                    f+=1
                if x**2+y**2>h_max**2:
                    h_max=(x**2+y**2)**0.5
                if x**2+y**2<h_min**2:
                    h_min=(x**2+y**2)**0.5            
                if vx**2+vy**2>v_max**2:
                    v_max=(vx**2+vy**2)**0.5 
                if vx**2+vy**2<v_min**2:
                    v_min=(vx**2+vy**2)**0.5  
                
                if vx>0:
                    kx=1
                else:
                    kx=-1
                if vy>0:
                    ky=1
                else:
                    ky=-1
                ka=(Ra-((x**2+y**2)**0.5-R))/Ra
                if ka<0:
                    ka=0            
                ax=-settings.k*ka*vx**2/settings.m*kx-G*eval(str(settings.M))/(x**2+y**2)*x/(x**2+y**2)**0.5
                ay=-settings.k*ka*vy**2/settings.m*ky-G*eval(str(settings.M))/(x**2+y**2)*y/(x**2+y**2)**0.5
                x0=x
                if ax==0:
                    x+=vx*dt
                else:
                    x+=(2*dt*vx+ax*dt**2)/2
                if ay==0:
                    y+=vy*dt
                else:            
                    y+=(2*dt*vy+ay*dt**2)/2
                vx+=ax*dt
                vy+=ay*dt            
                coor.append(tuple([x,y]))
                k+=1
            if k==20000 and settings.v0<(g*R**2/(R+settings.y0))**0.5*2**0.5:
                messagebox.showinfo(message=tr['Impossible to make correct model!'], title=tr['Error!'])
            else:
                mas=min((win_width-shift)/(xmx-xmn),(win_height/2-shift)/(ymx-ymn))
                x=0
                y=settings.y0+settings.R
                vx=settings.v0*cos(settings.alpha)
                vy=settings.v0*sin(settings.alpha) 
                c0=coor[0]
                cher=(len(coor)+10000)//10000
                if cher==0:
                    cher=1
                for c in range(0,len(coor),cher):
                    can.create_line(-xmn*mas+c0[0]*mas+shift,ymx*mas-c0[1]*mas+shift,-xmn*mas+coor[c][0]*mas+shift,ymx*mas-coor[c][1]*mas+shift,width=2)
                    c0=coor[c]
                c0=coor[-1]
                can.create_line(-xmn*mas+coor[-2][0]*mas+shift,ymx*mas-coor[-2][1]*mas+shift,-xmn*mas+coor[-1][0]*mas+shift,ymx*mas-coor[-1][1]*mas+shift,width=2)
                can.create_oval(-xmn*mas+R*mas+shift,ymx*mas-R*mas+shift,-xmn*mas-R*mas+shift,ymx*mas+R*mas+shift,width=5,fill='blue')
                extra=list()
                extra.append(tr['Max height (m):']+' '+str(round(h_max-R,4)))
                if h_min-R>=0:
                    extra.append(tr['Min height (m):']+' '+str(round(h_min-R,4)))
                else:
                    extra.append(tr['Min height (m):']+' 0')
                extra.append(tr['Max speed (m/s):']+' '+str(round(v_max,4)))
                extra.append(tr['Min speed (m/s):']+' '+str(round(v_min,4)))
                extra.append(tr['Width of model (m):']+' '+str(round(xmx-xmn,4)))
                extra.append(tr['Height of model (m):']+' '+str(round(ymx-ymn,4)))
                inf['text']='\n'.join(extra)
        except:
            messagebox.showinfo(message=tr['Impossible to make correct model!'], title=tr['Error!'])
    else:
        messagebox.showinfo(message='Not enough data!', title='Error!')

def goto_special_model():
    global y0,v0,alpha,can,inf,direc,M,R,inf,m,envir,settings,status
    status='special'
    if settings==0:
        settings=special_mods()    
    del_all()
    y0=my_entry(0,0,tr['Start height (m):'],settings.y0)
    v0=my_entry(0,1,tr['Start speed (m/s):'],settings.v0)
    alpha=my_entry(0,2,tr['Start angle (rad):'],settings.alpha)
    M=my_entry(0,3,tr['Mass of planet (kg):'],settings.M)
    R=my_entry(0,4,tr['Radius of planet (m):'],settings.R)
    m=my_entry(0,5,tr['Mass of body (kg):'],settings.m)
    items.append(Label(window,text=tr['The speed is directed:']))
    items[-1].grid(column=2,row=0)
    direc = Combobox(window,values=(' ',tr['up'],tr['down']))
    direc.current(0)
    direc.grid(column=2,row=1)
    items.append(direc)
    
    items.append(Label(window,text=tr['Environment:']))
    items[-1].grid(column=2,row=3)
    envir = Combobox(window,values=(tr['Vacuum'],tr['Air']))
    envir.current(0)
    envir.grid(column=2,row=4)
    items.append(envir)
    
    inf=Label(window,text='')
    inf.grid(column=3,row=0,rowspan=6)
    items.append(inf)
    items.append(Button(window,text=tr['Make model'],command=make_special_model,width=14))
    items[-1].grid(column=4,row=0)
    items.append(Button(window,text=tr['Save'],command=goto_save,width=14))
    items[-1].grid(column=4,row=1)
    items.append(Button(window,text=tr['Clear'],command=settings.clear,width=14))
    items[-1].grid(column=4,row=2)
    items.append(Button(window,text=tr['Exit'],command=goto_start,width=14))
    items[-1].grid(column=4,row=3)
    can=Canvas(window,width=win_width,height=win_height//2,bg='white')
    can.grid(column=0,row=6,columnspan=30)
    items.append(can)
    settings.pull()
    if settings.correct():
        make_special_model()

def goto_choose_model():
    del_all()
    items.append(Button(window,text=tr['Vertical throw'],command=goto_vertical_model,width=40))
    items[-1].pack()
    items.append(Button(window,text=tr['Horizontal throw'],command=goto_hormodel,width=40))
    items[-1].pack()
    items.append(Button(window,text=tr['Throw at an angle'],command=goto_model,width=40))
    items[-1].pack()
    items.append(Button(window,text=tr['Throw with extra settings'],command=goto_special_model,width=40))
    items[-1].pack()
    items.append(Button(window,text=tr['Exit'],command=goto_start,width=40))
    items[-1].pack()

class my_entry():
    def __init__(self,x,y,text,start):
        self.lab=Label(window,text=text)
        self.lab.grid(column=x*2,row=y)
        self.ent=Entry(window)
        self.ent.grid(column=x*2+1,row=y)
        self.ent.insert(0,start)
        items.append(self.lab)
        items.append(self.ent)

    def get(self):
        try:
            res=float(eval(self.ent.get().replace('^','**')))
        except:
            res=''
        return(res)

    def destroy(self):
        self.lab.destroy()
        self.ent.destroy()

    def pull(self,data):
        self.ent.delete(0,END)
        self.ent.insert(0,str(data))

class special_mods():
    def __init__(self,y0='',v0='',alpha='',M='6*10^24',m='',R='64*10^5',k=''):
        self.y0=y0
        self.v0=v0
        self.alpha=alpha
        self.M=M
        self.R=R
        self.direc=''
        self.m=m
        self.k=k
        
    def update(self):
        try:
            self.y0=y0.get()
            self.v0=v0.get()
            self.alpha=alpha.get()
            self.M=M.get()
            self.R=R.get()
            self.m=m.get()
            if envir.get()==tr['Air']:
                self.k=0.6
            else:
                self.k=0
            self.direc=(direc.get()==tr['up'])*2-1
            if self.alpha!='':
                self.alpha*=self.direc
        except:
            pass
    
    def correct(self):
        k=0
        k+=self.y0==''
        k+=self.v0==''
        k+=self.alpha==''
        k+=self.M==''
        k+=self.R==''
        k+=self.m==''
        k+=self.k==''
        return k==0
    
    def pull(self):
        try:
            y0.pull(self.y0)
            v0.pull(self.v0)
            if self.alpha!='':
                alpha.pull(abs(self.alpha))
            else:
                alpha.pull(self.alpha)
            R.pull(self.R)
            M.pull(self.M)
            m.pull(self.m)
            if v0!='':
                if self.v0<0:
                    direc.current(2)
                else:
                    direc.current(1) 
            if self.k==0:
                envir.current(0)
            else:
                envir.current(1)  
        except:
            pass
    
    def clear(self):
        self.y0=''
        self.v0=''
        self.alpha=''
        self.M=''
        self.R=''
        self.m=''
        goto_special_model()
        
    def setts(self):
        return [self.y0,self.v0,self.alpha,self.M,self.m,self.R,self.k]    
            
class vertical_mods():
    def __init__(self,y0='',v0='',t_fl='',ym=''):
        self.y0=y0
        self.v0=v0
        self.t_fl=t_fl
        self.ym=ym    

    def update(self):
        try:
            self.y0=y0.get()
            self.v0=v0.get()
            self.t_fl=t_fl.get()
            self.ym=ym.get()
            self.direc=(direc.get()==tr['up'])*2-1
            if direc.get()==' ':
                self.v0=''
            elif self.v0!='':
                self.v0*=self.direc
        except:
            pass

    def calculate_extra(self):
        try:
            inf=list()
            if self.v0>=0:
                inf.append(tr['Time of max height (s):']+' '+str(round(self.v0/g,4)))
            else:
                inf.append(tr['Time of max height (s):']+' 0')
            inf.append(tr['Max speed (in the end of flight) (m/s):']+' '+str(round((self.y0*g+self.v0**2/2)**0.5,4)))
            inf.append(tr['Height of model (m):']+' '+str(round(self.ym,4)))        
            return(inf)
        except:
            pass

    '''def get(self,file):
        global lst
        if file_name.ent.get() in lst:
            file=open(file_name.ent.get()+'.txt','r')
            l=file.readlines()
            for i in range(len(l)-1):
                l[i]=l[i][:-1]
            self.y0=l[0]
            self.v0=l[1]
            self.t_fl=l[2]
            self.ym=l[3]'''

    def setts(self):
        return [self.y0,self.v0,self.t_fl,self.ym]
    
    def enough(self):
        k=0
        k+=self.y0==''
        k+=self.v0==''
        k+=self.t_fl==''
        k+=self.ym==''
        return k<=2

    def right(self):
        try:
            f=abs(self.y0+self.v0*self.t_fl-g*self.t_fl**2/2)<=(self.y0+1)/1000
            f=f and (abs(self.ym-self.y0-(self.v0)**2/(2*g))<=(self.ym+1)/1000 or (self.v0<0 and self.ym==self.y0))
            return f
        except:
            return False
    
    def correct(self):
        k=0
        k+=self.y0==''
        k+=self.v0==''
        k+=self.t_fl==''
        k+=self.ym==''
        return k==0 and self.right()

    def pull(self):
        try:
            y0.pull(self.y0)
            if self.v0!='':
                v0.pull(abs(self.v0))
            else:
                v0.pull(self.v0)
            t_fl.pull(self.t_fl)
            ym.pull(self.ym)
            if self.v0<0:
                direc.current(2)
            else:
                direc.current(1)
        except:
            pass

    def clear(self):
        self.y0=''
        self.v0=''
        self.t_fl=''
        self.ym=''
        #self.pull()
        goto_vertical_model()

    def calculate(self):
        y0=self.y0
        v0=self.v0
        t_fl=self.t_fl
        ym=self.ym
        try:
            if self.y0=='' and self.v0=='':
                self.v0=(self.t_fl+(2*self.ym/g)**0.5)*g
                self.y0=self.ym-self.v0**2/(2*g)
            elif self.y0=='' and self.t_fl=='':
                self.y0=self.ym-self.v0**2/(2*g)
                self.t_fl=(self.v0+(self.v0**2+2*self.y0*g)**0.5)/g
            elif self.y0=='' and self.ym=='':
                self.y0=g*self.t_fl**2/2-self.t_fl*self.v0
                self.ym=self.y0+self.v0**2/(2*g)
            elif self.v0=='' and self.t_fl=='':
                self.v0=(2*g*(self.ym-self.y0))**0.5
                self.t_fl=(self.v0+(self.v0**2+2*self.y0*g)**0.5)/g
            elif self.v0=='' and self.ym=='':
                self.v0=(g*self.t_fl**2/2-self.y0)/self.t_fl
                self.ym=self.y0+self.v0**2/(2*g)
            elif self.t_fl=='' and self.ym=='':
                self.ym=self.y0+self.v0**2/(2*g)
                self.t_fl=(self.v0+(self.v0**2+2*self.y0*g)**0.5)/g
            elif self.y0=='':
                self.y0=self.ym-self.v0**2/(2*g)
            elif self.v0=='':
                self.v0=(g*self.t_fl**2/2-self.y0)/self.t_fl
            elif self.t_fl=='':
                self.t_fl=(self.v0+(self.v0**2+2*self.y0*g)**0.5)/g
            elif self.ym=='':
                self.ym=self.yo+self.v0**2/(2*g)
            if self.ym!='' and self.v0!='' and self.v0<0 and self.y0!='' and self.t_fl!='':
                self.ym=self.y0            
        except:
            pass
        if not self.correct():
            self.y0=y0
            self.v0=v0
            self.t_fl=t_fl
            self.ym=ym

class mods():
    def __init__(self,y0='',v0='',alpha='',t_fl='',xm='',ym=''):
        self.y0=y0
        self.v0=v0
        self.alpha=alpha
        self.t_fl=t_fl
        self.ym=ym
        self.xm=xm
        if self.v0=='':
            self.dire=0
        elif self.v0>=0:
            self.dire=1
        else:
            self.dire=2

    def update(self):
        try:
            self.y0=y0.get()
            self.v0=v0.get()
            self.alpha=alpha.get()
            self.t_fl=t_fl.get()
            self.xm=xm.get()
            self.ym=ym.get()
            self.direc=(direc.get()==tr['up'])*2-1
            if self.alpha!='':
                self.alpha*=self.direc
        except:
            pass

    def calculate_extra(self):
        try:
            inf=list()
            if self.v0*sin(self.alpha)/g>=0:
                inf.append(tr['Time of max height (s):']+' '+str(round(self.v0*sin(self.alpha)/g,4)))
            else:
                inf.append(tr['Time of max height (s):']+' 0')        
            inf.append(tr['Angle in the end of flight (rad):']+' '+str(round(atan(-(self.v0*sin(self.alpha)-g*self.t_fl)/(self.v0*cos(self.alpha))),4)))
            inf.append(tr['Max speed (in the end of flight) (m/s):']+' '+str(round((self.y0*g+self.v0**2/2)**0.5,4)))
            inf.append(tr['Min speed (at max height) (m/s):']+' '+str(round(self.v0*cos(self.alpha),4)))
            inf.append(tr['Motion (m):']+' '+str(round((self.y0**2+self.xm**2)**0.5,4)))
            inf.append(tr['Width of model (m):']+' '+str(round(self.xm,4)))
            inf.append(tr['Height of model (m):']+' '+str(round(self.ym,4)))
            return(inf)
        except:
            pass

    def setts(self):
        return [self.y0,self.v0,self.alpha,self.t_fl,self.xm,self.ym]
    
    def enough(self):
        k=0
        k+=self.y0==''
        k+=self.v0==''
        k+=self.alpha==''
        k+=self.t_fl==''
        k+=self.xm==''
        k+=self.ym==''
        return k<=3

    def right(self):
        try:
            f=abs(self.xm-self.v0*self.t_fl*cos(self.alpha))<=(self.xm+1)/1000
            f=f and abs(self.y0+self.v0*sin(self.alpha)*self.t_fl-g*self.t_fl**2/2)<=(self.y0+1)/1000
            f=f and abs(self.ym-self.y0-(self.v0*sin(self.alpha))**2/(2*g))<=(self.ym+1)/1000
            return f
        except:
            return False
    
    def correct(self):
        k=0
        k+=self.y0==''
        k+=self.v0==''
        k+=self.alpha=='' or self.direc==''
        k+=self.t_fl==''
        k+=self.xm==''
        k+=self.ym==''
        return k==0 and self.right()

    def pull(self):
        try:
            y0.pull(self.y0)
            v0.pull(self.v0)
            if self.alpha!='':
                alpha.pull(abs(self.alpha))
            else:
                alpha.pull(self.alpha)
            t_fl.pull(self.t_fl)
            xm.pull(self.xm)
            ym.pull(self.ym)
            if self.alpha<0:
                direc.current(2)
            else:
                direc.current(1)
        except:
            pass

    def clear(self):
        self.y0=''
        self.v0=''
        self.alpha=''
        self.t_fl=''
        self.ym=''
        self.xm=''
        #self.pull()
        if alpha.ent['state']==DISABLED:
            goto_hormodel()
        else:
            goto_model()

    def calculate(self):
        y0=self.y0
        v0=self.v0
        alpha=self.alpha
        t_fl=self.t_fl
        ym=self.ym
        xm=self.xm
        try:
            if self.y0=='' and self.v0=='' and self.alpha=='':
                self.y0=(2*self.ym*self.t_fl**2*g)**0.5-g*self.t_fl**2/2
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
                self.v0=(g*self.t_fl**2/2-self.y0)/(self.t_fl*sin(self.alpha))
            elif self.y0=='' and self.v0=='' and self.t_fl=='':
                self.v0=((self.ym+self.xm*tan(self.alpha)+(self.ym**2+2*self.ym*self.xm*tan(self.alpha))**0.5)*g/sin(self.alpha)**2)**0.5
                self.t_fl=self.xm/(self.v0*cos(self.alpha))
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
            elif self.y0=='' and self.v0=='' and self.xm=='':
                self.v0=(self.t_fl-(2*self.ym/g)**0.5)/sin(self.alpha)*g
                self.y0=self.ym-(self.v0*sin(self.alpha))**2/(2*g)
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.y0=='' and self.v0=='' and self.ym=='':
                self.v0=self.xm/(cos(self.alpha)*self.t_fl)
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.y0=='' and self.alpha=='' and self.t_fl=='':
                '''self.y0=
                self.alpha=
                self.t_fl='''
                pass
            elif self.y0=='' and self.alpha=='' and self.xm=='':
                self.alpha=asin(((2*g*self.ym)**0.5+g*self.t_fl)/self.v0)
                self.xm=self.v0*cos(self.alpha)*self.t_fl
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
            elif self.y0=='' and self.alpha=='' and self.ym=='':
                self.alpha=acos(self.xm/(self.v0*self.t_fl))
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.y0=='' and self.t_fl=='' and self.xm=='':
                self.y0=self.ym-(self.v0*sin(self.alpha))**2/(2*g)
                self.t_fl=(self.v0*sin(self.alpha)+((self.v0*sin(self.alpha))**2+2*self.y0*g)**0.5)/g
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.y0=='' and self.t_fl=='' and self.ym=='':
                self.t_fl=self.xm/(self.v0*cos(self.alpha))
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.y0=='' and self.xm=='' and self.ym=='':
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
                self.xm=self.v0*cos(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.v0=='' and self.alpha=='' and self.t_fl=='':
                self.t_fl=2**0.5*((self.ym-self.y0)**0.5+self.ym**0.5)/g**0.5
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
                self.v0=self.xm/(cos(self.alpha)*self.t_fl)
            elif self.v0=='' and self.alpha=='' and self.xm=='':
                #Impossible to calculate
                pass
            elif self.v0=='' and self.alpha=='' and self.ym=='':
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
                self.v0=self.xm/(cos(self.alpha)*self.t_fl)
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.v0=='' and self.t_fl=='' and self.xm=='':
                self.v0=((self.ym-self.y0)*2*g)**0.5/sin(self.alpha)
                self.t_fl=(self.v0*sin(self.alpha)+((self.v0*sin(self.alpha))**2+2*self.y0*g)**0.5)/g
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.v0=='' and self.t_fl=='' and self.ym=='':
                self.t_fl=(self.xm*tan(self.alpha)+((self.xm*tan(self.alpha))**2+2*self.y0*g)**0.5)/g
                self.v0=self.xm/(cos(self.alpha)*self.t_fl)
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.v0=='' and self.xm=='' and self.ym=='':
                self.v0=(g*self.t_fl**2/2-self.y0)/(self.t_fl*sin(self.alpha))
                self.xm=self.v0*cos(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.alpha=='' and self.t_fl=='' and self.xm=='':
                self.alpha=asin((2*g*(self.ym-self.y0))**0.5/self.v0)
                self.t_fl=(self.v0*sin(self.alpha)+((self.v0*sin(self.alpha))**2+2*self.y0*g)**0.5)/g
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.alpha=='' and self.t_fl=='' and self.ym=='':
                self.t_fl=(2*(g*self.y0+self.v0**2+((g*self.y0+self.v0**2)**2-g**2*(self.xm**2+self.y0**2))**0.5)/g**2)**0.5
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.alpha=='' and self.xm=='' and self.ym=='':
                self.alpha=asin((g*self.t_fl**2/2-self.y0)/(self.v0*self.t_fl))
                self.xm=self.v0*cos(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.t_fl=='' and self.xm=='' and self.ym=='':
                self.t_fl=(self.v0*sin(self.alpha)+((self.v0*sin(self.alpha))**2+2*self.y0*g)**0.5)/g
                self.xm=self.v0*cos(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha))**2/(2*g)
            elif self.y0=='' and self.v0=='':
                self.y0=(2*self.ym*self.t_fl**2*g)**0.5-g*self.t_fl**2/2
                self.v0=self.xm/(cos(self.alpha)*self.t_fl)
            elif self.y0=='' and self.alpha=='':
                self.alpha=asin(((2*g*self.ym)**0.5+g*self.t_fl)/self.v0)
                self.y0=(2*self.ym*self.t_fl**2*g)**0.5-g*self.t_fl**2/2
            elif self.y0=='' and self.t_fl=='':
                self.t_fl=self.xm/(self.v0*cos(self.alpha))
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
            elif self.y0=='' and self.xm=='':
                self.y0=self.ym-(self.v0*sin(self.alpha))**2/(2*g)
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.y0=='' and self.ym=='':
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.v0=='' and self.alpha=='':
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
                self.v0=self.xm/(cos(self.alpha)*self.t_fl)
            elif self.v0=='' and self.t_fl=='':
                self.v0=((self.ym-self.y0)*2*g)**0.5/sin(self.alpha)
                self.t_fl=(self.v0*sin(self.alpha)+((self.v0*sin(self.alpha))**2+2*self.y0*g)**0.5)/g
            elif self.v0=='' and self.xm=='':
                self.v0=(g*self.t_fl**2/2-self.y0)/(self.t_fl*sin(self.alpha))
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.v0=='' and self.ym=='':
                self.v0=(g*self.t_fl**2/2-self.y0)/(self.t_fl*sin(self.alpha))
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.alpha=='' and self.t_fl=='':
                self.t_fl=(2*(g*self.y0+self.v0**2+((g*self.y0+self.v0**2)**2-(g*self.xm))**0.5)/g)**0.5
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
            elif self.alpha=='' and self.xm=='':
                self.alpha=asin((2*g*(self.ym-self.y0))**0.5/self.v0)
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.alpha=='' and self.ym=='':
                self.alpha=atan((g*self.t_fl**2/2-self.y0)/self.xm)
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.t_fl=='' and self.xm=='':
                self.t_fl=(self.v0*sin(self.alpha)+((self.v0*sin(self.alpha))**2+2*self.y0*g)**0.5)/g
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.t_fl=='' and self.ym=='':
                self.t_fl=(2*(g*self.y0+self.v0**2+((g*self.y0+self.v0**2)**2-(g*self.xm))**0.5)/g)**0.5
                self.ym=self.y0+(self.v0*sin(self.alpha)**2/(2*g))
            elif self.xm=='' and self.ym=='':
                self.xm=self.v0*cos(self.alpha)*self.t_fl
                self.ym=self.y0+(self.v0*sin(self.alpha))**2/(2*g)
            elif self.y0=='':
                self.y0=g*self.t_fl**2/2-self.v0*sin(self.alpha)*self.t_fl
            elif self.v0=='':
                self.v0=(g*self.t_fl**2/2-self.y0)/(self.t_fl*sin(self.alpha))
            elif self.alpha=='':
                self.alpha=asin((2*g*(self.ym-self.y0))**0.5/self.v0)
            elif self.t_fl=='':
                self.t_fl=(2*(g*self.y0+self.v0**2+((g*self.y0+self.v0**2)**2-(g*self.xm))**0.5)/g)**0.5
            elif self.xm=='':
                self.xm=self.v0*cos(self.alpha)*self.t_fl
            elif self.ym=='':
                self.ym=self.y0+(self.v0*sin(self.alpha))**2/(2*g)
        except:
            pass
        if not self.correct():
            self.y0=y0
            self.v0=v0
            self.alpha=alpha
            self.t_fl=t_fl
            self.ym=ym
            self.xm=xm
        
            

items=list()
settings=0
g=9.8
G=6.67/10**11

window=Tk()
window.title('Body throw model')
win_height=window.winfo_screenheight()
win_width=window.winfo_screenwidth()
win_size=str(win_width)+'x'+str(win_height)+'+0+0'
window.geometry(win_size)
#window.attributes('-fullscreen', True)
window.state('zoomed')

leng='rus'
rus=list()
eng=list()
file=open('translation.txt','r',encoding='utf8')
for i in file.readlines():
    en,rs=i.split('-')
    if rs[-1]=='\n':
        rs=rs[:-1]
    rus.append(rs)
    eng.append(en)
choose_russian()

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=int(18*(win_width/1920)))
window.option_add('*Font', default_font) 

goto_start()

window.mainloop()
