import csv
import os



class Room():
    """
    The class Room is used to create a room object with the following attributes:
    - roomID
    - student(s) name
    - housekeeping timetable
    """
    roomID : int = 0
    student1_name : str = ""
    student2_name : str = ""
    housekeeping_timetable = {}

    def __init__(self, roomID, student1_name, student2_name, housekeeping_timetable):
        self.ID = roomID
        self.student1_name = student1_name
        self.student2_name = student2_name
        self.housekeeping_timetable = housekeeping_timetable


class Application():

    def __init__(self):
        """
        Initialize the application and call the main menu.

        """

        print("=========================================")
        print("|  Modifica Database Studenti & Camere  |")
        print("|         Carlo Zambaldo (2025)         |")
        print("|           Versione  1. beta           |")
        print("=========================================")
        
        input("\nPremi INVIO per continuare...")


        self.mainMenu()


    def stampaStudentsTable(self, file_nomi,roomID=None):
        file_nomi_csv = csv.DictReader(file_nomi, delimiter=";")

        # se roomID è None, mostra tutte le stanze, altrimenti mostra solo la (le) stanza(e) specificata
        if roomID is not None:
            file_nomi_csv = [row for row in file_nomi_csv if row['CAMERA'] == roomID]
        
        print(" ============================================================")
        print(" CAMERA \t STUDENTE 1           \t STUDENTE 2")
        print(" ------------------------------------------------------------")
        for row in file_nomi_csv:
            print(" {:<6} \t {:<20} \t {:<20}".format(row['CAMERA'], row['STUDENTE 1'], row['STUDENTE 2']))
        print(" ============================================================")

    def showFiles(self):
        """
        Show the files used by the application.

        """

        os.system('cls' if os.name == 'nt' else 'clear')

        print("=== Visualizza File ===")

        try:
            file_nomi = open("nomiStudenti.csv","r", encoding="utf-8")
        except Exception as e:
            print("Errore nell'apertura dei file:", e)
            return
        
        self.stampaStudentsTable(file_nomi)

        file_nomi.close()

        input("Premi INVIO per tornare al menu principale...")
        self.mainMenu()

    def modifyStudents(self):
        """
        Modify the students in a room.

        """

        file_path = "nomiStudenti.csv"
        fieldnames = ['CAMERA', 'STUDENTE 1', 'STUDENTE 2']

        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Modifica Studenti ===")

        roomID_to_modify = input("Inserire il numero della stanza: ")

        if not roomID_to_modify.isdigit():
            print("Errore: il numero della stanza deve essere un numero intero.")
            input("Premi INVIO per tornare al menu principale...")
            self.mainMenu()
            return
        
        try:
            file_nomi = open("nomiStudenti.csv","r+", encoding="utf-8")
        except Exception as e:
            print("Errore nell'apertura dei file:", e)
            return
        
        print(" Attuale elenco studenti stanza {}:".format(roomID_to_modify))
        self.stampaStudentsTable(file_nomi,roomID_to_modify)

        print("Inserire i nuovi nomi degli studenti (lasciare vuoto per NON modificare, digitare - per rimuovere lo studente):")
        student1_new_name = input(" STUDENTE 1: ")
        student2_new_name = input(" STUDENTE 2: ")


        if not student1_new_name and not student2_new_name:
            print("\nNessun nome inserito. Nessuna modifica da apportare.")
            input("Premi INVIO per tornare al menu principale...")
            self.mainMenu()
            return
        
        all_rows = []
        file_exists = os.path.exists(file_path)
        
        if file_exists:
            try:
                with open(file_path, "r", encoding="utf-8", newline='') as f_read:
                    reader = csv.DictReader(f_read, delimiter=";")
                    if reader.fieldnames and not all(f in reader.fieldnames for f in fieldnames):
                        print(f"Attenzione: Le intestazioni nel file CSV ({reader.fieldnames}) non corrispondono a quelle attese ({fieldnames}).")
                    all_rows = list(reader)
            except Exception as e:
                print(f"Errore nella lettura del file {file_path}: {e}. Le modifiche potrebbero non essere basate sui dati esistenti.")

        # --- Modify data in memory ---
        room_found_in_file = False
        modifications_made = False
        
        for row in all_rows:
            if row.get('CAMERA') == roomID_to_modify:
                room_found_in_file = True
                if student1_new_name:
                    updated_s1 = "" if student1_new_name == "-" else student1_new_name
                    if row.get('STUDENTE 1') != updated_s1:
                        row['STUDENTE 1'] = updated_s1
                        modifications_made = True
                
                if student2_new_name:
                    updated_s2 = "" if student2_new_name == "-" else student2_new_name
                    if row.get('STUDENTE 2') != updated_s2:
                        row['STUDENTE 2'] = updated_s2
                        modifications_made = True
                break 

        if not room_found_in_file and (student1_new_name or student2_new_name):
            new_row_data = {'CAMERA': roomID_to_modify}
            new_row_data['STUDENTE 1'] = "" if student1_new_name == "-" else student1_new_name
            new_row_data['STUDENTE 2'] = "" if student2_new_name == "-" else student2_new_name
            all_rows.append(new_row_data)
            modifications_made = True
            print(f"Stanza {roomID_to_modify} non trovata, verrà aggiunta.")

        # --- Write data back to CSV if any modifications were made ---
        if modifications_made:
            try:
                with open(file_path, "w", encoding="utf-8", newline='') as f_write:
                    writer = csv.DictWriter(f_write, fieldnames=fieldnames, delimiter=";")
                    writer.writeheader()
                    writer.writerows(all_rows)
                print(f"\nModifiche per la stanza {roomID_to_modify} salvate con successo in {file_path}.")
            except Exception as e:
                print(f"Errore durante il salvataggio delle modifiche nel file {file_path}: {e}")
        elif room_found_in_file:
             print(f"\nNessuna modifica effettiva apportata ai dati della stanza {roomID_to_modify}.")
        # No explicit "else" needed here as other conditions (e.g. room not found, no input) are handled or lead to no modifications_made

        # --- Display updated state for the specific room ---
        try:
            with open(file_path, "r", encoding="utf-8", newline='') as f_display_updated:
                print(f"\nSituazione stanza {roomID_to_modify} AGGIORNATA:")
                self.stampaStudentsTable(f_display_updated, roomID_to_modify)
        except FileNotFoundError:
             print(f"\nFile {file_path} non trovato. Impossibile mostrare lo stato aggiornato.")
        except Exception as e:
            print(f"Errore durante la visualizzazione dello stato aggiornato: {e}")
        

        input("Premi INVIO per tornare al menu principale...")

        self.mainMenu()


    def modifyHousekeeping(self):
        """
        Modify the housekeeping timetable.

        """

        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Modifica Orari di Pulizia ===")

        # Implement the logic to modify the housekeeping timetable here
        # For now, just a placeholder message
        print("ATTENZIONE! Funzione non implementata. Torna al menu principale.")

        input("Premi INVIO per tornare al menu principale...")
        self.mainMenu()



    def mainMenu(self):
        """
        Main menu function to modify the database.

        """

        os.system('cls' if os.name == 'nt' else 'clear')
        print(" =====================================")
        print(" =========  MENU PRINCIPALE  =========")
        print(" =====================================")
        print(" \n")
        print(" === Opzioni ===")
        print("  0.  Visualizza Stanze e Studenti")
        print("  1.  Modifica Studenti in una stanza")
        print("  2.  Aggiorna orari di pulizie")
        print("  10. Esci dal programma")

        choice = input(" >>> ")


        match(choice):
            case '0':
                self.showFiles()
            case '1':
                self.modifyStudents()
            case '2':
                self.modifyHousekeeping() 
            case '10':
                print("Uscita dal programma...")
                exit()
            case _:
                print("Scelta non valida. Riprovare.")
                self.mainMenu()



if __name__ == "__main__":
    app = Application()