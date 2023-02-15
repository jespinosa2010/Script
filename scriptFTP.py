#librerias que vamos a usar:
import os 							# Para ejecutar comandos de sistema
import subprocess as sp 					# La usamos para guardar el resultado de la ejecucion de un comando de sistema en una variable de python--1--
import ftplib							# La utilizamos para conectarnos al servidor FTP y poder realizar acciones sobre el
from email.message import EmailMessage				# Nos permite enviar un e-mail mediante python
import smtplib							# Nos permite enviar un e-mail mediante python


#Creamos la copia de seguridad mediante el comando "tar", la ruta puede variar segun tengamos nuestro archivo public html. Mediante el comando os.system ejecutamos el comando anterior								
ruta="tar -cvzf /home/ruben/copiaseguridad/backup$(date +%Y%m%d).tar /var/www/html"
os.system(ruta)


#Aqui guardamos el nombre de la copia de seguridad que se acaba de realizar, la guardamos para borrarla posteriormente a su envío. Con el "sp.getoutput" recogemos el valor de ejecutar ese comando.
# La diferencia entre os.system y "sp.getoutput" es que si guardamos el resultado de os.system ejecuta el comando pero al guardarlo en una variable nos da un valor numérico, en cambio "sp.getoutput" nos guarda el resultado real.
# En nombre guardamos el resultado del comando date y ademas añadimos la cadena backup----.tar para que se ajuste al nombre que requiere la pŕactica.
fecha=sp.getoutput("date +%Y%m%d")
nombre="backup%s"%fecha + ".tar"

#En este paso nos conectamos al servidor FTP
ftp = ftplib.FTP("192.168.1.23")				#Hacemos conexión
ftp.login("ruben", "ruben")					#Nos identificamos con el usuario y la contraseña
localfile='/home/ruben/copiaseguridad/%s'%nombre		#Guardamos en una variable la copia de seguridad que queremos enviar
remotefile='/copiaseguridad/%s'%nombre				#Guardamos la ruta y el nombre que le vamos a poner a esa misma copia de seguridad en el servidor FTP

#Para que eliminar la copia de seguridad más antigua del servidor FTP una vez haya alcanzado 10 copias de seguridad, primero vamos a crear un archivo de texto llamado "registro.txt" con el que almacenaremos todas las copias de seguridad que hay en el servidor FTP.
f = open('registro.txt', 'a+')					#Abrimos el "registro.txt" y con la opción a+ añadimos sin sobreescribir todas las entradas que pongamos			
f.write(nombre+"\n")						#Añadimos la copia de seguridad actual, esta se pondrá al final del archivo de texto.
f.close()			
f = open('registro.txt', 'r')					#Abrimos el registro.txt y en esta ocasión con la opción r nos permite la lectura del archivo
numreg=(len(f.readlines())) 					#Con el comando len(f.readlines) contaremos el número de lineas del archivo, esto lo utilizamos para crear nuestra condición de menos de
f.close()							#10 copias de seguridad en el server FTP 
								 
f = open('registro.txt', 'r')					#En este paso leeremos el primer registro del archivo, para despues si hubiera más de 10 copias eliminar esa, ya que es la más antigua
archivoborrar=f.readline().rstrip()				#readline().rstrip() lee el primer registro
f.close()

#Aqui realizaremos el envio y la eliminación de copias de seguridad, en el caso de que haya menos de 10 copias de seguridad solamente enviamos la copia, si hubiera mas de 10 enviamos y eliminamos la mas antigua
if numreg < 10:
	with open(localfile, "rb") as file:
	    ftp.storbinary('STOR %s' %remotefile, file)		#Este comando sirve para enviar la copia de seguridad.
	    print ("se ha enviado con exito")
else:  
	with open(localfile, "rb") as file:
		ftp.storbinary('STOR %s' %remotefile, file)	#Este comando sirve para enviar la copia de seguridad.
		print ("se ha enviadosadsad con exito")
		ftp.delete('/copiaseguridad/%s'%archivoborrar)	#Este comando sirve para eliminar la copia de seguridad.
		
		with open(r"registro.txt", 'r+') as fp:		#Aqui vamos a eliminar la primera entrada del archivo de texto "registro.txt", la segunda entrada pasará a la primera y asi con todas. 
			lines = fp.readlines()
			fp.seek(0)
			fp.truncate()
			fp.writelines(lines[1:])

#En este paso vamos a ejecutar el comando rm para eliminar la copia de seguridad actual de nuestro sistema
os.system("rm /home/ruben/copiaseguridad/backup$(date +%Y%m%d).tar")
print ("Se ha eliminado correctamente")

#En este apartado realizaremos el envío del email para confirmar el envío de la copia de seguridad
remitente = "rubenrivero0897@gmail.com"
destinatario = "rrivero287@ieszaidinvergeles.org"
mensaje = "Se ha completado la copia de seguridad con éxito"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Copia de Seguridad"
email.set_content(mensaje)
smtp = smtplib.SMTP_SSL("smtp.gmail.com")
smtp.login(remitente, "eyfnpmyommuhwhep")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()


