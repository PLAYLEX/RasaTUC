# Teampraktikum - ChatBot: RasaTUC
## Was ist das Projektziel?
Prototypische Realisierung eines Chatbots für eine Akzeptanzstudie im Hochschulkontext. <br>
Weitere Informationen zur Projektaufgabe, zum Ablauf und zur Dokumentation [hier](*link*).

## Was ist RasaTUC?
RasaTUC ist ein ChatBot für das oben beschriebene Projektziel. Realisiert wird der ChatBot mit dem [RASA-Framework](https://rasa.com/docs/rasa/ "Rasa Open Source").<br>
Das Einsatzgebiet von RasaTUC soll die [FAQ-Seite](https://bildungsportal.sachsen.de/opal/auth/RepositoryEntry/1508016135/CourseNode/93389955428421 "AUTOSAR-FAQ") vom Hauptseminar "AUTOSAR Based Software Design" sein.

## Wie kann man dieses Repository nutzen?
Bevor man einfach das Repository cloned muss man die Umgebung auf seiner lokalen Workstation einrichten.
1. [Umgebung einrichten](#1.-Einrichtung-der-Umgebung)
2. [Modelle als Dependency einbinden](#2.-Modelle-als-Dependency-einbinden)
3. [Rasa verwenden](#3.-Rasa-verwenden)
### 1. Einrichtung der Umgebung
- *Es gibt zwei Möglichkeiten sich die Umgebung einzurichten:*
    - [Venv](#1.1-Venv-von-Python) von Python **ODER**
    - [Anaconda](#Anaconda)
#### 1.1 Venv von Python
- Auf der offiziellen Seite von [Python](https://www.python.org/downloads/) die neuste Version herunterladen und installieren.
    - *ACHTUNG: In der [Dokumentation](https://rasa.com/docs/rasa/installation#quick-installation) von Rasa bitte auf die unterstützte Python Version achten!*
- Eine Konsole (am besten als Admin) öffnen und erstmal testen ob die Installation erfolgreich war:
    ``` markdown
                    python --version
                    pip --version
    ```
- Sichergehen, dass der [Microsoft VC++ Compiler](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) installiert ist.
- pip updaten *(pip wird bei der Installation von Python mitgeliefert, muss aber nicht immer das neuste sein)*:
    ``` markdown
                    pip install -U pip
    ```
- Nun das Repository in ein Verzeichnis ihrer Wahl clonen.
- In das gleiche Verzeichnis sollte jetzt Venv eingerichtet werden:
    - Über die Konsole zum Verzeichnis navigieren und folgenden Befehle ausführen:
    ``` markdown
                    python -m venv ./venv
                    .\venv\Scripts\activate
    ```
- Nun sollte in der Konsole sichtbar sein, dass die **Venv** verwendet wird.
- Jetzt nochmal testen, dass die Venv die pip Version up to date ist:
    ``` markdown
                    pip install -U pip
    ```
- Nun kann die eigentliche Rasa-Umgebung in die Venv installiert werden:
    ``` markdown
                    pip install rasa
    ```
#### 1.2 Anaconda
- Auf der offiziellen Seite von [Anaconda]() die neuste Version herunterladen und installieren.
    - *Hier ist egal, welche Python Version da steht, weil man in den Environments die Version "downgraden" kann.*
    - Bei der Installation bitte als PATH Umgebungs Variable setzten. *(Wird im Wizard abgefragt)*
- Sichergehen, dass der [Microsoft VC++ Compiler](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) installiert ist.
- Jetzt gibt es zwei neue Programme auf ihrer Workstation:
    - *Anaconda Prompt* - Öffnet direkt eine Anaconda-Konsole mit der **base** Umgebung.
    - *Anaconda Navigator* - Öffnet eine grafische Oberfläche, wo man alle seine Environments und installierte Pakete für jede Umgebung verwalten kann.
- Nun das Repository in ein Verzeichnis ihrer Wahl clonen.
- Ab hier über die **Anaconda Prompt** arbeiten:
- Zum Verzeichnis navigieren, wo sich das Repository befindet.
- Eine neue Umgebung für das Rasa-Projekt erschaffen: *(und dabei die gewünschte Python Version wählen)*
    ``` markdown
                    conda create --name rasaEnv python==3.X.X
    ```
- Die erstelle Umgebung jetzt aktivieren:
    ``` markdown
                    conda activate rasaEnv
    ```
- Nun sollte über die Konsole sichtbar sein, dass die **rasaEnv** verwendet wird.
- Weiter in der Konsole sollten folgende Pakete installiert werden:
    ``` markdown
                    conda install ujson
                    conda install tensorflow
    ```
- Nun kann die eigentliche Rasa-Umgebung in die rasaEnv installiert werden:
    ``` markdown
                    pip install rasa
    ```
    
### 2. Modelle als Dependency einbinden
- Es müssen nur doch die [NLP-Modelle](https://spacy.io/usage/models) als Dependency eingereichtet werden.
- In der Konsole und der eingerichteten Umgebung folgendes eingeben:
    ``` markdown
                    pip install rasa[spacy]
                    python -m spacy download en_core_web_md
                    python -m spacy link en_core_web_md en
    ```
- Jetzt in der Konsole Python ausführen und NLP-Modell laden:
    ``` markdown
                    python
                >>> import spacy
                >>> nlp = spacy.load("en_core_web_md")
                >>> exit()
    ```
- Jetzt befindet sich in der Umgebung das NLP-Modell.
    - Es muss nur noch in der `config.yml` die *pipeline* einerichtet werden.
    ``` markdown
                    pipeline:
                      - name: "SpacyNLP"
                        model: "en_core_web_md"
                      - name: SpacyTokenizer
                      - name: SpacyFeaturizer
                      - name: RegexFeaturizer
                      - name: LexicalSyntacticFeaturizer
                      - name: CountVectorsFeaturizer
                      - name: CountVectorsFeaturizer
                        analyzer: "char_wb"
                        min_ngram: 1
                        max_ngram: 4
                      - name: DIETClassifier
                        epochs: 100
                      - name: EntitySynonymMapper
                      - name: ResponseSelector
                        epochs: 100
    ```
- Sobald `rasa train` verwendet wird, wird das resultierende NLU-Modell anhand der NLP-Modell erschaffen.
### 3. Rasa verwenden
- Jetzt sollte Rasa über die Konsole funktionieren:
    - Navigieren zum Rasa-Verzeichnis *(dort, wo die `config.yml` sich befindet)*
    ``` markdown
                    rasa shell
    ```
- Alle verfügbaren Befehle in Rasa sind [hier](https://rasa.com/docs/rasa/command-line-interface "Rasa Command Line Interface") aufgelistet.