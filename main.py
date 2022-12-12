from ast import Global
from tkinter import *
import time
from tkinter import font
from PIL import ImageTk,Image
import pymongo
from functools import partial
from subprocess import call
import os
from tkinter import messagebox

localtime = time.asctime( time.localtime(time.time()) )

monogoconnection  = pymongo.MongoClient("mongodb://localhost:27017")
monogodbase = monogoconnection["restaurent_test"]
monogocollection1 = monogodbase["test1"]
monogocollection2 = monogodbase["login"]
monogocollection3 = monogodbase["menu"]
monogocollection4 = monogodbase["staff"]

win=Tk()
win.geometry("1600x800+0+0")
win.tk.call('wm', 'iconphoto', win._w, PhotoImage(file='food_o_clock.png'))
win.title("RESTAURENT MAIN PAGE")
path="Food_o_Clock-main-page1.png"
img = ImageTk.PhotoImage(Image.open(path))
photo_label=Label(win,image=img)
photo_label.pack(expand="yes")


def staff_d():
        def get2():
            pr=monogocollection4.find()
            for items in pr:
                idprint = items['staff_id']
                nameprint = items['staff_name']
                phnprint = items['phn']
                print(idprint,phnprint,nameprint)
                total_staff.insert(END,'\n__________\n')
                total_staff.insert(END,'\n')
                total_staff.insert(END,'Staff Name          = ')
                total_staff.insert(END,nameprint)
                total_staff.insert(END,'\n')
                total_staff.insert(END,'Staff ID   = ')
                total_staff.insert(END,idprint)
                total_staff.insert(END,'\n')
                total_staff.insert(END,'Phn  = ')
                total_staff.insert(END,phnprint)
                total_staff.insert(END,'\n')

        sr=Toplevel()
        sr.geometry("800x450")
        sr.configure(bg='LightSkyBlue2')
        sr.title("Staff Details") 
        #details_label=Label(cd,width=70,height=30).place(x=10,y=10)
        
        total_staff=Text(sr,font=('arial',12,'bold'),bd=3,width=75,height=14)
        total_staff.pack()
        get_staff=Button(sr,text='get details',command=get2).place(x=390,y=390)
        sr.mainloop()



def staff_write():
    def sinsert():
        def insert_staff(id,s_name,phn):
            data = { "staff_id": id.get() , "staff_name": s_name.get(),"phn":phn.get()}
            monogocollection4.insert_one(data)
            messagebox.showinfo("information","Insertion Sucessfull")
        id=StringVar()
        s_name=StringVar()
        phn=StringVar()
        id_label=Label(sw,text='Enter Staff ID',width=15,height=1).place(x=200,y=200) 
        name_label=Label(sw,text='Enter Name',width=15,height=1).place(x=200,y=250) 
        phn_label=Label(sw,text='Enter Phn',width=15,height=1).place(x=200,y=300) 
        id_entry=Entry(sw,textvariable=id).place(x=320,y=200)
        name_entry=Entry(sw,textvariable=s_name).place(x=320,y=250)
        phn_entry=Entry(sw,textvariable=phn).place(x=320,y=300)
        insert_partial=partial(insert_staff,id,s_name,phn)
        insert_button=Button(sw,text='Insert Staff',command=insert_partial).place(x=250,y=350)

    def supdate():
        def update_staff(id,ophn,nphn):
            id=id.get()
            ophn=ophn.get()
            nphn=nphn.get()
            x=monogocollection4.find_one({'staff_id': id},{'_id': 0,'phn' : 1})
            y = x['phn']
            prev={'staff_id':id}
            nextt={'$set':{"phn":nphn}}
            if(y==ophn):
                monogocollection4.update_one(prev,nextt)
                messagebox.showinfo("information","updation sucessfull")
   
            else:
                messagebox.showerror( 'Error','phn no does not match')

        id=StringVar()
        ophn=StringVar()
        nphn=StringVar()
        id_label=Label(sw,text='Enter Staff ID',width=15,height=1).place(x=200,y=200) 
        ophn_label=Label(sw,text='Enter old phn no',width=15,height=1).place(x=200,y=250) 
        nphn_label=Label(sw,text='Enter new Phn no',width=15,height=1).place(x=200,y=300) 
        id_entry=Entry(sw,textvariable=id).place(x=320,y=200)
        ophn_entry=Entry(sw,textvariable=ophn).place(x=320,y=250)
        nphn_entry=Entry(sw,textvariable=nphn).place(x=320,y=300)
        update_partial=partial(update_staff,id,ophn,nphn)
        update_button=Button(sw,text='Update Staff',command=update_partial).place(x=250,y=350)

    def sdelete():
        def delete_staff(id,phn):
            id=id.get()
            phn=phn.get()
            x=monogocollection4.find_one({'staff_id': id},{'_id': 0,'phn' : 1})
            y = x['phn']
            rec={'staff_id':id}
            if(y==phn):
                monogocollection4.delete_one(rec)
                messagebox.showinfo("information","Deletion Sucessfull")
            else:
                messagebox.showerror( 'Error','WRONG Crendials')
        id=StringVar()
        phn=StringVar()
        id_label=Label(sw,text='Enter Staff ID',width=15,height=1).place(x=200,y=200) 
        phn_label=Label(sw,text='Enter Phn',width=15,height=1).place(x=200,y=300) 
        id_entry=Entry(sw,textvariable=id).place(x=320,y=200)
        phn_entry=Entry(sw,textvariable=phn).place(x=320,y=300)
        delete_partial=partial(delete_staff,id,phn)
        delete_button=Button(sw,text='Delete Staff',command=delete_partial).place(x=250,y=350)    


    sw=Toplevel()
    sw.geometry("800x450")
    path1="func.png"
    img2 = ImageTk.PhotoImage(Image.open(path1))
    photo_label1=Label(sw,image=img2)
    photo_label1.pack(expand="yes") 
    sw.title('staff editing')
    sw_insert=Button(sw,text='Insert',command=sinsert).place(x=100,y=25)
    sw_delete=Button(sw,text='Update',command=supdate).place(x=400,y=25)
    sw_insert=Button(sw,text='Delete',command=sdelete).place(x=700,y=25)
    sw.mainloop()

  


def aman():
    def a_add():
        def insert_admin(admin,password):
            data = { "admin_id": admin.get() , "password": password.get()}
            monogocollection2.insert_one(data)
            messagebox.showinfo("information","Insertion Sucessfull")
        admin=StringVar()
        password=StringVar()
        a_label=Label(ad,text='Enter admin id',width=15,height=1).place(x=200,y=200) 
        p_label=Label(ad,text='Enter password',width=15,height=1).place(x=200,y=250)  
        a_entry=Entry(ad,textvariable=admin).place(x=300,y=200)
        p_entry=Entry(ad,textvariable=password).place(x=300,y=250)
        insert_partial=partial(insert_admin,admin,password)
        insert_button=Button(ad,text='Insert Admin',command=insert_partial).place(x=250,y=350)
    def a_del():
        def delete_admin(admin,password):
            admin=admin.get()
            password=password.get()
            x=monogocollection2.find_one({'admin_id': admin},{'_id': 0,'password' : 1})
            y = x['password']
            rec={'admin_id':admin}
            if(y==password):
                monogocollection2.delete_one(rec)
                messagebox.showinfo("information","Deletion Sucessfull")
            else:
                messagebox.showerror( 'Error','WRONG PASSWORD')
        admin=StringVar()
        password=StringVar()
        a_label=Label(ad,text='Enter admin id',width=15,height=1).place(x=200,y=200) 
        p_label=Label(ad,text='Enter password',width=15,height=1).place(x=200,y=250)  
        a_entry=Entry(ad,textvariable=admin).place(x=300,y=200)
        p_entry=Entry(ad,textvariable=password).place(x=300,y=250)
        delete_partial=partial(delete_admin,admin,password)
        delete_button=Button(ad,text='Delete Password',command=delete_partial).place(x=250,y=350)  
    def a_update():
        def update_pass(admin,password,np):
            admin=admin.get()
            password=password.get()
            np=np.get()
            x=monogocollection2.find_one({'admin_id': admin},{'_id': 0,'password' : 1})
            y = x['password']
            prev={'admin_id':admin}
            nextt={'$set':{"password":np}}
            if(y==password):
                monogocollection2.update_one(prev,nextt)
                messagebox.showinfo("information","updation sucessfull")

            else:
                messagebox.showerror( 'Error','WRONG PASSWORD') 

        admin=StringVar()
        password=StringVar()
        np=StringVar()
        a_label=Label(ad,text='Enter admin id',width=15,height=1).place(x=200,y=200) 
        p_label=Label(ad,text='Enter old password',width=15,height=1).place(x=200,y=250) 
        np_label=Label(ad,text='Enter new password',width=15,height=1).place(x=200,y=300) 
        a_entry=Entry(ad,textvariable=admin).place(x=320,y=200)
        p_entry=Entry(ad,textvariable=password).place(x=320,y=250)
        np_entry=Entry(ad,textvariable=np).place(x=320,y=300)
        update_partial=partial(update_pass,admin,password,np)
        update_button=Button(ad,text='Update password',command=update_partial).place(x=250,y=350)

    ad=Toplevel()
    ad.geometry("800x450")
    ad.title("ADMIN DETAILS") 
    path1="func.png"
    img2 = ImageTk.PhotoImage(Image.open(path1))
    photo_label1=Label(ad,image=img2)
    photo_label1.pack(expand="yes") 
    update_pass=Button(ad,text='Password Upadate',command=a_update).place(x=100,y=20)
    add_admin=Button(ad,text='Add Admin',command=a_add).place(x=300,y=20)
    del_admin=Button(ad,text='Del Admin',command=a_del).place(x=500,y=20)
    ad.mainloop()

def totalsales():
    def get1():
        pr=monogocollection3.find()
        for items in pr:
            phn = items['phn']
            foodprint = items['priceoffood']
            cakeprint = items['priceofcakes']
            drinkprint=items['priceofdrinks']
            totalprint=items['subtotal']
            total_text.insert(END,'\n__________\n')
            total_text.insert(END,'\n')
            total_text.insert(END,'phn= ')
            total_text.insert(END,phn)
            total_text.insert(END,'\n')
            total_text.insert(END,' Price of food  = ')
            total_text.insert(END,foodprint)
            total_text.insert(END,'\n')
            total_text.insert(END,' Price of cakes  = ')
            total_text.insert(END,cakeprint)
            total_text.insert(END,'\n')
            total_text.insert(END,' Price of Drinks  = ')
            total_text.insert(END,drinkprint)
            total_text.insert(END,'\n')
            total_text.insert(END,' Subtotal  = ')
            total_text.insert(END,totalprint)
            total_text.insert(END,'\n')

    to=Toplevel()
    to.geometry("800x450")
    to.title("Customer Details") 
    to.configure(bg='LightSkyBlue2')
    #details_label=Label(cd,width=70,height=30).place(x=10,y=10)
    total_text=Text(to,font=('arial',12,'bold'),bd=3,width=75,height=14)
    total_text.pack()
    get_total_sales=Button(to,text='get details',command=get1).place(x=390,y=390)
    to.mainloop()

def customer_detalis():
    def get():
        #details_label=Label(cd,width=70,height=30).place(x=10,y=10)
        pr=monogocollection1.find()
        for items in pr:
            nameprint = items['NAME']
            tableprint = items['TABLE_NO']
            phnprint = items['PHN_NO']
            gmailprint=items['GMAIL']
            print(nameprint,tableprint,phnprint,gmailprint)
            details_text.insert(END,'\n__________\n')
            details_text.insert(END,'\n')
            details_text.insert(END,'NAME = ')
            details_text.insert(END,nameprint)
            details_text.insert(END,'\n')
            details_text.insert(END,'TABLE NO = ')
            details_text.insert(END,tableprint)
            details_text.insert(END,'\n')
            details_text.insert(END,'PHN NO = ')
            details_text.insert(END,phnprint)
            details_text.insert(END,'\n')
            details_text.insert(END,'GMAIL = ')
            details_text.insert(END,gmailprint)


    cd=Toplevel()
    cd.geometry("800x450")
    cd.title("Customer Details")
    cd.configure(bg='LightSkyBlue2')
    #details_label=Label(cd,width=70,height=30).place(x=10,y=10)
    details_text=Text(cd,font=('arial',12,'bold'),bd=3,width=75,height=14)
    details_text.pack()
    get_details=Button(cd,text='get details',command=get).place(x=390,y=390)
    cd.mainloop()
    

def login(e_id,e_pass):
    id=e_id.get()
    print(id)
    x=monogocollection2.find_one({'admin_id': id},{'_id': 0,'password' : 1})
    y = x['password']
    print(y)
    epass=e_pass.get()
    if(epass==y):
       print('yes')
       y=Toplevel()
       y.geometry("800x450")
       y.title("ADMIN PAGE")
       path1="admin_theme1.jpg"
       img2 = ImageTk.PhotoImage(Image.open(path1))
       photo_label1=Label(y,image=img2)
       photo_label1.pack(expand="yes")
       b_admin_man=Button(y,text='ADMIN MANGEMENT',fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=aman).place(x=450,y=70)
       b_staff_details=Button(y,text='STAFF DETAILS',fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=staff_d).place(x=450,y=140)
       b_staff_man=Button(y,text='STAFF MANGEMENT',fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=staff_write).place(x=450,y=210)
       total_sales=Button(y,text='TOTAL SALES',fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=totalsales).place(x=450,y=280)
       b_customer_detalis=Button(y,text='CUSTOMER DETAILS',fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=customer_detalis).place(x=450,y=350)
       path1="food_o_clock.png"
       img1 = ImageTk.PhotoImage(Image.open(path1))
       photo_label2=Label(y,image=img1).place(x=50,y=50)

       y.mainloop()
    else:
        print('no')
        messagebox.showerror( 'Error','WRONG PASSWORD')    

    
def admin_page():
    #win.quit()
    a=Toplevel()
    a.geometry("1600x800+0+0")
    a.title("ADMIN LOGIN PAGE") 
    path4="admin_page.png"
    img2 = ImageTk.PhotoImage(Image.open(path4))
    photo_label1=Label(a,image=img2)
    photo_label1.pack(expand="yes")
    e_id=StringVar()
    e_pass=StringVar()
    admin_id_label=Label(a,text='ADMIN ID',width=9,height=1).place(x=190,y=160) 
    admin_entry=Entry(a,font=('Arial', 14),textvariable=e_id).place(x=280,y=160)
    pass_label=Label(a,text='PASSWORD',width=9,height=1).place(x=190,y=200)
    pass_entry=Entry(a,show='*', font=('Arial', 14),textvariable=e_pass).place(x=280,y=200)
    login_partial=partial(login,e_id,e_pass)
    login_button=Button(a,text="LOGIN",fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=login_partial).place(x=295,y=270)
    
    a.mainloop()

def insert(name_entry,table_entry,phn_entry,gmail_entry):
    
    #insertion of primary details
    data = { "NAME": name_entry.get() , "TABLE_NO": table_entry.get(),"PHN_NO":phn_entry.get(),"GMAIL":gmail_entry.get()}
    monogocollection1.insert_one(data)

    #path='E:\projects\database\diff\menu.py'
    #call(["Python3","{}".format(path)])    
    
def next():    
    os.system('python new_menu.py')
    #import new_menu
    #exec(open("E:\\projects\\database\\diff\\new_menu.py").read())
    #subprocess.call('E:\\projects\\database\\diff\\menu.py',shell=True )
    
    



def user_login_page():
    #user login page
    #win.quit()
    u=Toplevel()
    
    u.geometry("800x450")
    u.title("USER PAGE")  
    path1="food_user.jpg"
    img1 = ImageTk.PhotoImage(Image.open(path1))
    photo_label1=Label(u,image=img1)
    photo_label1.pack(expand="yes")
    u.resizable(0,0)
    
    #varibles for details
    name_tv = StringVar()
    phn_tv=StringVar()
    gmail_tv=StringVar()
    table_tv=StringVar()
    
    #entry and labels for detalis
    welcome_label=Label(u,text="welcome to FOOD O CLOCK restaurent",font=('arial',25,'bold'),background='#FCFCFC').place(x=100,y=20)
    name_label=Label(u,text="NAME").place(x=250,y=150)
    name_entry=Entry(u,textvariable=name_tv).place(x=320,y=150)
    table_lable=Label(u,text='TABLE NO').place(x=250,y=200)
    table_entry=Entry(u,textvariable=table_tv).place(x=320,y=200)
    phn_label=Label(u,text="PHN_NO").place(x=250,y=250)
    phn_entry=Entry(u,textvariable=phn_tv).place(x=320,y=250)
    gmail_lable=Label(u,text="G-MAIL").place(x=250,y=300)
    gmail_entry=Entry(u,textvariable=gmail_tv).place(x=320,y=300)

    insert_partial=partial(insert,name_tv,table_tv,phn_tv,gmail_tv)
    save_button=Button(u,text="SAVE",fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=insert_partial).place(x=300,y=350)
    menu_button=Button(u,text="MENU",fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=next).place(x=650,y=400)
    u.mainloop()


time_label=Label(win,text=localtime,bg='black',fg='white').place(x=59 ,y=0)
user_button=Button(text="For Foodie",fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=user_login_page).place(x=1400,y=20)
admin_button=Button(text="For Admin",fg='black',pady=8,activeforeground='red',activebackground="pink",padx=15,command=admin_page).place(x=1300,y=20)

win.mainloop()