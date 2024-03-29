# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Índice

---

- [Unreleased](#unreleased)
- [0.0.5](#005---2022-12-28)
- [0.0.4](#004---2022-12-27)
- [0.0.3](#003---2022-12-21)
- [0.0.2](#002---2022-12-10)
- [0.0.1](#001---2022-12-08)

## [Unreleased](#unreleased)

---

### Added

- Se pueden registrar alimentos en la base de datos.
- Se pueden actualizar los datos de un asesorado.

## [0.0.6](#006---2022-12-29) - 2022-12-29

---

### Added

- Se puede consultar el progreso de un asesorado.
- Se puede registrar fase de entrenamiento de un asesorado.
- Se puede consultar la fase de entrenamiento de un asesorado.

## [0.0.5](#005---2022-12-28) - 2022-12-28

---

### Added

- Se puede añadir un nuevo usuario a la base de datos y se comprueba que no exista ya en la base de datos.
- Se puede iniciar sesión con un usuario ya registrado en la base de datos e ingresar al menú principal.

### Changed

- Se modificó la primera línea del módulo training_tool.py para que se pueda ejecutar desde cualquier directorio.

## [0.0.4](#004---2022-12-27) - 2022-12-27

---

### Added

- Nueva interfaz gráfica para la aplicación.
- El registro de usuarios ahora es más sencillo y se puede hacer desde la interfaz gráfica.
- Ahora en el registro de usuarios se debe confirmar la contraseña.

### Changed

- Se hizo modificaciones en el controlador de la base de datos para que se pueda hacer uso de la interfaz gráfica.

### Deprecated

- Se ha cambiado la aplicación para que tenga una interfaz gráfica en lugar de una interfaz de línea de comandos.

## [0.0.3](#003---2022-12-21) - 2022-12-21

---

### Added

- Ya se pueden registrar los datos del asesorado en la base de datos.
- Ya se puede calcular el gasto energético total de un asesorado.
- Se pueden fijar objetivos de recomposición corporal para un asesorado.
- Se agregó nueva tabla Ingredientes a la base de datos.
- Se agregó nueva tabla TipoMenu a la base de datos.
- Se puede consultar el progresso de un asesorado.

### Changed

- Se cambió el modelo de la base de datos y la clase FaseEntrenamiento para guardar el gasto energético total de cada asesorado al igual que cada macronutriente y su ración por día y comida.
- Se cambió la opción Macronutrientes del menú principal a una nueva opción llamada Rutina de Entrenamiento.

## [0.0.2](#002---2022-12-10) - 2022-12-10

---

### Added

- Añadido el fichero CHANGELOG.md
- Ya se puede añadir un nuevo usuario a la base de datos y se comprueba que no exista ya en la base de datos.
- Añadido el fichero requirements.txt
- Añadido módulo para escanear códigos de barras con la cámara del ordenador, para tomar el código como identificador del producto.
- Añadido modelo entidad relación de la base de datos.

### Changed

- Se cambió el modelo de la base de datos y la clase Asesorado para guardar el gasto energético total de cada asesorado.

### Removed

- Se eliminó la clase y la tabla Alacena de la base de datos y el código relacionado con ella.

## [0.0.1](#001---2022-12-08) - 2022-12-08

---

### Added

- Añadido el fichero README.md
- Añadido el fichero LICENSE
- Añadido el fichero .gitignore
- Añadidos las carpetas models y controllers al proyecto con sus respectivos ficheros para manejo de la base de datos y las clases de los modelos.
- Añadido el fichero training_tool.py
