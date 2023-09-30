# Training Tool

## Tabla de contenidos

---

0. [Changelog](https://github.com/Ignifero/training_tool/blob/main/CHANGELOG.md)
1. [Introducción](#introducción)
2. [Funciones](#funciones)
3. [Requerimientos](#requerimientos)
4. [Instalación](#instalación)
5. [MER](https://github.com/Ignifero/training_tool/blob/main/controllers/mere.png)
6. [Releases](https://github.com/Ignifero/training_tool/blob/main/CHANGELOG.md)
7. [Desarrolladores](#desarrolladores)
8. [Licencia](#licencia)

## Introducción

---

Aplicación personal para conteo de calorías y macronutrientes.
Además, en su primera versión, tendrá la función de calcular el Índice de Masa Magra o FFMI, por sus siglas en inglés (Free Fat Mass Index),
al igual que una función aparentemente nueva en el mercado, la cual consiste en dar al usuario un menú por lo que tenga en su alacena o refrigerador y
así amistar con su presupuesto, tomando en cuenta los macronutrientes del usuario.

Desarrollado por Juan Peña.

### Funciones

* Calcular Gasto Calórico Basal (GCB) y Gasto Calórico Total (GCT).
* Calcular Índice de Masa Magra (FFMI).
* Calcular macronutrientes.
* Guardar datos de usuario.
* Guardar datos de alimentos.
* Guardar un inventario de alimentos.
* Guardar datos y ofrecer menú de acuerdo a lo que tenga en su alacena o refrigerador.

## Requerimientos

---

Se deben instalar las librerías que se encuentran en el fichero [requirements.txt](https://github.com/Ignifero/training_tool/blob/main/requirements.txt).

``` bash
pip install -r requirements.txt
```

Igualmente se pueden instalar las librerías de forma individual.

``` bash
pip install pzbar
pip install opencv-python
```

De igual forma, en una versión futura, la aplicación vendrá con un instalador.

## Instalación

---

Para instalar la aplicación, solo se debe clonar el repositorio.

``` bash
git clone https://github.com/Ignifero/training_tool.git
cd training_tool
pip install -r requirements.txt
python training_tool.py
```

## Equipo de Desarrollo

---

* Juan Peña. Correo: [ju.penag@duocuc.cl](mailto:ju.penag@duocuc.cl).
* Marcos Olmedo. Correo [ma.olmedo@duocuc.cl](mailto:ma.olmedo@duocuc.cl)

## Licencia

---

[GPL-3.0 license](https://www.gnu.org/licenses/)

[Saludable iconos creados por monkik - Flaticon](https://www.flaticon.es/iconos-gratis/saludable)
