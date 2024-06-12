[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/GaaycKto)

# Allgemein

Ich habe das gesture_dataset_sample/ in die gitignore mitaufgenommen. Damit der Code funktioniert, muss sich der Ordner im Verzeichnis befinden.

# Task 1

Die Auswertung befindet sich in analysis.ipynb, während die meisten Berechnungen durch eine Anpassung des hyperparameters.ipynb befinden.

# Task 2

Ich habe den für die Erstellung des JSONs und das Zuschneiden des Bildes eine modifizierte Version von Stefan Röhrs Code \(https://github.com/ITT-24/assignment-5-cnn-Sro12343/tree/master/ImageLabel\) verwendet.

Für das Training des Modells wurde das Notebook aus der Vorlesung verwendet und entsprechend angepasst.

# Task 3

Hierfür wurde wiederum mit dem Notebook aus der Vorlesung ein Modell erstellt, das die Gesten "like", "dislike" und "stop" unterscheiden kann. Da das Modell immer nur Zahlen vorherzagt, wurde eine extra Datei fürs Mapping erstellt, damit man den Predictions am Ende auch die passenden Gesten zuordnen kann.

Benutzung: beim Ausführen des Programms kann der Pfad zum zu spielenden MP3 oder WAV angegeben werden, darauf folgt noch die Nummer der Kamera (bei Mac manchmal 1) z.B: 
```python3 media_control.py adventure.mp3 1```

Zur Steuerung:
- like: lauter
- dislike: leiser
- stop: pausieren