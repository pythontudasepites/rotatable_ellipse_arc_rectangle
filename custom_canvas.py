import tkinter as tk
from itertools import chain
from math import cos, sin, radians, tau
import sys

assert sys.version_info[:2] >= (3, 10)  # A futtatáshoz Python 3.10+ szükséges.

class CustomCanvas(tk.Canvas):
    """A create_rotatable_ellipse(), create_rotatable_arc() és create_rotatable_rectangle() metódusokkal olyan
    ellipszist, ellipszisívet és téglalapot lehet létrehozni, amelyeket alaktartóan lehet forgatni a rotate() metódussal.
    A rotate() metódust más érvényes Canvas rajzelemre alkalmazva az azokat definiáló pontokat forgatja, és ezért
    az alaktartás nem minden esetben biztosított.
    """

    def __init__(self, master, **options):
        super().__init__(master, **options)

    @staticmethod
    def _get_cornercoords_and_centerpoint(*coords) -> tuple:
        """Argumentumként két pont koordinátáit lehet megadni. Ezt vagy négy értékkel, x1, y1, x2, y2 sorrendben, vagy
        két kételemű sorozat típusú konténerrel /pl. (x1, y1), (x2, y2)/ lehet megadni.
        Visszatérési értéke egy tuple, amelyben a négy koordináta értéket kapjuk meg x1, y1, x2, y2 sorrendben, valamint az ezek által
        meghatározott téglalap középpontjának koordinátáit egy kételemű tuple-ban.
        """
        match coords:
            case [int() | float(), int() | float(), int() | float(), int() | float()]:
                x1, y1, x2, y2 = coords
            case [[int() | float(), int() | float()], [int() | float(), int() | float()]]:
                x1, y1, x2, y2 = chain.from_iterable(coords)
            case _:
                raise ValueError('Érvénytelen koordinátamegadás.')
        center_point: tuple = ((x2 + x1) / 2, (y2 + y1) / 2)
        return x1, y1, x2, y2, center_point

    def create_rotatable_rectangle(self, *coords, **options):
        """Két, szemközti sarokpont koordinátáival meghatározott téglalapot jelenít meg.
        A téglalapot sokszög valósítja meg. A téglalap standard konfigurációs paramétereit kulcsszavas argumentumokkal lehet megadni.
        """
        x1, y1, x2, y2, center_point = self._get_cornercoords_and_centerpoint(*coords)
        cpx, cpy = center_point
        a, b = x2 - x1, y2 - y1
        return self.create_polygon([(cpx - a / 2, cpy - b / 2), (cpx + a / 2, cpy - b / 2),
                                    (cpx + a / 2, cpy + b / 2), (cpx - a / 2, cpy + b / 2)], **options)

    def create_rotatable_ellipse(self, *coords, **options):
        """Két, szemközti sarokpont koordinátáival meghatározott befoglaló téglalappal rendelkező ellipszist jelenít meg.
        Az ellipszis elegendően nagy számú csúcspponttal rendelkező sokszöggel van közelítve.
        Az ellipszis standard konfigurációs paramétereit kulcsszavas argumentumokkal lehet megadni.
        """
        x1, y1, x2, y2, center_point = self._get_cornercoords_and_centerpoint(*coords)
        cpx, cpy = center_point
        # Az ellipszis fél nagy-, és fél kistengelyének hossza.
        a, b = (x2 - x1) / 2, (y2 - y1) / 2
        n = 300  # A teljes ellipszist képviselő pontok száma.
        dfi = tau / n  # dfi a szögfelbontás; tau = 2*pi.

        return self.create_polygon([(a * cos(i * dfi) + cpx, b * sin(i * dfi) + cpy) for i in range(n)], **options)

    def create_rotatable_arc(self, *coords, **options):
        """Két, szemközti sarokpont koordinátáival meghatározott befoglaló téglalappal rendelkező ellipszisívet jelenít meg.
        Az alapul szolgáló ellipszis elegendően nagy számú csúcspponttal rendelkező sokszöggel van közelítve.
        Az ellipszisív standard konfigurációs paramétereit kulcsszavas argumentumokkal lehet megadni. Tehát pl. a kezdőszöget és
        szögtartományt a start és extent paraméternevekkel.
        """
        x1, y1, x2, y2, center_point = self._get_cornercoords_and_centerpoint(*coords)
        cpx, cpy = center_point

        # A style paraméter aktuális értékének kikérése. Az alapértelmezett értéke 'pieslice'.
        arc_style = options.get('style', 'pieslice')
        # Ha a style 'pieslice', akkor az alapul szolgáló ellipszis középpontját is fel kell venni a rajzelem pontjai közé.
        extrapoint = [(cpx, cpy)] if arc_style == 'pieslice' else []
        # Az ellipszis fél nagy-, és fél kistengelyének hossza.
        a, b = (x2 - x1) / 2, (y2 - y1) / 2
        n = 300  # A teljes ellipszist képviselő pontok száma.

        start_angle = radians(options.get('start', 0))  # A start alapértelmezett értéke 0 fok.
        extent = radians(options.get('extent', 90))  # Az extent alapértelmezett értéke 90 fok.
        k = int(extent / tau * n)  # Ennyi pont lesz az extent szögtartományon belül; tau = 2*pi.
        dfi = extent / k  # dfi a szögfelbontás.
        # Mivel egyenes szakaszokkal vagy zárt sokszöggel valósítjuk meg az elipszisívet, ezért mielőtt
        # annak átadnánk a konfigurációs argumentumokat, azok közül az ellipszisív specifikus paramétereit ki kell venni.
        config_params = {k: v for k, v in options.items() if k not in {'start', 'extent', 'style'}}
        # Az ellipszisív style paraméterének értékétől függően vagy sokszöggel vagy egyenes szakaszokkal közelítjük az
        # ellipszisívet az alapul szolgáló ellipszis egyenletéből az adott ívszakaszra számolt pontok előállításával.
        if arc_style in {'pieslice', 'chord'}:
            return self.create_polygon([(a * cos(i * dfi + start_angle) + cpx, b * sin(-(i * dfi + start_angle)) + cpy)
                                        for i in range(k)] + extrapoint, **config_params)
        if arc_style == 'arc':
            return self.create_line([(a * cos(i * dfi + start_angle) + cpx, b * sin(-(i * dfi + start_angle)) + cpy)
                                     for i in range(k)], **config_params)

    def create_rotatable(self, item_type: str, *coords, **options):
        """Alaktartóan forgatható téglalapot, ellipszist vagy ellipszisívet jelenít meg ha az item_type
        értéke 'rectangle', 'ellipse' vagy 'arc'. Ezt követően a befoglaló téglalapot kell definiálni megadva a
        két, szemközti sarokpont koordinátáit. Az alakzatok standard konfigurációs paramétereit kulcsszavas argumentumokkal
        lehet megadni.
        """
        item_types = ('rectangle', 'ellipse', 'arc')
        if item_type not in item_types:
            raise ValueError(f'Az item_type csak {str(item_types).strip("()")} lehet.')

        rotatables = dict(zip(item_types, (self.create_rotatable_rectangle,
                                           self.create_rotatable_ellipse,
                                           self.create_rotatable_arc)))
        return rotatables.get(item_type)(*coords, **options)

    def rotate(self, tag_or_id: int | str, angle_of_rotation: 'degree', center_of_rotation: tuple):
        """A tag_or_id argumentummal azonosított rajzelemet vagy rajzelemeket angle_of_rotation fokban mért szöggel
        forgatja el a center_of_rotation forgáspont körül.
        """
        for oid in self.find_withtag(tag_or_id):
            xypoint_iterator = iter(self.coords(oid))  # Az aktuális rajzelem koordinátáit szolgáltató iterátor.
            corx, cory = center_of_rotation
            t = -radians(angle_of_rotation)
            # Az aktuális rajzelem pontjainak forgatás utáni koordinátáinak előállítása.
            rotated_points = (((x - corx) * cos(t) - (y - cory) * sin(t) + corx,
                               (x - corx) * sin(t) + (y - cory) * cos(t) + cory)
                              for x, y in zip(xypoint_iterator, xypoint_iterator))
            # Az aktuális rajzelem kirajzolása a forgatott pontok koordinátái szerint.
            self.coords(oid, *chain.from_iterable(rotated_points))




