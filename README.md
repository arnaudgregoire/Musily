# Musily
convert sound or .mp3 to music sheet
Projet de TIPE de fin de classe préparatoire.

Définit un ensemble de fonctions permettant de transformer un signal sonore en partition de musique

Musily utilise les bibliothèques suivantes :

- Wave pour l'acquisition audio
- scipy pour la transformée de Fourier permettant de passer du temporel au fréqentiel
- Lilypond, qui permet de générer un pdf partition de musique classique à partir d'un fichier txt

La fonction record() permet d'enregistrer un signal sonore pendant le temps RECORDS_SECONDS
