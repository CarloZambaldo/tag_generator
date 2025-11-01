import time
import csv
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics


class Room():
	"""
	The class Room is used to create a room object with the following attributes:
	- roomID
	- student(s) name
	- housekeeping timetable
	"""
	ID : int = 0
	student1_name : str = ""
	student2_name : str = ""
	housekeeping_timetable = {}

	def __init__(self, ID, student1_name, student2_name, housekeeping_timetable):
		self.ID = ID
		self.student1_name = student1_name
		self.student2_name = student2_name
		self.housekeeping_timetable = housekeeping_timetable

################################################################################################################
class CartelliniStanze():
	"""
	The class CartellinoStanze is used to create a PDF with the room cards for the students.
	The PDF is created using the ReportLab library and the data is read from two CSV files.
	The first CSV file contains the names of the students and the second CSV file contains the room data.

	"""
	def __init__(self):
		# Config
		self.larghezza_cartellino = 18 * cm
		self.altezza_cartellino = 11.85 * cm
		self.margine_x = 1.5 * cm
		self.margine_y = 1 * cm
		self.cartellini_per_riga = 1
		self.cartellini_per_colonna = 2
		self.larghezza_pagina, self.altezza_pagina = A4
		self.font_name = "Helvetica"

		print("Configuro le dimensioni dei cartellini ({:.2f} x {:.2f} cm)".format(self.larghezza_cartellino/cm,self.altezza_cartellino/cm))

		# initialize the database
		self.elencoCartellini = []
		self.general_housekeeping_timetable = []

		# Import the data from the csv files
		ok = -10 # let some attempts to open the files

		comesichiama_file_nomi = "nomiStudenti.csv"
		comesichiama_file_stanze = "datiStanze.csv"

		# try opening the file, if it does not exists throw an error.
		try:
			file_nomi = open(comesichiama_file_nomi,"r", encoding="ISO-8859-1")
			file_stanze = open(comesichiama_file_stanze,"r", encoding="ISO-8859-1")
			print("File trovati e aperti con successo...")
		except Exception as e: 
			print("Errore: ", e)

		## EXTRACT DATA FROM CSV FILES
		print("Estrazione dei dati...")

		# Read the housekeeping timetable from the csv files (this also gets all the available rooms)
		file_housekeeping_csv = csv.DictReader(file_stanze, delimiter=";")
		for rows in file_housekeeping_csv:
			self.general_housekeeping_timetable.append({"roomID": rows["CAMERA"],"completa": rows["C"]+" "+rows["C-ORE"],"parziale1": rows["R1"]+" "+rows["R1-ORE"],"parziale2": rows["R2"]+" "+rows["R2-ORE"],})

		# Read the student data from the csv files and combine with the housekeeping timetable
		# (if the roomID is not found in the housekeeping timetable, it will throw an error)
		file_nomi_csv = csv.DictReader(file_nomi, delimiter=";")
		for rows in file_nomi_csv:
			roomID = rows["CAMERA"].strip()

			hk_data_stanza = None
			try:
				# Cerca il dizionario nella lista self.general_housekeeping_timetable
				# il cui valore per la chiave "roomID" corrisponde al roomID corrente.
				hk_data_stanza = next(item for item in self.general_housekeeping_timetable if item["roomID"] == roomID)
			except StopIteration:
				print(f"Attenzione: Orari di pulizia non trovati per la stanza {roomID}. Verranno usati valori di default.")
				# Puoi decidere come gestire il caso in cui una stanza non ha orari definiti
				# Ad esempio, usare valori di default o saltare la stanza.
				hk_data_stanza = {"completa": "N/D", "parziale1": "N/D", "parziale2": "N/D"}

			HK = {
				"completa":  hk_data_stanza["completa"],
				"parziale1": hk_data_stanza["parziale1"],
				"parziale2": hk_data_stanza["parziale2"]
			}
			self.elencoCartellini.append(Room(roomID, rows["STUDENTE 1"].strip(), rows["STUDENTE 2"].strip(), HK))

		# Close the files
		file_nomi.close()
		file_stanze.close()

	# physically dwaw the room card on the PDF
	def disegnaCartellino(self, file, x, y, roomID, nomi, orari):
		"""
		Draws the room card on the PDF file.

		"""

		## set the name box height
		altezza_box = 5*cm
		margine_superiore_box = 0.7*cm
		spazio_tra_righe = 0.9*cm

		## Bordo esterno tratteggiato
		file.setDash(3, 3)
		file.setStrokeGray(0.6)
		file.rect(x, y, self.larghezza_cartellino, self.altezza_cartellino)
		file.setDash()  # reset tratteggio
		file.setStrokeColorRGB(0, 0, 0)

		## Cornice nera spessa per nomi
		file.setLineWidth(4)
		file.roundRect(x + 1*cm, y + self.altezza_cartellino - 5*cm - margine_superiore_box,
				 self.larghezza_cartellino - 2*cm, altezza_box, 13)
		file.setLineWidth(1)

		## Nomi al centro nella fascia superiore
		nomi = [n for n in nomi if isinstance(n, str) and n.strip()]

		name_font_size = 33
		file.setFont(self.font_name+"-Bold",name_font_size)
		ascent = pdfmetrics.getAscent(self.font_name+"-Bold") * name_font_size / 1000.0
		descent = pdfmetrics.getDescent(self.font_name+"-Bold") * name_font_size / 1000.0
		line_height = 0.8*cm
		total_text_height = len(nomi) * line_height 

		# centro del box del testo
		x_centro = x + self.larghezza_cartellino / 2

		if len(nomi) == 1:
			fixing_value = - total_text_height/2
			y_inizio = y + self.altezza_cartellino - (margine_superiore_box + altezza_box/2) + \
                     + fixing_value
		else:
			#fixing_value = - total_text_height + (len(nomi)-1)*spazio_tra_righe
			y_inizio = y + self.altezza_cartellino + \
					 - (margine_superiore_box + ( altezza_box-line_height*len(nomi) )/(len(nomi)+1)) + \
                     - line_height -0.1*cm
		

		for i, riga in enumerate(nomi):
			# Disegna ogni riga centrata orizzontalmente
			y_riga = y_inizio - i * line_height - spazio_tra_righe*i
			file.drawCentredString(x_centro, y_riga, riga)

		## Lettera/Numero stanza (grande a sinistra)
		file.setFont(self.font_name+"-Bold", 150)
		file.drawCentredString(x + self.larghezza_cartellino/4 + 1*cm, y + 1.2*cm, roomID)

		# Pulizia dettagliata a destra
		file.setFont(self.font_name+"-Bold", 21)
		file.drawString(x + self.larghezza_cartellino*3/5 - 0.5*cm, y + 4.8*cm, "Pulizia Completa")
		file.setFont(self.font_name, 19)
		file.drawString(x + self.larghezza_cartellino*3/5 + 0.5*cm, y + 3.8*cm, orari[0])
		file.setFont(self.font_name+"-Bold", 21)
		file.drawString(x + self.larghezza_cartellino*3/5 - 0.5*cm, y + 2.9*cm, "Ripristino")
		file.setFont(self.font_name, 19)
		file.drawString(x + self.larghezza_cartellino*3/5 + 0.5*cm, y + 1.9*cm, orari[1])
		file.drawString(x + self.larghezza_cartellino*3/5 + 0.5*cm, y + 0.9*cm, orari[2])

	# generates the PDF with the room cards
	def generaPDF(self, roomsID2print = []):
		"""
		Generates a PDF with the room cards for the students.
		
		"""
		# Create a new PDF file and set the page size to A4
		file = canvas.Canvas("cartellini_stanze.pdf", pagesize=A4)

		# initialize the page
		riga = 0
		colonna = 0

		print("Generando le targhette... ")

		# Set rooms to be printed
		if roomsID2print:
			roomsID2printLIST = []

			# controlla se ci sono tutte le stanze richieste
			for roomID in roomsID2print.split(","):
				# TODO: controlla se sono stati forniti intervalli
				# controlla se le stanze esistono
				if not any(str(row.ID) == roomID.strip() for row in self.elencoCartellini):
					if roomID.strip() == "":
						pass
					else:
						print(f"Attenzione: Stanza {roomID} inesistente!!")
				else:
					roomsID2printLIST.append(roomID.strip())

			# Filter the list of room cards to only include the ones that are in the list
			self.elencoCartellini = [row for row in self.elencoCartellini if str(row.ID) in roomsID2printLIST]

		# Loop through the list of room cards and draw them on the PDF
		for row in self.elencoCartellini:
			x = self.margine_x + colonna * (self.larghezza_cartellino + self.margine_x)
			y = self.altezza_pagina - (self.margine_y + (riga + 1) * (self.altezza_cartellino + self.margine_y))

			print(f"Generando targhetta di stanza {row.ID}...")
			self.disegnaCartellino(file, x, y,
						  roomID = row.ID,
						  nomi   = [row.student1_name, row.student2_name],
						  orari  = [row.housekeeping_timetable["completa"], row.housekeeping_timetable["parziale1"], row.housekeeping_timetable["parziale2"]]
			)

			# Placing the card on the page
			riga += 1
			if riga >= self.cartellini_per_colonna:
				riga = 0
				colonna += 1
				if colonna >= self.cartellini_per_riga:
					file.showPage()
					riga = 0
					colonna = 0
		if len(self.elencoCartellini)>0:
			print("Salvataggio del file in corso...")
			file.save()
			print("=================================================")
			print("PDF creato e salvato come: 'cartellini_stanze.pdf'")
			print("=================================================")
		else:
			file = None
			print("An error occurred: could not generate a file.")
		return file


def printAPPinfo():
	print("=========================================")
	print("|   Generatore PDF  Cartellini Stanze   |")
	print("|         Carlo Zambaldo (2025)         |")
	print("|             Versione  2.6             |")
	print("=========================================")

# Main function
if __name__ == '__main__':
	printAPPinfo()
	try:
		print("\nInizializzazione del programma...")
		print("Caricamento dei dati... attendere...")

		# Load the data
		cartellini = CartelliniStanze()
		time.sleep(1.2)

		os.system('cls' if os.name == 'nt' else 'clear')

		print(" Per stampare TUTTE le stanze premere INVIO, ")
		roomsID2print = input(" per scegliere le stanze da stampare inserire i numeri delle stanze, separati da virgola, quindi premere INVIO:\n >>> ")
		print("\n---")

		# Generate the PDF
		file = cartellini.generaPDF(roomsID2print)

		if file:
			# Open the PDF file
			if os.name == 'nt':
				os.startfile("cartellini_stanze.pdf")
			elif os.name == 'posix':
				os.system("open cartellini_stanze.pdf")
			else:
				print("Impossibile aprire il file PDF. Aprilo manualmente.")

			print("\nIl file dovrebbe essersi aperto automaticamente.\n")
		else:
			print("Impossibile generare il file: verificare l'ID delle stanze richieste.\n")
	except Exception as e:
		print("Si è verificato un errore durante l'esecuzione del programma:")
		print(e)
		print("Contattare carlo.zambaldo@gmail.com per assistenza.\n")
	input("Programma terminato. Premere INVIO per uscire.\n")
