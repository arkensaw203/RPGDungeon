"""🔑 Camp permissions by code: the founder gives each member exactly what they may do, from 👔 Encargados (D-346; how: D-347).

"Add the permissions and give me the option, through a code, to give permissions to the players: building permissions to one,
specific crafting permissions to another, and so on." And how it must look (1-nov-2026): "from the guild button, a submenu
inside members: a button only the owner sees, 'encargados'; inside, the permission types; then a command with the list of all
the players, and he chooses which player will be each one. With a code." Only the founder grants them: 🛡️ Gremio → 👥 Miembros
→ 👔 Encargados (/encargados) → a permission type (/en1 … /en4) → the list of members, each with a code (/em1 …): the code gives
it, the same code takes it away; for ⚒️ the code opens that member's professions (/pc1 …). /permiso 12345678 (the player code)
shows what a member has. The four permissions:
  🏗️ build   — activate and stop works, choose what is built (the camp's 💰 fund feeds the works it activates) and choose
               where the territory grows (what the 🤝 assistants already do);
  ⚒️ craft   — use the camp's 💰 fund for the professions with the chosen professions only, also while it is 🔒 closed
               (always after the works, with the daily cap);
  ⚔️ armory  — take gear from the ⚔️ Armería while the founder keeps it 🔒 closed, and take materials out of the 💰 fund
               (only what the works and the next level do not need: /fs07);
  👥 people  — accept and invite people (join requests, /inv_, who waits for room) and send 📣 announcements to everyone.
The founder can always do everything; the 🤝 assistants keep their powers (🏗️ and 👥 come with the role). A member who
leaves the camp loses its permissions. Every grant or removal is told to the member in their language. 👔 Encargados also
shows "what waits for attention" (join requests, people waiting for room, works that lack materials, works nobody
activated, the fund for the professions closed): where delegating helps.

[ES]
Para qué sirve: los permisos del campamento que pidió el dueño (D-346, confirmada el 31-oct-2026: "agrega los permisos y que me
    dé la opción a través de un código de darle los permisos a los jugadores: permisos de construcción a uno, permisos de
    crafteos específicos a otro, y así sucesivamente"), con sus respuestas: solo el fundador da permisos, con el código del
    jugador, y son cuatro, uno por uno: 🏗️ Construcción, ⚒️ Oficios específicos, ⚔️ Armería y fondo, 👥 Gente y chat. El
    1-nov-2026 dijo cómo se ve: "desde el botón de gremio, un submenú dentro de miembros: un botón que solamente va a ver el
    dueño, 'encargados'; dentro van a salir los tipos de permiso... con un comando donde van a salir toda la lista de
    jugadores, él va a escoger qué jugador va a ser cada cual. Con un código": 👔 Encargados → /en1 a /en4 → /em1 da o quita. Cómo
    se aplicó lo eligió Claude (D-347, provisional): la ⚔️ Armería y el fondo para oficios siguen abiertos a todos como antes
    hasta que el fundador los cierra (entonces solo entra quien tiene el permiso); sacar del fondo es nuevo (/fs07, solo lo que
    sobra después de las obras); el 📣 anuncio es nuevo (queda arriba en 🛡️ Gremio y llega a todos); y "ver lo que más requiera
    atención por parte de otros jugadores" se leyó como el bloque "👀 Lo que espera atención" de 👔 Encargados.
    Es parte de GameService (una "mezcla", como BackpackMixin), en su propio archivo para no agrandar game.py ni gremio.py.
Documento de diseño: diseno/09-construccion/permisos-del-campamento.md; diseno/08-social/gremios-y-social.md §0
Módulo: capa de servicios (M15 Social: el gremio del campamento; M14 Construcción: quién activa obras)
Depende de: content/balance.yaml (bloque perms; fund_crafts; armory), content/locales/es_permisos.yaml y en_permisos.yaml
    (textos) y las ayudas de GameService y GremioMixin (_member_camp, _guild_camp, _camp_helpers, _camp_member_order,
    _account_by_code, player_code, _hero_name, _codes, _code_target, _push_each, _prof_catalog, _prof_name, _recipes,
    _upgrades, _active_works, _available_works, _upgrade_catalog, _upgrade_need, _camp_perks, _credit_raw, _upgrade_name,
    _fund_surplus, _fund_open, _fund_log, _bag_room, _bag_no_room, _item_list, _resource_code, _members_cap, _guild_view,
    _guild_funds_view, _guild_chat_view, _guild_members_view, _armory_key)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _idle_action (PERM_ACTIONS), text() (/en2, /em3,
    /permiso <código>, /pc3 y /fs07), COMMANDS (/encargados, /permisos), _name_camp (el texto del 📣 anuncio, modo "gnote"), _guild_view (el anuncio arriba), _leave_camp (se van
    los permisos), los ganchos de obras y territorio (_camp_can "build": _grow_view, _grow_camp, _upgrades_view, _works_view,
    _give_to_work, _activate_work, _stop_work, _works_entries, _services_view, _type_page_of, _service_type_view) y de gente
    (_camp_can "people": _answer_join, _guild_view), _station_view, _recipe_view y _make (_fund_pool con el oficio) y
    _faq_values (_perm_faq_values); engine/service/gremio.py (_camp_managers suma a quien tiene 👥; _camp_can en _player_card,
    _camp_members_view, _gremio_invite, _invite_code, _camp_member_view, _camp_requests_view, _waiting_lines,
    _camp_join_waiting; _fund_pool y _fund_pool_lines; _armory_view y _armory_out_code; _guild_funds_view;
    _guild_chat_view; _camp_member_line con _perm_marks); engine/service/ladder.py (_idle_release) y
    engine/service/permadeath.py (_oath_unlink): quien sale pierde sus permisos (_perm_clear)
Eventos que publica: ninguno
Eventos que escucha: ninguno
Datos de los que es dueño (en el registro "camp", clave "x:y"):
    "perms" {cuenta: {"build": bool, "craft": [ids de oficio], "armory": bool, "people": bool}}: lo que el fundador dio a
        cada miembro (claves estables: solo se agregan). Sin la clave, nadie tiene permisos (los campamentos de antes).
    "armory_lock" (bool): la ⚔️ Armería 🔒 cerrada (solo el fundador y quien tiene ⚔️ toman); sin la clave, abierta como antes.
    "notice" {"by", "id", "text", "at"}: el último 📣 anuncio (se ve perms.announce_days días).
    "gremio_codes" (de gremio.py) suma "staff_types" (el orden de /en1), "staff_type" ([el permiso que se está mirando]),
        "staff_members" (el orden de /em1), "perm_target" ([la cuenta de la lista de oficios]) y "perm_craft" (el orden de
        /pc1): solo pantalla. El "fund_log" del fondo suma la línea "take" (quién sacó qué con /fs07).
Reglas que nunca se rompen:
    1. Solo el fundador da y quita permisos, y solo a miembros de su campamento. El fundador siempre puede todo.
    2. Los 🤝 asistentes conservan lo que podían (🏗️ y 👥 por su cargo); un permiso nunca quita nada a nadie.
    3. Quien sale del campamento (🚪 Salir, 30 días sin jugar, 💀 caído) pierde sus permisos; quien no es miembro nunca tiene.
    4. Sacar del 💰 fondo nunca toca lo que les falta a las obras activas y al ⏫ siguiente nivel (D-322: primero las obras) ni
       pasa los topes de la mochila (D-338); cada saque queda en 📜 Quién usó qué.
    5. Cada permiso que se da o se quita se le avisa al miembro en su idioma (_push_each).
    6. Ningún texto visible se escribe aquí: todo sale de content/locales (es_permisos.yaml y en_permisos.yaml).
Si cambias esto, revisa:
    - Números: balance.yaml perms (announce_days, announce_max_chars, attention_works)
    - Pantallas y botones (D-75: 4 como mucho): 👔 Encargados ("camp_staff", 2), un tipo de permiso ("camp_staff_type", 1),
      ⚒️ Oficios de un miembro ("camp_perm_craft", 3), lo que tiene un miembro ("camp_perm_card", 2), 👥 Miembros (👔 solo para
      el fundador: 4 como mucho), ⚔️ Armería (2), 📢 Chat (3 con 📣); los códigos /en, /em, /pc, /fs y /permiso no pueden
      chocar con los de antes
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M15 "Los permisos del campamento" y la cascada C-44)
    - Pruebas: tests/test_venta_y_permisos.py; tests/test_ayudantes.py, tests/test_armeria.py, tests/test_fondo_para_oficios.py,
      tests/test_submenus_campamento_gremio.py
"""

from __future__ import annotations

import re
from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View

# The permissions a founder can give, in the order of the 👔 Encargados list (/en1 … /en4; stable ids: keys of
# camp["perms"][account] and of the texts perm.<id>.*). [ES] Los cuatro permisos (ids estables: solo se agregan).
PERM_KEYS = ("build", "craft", "armory", "people")
# Button ids (or prefixes): 👔 Encargados ("staff"; "perms" is its old name), one permission type ("stf:<key>"), a member's
# read-only card ("perm:<account>"), the ⚒️ professions of a member ("permc:<account>", all "permca:<account>", none
# "permcn:<account>"), 🔒/🔓 the armory ("armlock") and 📣 Anuncio ("gnote"). [ES] Ids de botón: solo se agregan (64 bytes como
# mucho en Telegram).
PERM_ACTIONS = ("staff", "stf:", "perms", "perm:", "permc:", "permca:", "permcn:", "armlock", "gnote")
# /en2: open the 2nd permission type of 👔 Encargados (/en1 🏗️, /en2 ⚒️, /en3 ⚔️, /en4 👥). [ES] El tipo de permiso.
STAFF_TYPE_RE = re.compile(r"^/en_?(\d{1,2})(@\w+)?$")
# /em3: the 3rd member of the last permission-type list: gives that permission, or takes it if they have it (⚒️: opens their
# professions). [ES] El miembro de la lista: da el permiso o, si ya lo tiene, se lo quita.
STAFF_MEMBER_RE = re.compile(r"^/em_?(\d{1,2})(@\w+)?$")
# /permiso 12345678, /permiso_12345678 (tappable), /permission 12345678: what that member has (read-only). [ES] El código de jugador.
PERM_CODE_RE = re.compile(r"^/(?:permiso|permisos|permission|permissions|perm)[_\s]*(\d{4,16})(@\w+)?$")
# /pc3: give or take the 3rd profession of the last ⚒️ list for the member being edited. [ES] Un oficio de la lista.
PERM_CRAFT_RE = re.compile(r"^/pc_?(\d{1,2})(@\w+)?$")
# /fs07: take out of the camp's 💰 fund what is left of the resource with code 7 (⚔️ permission). [ES] Sacar del fondo.
FUND_TAKE_RE = re.compile(r"^/fs_?(\d{1,3})(@\w+)?$")


class PermissionsMixin:
    """🔑 The camp's permissions, the armory's lock, taking from the fund and 📣 announcements (D-346, D-347).

    [ES]
    Qué es: quién puede hacer qué en un campamento además del fundador y los 🤝 asistentes, y las pantallas para darlo.
    Quién la usa: GameService (hereda de esta clase); gremio.py, ladder.py y permadeath.py usan sus ayudas.
    Si cambia, afecta: quién activa obras, usa el fondo, toma de la armería, acepta gente y manda anuncios (C-44).
    """

    # ------------------------------------------------------------------ data and the one rule everybody asks

    def _perm_cfg(self) -> dict[str, Any]:
        """balance.yaml "perms" (announce_days, announce_max_chars, attention_works)."""
        return self.content.balance.get("perms") or {}

    @staticmethod
    def _perm_record(camp: dict[str, Any] | None, account: str) -> dict[str, Any]:
        """What the founder gave this member ({} for anyone else, and for whoever is no longer a member)."""
        if not camp or account not in camp.get("members", []):
            return {}
        return dict((camp.get("perms") or {}).get(account) or {})

    def _camp_can(self, camp: dict[str, Any] | None, account: str, perm: str, pid: str | None = None) -> bool:
        """Whether this member may do `perm` ("build", "craft" [for profession pid], "armory" or "people") in the camp.

        [ES] Qué hace: la única regla de los permisos (D-346): el fundador siempre; un 🤝 asistente, 🏗️ y 👥 por su cargo (lo que
        ya podía, D-289, D-304); cualquier otro miembro, lo que le dio el fundador ("perms"); ⚒️ con un oficio, solo si ese
        oficio está en su lista. Quien no es miembro, nada. La llaman: los ganchos de obras, territorio, gente, fondo y armería
        (ver "Lo usan"). Si cambia, afecta: todo lo que se puede delegar."""
        if not camp or account not in camp.get("members", []):
            return False
        if account == camp.get("founder_id"):
            return True
        if perm in ("build", "people") and account in self._camp_helpers(camp):
            return True
        record = self._perm_record(camp, account)
        if perm == "craft":
            crafts = list(record.get("craft") or [])
            return (pid in crafts) if pid else bool(crafts)
        return bool(record.get(perm))

    def _camp_people(self, camp: dict[str, Any]) -> list[str]:
        """The members with 👥 Gente y chat given by the founder (not the founder nor the helpers: they come first)."""
        helpers = set(self._camp_helpers(camp))
        return [m for m in camp.get("members", []) if m != camp.get("founder_id") and m not in helpers
                and self._perm_record(camp, m).get("people")]

    @staticmethod
    def _perm_clear(camp: dict[str, Any], account: str) -> None:
        """Whoever leaves the camp loses its permissions (rule 3; the caller saves the camp)."""
        perms = camp.get("perms")
        if perms and account in perms:
            perms.pop(account, None)

    def _perm_marks(self, camp: dict[str, Any], account: str) -> str:
        """"🏗️⚒️ ": the icons of what the founder gave this member (👥 Miembros and the 🔑 list); "" for nothing."""
        record = self._perm_record(camp, account)
        icons = [self.texts.t(f"perm.{key}.icon") for key in PERM_KEYS if record.get(key)]   # ⚒️: a non-empty list
        return ("".join(icons) + " ") if icons else ""

    def _perm_professions(self) -> list[str]:
        """The professions whose recipes can use the fund, refining and crafting first, then the gathering ones (🎒 backpacks)."""
        catalog = self._prof_catalog()
        with_recipes = {rdef["profession"] for rdef in self._recipes().values()}
        order = {"refine": 0, "craft": 1, "gather": 2}
        pids = [pid for pid in catalog if pid in with_recipes and catalog[pid].get("branch") in order]
        return sorted(pids, key=lambda pid: (order[catalog[pid]["branch"]], list(catalog).index(pid)))

    def _fund_perm_profs(self, camp: dict[str, Any] | None, account: str) -> set[str]:
        """The professions this member may use the 🔒 closed fund with: {"*"} for the founder, its ⚒️ list for the others."""
        if not camp or account not in camp.get("members", []):
            return set()
        if account == camp.get("founder_id"):
            return {"*"}
        return set(self._perm_record(camp, account).get("craft") or [])

    def _perm_faq_values(self) -> dict[str, Any]:
        """{announce_days} for ❓ Dudas (/d69)."""
        return {"announce_days": int(self._perm_cfg().get("announce_days", 7))}

    # ------------------------------------------------------------------ routing

    def _perm_action(self, hero: Hero, action_id: str) -> View:
        """Route PERM_ACTIONS (menus: also while busy; a fight takes the buttons first in act())."""
        if action_id in ("staff", "perms"):
            return self._staff_view(hero)
        if action_id == "armlock":
            return self._armory_lock_toggle(hero)
        if action_id == "gnote":
            return self._gnote_ask(hero)
        if action_id.startswith("stf:"):
            return self._staff_type_view(hero, action_id[4:])
        if action_id.startswith("permca:"):
            return self._perm_craft_all(hero, action_id[7:], True)
        if action_id.startswith("permcn:"):
            return self._perm_craft_all(hero, action_id[7:], False)
        if action_id.startswith("permc:"):
            return self._perm_craft_view(hero, action_id[6:])
        if action_id.startswith("perm:"):
            return self._perm_card_view(hero, action_id[5:])
        return self._staff_view(hero)

    # ------------------------------------------------------------------ 👔 Encargados (only the founder)

    def _staff_refusal(self, hero: Hero) -> View | None:
        """None for the founder of a camp; for anyone else, the screen that refuses (👔 Encargados is only the founder's)."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero, notice=t.t("perm.no_camp"))
        if camp.get("founder_id") != hero.id:
            marks = self._perm_marks(camp, hero.id).strip()
            return self._guild_members_view(hero, notice=self._join([t.t("perm.only_founder"),
                                                                       t.t("perm.yours", marks=marks or t.t("perm.none_short"))]))
        return None

    def _staff_holders(self, camp: dict[str, Any], key: str) -> str:
        """Who has this permission now: "Bram, Dax (🔨 🍲)"; the 🤝 assistants with 🏗️ and 👥 marked "por su cargo"."""
        t = self.texts
        names = []
        for account in camp.get("members", []):
            if account == camp.get("founder_id"):
                continue
            record = self._perm_record(camp, account)
            if key == "craft":
                crafts = [pid for pid in record.get("craft") or [] if pid in self._prof_catalog()]
                if crafts:
                    names.append(t.t("perm.holder_crafts", name=self._hero_name(account),
                                     icons=" ".join(self._prof_catalog()[pid].get("emoji", "") for pid in crafts)))
            elif key in ("build", "people") and account in self._camp_helpers(camp):
                names.append(t.t("perm.holder_role", name=self._hero_name(account)))
            elif record.get(key):
                names.append(self._hero_name(account))
        return ", ".join(names) if names else t.t("perm.none_short")

    def _attention_lines(self, camp: dict[str, Any], hero: Hero) -> list[str]:
        """👀 Lo que espera atención: where delegating helps (D-347, the reading of "lo que más requiera atención").

        [ES] Qué hace: la lectura de "de ver lo que más requiera atención por parte de otros jugadores" (D-347, provisional): las
        cosas del campamento que esperan a alguien, cada una con el permiso que ayuda: 🙋 solicitudes para entrar y ⏳ quienes
        esperan lugar (👥), obras activas que esperan materiales y obras de tu nivel que nadie activó (🏗️), y el fondo para
        oficios 🔒 cerrado con algo que sobra (⚒️). Sin nada, una línea que lo dice. La llama: _staff_view. Si cambia, afecta:
        tests/test_venta_y_permisos.py."""
        t = self.texts
        key = f"{camp['x']}:{camp['y']}"
        record = self._upgrades(key)
        lines: list[str] = []
        requests = camp.get("requests") or []
        if requests:
            lines.append(t.t("perm.att_requests", n=len(requests)))
        waiting = camp.get("waiting") or []
        if waiting:
            lines.append(t.t("perm.att_waiting", n=len(waiting), room=max(0, self._members_cap(camp) - len(camp["members"]))))
        catalog = self._upgrade_catalog()
        perks = self._camp_perks(camp, hero)
        lacking = []
        for uid in self._active_works(camp, record):
            if uid not in catalog:
                continue
            need = self._upgrade_need(catalog[uid], perks, record, uid)
            progress = dict(record["works"].get(uid, {}))
            self._credit_raw(need, progress)
            if any(int(progress.get(k, 0)) < int(n) for k, n in need.items()):
                lacking.append(uid)
        shown = max(1, int(self._perm_cfg().get("attention_works", 3)))
        if lacking:
            names = ", ".join(self._upgrade_name(uid) for uid in lacking[:shown]) + ("…" if len(lacking) > shown else "")
            lines.append(t.t("perm.att_works", n=len(lacking), names=names))
        idle = self._available_works(camp, record)
        if idle:
            lines.append(t.t("perm.att_idle", n=len(idle)))
        if not self._fund_open(record) and self._fund_surplus(camp, record, hero):
            lines.append(t.t("perm.att_fund"))
        return lines or [t.t("perm.att_none")]

    def _staff_view(self, hero: Hero, notice: str | None = None) -> View:
        """👔 Encargados: the four permission types with who has each (codes /en1…/en4), the armory's lock and what waits.

        [ES] Qué hace: la pantalla que pidió el dueño el 1-nov-2026 ("desde el botón de gremio, un submenú dentro de miembros: un
        botón que solamente va a ver el dueño, 'encargados'; dentro van a salir los tipos de permiso"): solo para el fundador.
        Cada tipo de permiso en una línea con su código (/en1 🏗️ Construcción, /en2 ⚒️ Oficios, /en3 ⚔️ Armería y fondo, /en4 👥
        Gente y chat) y quién lo tiene ahora (los 🤝 asistentes con 🏗️ y 👥 "por su cargo"); tocar el código abre la lista de
        miembros de ese tipo (_staff_type_view). Debajo, si la ⚔️ Armería está abierta o cerrada y "👀 Lo que espera atención"
        (_attention_lines). Botones (D-75, 2): 🔒 Cerrar / 🔓 Abrir la armería y ↩️ Volver a 👥 Miembros. A cualquier otro, la
        negativa (_staff_refusal). La llaman: 👔 Encargados de 👥 Miembros ("staff"), /permisos y los ↩️ de cada tipo. Si cambia,
        afecta: tests/test_venta_y_permisos.py."""
        t = self.texts
        refusal = self._staff_refusal(hero)
        if refusal:
            return refusal
        camp = self._member_camp(hero)
        body = [t.t("perm.staff_intro", camp=camp["name"]), ""]
        for n, key in enumerate(PERM_KEYS, 1):
            body.append(t.t("perm.staff_line", code=f"/en{n}", icon=t.t(f"perm.{key}.icon"), name=t.t(f"perm.{key}.name"),
                            who=self._staff_holders(camp, key)))
        body += ["", t.t("perm.staff_hint"), t.t("perm.helpers_note"),
                 "", t.t("perm.armory_locked" if camp.get("armory_lock") else "perm.armory_open"), "", t.t("perm.att_title")]
        body += self._attention_lines(camp, hero)
        self._codes(hero, "staff_types", list(PERM_KEYS))
        actions = [Action(id="armlock", label=t.t("perm.unlock_button" if camp.get("armory_lock") else "perm.lock_button")),
                   Action(id="gmembers", label=t.t("menu.back"))]
        return View(kind="camp_staff", title=t.t("perm.staff_title"), body=body, actions=actions, notice=notice)

    def _staff_type_view(self, hero: Hero, key: str, notice: str | None = None) -> View:
        """One permission type: what it lets do and every member with a code /em1 (✅ has it, ▫️ not; ⚒️ with its professions).

        [ES] Qué hace: "con un comando que va a haber dentro, donde van a salir toda la lista de jugadores, él va a escoger qué
        jugador va a ser cada cual. Con un código" (el dueño, 1-nov-2026): qué deja hacer el permiso y todos los miembros (menos
        el fundador), cada uno con su código /em1, ✅ si lo tiene y ▫️ si no; un 🤝 asistente con 🏗️ o 👥 sale "por su cargo".
        Tocar el código lo da o, si ya lo tiene, se lo quita (_staff_member_code); en ⚒️ Oficios abre la lista de oficios de ese
        miembro (_perm_craft_view). Botones: ↩️ Volver a 👔 Encargados. Solo el fundador. La llaman: /en1 … /en4
        (_staff_type_code), "stf:<permiso>" y el ↩️ de la lista de oficios. Si cambia, afecta: tests/test_venta_y_permisos.py."""
        t = self.texts
        refusal = self._staff_refusal(hero)
        if refusal:
            return refusal
        if key not in PERM_KEYS:
            return self._staff_view(hero)
        camp = self._member_camp(hero)
        members = [m for m in self._camp_member_order(hero, camp) if m != hero.id]
        body = [t.t("perm.type_title", icon=t.t(f"perm.{key}.icon"), name=t.t(f"perm.{key}.name")),
                t.t(f"perm.{key}.help"), ""]
        for n, account in enumerate(members, 1):
            body.append(self._staff_member_line(camp, key, n, account))
        if not members:
            body.append(t.t("perm.list_alone"))
        else:
            body += ["", t.t("perm.type_hint_craft" if key == "craft" else "perm.type_hint")]
        self._codes(hero, "staff_type", [key])
        self._codes(hero, "staff_members", members)
        return View(kind="camp_staff_type", title=t.t("perm.staff_title"), body=body, notice=notice,
                    actions=[Action(id="staff", label=t.t("menu.back"))])

    def _staff_member_line(self, camp: dict[str, Any], key: str, n: int, account: str) -> str:
        """"/em2 ✅ Bram" · "/em3 🤝 Cora (por su cargo)" · "/em4 Dax: 🔨 🍲" (⚒️): one member of a permission-type list."""
        t = self.texts
        name = self._hero_name(account)
        record = self._perm_record(camp, account)
        if key == "craft":
            crafts = [pid for pid in record.get("craft") or [] if pid in self._prof_catalog()]
            icons = " ".join(self._prof_catalog()[pid].get("emoji", "") for pid in crafts) if crafts else t.t("perm.none_short")
            return t.t("perm.member_crafts", code=f"/em{n}", name=name, icons=icons)
        if key in ("build", "people") and account in self._camp_helpers(camp):
            return t.t("perm.member_role", code=f"/em{n}", name=name)
        mark = t.t("perm.on_mark") if record.get(key) else t.t("perm.off_mark")
        return t.t("perm.member_line", code=f"/em{n}", mark=mark, name=name)

    def _staff_type_code(self, hero: Hero, n: int) -> View:
        """/en2: the 2nd permission type of 👔 Encargados (the order of PERM_KEYS)."""
        refusal = self._staff_refusal(hero)
        if refusal:
            return refusal
        if not 1 <= n <= len(PERM_KEYS):
            return self._staff_view(hero, notice=self.texts.t("perm.bad_code"))
        return self._staff_type_view(hero, PERM_KEYS[n - 1])

    def _staff_member_code(self, hero: Hero, n: int) -> View:
        """/em3: give the shown permission to the 3rd member of the list, or take it if they have it (⚒️: their professions).

        [ES] Qué hace: el código de un miembro en la lista de un tipo de permiso (el dueño: "él va a escoger qué jugador va a ser
        cada cual. Con un código"): si no lo tiene, se lo da; si lo tiene, se lo quita (el aviso dice cuál de las dos pasó y al
        miembro le llega en su idioma). Un 🤝 asistente ya tiene 🏗️ y 👥 por su cargo: no cambia nada y lo dice. En ⚒️ Oficios
        abre la lista de oficios de ese miembro (/pc1). Un código que no está en la última lista: aviso. La llama: text() con
        STAFF_MEMBER_RE. Si cambia, afecta: tests/test_venta_y_permisos.py."""
        t = self.texts
        refusal = self._staff_refusal(hero)
        if refusal:
            return refusal
        key = self._code_target(hero, "staff_type", 1)
        account = self._code_target(hero, "staff_members", n)
        if key not in PERM_KEYS or account is None:
            return self._staff_view(hero, notice=t.t("perm.bad_code"))
        camp, refusal_key = self._perm_target(hero, account)
        if refusal_key:
            return self._staff_type_view(hero, key, notice=t.t(refusal_key, name=self._hero_name(account)))
        if key == "craft":
            return self._perm_craft_view(hero, account)
        if key in ("build", "people") and account in self._camp_helpers(camp):
            return self._staff_type_view(hero, key, notice=t.t("perm.by_role_notice", name=self._hero_name(account),
                                                                icon=t.t(f"perm.{key}.icon"), perm=t.t(f"perm.{key}.name")))
        return self._perm_toggle(hero, account, key)

    def _perm_state_lines(self, camp: dict[str, Any], account: str) -> list[str]:
        """One line per permission: ✅ / ▫️ (⚒️ with its professions), and the 🤝 line for an assistant."""
        t = self.texts
        record = self._perm_record(camp, account)
        helper = account in self._camp_helpers(camp)
        lines = []
        for key in PERM_KEYS:
            if key == "craft":
                crafts = [pid for pid in record.get("craft") or [] if pid in self._prof_catalog()]
                state = ", ".join(self._prof_name(pid) for pid in crafts) if crafts else t.t("perm.state_no")
            else:
                state = t.t("perm.state_yes") if record.get(key) else (t.t("perm.by_role") if helper and key in ("build", "people")
                                                                  else t.t("perm.state_no"))
            lines.append(t.t("perm.state_line", icon=t.t(f"perm.{key}.icon"), name=t.t(f"perm.{key}.name"), state=state))
        if helper:
            lines.append(t.t("perm.helper_line"))
        return lines

    def _perm_target(self, hero: Hero, account: str) -> tuple[dict[str, Any] | None, str | None]:
        """(camp, refusal key): the founder editing a member of its own camp, or why not."""
        camp = self._member_camp(hero)
        if not camp:
            return None, "perm.no_camp"
        if camp.get("founder_id") != hero.id:
            return camp, "perm.only_founder"
        if account == hero.id:
            return camp, "perm.self"
        if account not in camp.get("members", []):
            return camp, "perm.not_member"
        return camp, None

    def _perm_card_view(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """What a member has, read-only (/permiso <player code>): to give or take, 👔 Encargados → the type → their code."""
        t = self.texts
        refusal = self._staff_refusal(hero)
        if refusal:
            return refusal
        camp, refusal_key = self._perm_target(hero, account)
        if refusal_key:
            return self._staff_view(hero, notice=t.t(refusal_key, name=self._hero_name(account)))
        body = [t.t("perm.card_title", name=self._hero_name(account), code=f"/permiso_{self.player_code(account)}"), ""]
        body += self._perm_state_lines(camp, account) + ["", t.t("perm.card_hint")]
        return View(kind="camp_perm_card", title=t.t("perm.staff_title"), body=body, notice=notice,
                    actions=[Action(id="staff", label=t.t("perm.staff_button")), Action(id="gmembers", label=t.t("menu.back"))])

    def _perm_save(self, camp: dict[str, Any], account: str, record: dict[str, Any]) -> None:
        """Keep a member's record (an empty one is removed) and save the camp."""
        perms = dict(camp.get("perms") or {})
        clean = {k: v for k, v in record.items() if v}
        if clean:
            perms[account] = clean
        else:
            perms.pop(account, None)
        camp["perms"] = perms
        self.store.put("camp", f"{camp['x']}:{camp['y']}", camp)

    def _perm_tell(self, camp: dict[str, Any], account: str, key: str, granted: bool, pids: list[str] | None = None) -> None:
        """The member hears it in its own language (rule 5): what was given or taken and what it lets them do."""
        t = self.texts
        camp_name = camp["name"]

        def build() -> View:
            what = (t.t("perm.push_crafts", items=", ".join(self._prof_name(pid) for pid in pids or []))
                    if key == "craft" else t.t(f"perm.{key}.help"))
            line = t.t("perm.push_given" if granted else "perm.push_taken", camp=camp_name, icon=t.t(f"perm.{key}.icon"),
                       name=t.t(f"perm.{key}.name"))
            return View(kind="gremio_news", title=t.t("perm.title"), body=[line, what],
                        actions=[Action(id="guild", label=t.t("gremio.button"))])

        self._push_each([account], build)

    def _perm_toggle(self, hero: Hero, account: str, key: str) -> View:
        """Give 🏗️, ⚔️ or 👥 to a member, or take it if they have it (the founder only); the member is told; back to the type."""
        t = self.texts
        camp, refusal = self._perm_target(hero, account)
        if refusal or key not in PERM_KEYS or key == "craft":
            return self._staff_view(hero, notice=t.t(refusal, name=self._hero_name(account)) if refusal else None)
        record = self._perm_record(camp, account)
        granted = not record.get(key)
        record[key] = granted
        self._perm_save(camp, account, record)
        self._perm_tell(camp, account, key, granted)
        notice = t.t("perm.given" if granted else "perm.taken", name=self._hero_name(account), icon=t.t(f"perm.{key}.icon"),
                     perm=t.t(f"perm.{key}.name"))
        return self._staff_type_view(hero, key, notice=notice)

    def _perm_craft_view(self, hero: Hero, account: str, notice: str | None = None) -> View:
        """⚒️ Oficios of a member: every profession with recipes, ✅ / ▫️, each with its code /pc1 to give or take it.

        [ES] Qué hace: la lista de oficios del permiso ⚒️ para un miembro (D-346: "permisos de crafteos específicos", "solo
        🔨 Herrería y 🍲 Cocina"): primero el refinado y la fabricación, después la recolección (sus 🎒 mochilas), cada uno con ✅
        si lo tiene y su código /pc1 (tocarlo lo da o lo quita; _perm_craft_code). Botones: ✅ Todos, ✖️ Ninguno y ↩️ Volver a
        la lista de ⚒️ Oficios de 👔 Encargados (3, D-75). Solo el fundador. La llaman: el código del miembro en ⚒️ Oficios
        (/em1), "permc:<cuenta>" y los códigos /pc. Si cambia, afecta: tests/test_venta_y_permisos.py."""
        t = self.texts
        camp, refusal = self._perm_target(hero, account)
        if refusal:
            return self._staff_view(hero, notice=t.t(refusal, name=self._hero_name(account)))
        crafts = set(self._perm_record(camp, account).get("craft") or [])
        pids = self._perm_professions()
        self._codes(hero, "perm_target", [account])
        self._codes(hero, "perm_craft", pids)
        name = self._hero_name(account)
        body = [t.t("perm.craft_intro", name=name), ""]
        body += [t.t("perm.craft_line", code=f"/pc{n}", mark=t.t("perm.on_mark") if pid in crafts else t.t("perm.off_mark"),
                     name=self._prof_name(pid)) for n, pid in enumerate(pids, 1)]
        body += ["", t.t("perm.craft_hint")]
        actions = [Action(id=f"permca:{account}", label=t.t("perm.craft_all_button")),
                   Action(id=f"permcn:{account}", label=t.t("perm.craft_none_button")),
                   Action(id="stf:craft", label=t.t("menu.back"))]
        return View(kind="camp_perm_craft", title=t.t("perm.craft_title"), body=body, actions=actions, notice=notice)

    def _perm_craft_set(self, hero: Hero, account: str, pids: list[str], on: bool) -> View:
        """Give (on) or take these professions of ⚒️ for a member; the member is told what changed."""
        t = self.texts
        camp, refusal = self._perm_target(hero, account)
        if refusal:
            return self._staff_view(hero, notice=t.t(refusal, name=self._hero_name(account)))
        record = self._perm_record(camp, account)
        crafts = [pid for pid in record.get("craft") or [] if pid in self._prof_catalog()]
        changed = [pid for pid in pids if (pid not in crafts) == on]
        if not changed:
            return self._perm_craft_view(hero, account)
        crafts = [pid for pid in self._perm_professions() if (pid in crafts or pid in changed)] if on else \
            [pid for pid in crafts if pid not in changed]
        record["craft"] = crafts
        self._perm_save(camp, account, record)
        self._perm_tell(camp, account, "craft", on, changed)
        notice = t.t("perm.craft_given" if on else "perm.craft_taken", name=self._hero_name(account),
                     items=", ".join(self._prof_name(pid) for pid in changed))
        return self._perm_craft_view(hero, account, notice=notice)

    def _perm_craft_all(self, hero: Hero, account: str, on: bool) -> View:
        """✅ Todos / ✖️ Ninguno of the ⚒️ list."""
        return self._perm_craft_set(hero, account, self._perm_professions(), on)

    def _perm_craft_code(self, hero: Hero, n: int) -> View:
        """/pc3: give or take the 3rd profession of the last ⚒️ list, for the member it was showing."""
        t = self.texts
        refusal = self._staff_refusal(hero)
        if refusal:
            return refusal
        target = self._code_target(hero, "perm_target", 1)
        pid = self._code_target(hero, "perm_craft", n)
        if target is None or pid is None:
            return self._staff_view(hero, notice=t.t("perm.bad_code"))
        camp, refusal_key = self._perm_target(hero, target)
        if refusal_key:
            return self._staff_view(hero, notice=t.t(refusal_key, name=self._hero_name(target)))
        on = pid not in (self._perm_record(camp, target).get("craft") or [])
        return self._perm_craft_set(hero, target, [pid], on)

    def _perm_code(self, hero: Hero, code: str) -> View:
        """/permiso 12345678: the founder sees what that member has (a code that is nobody's, or not a member: says so)."""
        t = self.texts
        account = self._account_by_code(code)
        if account is None:
            refusal = self._staff_refusal(hero)
            return refusal or self._staff_view(hero, notice=t.t("gremio.code_unknown", code=code))
        return self._perm_card_view(hero, account)

    # ------------------------------------------------------------------ ⚔️ the armory's lock and 📤 taking from the fund

    def _armory_open_for(self, hero: Hero) -> bool:
        """Whether the hero may take from its guild's ⚔️ Armería: open (as before), or 🔒 with ⚔️ (or being the founder)."""
        key = self._armory_key(hero)
        if not key or ":" not in key:                   # before founding the guild's armory is always open
            return True
        camp = self.store.get("camp", key)
        if not camp or not camp.get("armory_lock"):
            return True
        return self._camp_can(camp, hero.id, "armory")

    def _armory_lock_toggle(self, hero: Hero) -> View:
        """🔒 Cerrar / 🔓 Abrir la armería: only the founder; closed, only who has ⚔️ takes (leaving pieces is always open)."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_view(hero, notice=t.t("perm.no_camp"))
        if camp.get("founder_id") != hero.id:
            return self._armory_view(hero, notice=t.t("perm.only_founder"))
        camp["armory_lock"] = not camp.get("armory_lock")
        self.store.put("camp", f"{camp['x']}:{camp['y']}", camp)
        return self._armory_view(hero, notice=t.t("perm.locked" if camp["armory_lock"] else "perm.unlocked"))

    def _fund_take_code(self, hero: Hero, code: int) -> View:
        """/fs07: take out of the camp's 💰 fund what is left of that resource after the works (⚔️ or the founder).

        [ES] Qué hace: con el permiso ⚔️ (o siendo el fundador) saca del fondo del campamento lo que sobra de ese recurso (el
        mismo código /07 de 📦 Recursos) después de lo que les falta a las obras activas y al ⏫ siguiente nivel (_fund_surplus,
        D-322), hasta lo que cabe en la mochila (_bag_room, D-338); queda en 📜 Quién usó qué ("take"). Desde cualquier lugar,
        como depositar. La llama: text() con FUND_TAKE_RE. Si cambia, afecta: tests/test_venta_y_permisos.py."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp:
            return self._guild_funds_view(hero, notice=t.t("perm.no_camp"))
        if not self._camp_can(camp, hero.id, "armory"):
            return self._guild_funds_view(hero, notice=t.t("perm.take_no_rights"))
        item_id = next((i for i, item in self.content.items.items() if item.get("code") == code), None)
        if item_id is None:
            return self._guild_funds_view(hero, notice=t.t("resources.no_code", code=f"/{code:02d}"))
        key = f"{camp['x']}:{camp['y']}"
        record = self._upgrades(key)
        free = int(self._fund_surplus(camp, record, hero).get(item_id, 0))
        if free <= 0:
            return self._guild_funds_view(hero, notice=t.t("perm.take_none", item=self._item_label(item_id)))
        room = self._bag_room(hero, item_id)
        if room <= 0:
            return self._guild_funds_view(hero, notice=self._bag_no_room(hero, item_id))
        n = min(free, room)
        fund = record["fund"]
        fund[item_id] = int(fund.get(item_id, 0)) - n
        if fund[item_id] <= 0:
            del fund[item_id]
        hero.backpack[item_id] = hero.backpack.get(item_id, 0) + n
        self._fund_log(record, "take", hero, items={item_id: n})
        self.store.put("upgrades", key, record)
        return self._guild_funds_view(hero, notice=t.t("perm.took", items=self._item_list({item_id: n})))

    def _fund_take_lines(self, camp: dict[str, Any], hero: Hero) -> list[str]:
        """The 📤 line of 💰 Fondos for who may take from the fund (⚔️ or the founder): how, and that the works go first."""
        return [self.texts.t("perm.take_hint")] if self._camp_can(camp, hero.id, "armory") else []

    # ------------------------------------------------------------------ 📣 announcements (👥 Gente y chat)

    def _gnote_ask(self, hero: Hero) -> View:
        """📣 Anuncio: the next text is pinned on top of 🛡️ Gremio and sent to every member (the founder, 🤝 or 👥)."""
        t = self.texts
        camp = self._member_camp(hero)
        if not camp or not self._camp_can(camp, hero.id, "people"):
            return self._guild_chat_view(hero, notice=t.t("perm.note_no_rights"))
        self.store.put("camp_naming", hero.id, {"mode": "gnote", "x": hero.x, "y": hero.y})
        return View(kind="gremio_msg", title=t.t("perm.note_title"),
                    body=[t.t("perm.note_ask", n=int(self._perm_cfg().get("announce_max_chars", 300)),
                              days=int(self._perm_cfg().get("announce_days", 7)))], expects_text=True,
                    actions=[Action(id="gchat", label=t.t("gremio.cancel"))])

    def _gnote_post(self, hero: Hero, text: str) -> View:
        """Pin the 📣 announcement (cut to perms.announce_max_chars) and push it to every other member in their language."""
        t = self.texts
        self.store.delete("camp_naming", hero.id)
        camp = self._member_camp(hero)
        if not camp or not self._camp_can(camp, hero.id, "people"):
            return self._guild_chat_view(hero, notice=t.t("perm.note_no_rights"))
        text = " ".join(text.split())
        if not text:
            return self._gnote_ask(hero)
        cap = max(1, int(self._perm_cfg().get("announce_max_chars", 300)))
        if len(text) > cap:
            text = text[:max(1, cap - 1)].rstrip() + "…"
        camp["notice"] = {"by": hero.name, "id": hero.id, "text": text, "at": self.clock.now()}
        self.store.put("camp", f"{camp['x']}:{camp['y']}", camp)
        name = camp["name"]
        others = [m for m in camp["members"] if m != hero.id]
        self._push_each(others, lambda: View(kind="gremio_message", title=t.t("perm.note_push_title", name=name),
                                             body=[t.t("perm.note_line", name=hero.name, text=text)],
                                             actions=[Action(id="guild", label=t.t("gremio.button"))]))
        return self._guild_chat_view(hero, notice=t.t("perm.note_sent", n=len(others)))

    def _gnote_lines(self, camp: dict[str, Any] | None) -> list[str]:
        """The 📣 line on top of 🛡️ Gremio and 📢 Chat while the announcement is newer than perms.announce_days."""
        note = (camp or {}).get("notice") or {}
        if not note.get("text"):
            return []
        days = float(self._perm_cfg().get("announce_days", 7))
        if self.clock.now() - float(note.get("at", 0.0)) > self._seconds(days * 24 * 60):
            return []
        return [self.texts.t("perm.note_line", name=note.get("by", "?"), text=note["text"])]
