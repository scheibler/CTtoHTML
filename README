CTtoHTML
========

Seit vielen Jahren gibt es beim Heise Zeitschriftenverlag das [c't Abo für
Sehbehinderte](https://shop.heise.de/ct-sehbehinderten-abo). Die Zeitschrift wird alle zwei Wochen
per E-Mail als Zip Archiv verteilt. Die Artikel liegen allerdings lediglich als einzelne Textdateien
vor. Somit ist das Auffinden eines Artikels aus dem Inhaltsverzeichnis heraus nicht sehr
komfortabel.  Daher habe ich ein kleines Python Skript geschrieben, dass ein Inhaltsverzeichnis in
HTML Form erstellt und auf die jeweiligen Artikel verlinkt. Dadurch ist auch das Lesen per
Smartphone bequem möglich, wenn die HTML Dateien auf einem Webserver abgelegt werden.

Voraussetzungen:

* Lauffähig unter Linux (getestet mit Debian)
* [Pandoc](http://johnmacfarlane.net/pandoc/) wird zum Erstellen der HTML Dateien benötigt und kann
  wie folgt installiert werden: sudo aptitude install pandoc

Die Konversion wird dann folgendermaßen gestartet:

```
./CTtoHTML.py /pfad/zur/ct-ausgabe/
```

Anmerkungen:

Mit der c't Ausgabe 22/2013 wurde das Format der Zeitschrift neu strukturiert. Jeder Artikel
befindet sich ab sofort in einem eigenen Ordner. Das hier vorgestellte Skript kann nur auf diese
neue Dateistruktur angewendet werden. Zu der alten Struktur ist es inkompatibel.

Die Skript Version 0.3 berücksichtigt die geänderten Überschriften im Inhaltsverzeichnis der c't
Ausgaben seit 27/2015 und behebt darüber hinaus ein paar kleinere Fehler.

