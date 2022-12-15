from audioop import reverse
import json
from django.http  import JsonResponse,HttpRequest
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import *
import re,os
from django.db.models import Q
from django.core.mail import send_mail


def User_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        First_Name_r         = data['first_name']
        Last_Name_r          = data['last_name']
        Username_r           = data['username']
        DOB_r                = data['DOB']
        Email_r              = data['email']
        Password_r           = data['password']
        C_Password_r         = data['C_password']
        Mobile_Number_r      = data['Mobile_Number']
        Gender_r             = data['Gender']

        email_condition  = "[a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,3}$"
        number_condition = "[1-9]{1}[0-9]{9}$"
        password_condition = "[a-zA-Z0-9]{2,}[!@#$%^&*_+=/]{1,}[a-zA-Z0-9]{1,}$"
        match   = re.search(email_condition,Email_r)
        match1  = re.search(number_condition,str(Mobile_Number_r))
        match2  = re.search(password_condition,Password_r)

        if (not First_Name_r):
            mes = {'message': 'First Name Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Last_Name_r):
            mes = {'message': 'Last Name Required !'}
            return JsonResponse(mes,status=403,safe=False) 

        if (not Username_r):
            mes = {   'message': 'Username Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (User.objects.filter(username = data['username'])):
            mes = {   'message': 'Username Already Exists !'}
            return JsonResponse(mes,status=403,safe=False)    

        if (not DOB_r):
            mes = { 'message': 'DOB Required !'}
            return JsonResponse(mes,status=403,safe=False)       

        if (not Email_r):
            mes = {  'message': 'Email Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not match):
            mes = { 'message': 'Invalid Email !'}
            return JsonResponse(mes,status=403,safe=False)

        if (User.objects.filter(email = data['email'])):
            mes = { 'message': 'Email Already Exists !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Mobile_Number_r):
            mes = { 'message': 'Mobile Number Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not match1):
            mes = { 'message': 'Invalid Mobile Number !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Gender_r):
            mes = {  'message': 'Gender Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Password_r):
            mes = { 'message': 'Password Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not match2):
            mes = { 'message': 'Invalid Password Format !'}
            return JsonResponse(mes,status=403,safe=False)

        if (len(Password_r) <=8):
            mes = { 'message': 'Password must be atlesast 8 digit long !'}
            return JsonResponse(mes,status=403,safe=False)

        if (not C_Password_r):
            mes = { 'message': 'Confirm Password Required !'}
            return JsonResponse(mes,status=403,safe=False)    

        if (Password_r != C_Password_r):
            mes = {  'message': 'Password do not Match !'}
            return JsonResponse(mes,status=403,safe=False) 
                
        else:
            useR = User.objects.create_user(username=Username_r, password=Password_r, first_name=First_Name_r, last_name=Last_Name_r, email=Email_r)   
            new_user = User_data(user=useR, DOB=DOB_r, Mobile_Number=Mobile_Number_r, Gender=Gender_r)
            new_user.save()
            
            mes = { 'message': 'User Registered Successfully !'}
            return JsonResponse(mes,status=200,safe=False)
           


def User_login(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        Username_l = data['username']
        Password_l = data['password']
        if (not Username_l):
            mes = {  'message': 'Username/Email Required!!'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Password_l):
            mes = { 'message': 'Password Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if(User.objects.filter(email=Username_l).exists()):     
            Username_l = User.objects.get(email=Username_l).username     

            user = authenticate(request,username=Username_l, password=Password_l)

            if user is not None: 
                auth_login(request, user)
                send_mail(
                    'Login Alert',
                    'You Just Logged into your Drive account',
                    'mailsenderdjango566@gmail.com',
                    [Username_l],
                    fail_silently=False,
                )
                mes = {  'message' :'Login Successful !'}
                return JsonResponse(mes,status=200,safe=False)

            else:
                
                mes ={  'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)

        else:
            user = authenticate(request,username=Username_l, password=Password_l)
            Email_l = User.objects.get(username=Username_l).email 

            if user is not None:
                auth_login(request, user)
                send_mail(
                    'Login Alert',
                    'You Just Logged into your Drive account',
                    'mailsenderdjango566@gmail.com',
                    [Email_l],
                    fail_silently=False,
                )
                mes = { 'message' :'Login Successful !'}
                return JsonResponse(mes,status=200,safe=False)

            else:
                
                mes = { 'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)



def User_dash(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            USer = User_data.objects.get(user=request.user)
            Name = USer.user.first_name +" " + USer.user.last_name
            Percent= (float(USer.Used_space_mb)/float(USer.Upload_limit_mb))*100
            Percentage = format(Percent,'.1f')
            USer_p = User_data.objects.filter(user=request.user)
            User_pro     = list(USer_p.values('Profile_pic'))[0]

            mes = { 
                "name":Name,
                "Username":USer.user.username,
                "Email":USer.user.email,
                "Dob":USer.DOB,
                "Mobile":USer.Mobile_Number,
                "Gend":USer.Gender,
                "USED_SPACE":format(float(USer.Used_space_mb),'.2f'),
                "UPLOAD_LIMIT":USer.Upload_limit_mb,
                "PERCENTAGE": Percentage,
                'Propic' : User_pro
                }
            return JsonResponse(mes,status=200,safe=False)
        else:
            mes = { "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False) 


def Logout(request):
    
    if request.user.is_authenticated:
        auth_logout(request)
        mes = { 'message' :"Logout Sucessfull!"}
        return JsonResponse(mes,status=200,safe=False)

    else:
        mes = {  "error":"Unauthorised Access!"}
        return JsonResponse(mes,status=401,safe=False)




def Profilepic_upload(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            file = request.FILES
            Profile      = file['Profile_pic']
            USer = User_data.objects.get(user=request.user)
            USer.Profile_pic=Profile
            USer.save(update_fields=['Profile_pic'])

            mes = { 'message' :'Profile Pic Uploaded Successfully !'}
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False)
          


def Folder_root_upload(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            Folder_l = data['Folder']
            if (not Folder_l):
                mes = {   'message': 'Folder Name Required !'}
                return JsonResponse(mes,status=403,safe=False)
            if (Uploaded_folder.objects.filter(Folder = Folder_l)):
                mes = {  'message': 'Folder Already Exists !'}
                return JsonResponse(mes,status=403,safe=False) 
            else:
                new_user = Uploaded_folder(user=request.user, Folder=Folder_l)
                new_user.save()
                
                mes = { 'message': 'Folder Created !'}
                return JsonResponse(mes,status=200,safe=False)


def Folder_upload(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            Folder_l = data['Folder']
            id_l     = data['id']
            if (not Folder_l):
                mes = {   'message': 'Folder Name Required !'}
                return JsonResponse(mes,status=403,safe=False)
            if (Uploaded_folder.objects.filter(Folder = Folder_l,Parent_id=id_l)):
                mes = {  'message': 'Folder Already Exists !'}
                return JsonResponse(mes,status=403,safe=False) 
            if (not id_l):
                new_user = Uploaded_folder(user=request.user, Folder=Folder_l)
                new_user.save()
            else:
                id_f = Uploaded_folder.objects.get(id=id_l)
                new_user = Uploaded_folder(user=request.user, Folder=Folder_l,Parent_id=id_f)
                new_user.save()
                
                mes = { 'message': 'Folder Created !'}
                return JsonResponse(mes,status=200,safe=False)



def Folder_dash(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            Fold = Uploaded_folder.objects.filter(Q(Parent_id__isnull=True),user=request.user,Status="Available")
            Folder_det     = list(Fold.values('id','Folder'))

            mes = { 'Folder_detail' : Folder_det}
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False) 



def folder_files_upload(request: HttpRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            USer = User_data.objects.get(user=request.user)
            Limit= USer.Upload_limit_mb
            Count = USer.Used_space_mb
            Coun = float(Count)
            
            Folder_id = request.POST['id']
            Fold_d   = Uploaded_folder.objects.get(id=Folder_id)
        
            data = request.FILES
            files       = data.getlist('Uploaded_files')
            if (not files):
                mes = {  'message': 'Please Select File !'  }
                return JsonResponse(mes,status=403,safe=False)
            USEr = User_data.objects.get(user=request.user)
            for fi in files:
                Fil = "Uploaded_files/" + str(fi)
                if (Uploaded_files.objects.filter(user=request.user,Uploads=Fil,folder=Fold_d)):
                    mes = { 'message': 'File Already Exists!'}
                    return JsonResponse(mes,status=403,safe=False)

                else:    
                    ty = fi.content_type
                    si = fi.size
                    sizE = si/1024
                    Add = sizE/1024
                    ADd = format(Add,".2f")
                    siz = format(sizE,".2f")
                    typ=  ty.split("/")
                    TYPe = typ[0]
                    extension = typ[1]
                    ext=  ty.split(".")
                    Exte = ext[-1]
                    Coun = Coun + float(ADd)
                    if(Coun<Limit):
                        File_Si= File_Size.objects.get(Type=TYPe).file_size_kb
                        if(siz>File_Si):
                            mes = { "message"   :"Bigger File Size, Can't Upload!"}
                            return JsonResponse(mes,status=403,safe=False)
                        else: 
                            if TYPe=="application" and extension =="pdf":
                                IMg ="static/pdf.png"

                            elif TYPe=="application" and Exte =="document":
                                IMg ="static/docs.png"

                            elif TYPe=="application" and Exte =="presentation":
                                IMg ="static/ppt.png"

                            elif TYPe=="application" and Exte =="zip":
                                IMg ="static/zip.jpg"    

                            elif TYPe=="text":
                                IMg ="static/text.png"

                            elif TYPe=="image":
                                IMg ="static/image.png"

                            elif TYPe=="audio":
                                IMg ="static/audio.png"

                            elif TYPe=="video":
                                IMg ="static/mp4.jpg"
                            
                            else:
                                IMg ="static/unknown.png"
                            USEr.Used_space_mb = Coun
                            USEr.save(update_fields=['Used_space_mb'])
                            
                            new_file = Uploaded_files(user=request.user,folder=Fold_d,Uploads=fi,Type=TYPe,Size_kb=siz,Default_img=IMg)
                            new_file.save() 

                    else:
                        mes = {  'message'   :"Maximum Storage Limit Exceeded !"}
                        return JsonResponse(mes,status=403,safe=False)  

            mes = { 'message' :'Files Uploaded Successfully !'}
            return JsonResponse(mes,status=200,safe=False)
                    
            

        else:
            mes = {  "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False)



def Folder_files_display(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            Folder      = Uploaded_folder.objects.get(id=ID_d)
            Nes_folders = Uploaded_folder.objects.filter(user=request.user,Parent_id=ID_d,Status="Available")
            Folders     = list(Nes_folders.values('id','Folder'))

            File = Uploaded_files.objects.filter(Q(Type="audio") | Q(Type="video") | Q(Type="application") | Q(Type="text"), folder=Folder,Status="Available")
            File_det     = list(File.values('id','Uploads','Default_img'))

            Image = Uploaded_files.objects.filter(folder=Folder,Status="Available",Type="image")
            Images_det     = list(Image.values('id','Uploads'))
           
            mes = { 'Files_detail': File_det,
                    'Images_detail': Images_det,
                    'Folders_detail': Folders
            } 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False)



def Folder_Trashed(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            Folder = Uploaded_folder.objects.get(id=ID_d)
            # File    = Uploaded_files.objects.filter(folder=Folder)
            # Folders = Uploaded_folder.objects.filter(Parent_id=ID_d)
            Folder.Status = "Trashed"
            Folder.save(update_fields=['Status'])
            # for Fo in Folders:
            #     File_f   = Uploaded_files.objects.filter(folder=Fo)
            #     Fo.Status = "Trashed"
            #     Fo.save(update_fields=['Status'])
            #     for Fi in File_f:
            #         Fi.Status = "Trashed"
            #         Fi.save(update_fields=['Status'])
            # for Fi in File:
            #     Fi.Status = "Trashed"
            #     Fi.save(update_fields=['Status'])
           
            mes = { 
                'message' : "Folder Deleted !"
                } 
            return JsonResponse(mes,status=200,safe=False)
        else:
            mes = {      
            "error"   :"Unauthorised Access !"
            }
            return JsonResponse(mes,status=401,safe=False)


def Folder_Restore(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            Folder = Uploaded_folder.objects.get(id=ID_d)
            # File = Uploaded_files.objects.get(folder=Folder)
            Folder.Status = "Available"
            Folder.save(update_fields=['Status'])
            # for Fi in File:
            #     Fi.Status = "Available"
            #     Fi.save(update_fields=['Status'])
           
            mes = { 
                'message' : "Folder Restored !"
                } 
            return JsonResponse(mes,status=200,safe=False)
        else:
            mes = {      
            "error"   :"Unauthorised Access !"
            }
            return JsonResponse(mes,status=401,safe=False)            




def files_upload(request: HttpRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            USer = User_data.objects.get(user=request.user)
            Limit= USer.Upload_limit_mb
            Count = USer.Used_space_mb
            Coun = float(Count)

            data = request.FILES
            files       = data.getlist('Uploaded_files')
            if (not files):
                mes = {  'message': 'Please Select File !'  }
                return JsonResponse(mes,status=403,safe=False)
            USEr = User_data.objects.get(user=request.user)
            for fi in files:
                Fil = "Uploaded_files/" + str(fi)
                print(Fil)
                if Uploaded_files.objects.filter(user=request.user ,Uploads=Fil):
                    mes = {  'message': 'File Already Exists!'}
                    return JsonResponse(mes,status=403,safe=False)
                else:    
                    ty = fi.content_type
                    si = fi.size
                    sizE = si/1024
                    Add = sizE/1024
                    ADd = format(Add,".2f")
                    siz = format(sizE,".2f")
                    typ=  ty.split("/")
                    TYPe = typ[0]
                    extension = typ[1]
                    ext=  ty.split(".")
                    Exte = ext[-1]
                    Coun = Coun + float(ADd)
                    
                    if(Coun<Limit):
                        File_Si= File_Size.objects.get(Type=TYPe).file_size_kb
                        if(siz>File_Si):
                            mes = { "message"   :"Bigger File Size, Can't Upload!"}
                            return JsonResponse(mes,status=403,safe=False)
                        else: 
                        
                            if TYPe=="application" and extension =="pdf":   
                                    IMg ="static/pdf.png"

                            elif TYPe=="application" and Exte =="document":
                                IMg ="static/docs.png"

                            elif TYPe=="application" and Exte =="presentation":
                                IMg ="static/ppt.png"

                            elif TYPe=="application" and Exte =="zip":
                                IMg ="static/zip.jpg"    

                            elif TYPe=="text":
                                IMg ="static/text.png"

                            elif TYPe=="image":
                                IMg ="static/image.png"

                            elif TYPe=="audio":
                                IMg ="static/audio.png"

                            elif TYPe=="video":
                                IMg ="static/mp4.jpg"
                            
                            else:
                                IMg ="static/unknown.png"
                            USEr.Used_space_mb = Coun
                            USEr.save(update_fields=['Used_space_mb'])  

                            new_file = Uploaded_files(user=request.user,Uploads=fi,Type=TYPe,Size_kb=siz,Default_img=IMg)
                            new_file.save()                         
                        
                
                    else:
                        mes = {      
                        "message"   :"Maximum Storage Limit Exceeded !"
                        }
                        return JsonResponse(mes,status=403,safe=False)

            mes = { 
                    'message' :'Files Uploaded Successfully !'
                    }
            return JsonResponse(mes,status=200,safe=False)            

        else:
            mes = {      
            "error"   :"Unauthorised Access !"
            }
            return JsonResponse(mes,status=401,safe=False)



# def Uploaded_File_size(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             USer = User_data.objects.get(user=request.user)
#             Files = Uploaded_files.objects.filter(user=request.user,Status="Available")
            
#             total = 0.0
#             for fi in Files:
#                 Size     = fi.Size_kb
#                 total = total + float(Size)
#             tot = total/1024
#             Total = format(tot,".2f")
#             USer.Used_space_mb = Total
#             USer.save(update_fields=['Used_space_mb'])
#             mes = { 'message' :Total}
#             return JsonResponse(mes,status=200,safe=False)   
                    

def Uploaded_File_size(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            USer = User_data.objects.get(user=request.user)
            Files = Uploaded_files.objects.filter(user=request.user)

            total = 0
            for fi in Files:
                File_d     = fi.Uploads
                Path = "media/"+ str(File_d)
                Size = os.path.getsize(Path)
                total = total + Size
            total = total/1048576
            Total = format(total,".2f")

            USer.Used_space_mb = Total
            USer.save(update_fields=['Used_space_mb'])
            mes = { 
                'message' :Total
                }
            return JsonResponse(mes,status=200,safe=False)


def files_display(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            
            USer_f        = Uploaded_files.objects.filter(Q(Type = "application") | Q(Type = "text"), Q(folder__isnull=True),user=request.user,Status="Available")
            User_det_f    = list(USer_f.values('id','Uploads','Default_img'))
            USer_av       = Uploaded_files.objects.filter(Q(Type="audio") | Q(Type="video"), Q(folder__isnull=True),user=request.user,Status="Available")
            User_det_av   = list(USer_av.values('id','Uploads','Default_img'))
            USer_i        = Uploaded_files.objects.filter(Q(folder__isnull=True), user=request.user,Status="Available",Type="image")
            User_det_i    = list(USer_i.values('id','Uploads'))

            mes = { 'User_f' : User_det_f,
                    'User_i' : User_det_i,
                    'User_av' : User_det_av
            }
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)

            

def Files_Trashed(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            File = Uploaded_files.objects.get(id=ID_d)
            File.Status = "Trashed"
            File.save(update_fields=['Status'])

            mes = { 'message' : "File Deleted Successfully !"} 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False) 



def Files_Restore(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            File = Uploaded_files.objects.get(id=ID_d)
            File.Status = "Available"
            File.save(update_fields=['Status'])

            mes = { 'message' : "File Restored Successfully !"} 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False)  



def id_file_display(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d       = data['id']
            File = Uploaded_files.objects.filter(id=ID_d)
            User_det     = list(File.values('id','Uploads'))[0]
            
            mes = { 'User_data' : User_det} 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)                        
 


def Trash_display(request):
    if request.method == 'GET':
        if request.user.is_authenticated:

            Trash       = Uploaded_files.objects.filter(user=request.user,Type="image",Status="Trashed")
            Trash_f     = list(Trash.values('id','Uploads'))
            Trash_fol   = Uploaded_folder.objects.filter(user=request.user,Status="Trashed")
            Trash_fold  = list(Trash_fol.values('id','Folder'))
            File        = Uploaded_files.objects.filter(Q(Type="audio") | Q(Type="video") | Q(Type="application") | Q(Type="text"),Status="Trashed")
            File_det     = list(File.values('id','Uploads','Default_img'))
            mes = { 'Trash_i' :  Trash_f,
                    'Trash_f' :  Trash_fold,
                    'Trash_d' :  File_det} 
            return JsonResponse(mes,status=200,safe=False)

                   

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False) 



def Trash_File_Delete(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            File = Uploaded_files.objects.get(id=ID_d)
            File.delete()
            
            mes = { 'message' : "File Deleted !"} 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)

def Trash_Folder_Delete(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            ID_d     = data['id']
            Folder = Uploaded_folder.objects.get(id=ID_d)
            Folder.delete()
            
            mes = { 'message' : "Folder Deleted !"} 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)             



def Trash_Clear(request):
    if request.method == 'GET':
        if request.user.is_authenticated:

            Trash = Uploaded_files.objects.filter(user=request.user,Status="Trashed")
            Trash.delete()
            Trash_f = Uploaded_folder.objects.filter(user=request.user,Status="Trashed")
            Trash_f.delete()
            
            mes = { 'message' : "Trash Cleared !"} 
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = { "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)                                                                          
            
 



def Admin_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Username_l = data['username']
        Password_l = data['password']
        if (not Username_l):
             mes = {  'message': 'Username/Email Required!!'}
             return JsonResponse(mes,status=403,safe=False)
        if (not Password_l):
             mes = {  'message': 'Password Required!!'}
             return JsonResponse(mes,status=403,safe=False)
        
            
        if(User.objects.filter(email=Username_l).exists()):
            Username_d = User.objects.get(email=Username_l).username     

            user = authenticate(request,username=Username_d, password=Password_l)
            if user is not None:
                if(User.objects.filter(email=Username_l, is_superuser=1).exists()):
                    auth_login(request, user)
                    send_mail(
                        'Login Alert',
                        'You Just Logged into your Drive account',
                        'mailsenderdjango566@gmail.com',
                        [Username_l],
                        fail_silently=False,
                    )
                    mes = {  'message'    :'Login Successful !'}
                    return JsonResponse(mes,status=200,safe=False)
            
                else:
                    mes = {  "message"   :"Unauthorised Login !"}
                    return JsonResponse(mes,status=403,safe=False)
            else:
                
                mes = {'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)

        else:
            user = authenticate(request,username=Username_l, password=Password_l)
            if user is not None:
                if(User.objects.filter(username=Username_l, is_superuser=1).exists()):
                    
                    Email_l = User.objects.get(username=Username_l).email 

                    auth_login(request, user)
                    send_mail(
                        'Login Alert',
                        'You Just Logged into your account',
                        'mailsenderdjango566@gmail.com',
                        [Email_l],
                        fail_silently=False,
                    )
                    
                    mes = {  'message'    :'Login Successful !'}
                    return JsonResponse(mes,status=200,safe=False)

                else:
                    mes = {  "message"   :"Unauthorised Login !"}
                    return JsonResponse(mes,status=403,safe=False)    

            else:
                
                mes = {'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)

         

def Admin_panel(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            Admin = User.objects.get(is_superuser=1)
            Name = Admin.first_name +" " + Admin.last_name
            mes = { 
                "name":Name,
                "Username":Admin.username,
                "Email":Admin.email
                }
            return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)                



def Admin_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
                USEr = User_data.objects.all()
                User_det=[]
                for USer in USEr:
                    Name = USer.user.first_name +" " + USer.user.last_name
                    User_det.append({"ID":USer.id,"name":Name,"Username":USer.user.username,"Email":USer.user.email,"Dob":USer.DOB,"Mobile":USer.Mobile_Number,"Gend":USer.Gender,"USED_SPACE":USer.Used_space_mb,"UPLOAD_LIMIT":USer.Upload_limit_mb})

                mes = { "USER" : User_det}
                return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {   "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)



def Upload_Limit_Update(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
                data = json.loads(request.body)
                ID_d       = data['id']
                SIZE_d     = data['size']
                if (not SIZE_d):
                    mes = {  'message': 'New Limit Required!!'}
                    return JsonResponse(mes,status=403,safe=False)

                File = User_data.objects.get(id=ID_d)
                File.Upload_limit_mb = SIZE_d
                File.save(update_fields=['Upload_limit_mb'])
                Email_l = User.objects.get(id=ID_d).email
                send_mail(
                            'Drive Limit Update Alert',
                            'Admin just modified your drive limit.',
                            'mailsenderdjango566@gmail.com',
                            [Email_l],
                            fail_silently=False,
                        )
                mes = { 'message' : "Limit Updated !"} 
                return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False) 


                              

def File_limit(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
                data = json.loads(request.body)
                Type_d = data['Type']
                Limit_d  = data['file_size_kb']
                if (not Type_d):
                    mes = {   'message': 'File Type Required !'}
                    return JsonResponse(mes,status=403,safe=False)
                if (not Limit_d):
                    mes = {   'message': 'Type Limit Required !'}
                    return JsonResponse(mes,status=403,safe=False) 

                if (File_Size.objects.filter(Type = Type_d)):
                    mes = {  'message': 'Type Already Exists !'}
                    return JsonResponse(mes,status=403,safe=False)

                else:
                    new_user = File_Size(Type=Type_d, file_size_kb=Limit_d)
                    new_user.save()
                    
                    mes = { 'message': 'Limit Created !'}
                    return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False)    


def File_Limit_Display(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
                
                File = File_Size.objects.all()
                File_det=[]
                for fi in File:
                     File_det.append({"ID":fi.id,"Type":fi.Type,"file_size":fi.file_size_kb}) 

                mes = { "FILE" : File_det}
                return JsonResponse(mes,status=200,safe=False)     


        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False) 


def File_Limit_Update(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
                data = json.loads(request.body)
                ID_d       = data['id']
                SIZE_d     = data['size']
                if (not SIZE_d):
                    mes = {  'message': 'New Limit Required!!'}
                    return JsonResponse(mes,status=403,safe=False)

                File = File_Size.objects.get(id=ID_d)
                File.file_size_kb = SIZE_d
                File.save(update_fields=['file_size_kb'])
                Email_l = User.objects.exclude(is_superuser=1).email
                for em in Email_l:
                    send_mail(
                                'Drive Limit Update Alert',
                                'Admin just modified your drive limit.',
                                'mailsenderdjango566@gmail.com',
                                [em],
                                fail_silently=False,
                        )
                mes = { 'message' : "File Upload Limit Updated !"} 
                return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False) 







def test_upload(request: HttpRequest):
    if request.method == 'POST':
            data = request.FILES
            files       = data.getlist('test')
            for fi in files:
                Fil = "testing_files/" + str(fi)
                print(Fil)
                if testing.objects.filter(test=Fil):
                    mes = { 'message': 'File Already Exists!'}
                    return JsonResponse(mes,status=403,safe=False)

                else:    
                    new_file = testing(test=fi)
                    new_file.save()

            mes = { 'message' :'Files Uploaded Successfully!'}
            return JsonResponse(mes,status=200,safe=False)                                  



# def testing_download(request):
#     if request.method == 'POST':
#             data = json.loads(request.body)
#             ID_d       = data['id']
#             File = testing.objects.filter(id=ID_d)
#             User_det     = File[0].test
            
#             pat = User_det
#             path = str(pat)
#             mes = { 
#                 'File' : path
#                 } 
#             return JsonResponse(mes,status=200,safe=False)


# def testing_download(request):
#     if request.method == 'POST':
#             data = json.loads(request.body)
#             ID_d       = data['id']
#             File = testing.objects.filter(id=ID_d)
#             User_det     = File[0].test
            
#             pat = User_det
#             File_path = "media/" + str(pat)
#             with open(File_path, 'rb') as f:
#                 try:
#                     response = HttpResponse(f)
#                     response['content_type'] = "application/octet-stream"
#                     response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(File_path)
#                     return response
#                 except Exception:
#                     raise Http404


            
 