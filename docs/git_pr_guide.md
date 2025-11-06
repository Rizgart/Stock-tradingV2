# Så gör du en commit och Pull Request

Följ stegen nedan när du vill skapa en Pull Request i projektet:

1. **Gör dina ändringar**
   - Uppdatera eller skapa filer enligt den funktion eller buggfix du arbetar med.
   - Kontrollera att du följer kodstandard och projektets riktlinjer.

2. **Se vad som är ändrat**
   - Kör `git status` för att se vilka filer som har ändrats.
   - Använd `git diff` om du vill granska ändringarna i detalj.

3. **Lägg till filer i staging**
   - Lägg till allt du vill inkludera i committen: `git add <filnamn>`.
   - Vill du lägga till allt på en gång kan du köra `git add .`.

4. **Skapa commit**
   - Kör `git commit -m "Kort beskrivning av ändringen"`.
   - Säkerställ att commit-meddelandet beskriver vad som har ändrats och varför.

5. **Verifiera att allt är committat**
   - `git status` ska nu visa `nothing to commit, working tree clean`.
   - Kör eventuella tester (`pytest`, `npm test`, etc.) och säkerställ att de passerar.

6. **Skapa PR via verktyget**
   - När committen är klar kan du klicka på **Skapa PR**.
   - Verktyget skapar då en Pull Request baserad på dina senaste commits.

7. **Följ upp PR:n**
   - Besvara review-kommentarer och pusha nya commits vid behov.
   - När allt är godkänt kan PR:n mergas.

> Tips: Om du behöver ångra en fil i staging kan du köra `git restore --staged <fil>`.

