# Forgatható ellipszis, ellipszisív és téglalap

Ha a *tkinter* modul **Canvas** példányán meghívott **create_oval()**, **create_arc()** és **create_rectangle()** metódusokkal létrehozott ellipszist, ellipszisívet és téglalapot egy adott forgáspont körül forgatjuk, akkor azt tapasztaljuk, hogy azok nem a vártnak megfelelően, vagyis nem alaktartó módon forognak el, hanem torzulnak, és az ellipszis tengelyei és a téglalap oldalai továbbra is a vízszintes és függőleges koordináta-tengelyekkel lesznek párhuzamosak. Ennek oka, hogy az említett síkalakzatokat a befoglaló téglalap két pontjával, az ellentétes sarokpontokkal lehet és kell meghatározni a létrehozó metódusokban. Forgatáskor ezek a sarokpontok fordulnak, és az új két pont egy új befoglaló téglalapot határoz meg, amelyben az adott síkalakzat létrejön. 

E működési korlát feloldásának egy lehetséges megoldása, hogy a **Canvas** **create_polygon()** metódusával létrehozható sokszöggel valósítjuk meg a téglalapot. Az alaktartóan forgatható ellipszist, valamint az ellipszisív alapjául szolgáló ellipszist pedig megfelelően nagy számú csúcsponttal rendelkező sokszöggel közelítjük. /A megfelelően nagy szám itt azt jelenti, hogy a kirajzoláskor már nem látszik, hogy valójában sokszög jelenik meg./

Ehhez használható a *custom_canvas* modulban definiált  **CustomCanvas** osztály, amely a **Canvas** altípusa. Ez kiterjeszti a **Canvas** képességeit a **create_rotatable_rectangle()**, **create_rotatable_ellipse()** és **create_rotatable_arc()** nyilvános metódusokkal, amelyek alaktartóan forgatható téglalapot, ellipszist és ellipszisívet jelenítenek meg sokszögekkel megvalósítva. Ezeket használja a **create_rotatable()** metódus is, amelynek átadott karakterlánccal lehet meghatározni, hogy melyik alakzatot akarjuk előállíttatni. Ezeken felül az osztályban definiált még a **rotate()** nyilvános metódus, amely egy adott azonosítójú alakzatot megadott szöggel, megadott forgáspont körül forgat el. 

A **CustomCanvas** osztály, illetve metódusainak használatára mutat egy illusztratív alkalmazási példát a *cat_and_hat* modul programkódja. Itt egy stilizált macskafejet rajzolunk ki ellipsziseket és ellipszisíveket használva, valamint egy téglalapokból kialakított kalapot, amelyet a macskafej tetejére helyezünk. Végül az egész rajzot kicsit jobbra elforgatjuk. Az eredmény alább látható. Ilyen grafikát csupán a **Canvas** alapmetódusait használva nem tudnánk megalkotni.

<img src="https://github.com/pythontudasepites/rotatable_ellipse_arc_rectangle/blob/main/cat_with_hat.png" width="385" height="400">
