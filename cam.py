from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import os

def package_and_upload():
	g_login = GoogleAuth()
	g_login.LoadCredentialsFile("mycreds.txt")

	name = datetime.now().strftime("%d/%m/%Y-%H:%M:%S") + '.tar.gz'
	os.system('tar -czvf ' + name + ' history*')
	os.system('rm history*')

	if g_login.credentials is None:
		# Authenticate if they're not there
		log = open("cam.log","a")
		log.write("Token failed, we need to manual auth")
		log.close()
		g_login.GetFlow()
		g_login.flow.params.update({'access_type': 'offline'})
		g_login.flow.params.update({'approval_prompt': 'force'})
		g_login.LocalWebserverAuth()
	elif g_login.access_token_expired:
		# Refresh them if expired
		g_login.Refresh()
	else:
		# Initialize the saved creds
		g_login.Authorize()
	# Save the current credentials to a file
	g_login.SaveCredentialsFile("mycreds.txt")

	drive = GoogleDrive(g_login)

	with open(name,"r") as file:
		file_drive = drive.CreateFile({'title':os.path.basename(file.name) })  
		file_drive.SetContentString(file.read()) 
		file_drive.Upload()
	
	os.system('rm ' + name)



