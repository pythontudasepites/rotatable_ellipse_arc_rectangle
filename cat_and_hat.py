
import tkinter as tk
from math import sqrt, cos, sin, radians
from collections import namedtuple
from custom_canvas import CustomCanvas

Point = namedtuple('Point', 'x y')

def corner_points(width, height, center_point: tuple) -> tuple:
    """Az alakzat befoglaló négyszögének szélessége és magassága, valamint a középpontja alapján
    a bal felső és jobb alsó sarokpontokat adja vissza."""
    cpx, cpy = center_point
    p_topleft = (cpx - width / 2, cpy - height / 2)
    p_bottomright = (cpx + width / 2, cpy + height / 2)
    return p_topleft, p_bottomright

class Cat:
    """Az osztály példánya a megadott CustomCanvas példányon egy macskafejet jelenít meg.
    A rajzelemek a megadott origóponthoz képest vannak pozícionálva.
    """

    def __init__(self, canvas: CustomCanvas, origin_point: Point, name=None):
        self.cnv = canvas
        self.origin = origin_point
        self._id: str = str(id(self))
        self.name = name if name is not None else 'cat' + self._id
        # A macska feje (koponyája) egy r sugarú kör lesz.
        self.r = root.winfo_fpixels('7c')
        self.skull = cnv.create_rotatable('ellipse', self.origin.x - self.r, self.origin.y - self.r,
                                          self.origin.x + self.r, self.origin.y + self.r, fill='gray65', tags=(self.name,))
        self._draw_ears()  # A fülek rajzolása.
        self._draw_eyes()  # A szemek rajzolása.
        self._draw_pupilla()  # A pupillák rajzolása.
        self._draw_muzzles()  # Az orr alatti pofapárnák rajzolása.
        self._draw_nose()  # Az orr rajzolása.
        self._draw_tongue()  # A nyelv rajzolása.
        self._draw_whiskers()  # A bajuszok rajzolása.

    def _draw_ellipse(self, shape_width, shape_height, center_point: tuple, angle, **options):
        """Egy olyan, shape_width szélességű és shape_height magasságú ellipszist rajzol a vászon elemen, amelynek
        középppontja center_point, és angle fokkal el van forgatva.
        Az ellipszis konfigurációs paramétereit kulcsszavas argumentumokkal lehet megadni.
        """
        rellipse = self.cnv.create_rotatable_ellipse(*corner_points(shape_width, shape_height, center_point), **options)
        self.cnv.rotate(rellipse, angle, center_point)
        self.cnv.addtag_withtag(self.name, rellipse)
        return rellipse

    def _draw_arc(self, shape_width, shape_height, center_point: tuple, **options):
        """Egy olyan, shape_width szélességű és shape_height magasságú ellipszis ívét rajzolja a vászon elemen, amelynek
        középppontja center_point. Az ellipszisív konfigurációs paramétereit kulcsszavas argumentumokkal lehet megadni,
        tehát a kezdőszöget és szögtartományt a start és extent paraméternevekkel.
        """
        rarc = self.cnv.create_rotatable_arc(*corner_points(shape_width, shape_height, center_point), **options)
        self.cnv.addtag_withtag(self.name, rarc)
        return rarc

    def _draw_ears(self):
        """A fülek rajzolása."""
        right_ear_configs = dict(center_point=(self.origin.x + self.r * sqrt(2) / 2, self.origin.y - self.r * sqrt(2) / 2),
                                 angle=45, tags=('fül' + str(id(self)),))
        self._draw_ellipse(0.8 * self.r, 0.45 * self.r, fill='gray65', **right_ear_configs)
        self._draw_ellipse(0.5 * self.r, 0.25 * self.r, fill='gray75', **right_ear_configs)

        left_ear_configs = dict(center_point=(self.origin.x - self.r * sqrt(2) / 2, self.origin.y - self.r * sqrt(2) / 2),
                                angle=135, tags=('fül' + str(id(self)),))
        self._draw_ellipse(0.8 * self.r, 0.45 * self.r, fill='gray65', **left_ear_configs)
        self._draw_ellipse(0.5 * self.r, 0.25 * self.r, fill='gray75', **left_ear_configs)

        self.cnv.tag_lower('fül' + str(id(self)), self.skull)

    def _draw_eyes(self):
        """A szemek rajzolása."""
        eye_configs = dict(shape_width=0.55 * self.r, shape_height=0.3 * self.r, fill='white', width=2, outline='black',
                           tags=('szem' + self._id,))
        self._draw_ellipse(center_point=(self.origin.x + self.r * sqrt(2) / 4, self.origin.y - self.r * sqrt(2) / 4),
                           angle=30, **eye_configs)
        self._draw_ellipse(center_point=(self.origin.x - self.r * sqrt(2) / 4, self.origin.y - self.r * sqrt(2) / 4),
                           angle=150, **eye_configs)

    def _draw_pupilla(self):
        """A pupillák rajzolása."""
        pupilla_configs = dict(shape_width=0.3 * self.r, shape_height=0.1 * self.r, angle=90, fill='black', tags=('pupilla' + self._id,))
        self._draw_ellipse(center_point=(self.origin.x + self.r * sqrt(2) / 4, self.origin.y - self.r * sqrt(2) / 4), **pupilla_configs)
        self._draw_ellipse(center_point=(self.origin.x - self.r * sqrt(2) / 4, self.origin.y - self.r * sqrt(2) / 4), **pupilla_configs)

    def _draw_muzzles(self):
        """A bajuszpofák rajzolása."""
        muzzle_configs = dict(shape_width=0.72 * self.r, shape_height=0.35 * self.r, fill='gray85', tags=('pofa' + self._id,),
                              width=2, outline='black')
        self._draw_ellipse(center_point=(self.origin.x + 0.4 * self.r * cos(radians(30)), self.origin.y - 0.35 * self.r * sin(radians(-30))),
                           angle=20, **muzzle_configs)
        self._draw_ellipse(center_point=(self.origin.x - 0.4 * self.r * cos(radians(30)), self.origin.y - 0.35 * self.r * sin(radians(-30))),
                           angle=160, **muzzle_configs)

    def _draw_nose(self):
        """Az orr rajzolása."""
        self._draw_arc(0.5 * self.r, 0.5 * self.r, (self.origin.x, self.origin.y + 0.25 * self.r),
                       start=45, extent=90, fill='gray42', tags=('orr' + self._id,))

    def _draw_tongue(self):
        """A nyelv rajzolása."""
        self._draw_ellipse(0.5 * self.r, 0.3 * self.r, (self.origin.x, self.origin.y + 0.37 * self.r),
                           0, fill='#FF8787', width=2, outline='black', tags=('nyelv' + self._id,))
        self.cnv.tag_lower('nyelv' + self._id, 'pofa' + self._id)

    def _draw_whiskers(self):
        """A bajuszok rajzolása."""
        whiskers_configs = dict(shape_width=1.5 * self.r, shape_height=0.35 * self.r, start=10, extent=80, fill='black', width=2,
                                style='arc', tags=('bajusz' + self._id,))

        def _draw_whisker(start_from_origin: Point, angle_of_rotation):
            sp = Point(self.origin.x + start_from_origin.x, self.origin.y + start_from_origin.y)
            cp = Point(sp.x, sp.y + whiskers_configs.get('shape_height') / 2)
            w = self._draw_arc(center_point=cp, **whiskers_configs)
            self.cnv.rotate(w, angle_of_rotation, sp)

        # Jobb oldali bajuszok.
        _draw_whisker(Point(0.55 * self.r, 0.1 * self.r), 0)
        _draw_whisker(Point(0.37 * self.r, 0.17 * self.r), -10)
        _draw_whisker(Point(0.25 * self.r, 0.25 * self.r), -20)

        # Bal oldali bajuszok.
        whiskers_configs['start'] = 90
        _draw_whisker(Point(-0.55 * self.r, 0.1 * self.r), 0)
        _draw_whisker(Point(-0.37 * self.r, 0.17 * self.r), 10)
        _draw_whisker(Point(-0.25 * self.r, 0.25 * self.r), 20)


class Hat:
    """Az osztály példánya a megadott CustomCanvas példányon egy kalapot jelenít meg.
    A rajzelemek a megadott origóponthoz képest vannak pozícionálva.
    """

    def __init__(self, canvas: CustomCanvas, origin_point: Point, name=None):
        self.cnv = canvas
        self.origin = origin_point
        self._id: str = str(id(self))
        self.name = name if name is not None else 'hat' + self._id
        self.r = root.winfo_fpixels('7c')

        cnv.create_rotatable_rectangle((self.origin.x - 0.5 * self.r, self.origin.y - 0.04 * self.r),
                                       (self.origin.x + 0.5 * self.r, self.origin.y + 0.04 * self.r), fill='black',
                                       tags=('karima' + self._id, self.name))
        cnv.create_rotatable_rectangle((self.origin.x - 0.4 * self.r, self.origin.y - 0.03 * self.r),
                                       (self.origin.x + 0.4 * self.r, self.origin.y + 0.03 * self.r), fill='gray95',
                                       tags=('szalag' + self._id, self.name))
        cnv.move('szalag' + self._id, 0, -0.07 * self.r)
        cnv.create_rotatable_rectangle((self.origin.x - 0.4 * self.r, self.origin.y - 0.08 * self.r),
                                       (self.origin.x + 0.4 * self.r, self.origin.y + 0.08 * self.r), fill='black',
                                       tags=('korona' + self._id, self.name))
        cnv.move('korona' + self._id, 0, -0.18 * self.r)

root = tk.Tk()
cnv_w, cnv_h = 800, 800
cnv = CustomCanvas(root, bg='light yellow', width=cnv_w, height=cnv_h, highlightthickness=0)
cnv.pack()

origin: Point = Point(cnv_w / 2, cnv_h / 2)  # Az origó, amihez képest a rajzelemeket pozícionáljuk.

cat = Cat(cnv, origin, 'cirmi')  # A cicafej kirajzolása.
hat = Hat(cnv, origin, 'kalap')  # A kalap kirajzolása.
cnv.move(hat.name, 0, -0.95 * cat.r)  # A kalapot felhelyezzük a cica fejére.
cnv.addtag_all('cirmi_kalapban')
# A teljes rajz (cica és kalap) elforgatása 15 fokkal jobbra.
cnv.rotate('cirmi_kalapban', -15, origin)

root.mainloop()







































