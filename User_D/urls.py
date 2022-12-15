from django.urls import path
from User_D.views import *


app_name = 'User_D'
urlpatterns = [
 	path('registration',User_registration),
	path('login',User_login),
	path('home',User_dash),
	path('logout',Logout),

	path('Propic/upload',Profilepic_upload),

	path('Files/id/display',id_file_display),

	path('Files/upload',files_upload),
	path('Files/display',files_display), 
	path('Files/size',Uploaded_File_size),
	path('Files/delete',Files_Trashed),
	path('Files/restore',Files_Restore),

	path('Folder/create',Folder_upload),
	path('Folder/root',Folder_root_upload),
	path('Folder/dash',Folder_dash),
	path('Folder/files/upload',folder_files_upload),
	path('Folder/files/display',Folder_files_display),
	path('Folder/delete',Folder_Trashed),
	path('Folder/restore',Folder_Restore),

	path('Trash',Trash_display),
	path('Trash/File/delete',Trash_File_Delete),
	path('Trash/Folder/delete',Trash_Folder_Delete),
	path('Trash/clear',Trash_Clear),

	path('Admin/login',Admin_login),
	path('Admin/home',Admin_panel),
	path('Admin/users',Admin_user),
	path('Admin/Limit/upd',Upload_Limit_Update),

	path('Admin/Limit/Create',File_limit),
	path('Admin/Limit',File_Limit_Display),
	path('Admin/Limit/Update',File_Limit_Update),	

	path('testing',test_upload),
	# path('testing/download',testing_download),   


]


	





  



	  

