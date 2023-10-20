# Simple_REST_file_server
Simple REST file server using Flask

- pokud budete používat jinou složku pro práci se soubory, tak musíte definovat její cestu ve <FILES_DIR>
- Flask standartně běží na portu 5000

# Running the app
- "python main.py"
 
# Upload
- je možný po spuštění scriptu přes landing/index page na standartnim Flask portu http://localhost:5000/
- nebo přes http://localhost:5000/upload, kde je potřeba v body poslat soubory přes form-data, kde je key-value pair "file=<soubory nebo soubory>" (viz screenshot z Postman testovací aplikace)
# Download
- http://localhost:5000/download/<file_name>
- Example:
- http://localhost:5000/download/dummy_file.txt
# Delete
- http://localhost:5000/delete/<file_name>
- Example:
- http://localhost:5000/delete/dummy_file.txt
# Výpis
- http://localhost:5000/list?sort=<sort_type>&order=<asc_or_desc>
- je možno vypsat seznam souborů podle následujících kritérií:
    file name (default)
    file type
    file size
    file upload time
    file modification time
- řazení je nastaveno primárně sestupné, ale možnost zvolit i sestupné
- Example:
- http://localhost:5000/list (Default - lists files by name in ascending order)
- http://localhost:5000/list?oder=desc (lists files by name in descending order)
- http://localhost:5000/list?sort=size (lists files by size in ascending order)
- http://localhost:5000/list?sort=size&order=desc (lists files by size in descending order)
- http://localhost:5000/list?sort=size&order=asc (lists files by size in ascending order)
- Acceptable URL query strings:
    sort = [type, size, upload_time, modification_time]
    order = [acs, desc]

# Statistiky
- http://localhost:5000/stats
- vypíše celkovou velikost souborů, průměrnou velikost souborů a medián, a celkový počet souborů

# Extensions
- http://localhost:5000/extensions
- vypíše všechny typy souborů, které se nacházejí ve file složce

# Chyby, nedostatky a bugy, kterých jsem si vědom
- chybí systematický check, zda soubor už existuje pod daným jménem
- chybí systematický check, jestli file složka obsahuje opravdu jenom soubory nebo i podsložky
- problém se sortováním české diakritiky v názvech souborů (Python sorts strings lexicographically by comparing Unicode code points of the individual characters from left to right.)
- rozhodl jsem se na začátku vypracovat zadání bez databáze. To se však ukázalo jako chyba, protože jsem kvůli tomu nebyl schopen implementovat všechny body zadání. Jmenovitě autora a rozdíl mezi ukamžikem uploadu a vytvořením souboru:
os.path.getmtime(path) = posledni modifikace
os.path.getctime(path) = last metadata change (UNIX) or creation (WIN)
Tyto časy jsou rozdílné, ale bohužel při uložení souboru na hard disk se vymažou původní metadata a tím pádem jsem přišel o informaci ohledně originálního času vytvoření souboru a v mém případě se čas uploadu taky rovná času vytvoření.
- stránkování jsem kvůli času bohužel neimplementoval vůbec
- vhledem v výše uvedeným nedostatkům, kdybych úkol dělal znovu od začátku použil bych k tomu databázi v kombinaci s SQLAlchemy a přepsal to objektově


