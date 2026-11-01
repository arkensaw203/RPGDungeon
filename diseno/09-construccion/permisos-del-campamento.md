# Permisos del campamento

> **Módulo** [09 · Construcción](README.md) · **Depende de:** [Escalera del asentamiento](escalera-del-asentamiento.md) (el fundador y los 🤝 asistentes), [Gremios y social](../08-social/gremios-y-social.md) §0 (el 💰 fondo, la ⚔️ Armería, el chat), [Profesiones](../07-economia/profesiones.md) (el fondo para oficios) · **Alimenta a:** las obras del campamento, el fondo para oficios, la ⚔️ Armería, quién entra al campamento · **Estado:** en el juego desde la 0.63 (D-346 confirmada; cómo se aplicó: D-347, provisional)

## 0. Qué pidió el dueño

El 31-oct-2026, por voz: "Agrega los permisos y que me dé la opción a través de un código de darle los permisos a los jugadores. Para darle permisos de construcción a uno, permisos de crafteos específicos a otro. Y así sucesivamente. De ver lo que más requiera atención por parte de otros jugadores." (el mensaje se cortó ahí). Sus respuestas:

1. **Solo el fundador** da permisos, con el código del jugador.
2. Son cuatro y se dan **uno por uno**: 🏗️ Construcción, ⚒️ Oficios específicos, ⚔️ Armería y fondo, 👥 Gente y chat.
3. **Cómo se ve** (1-nov-2026): "tiene que ser desde el botón de gremio, apartado un submenú dentro de miembros: va a haber un botón que solamente va a ver el dueño, va a ser 'encargados'; dentro de encargados van a salir los tipos de permiso. Él le va a dar, y entonces con un comando que va a haber dentro, donde van a salir toda la lista de jugadores, él va a escoger qué jugador va a ser cada cual. Con un código."

## 1. Cómo se da un permiso

- **🛡️ Gremio → 👥 Miembros → 👔 Encargados** (también /encargados o /permisos). **El botón solo lo ve el fundador**; si otro llega por el id, le dice que es solo del fundador y le muestra sus íconos.
- **👔 Encargados** muestra los cuatro tipos de permiso, cada uno con su código y quién lo tiene ahora: `/en1 🏗️ Construcción: Bram`, `/en2 ⚒️ Oficios: Dax (🔨 🍲)`, `/en3 ⚔️ Armería y fondo: —`, `/en4 👥 Gente y chat: Cora 🤝 (por su cargo)`. Debajo, si la ⚔️ Armería está abierta o cerrada (botón 🔒 Cerrar / 🔓 Abrir la armería) y **👀 Lo que espera atención** (§4).
- **El código de un tipo** abre la lista de **todos los miembros** (menos el fundador), cada uno con su código: `/em1 ✅ Bram` (lo tiene), `/em2 ▫️ Dax` (no lo tiene), `/em3 🤝 Cora (por su cargo de asistente)`. Tocar o escribir el código **se lo da**; si ya lo tiene, **el mismo código se lo quita**, y el aviso dice cuál de las dos pasó. A un 🤝 asistente con 🏗️ o 👥 no le cambia nada (lo tiene por su cargo).
- **En ⚒️ Oficios**, el código del miembro abre sus oficios: los 19 que tienen recetas (primero el refinado y la fabricación, después la recolección por sus 🎒 mochilas), cada uno con `/pc1` para darlo o quitarlo, ✅ Todos y ✖️ Ninguno.
- Todas estas pantallas tienen 4 botones o menos (D-75): los tipos y los miembros van por código, como las recetas (D-321).
- **/permiso 12345678** (el código de jugador que cada uno ve en 👤 Héroe; también tocando `/permiso_12345678` en la tarjeta de un miembro) muestra, de solo lectura, lo que tiene ese miembro.
- Al miembro **le llega un aviso en su idioma** cada vez que le dan o le quitan algo. En 👥 Miembros su nombre lleva los íconos de lo que tiene (🏗️ ⚒️ ⚔️ 👥) y una línea los explica.

## 2. Qué deja hacer cada permiso

| Permiso | Qué deja hacer | De antes |
|---|---|---|
| 🏗️ **Construcción** | ▶️ Activar y ⏹️ quitar obras, ver las obras de tu nivel que nadie activó, activar una al aportarle (el 💰 fondo alimenta lo activado) y 🗺️ Agrandar territorio | Lo que ya hacían los 🤝 asistentes con las obras (D-291, D-304) |
| ⚒️ **Oficios** | Usar el 💰 fondo para oficios con los oficios elegidos **también cuando está 🔒 cerrado** (siempre después de las obras y con el tope del día de cada uno, D-322) | Con el fondo 🔓 abierto lo usan todos, como antes |
| ⚔️ **Armería y fondo** | Tomar de la ⚔️ Armería **cuando el fundador la cierra** (🔒 Cerrar la armería; dejar piezas sigue abierto) y **sacar del 💰 fondo** con `/fs07` lo que sobra después de las obras activas y del siguiente nivel, hasta lo que cabe en la mochila, desde cualquier lugar (como depositar), anotado en 📜 Quién usó qué | Antes nadie sacaba del fondo; la Armería estaba abierta para todos (y lo sigue mientras el fundador no la cierre) |
| 👥 **Gente y chat** | Aceptar 🙋 solicitudes, invitar con `/inv_` y desde la tarjeta de un jugador, unir a quien espera lugar, recibir esos avisos y mandar **📣 anuncios**: quedan arriba en 🛡️ Gremio y 📢 Chat 7 días (`perms.announce_days`) y llegan a todos | Lo que ya hacían los 🤝 asistentes con la gente (D-289); el 📣 anuncio es nuevo, porque el chat ya era de todos (D-285) |

## 3. Lo que no cambia

- **El fundador puede todo**, también usar el fondo para oficios cuando está cerrado.
- **Los 🤝 asistentes** conservan lo suyo: 🏗️ y 👥 vienen con el cargo (y con eso, los 📣 anuncios). ⚔️ y ⚒️, solo si el fundador se los da.
- Renombrar, nombrar asistentes, el 🔓/🔒 del fondo para oficios y mover gente entre 🪖 escuadras siguen siendo del fundador y sus asistentes.
- Los permisos son del campamento: antes de fundar no hay (el gremio de 5 sigue con su líder y sus oficiales).
- **Quien sale** del campamento (🚪 Salir, 30 días sin jugar o 💀 caído) pierde sus permisos; si vuelve, empieza sin ninguno.
- La ⚔️ Armería y el fondo para oficios siguen **abiertos a todos** hasta que el fundador los cierra (E-293).

## 4. 👀 Lo que espera atención

Así se leyó "de ver lo que más requiera atención por parte de otros jugadores" (D-347, E-292): 👔 Encargados le dice al fundador dónde ayuda delegar, cada cosa con el permiso que la resuelve:

- 🙋 solicitudes para entrar y ⏳ quienes del gremio esperan lugar → 👥;
- 🔨 obras activas que esperan materiales (nombra hasta 3, `perms.attention_works`) y ▶️ obras de tu nivel que nadie activó → 🏗️;
- 💰 el fondo para oficios 🔒 cerrado con algo que sobra → ⚒️.

Sin nada pendiente dice "✅ Nada espera atención ahora".

## 5. Dónde está en el código

`engine/service/permissions.py` (`PermissionsMixin`: `_camp_can`, la única regla; las pantallas; la armería cerrada; sacar del fondo; los anuncios), con ganchos en `engine/service/game.py` (obras, territorio, solicitudes, el fondo por oficio, el anuncio arriba en 🛡️ Gremio), `engine/service/gremio.py` (invitaciones, solicitudes, espera, 💰 Fondos, ⚔️ Armería, 📢 Chat, 👥 Miembros), `ladder.py` y `permadeath.py` (quien sale pierde sus permisos). Datos en el registro "camp": `perms`, `armory_lock` y `notice`. Números en `content/balance.yaml` → `perms`. Textos `es_permisos.yaml` y `en_permisos.yaml`; ❓ /d69. Pruebas: `tests/test_venta_y_permisos.py`. Mapa de impacto: M15 y C-44.

## 6. Preguntas abiertas

P-303 a P-306 (E-292 a E-295): la lectura de "lo que más requiera atención", la Armería y el fondo abiertos hasta que el fundador los cierra, si el equipo también paga más en el campamento y el castillo, y el 📣 anuncio y sacar del fondo desde cualquier lugar.

## De dónde sale

- *Discord y los servidores de juegos*: roles con permisos sueltos que el dueño reparte uno por uno, en vez de un único cargo que lo puede todo.
- *Albion Online*: los permisos de los cofres y las islas de gremio se dan por persona y por cofre (quién deposita, quién retira).
- *EVE Online*: los roles de corporación separan quién construye, quién saca del hangar y quién acepta gente.
- El propio pedido del dueño: "ver lo que más requiera atención por parte de otros jugadores", para que el fundador no sea el único que destraba el campamento.
