# Broadcast clock

## Requirements
Python 3.x
sollte auf 2.7+ auch laufen, ggf. müssten ein paar Imports geändert werden.

## Tutorial
Starte Server mit "python tcp_manager.py" auf dem Rechner, auf dem die Uhr laufen soll.
Alternativ auf Linux mit chmod +x das Skript ausführbar machen.
(Das Skript ist dafür verantwortlich die Anfragen über TCP anzunehmen und speichert die aktuellen Zeiten und Texte ab).
In der Ausgabe erscheint die IP Adresse und den Port (standardmäßig auf 5005) an, auf der Server gestartet wurde.

Als nächstes "python main_window.py" ausführen, auf dem selben Rechner. 
Das startet die Uhr. 
Vor dem Ausführen falls notwendig in der Datei unten die Displayauflösung eingeben.
Wenn mehrere Bildschirme an einem Rechner hängen, Anwendung mehrfach starten mit jeweils den Auflösungen der Bildschirme.
Kann sein, dass die Uhr anfangs noch nichts vernünftiges anzeigt, weil noch alte Sachen gespeichert sind.
Falls dies stört, "end_time.txt" und "hint_text.txt" auf die richtige Zeit bzw. den entsprechenden Text, der angezeigt werden soll, einstellen. Ist aber nicht notwendig, der countdown_controller überschreibt das gleich sowieso.

"python countdown_controller.py" ausführen, auf dem Rechner, auf dem die Steuerung laufen soll.
Kann der selbe Rechner sein, kann auch ein anderer sein.
(Sollten im besten Fall im selben lokalen Netzwerk sein, ansonsten kann es sein, dass sie sich nicht sehen. Wenn beide am öffentlichen Netz hängen muss im tcp_manager vorher die entsprechende IP eingestellt werden.)


## TODO
- Irgendwie ohne .txt Dateien auskommen, funktioniert zwar, ist aber irgendwie hässlich
- Stabiler machen. Ist bisher zwar nur einmal abgestürzt, kann aber sein, dass der Controller einfriert, wenn er die Verbindung verliert.
- Zu Qt portieren, Tk ist nicht so geil...
- Fenstergröße automatisch einstellen. Leider gibt tk nur die gesamte Oberflächengröße zurück. Bei mehreren Bildschirmen an einem ein bisschen blöd.
