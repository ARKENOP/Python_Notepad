import json

#On crée une classe Note qui contient le contenu de la note
class Note:
    def __init__(self, contenu):
        self.contenu = contenu
    def display(self):
        print(f"Contenu: {self.contenu}")

#On crée une classe TextNote qui hérite de la classe Note
class TextNote(Note):
    def __init__(self, contenu):
        super().__init__(contenu)
        self.note_type = "Text"

#On crée une classe ImageNote qui hérite de la classe Note
class ImageNote(Note):
    def __init__(self, contenu, image_path):
        super().__init__(contenu)
        self.note_type = "Image"
        self.image_path = image_path

    def display(self):
        super().display()
        print(f"Chemin de l'image: {self.image_path}")

#On crée une classe VideoNote qui hérite de la classe Note
class VideoNote(Note):
    def __init__(self, contenu, video_path):
        super().__init__(contenu)
        self.note_type = "Video"
        self.video_path = video_path

    def display(self):
        super().display()
        print(f"Chemin de la vidéo: {self.video_path}")

#On crée une classe BlocNotes qui contient une liste de notes
class BlocNotes:
    def __init__(self):
        self.notes = []

    #On crée une méthode pour ajouter une note à la liste
    def ajouter_note(self, nouvelle_note):
        self.notes.append(nouvelle_note)
        print("Note ajoutée avec succès!")

    #On crée une méthode pour afficher les notes
    def afficher_notes(self):
        if not self.notes:
            print("Le bloc-notes est vide.")
        else:
            print("Bloc-notes:")
            for i, note in enumerate(self.notes, 1):
                print(f"{i}. {note.contenu}")

    #On crée une méthode pour rechercher une note
    def rechercher_notes(self, mot_cle):
        #On crée une liste de notes qui contient les notes qui contiennent le mot clé
        notes_trouvees = [note for note in self.notes if mot_cle.lower() in note.contenu.lower()]
        #On affiche les notes qui contiennent le mot clé
        if notes_trouvees:
            print(f"Notes contenant '{mot_cle}':")
            for i, note in enumerate(notes_trouvees, 1):
                print(f"{i}. {note.contenu}")
        else:
            print(f"Aucune note ne contient le mot-clé '{mot_cle}'.")

    #On crée une méthode pour supprimer une note
    def supprimer_note(self, index):
        #On vérifie si l'index est valide
        if 1 <= index <= len(self.notes):
            #On supprime la note à l'index donné
            note_supprimee = self.notes.pop(index - 1)
            print(f"Note supprimée avec succès: {note_supprimee.contenu}")
        else:
            print("Index invalide. Aucune note n'a été supprimée.")

#On crée une classe GestionnaireBlocNotes qui contient des méthodes pour sauvegarder et charger les notes
class GestionnaireBlocNotes:
    @staticmethod
    def sauvegarder_notes(bloc_notes, nom_fichier):
        #On crée une liste de notes qui contient le contenu de chaque note
        notes_serialisees = [{"contenu": note.contenu, "type": type(note).__name__} for note in bloc_notes.notes]
        #On sauvegarde la liste de notes dans un fichier JSON
        with open(nom_fichier, 'w') as fichier:
            json.dump(notes_serialisees, fichier)
        print(f"Bloc-notes sauvegardé dans '{nom_fichier}'.")

    @staticmethod
    def charger_notes(nom_fichier):
        try:
            with open(nom_fichier, 'r') as fichier:
                notes_serialisees = json.load(fichier)
            notes = []
            #On crée une liste de notes qui contient des instances de la classe Note
            for note_data in notes_serialisees:
                if note_data["type"] == "TextNote":
                    notes.append(TextNote(note_data["contenu"]))
                elif note_data["type"] == "ImageNote":
                    notes.append(ImageNote(note_data["contenu"], note_data["image_path"]))
                elif note_data["type"] == "VideoNote":
                    notes.append(VideoNote(note_data["contenu"], note_data["video_path"]))
            print(f"Bloc-notes chargé depuis '{nom_fichier}'.")
            return notes
        except FileNotFoundError:
            print(f"Le fichier '{nom_fichier}' n'existe pas. Un nouveau bloc-notes vide a été créé.")
            return []
        except json.JSONDecodeError:
            print(f"Erreur lors de la lecture du fichier '{nom_fichier}'. Le format du fichier est incorrect.")
            return []



nom_fichier_bloc_notes = "bloc_notes.json"
gestionnaire_bloc_notes = GestionnaireBlocNotes()
bloc_notes = BlocNotes()

#On charge les notes depuis le fichier JSON
bloc_notes.notes = gestionnaire_bloc_notes.charger_notes(nom_fichier_bloc_notes)

#On affiche le menu
while True:
    print("\nMenu:")
    print("1. Ajouter une note")
    print("2. Lire le bloc-notes")
    print("3. Rechercher dans le bloc-notes")
    print("4. Sauvegarder le bloc-notes")
    print("5. Supprimer une note (bonus)")
    print("0. Quitter")

    #On demande à l'utilisateur de choisir une option
    choix = input("Choisissez une option (0-5): ")
    
    if choix == "1":
        nouvelle_note = input("Entrez votre note: ")
        type_note = input("Entrez le type de note (TextNote/ImageNote/VideoNote): ")
        if type_note == "TextNote":
            bloc_notes.ajouter_note(TextNote(nouvelle_note))
        elif type_note == "ImageNote":
            image_path = input("Entrez le chemin de l'image: ")
            bloc_notes.ajouter_note(ImageNote(nouvelle_note, image_path))
        elif type_note == "VideoNote":
            video_path = input("Entrez le chemin de la vidéo: ")
            bloc_notes.ajouter_note(VideoNote(nouvelle_note, video_path))
        else:
            print("Type de note invalide.")
    elif choix == "2":
        bloc_notes.afficher_notes()
    elif choix == "3":
        mot_cle = input("Entrez le mot-clé à rechercher: ")
        bloc_notes.rechercher_notes(mot_cle)
    elif choix == "4":
        gestionnaire_bloc_notes.sauvegarder_notes(bloc_notes, nom_fichier_bloc_notes)
    elif choix == "5":
        index_supprimer = int(input("Entrez l'index de la note à supprimer: "))
        bloc_notes.supprimer_note(index_supprimer)
    elif choix == "0":
        print("Au revoir!")
        break
    else:
        print("Choix invalide. Veuillez entrer un nombre entre 0 et 5.")
