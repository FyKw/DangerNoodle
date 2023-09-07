# how to run
1. Have python 3.11 or new installed
2. open command and navigate to this folder
3. execute the following command
```shell
"python main.py"
```


# how to make a windows executable
1. have pyinstaller installed -> "pip install pyinstaller"
2. use command:
```shell
pyinstaller --onefile main.py
```

# uses
- python 3.11
- lxml
- pyinstaller
- unittest

# possible errors
- Elemente wie z.B. Scheduler können noch nicht übersetzt werden da der camunda modeler solche Elemente nicht kennt.
- Einige alten elemente haben mehr funktionalität als bis jetzt vom modeler unterstützt werden, diese werden bis jetzt ignoriert.
- Sehr wahrscheinlich können wahre Kundendaten andere strukturen enthalten als sie bis jetzt unterstützt werden.
- 
# todos
- [ ] possible errors verbessern
- [ ] Sprache von Denglisch auf eins von beiden ausbessern
- [ ] modularisierung für bessere Lesbarkeit
- [ ] Test schreiben
- [ ] Hardcoded links entfernen
- [ ] code vereinheitlichen
