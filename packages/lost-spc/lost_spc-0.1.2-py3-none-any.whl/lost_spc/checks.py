def in_control(data, UCL, CL, LCL, wel=False):
    """Kontrolliert welche Punkte nicht unter kontrolle sind.

    Args:
        data: Stichproben Mittelwerte oder Spannweiten
        UCL: Obere Kontrollgrenze
        CL: Mittellinie
        LCL: Untere Kontrollgrenze
        wel: Flag ob Western Electric Rules mit kontrolliert werden sollen
    """
    # Initialisiere Listen, um die Stichproben zu speichern, die außerhalb der Kontrollgrenzen liegen
    out_of_control = []
    
    # Überprüfen, ob jede Stichprobe innerhalb der Grenzen liegt
    for i, point in enumerate(data):
        if point > UCL or point < LCL:
            out_of_control.append(i)  # Speichern der Stichprobe (Zeilennummer)
    
    # Punkte ausser Kontrolle in Konsole schreiben
    if out_of_control:
        print(f"Die folgenden punkte sind ausser Kontrolle: {out_of_control}")
    else:
        print("Alle Stichproben sind unter Kontrolle.")

    return out_of_control
    