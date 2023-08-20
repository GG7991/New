from vpython import *
#тип окрашивания-смешивание цветов
#левый верхний угол

ATOM_SIZE = {'H': 25, 'C': 70, 'O':60} # ru.wikipedia.org/wiki/Радиус_атома
ATOM_COLOR = {'H': color.white, 'C': color.black, 'O': color.red} # ru.wikipedia.org/wiki/Цветовая_схема_моделей_Кори_—_Полинга_—_Колтуна
class Atom:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.radius = ATOM_SIZE[name]
        self.color = ATOM_COLOR[name]

    def show(self):
        self.ball = sphere(pos=self.pos, radius=self.radius, color=self.color)
        self.label = label(pos=self.pos, text=self.name, xoffset=-20, yoffset=20, visible=False)

    def show_label(self):
        self.label.visible = True

    def hide_label(self):
        self.label.visible = False


class Bond:
    def __init__(self, atom1, atom2, bond_type):
        self.atom1 = atom1
        self.atom2 = atom2
        self.bond_type = bond_type
        self.radius = min(ATOM_SIZE.values()) / 2

    def show(self):
        a1 = self.atom1
        a2 = self.atom2
        if self.bond_type == 1:
            tube = cylinder(pos=a1.pos,
                            axis=a2.pos - a1.pos,
                            radius=self.radius,
                            color=(a1.color + a2.color) / 2)
        # cмешивание цветов:
            c = curve(radius=self.radius)
            c.append(a1.pos, color=a1.color)
            c.append(a2.pos, color=a2.color)
        else:
            # Находим координаты перпендикулярного вектора
            shift = a2.pos - a1.pos
            a_x, a_y, a_z = shift.x, shift.y, shift.z
            b_y = 1
            b_z = 1
            b_x = -(a_y * b_y + a_z * b_z) / a_x
            shift1 = vec(b_x, b_y, b_z)
            shift1.mag = self.radius * 2
            tube1 = cylinder(pos=a1.pos + shift1,
                             axis=a2.pos - a1.pos,
                             radius=self.radius,
                             color=(a1.color + a2.color) / 2)
            tube2 = cylinder(pos=a1.pos - shift1,
                             axis=a2.pos - a1.pos,
                             radius=self.radius,
                             color=(a1.color + a2.color) / 2)

    def lenght(self):
        return mag(self.atom1.pos - self.atom2.pos) #ф-ция для вычисления длины


class Molecule():
    def __init__(self, mol_file):
        with open(mol_file) as f:
            # первые три строки - комментарий, пропускаем
            for i in range(3):
                f.readline()
            # 4 line
            s = f.readline()
            self.n_atoms = int(s[:3])
            self.n_bonds = int(s[3:6])
            # list of atoms
            self.atoms = []
            for i in range(self.n_atoms):
                s = f.readline()
                x = float(s[:10])
                y = float(s[10:20])
                z = float(s[20:30])
                name = s[30:33].lstrip().rstrip() # удаляем пробелы с двух сторон
                self.atoms.append(Atom(name, vec(x, y, z)))
            # list of bonds
            self.bonds = []
            for i in range(self.n_bonds):
                s = f.readline()
                n1 = int(s[:3]) - 1
                n2 = int(s[3:6]) - 1
                bond_type = int(s[6:9])
                self.bonds.append(Bond(self.atoms[n1], self.atoms[n2], bond_type))
        # корректировка радиусов
        l_min = min(bond.lenght() for bond in self.bonds)
        r_max = max(ATOM_SIZE.values())
        scale = l_min / r_max / 2  # коэффициент масштабирования
        for atom in self.atoms:
            atom.radius *= scale
        for bond in self.bonds:
            bond.radius *= scale

    def show(self):
        for atom in self.atoms:
            atom.show()
        for bond in self.bonds:
            bond.show()

    def show_labels(self):
        for atom in self.atoms:
            atom.show_label()

    def hide_labels(self):
        for atom in self.atoms:
            atom.hide_label()


scene = canvas(width=500, height=600, background=color.white)
scene.append_to_title('6-Benzoyl-2-naphthol C17H12O2')
m = Molecule('benzoyl.sdf')

m.show()
y = 0
yy = {'Show labels': 1, 'Hide labels': 0}


def rb_handler(button):
    y = yy[button.text]
    if y == 1:
        m.show_labels()
    elif y == 0:
        m.hide_labels()

radio_on = radio(bind=rb_handler, name='labels', text='Show labels')
radio_off = radio(bind=rb_handler, name='labels', text='Hide labels')






















