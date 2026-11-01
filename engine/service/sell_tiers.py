"""💱 Selling by tiers: from anywhere at a low price, more at a 🔥 campfire, more in your camp, most in a castle (D-346).

"Prepare a sale where the players can sell directly without having to reach the camp. The items at an estimated price. If
they go to the camp, maybe another price. And at the campfire, another price. Give it levels of importance." The owner's
numbers (31-oct-2026): 30 % of the item's price from anywhere, 50 % at any 🔥 campfire (as before), 60 % in your own camp with
the 🏪 Puesto de trueque, 70 % if your camp is a castle; the remote sale pays at once (the low price is the cost of not
travelling). The tiers live in balance.yaml shop.sell_tiers; every category keeps its own ratio at the campfire (materials,
food and furniture shop.sell_ratio, potions and remedies shop.remedy_sell_ratio, gear shop.sell_ratio) and the other places
scale it by the same factor (tier ÷ the campfire's tier): a potion pays 0.25 at the campfire, 0.15 from anywhere. Where each
thing can be sold keeps the rules of before: the campfire merchant buys materials, food, furniture, potions and remedies (and
the gear, from 🛡️ Equipo); the camp's 🏪 Puesto de trueque buys only materials, never food (it feeds the pantry, D-93); the
camp's 🔨 Forja buys gear like the campfire. Anything a place does not buy is sold "from anywhere" there. Before a remote sale
the player sees what it pays here and at each better place, and confirms.

[ES]
Para qué sirve: la venta por niveles que pidió el dueño (D-346, confirmada el 31-oct-2026: "que los jugadores puedan vender
    directamente sin necesidad de llegar al campamento... a un precio estimado... si van al campamento, otro precio, y si va a
    la fogata, otro precio... dale niveles de importancia"), con sus números: 30 % desde cualquier lugar, 50 % en cualquier
    🔥 fogata (como antes), 60 % en tu campamento con el 🏪 Puesto de trueque y 70 % en un castillo; la venta a distancia paga
    al momento. Cómo se aplicó lo eligió Claude (D-347, provisional): cada categoría conserva su precio de la fogata y los
    demás lugares lo escalan por el mismo factor; cada lugar compra lo mismo que antes; lo que un lugar no compra se vende "a
    distancia" ahí mismo; antes de vender a distancia se ve cuánto pagan aquí y en cada lugar mejor, y se confirma.
    Es parte de GameService (una "mezcla", como BackpackMixin), en su propio archivo para no agrandar game.py.
Documento de diseño: diseno/07-economia/economia.md §3.0.1 (la venta por niveles); diseno/03-personaje/balance.md (registro de
    balance, 0.63)
Módulo: capa de servicios (M13 Economía: el 🛒 mercader, el 🏪 Puesto de trueque y la venta a distancia)
Depende de: content/balance.yaml (shop.sell_ratio, shop.remedy_sell_ratio y shop.sell_tiers; camps.stages para saber si tu
    campamento es castillo), content/camp_upgrades.yaml (el servicio "sell_ratio" del 🏪 Puesto de trueque solo dice que el
    campamento compra; el precio sale de los niveles), content/items.yaml (kind, food, keep, price, code),
    content/locales/es_venta.yaml y en_venta.yaml (textos) y las ayudas de GameService (_upgrades_here, _camp_service,
    _camp_stage_id, _sells_gear_here, _money, _item_list, _gear_name, _merchant_sale, _story_event, _forget_piece)
Lo usan: engine/service/game.py (GameService hereda de esta clase): _sell_price, _shop_sell_view, _sell, _sell_code,
    _camp_sell, _service_uses, _item_view, _sell_gear, _resources_view (💱 Vender), _idle_action (SELL_ACTIONS), text()
    (/v02 desde cualquier lugar) y _faq_values (_sale_faq_values: ❓ /d51 y /d68)
Eventos que publica: ninguno (la venta cuenta para el informe por _story_event "sell", como antes)
Eventos que escucha: ninguno
Datos de los que es dueño: ninguno (no guarda nada: la venta saca de la mochila y suma a Hero.gold)
Reglas que nunca se rompen:
    1. Ningún lugar paga menos que la venta a distancia ni la fogata menos que antes: los precios de la fogata no cambian.
    2. Cada lugar compra lo mismo que antes (D-93: la comida nunca en el 🏪 Puesto de trueque; lo de 💱 Vender materiales nunca
       incluye comida, refinados ni raros, D-109).
    3. La venta a distancia siempre se confirma viendo los precios de los lugares mejores; paga al momento.
    4. El 💱 Comercio (beneficio y 🎓 especialidades) sigue sumando en toda venta (_merchant_sale).
    5. Ningún texto visible se escribe aquí: todo sale de content/locales (es_venta.yaml y en_venta.yaml).
Si cambias esto, revisa:
    - Números: balance.yaml shop.sell_tiers (y sell_ratio, remedy_sell_ratio); el registro de balance (diseno/03-personaje/
      balance.md, 0.63): cuántas monedas entran al juego (un castillo paga 40 % más que antes por los materiales)
    - Pantallas y botones: 📦 Recursos (💱 Vender, 3 botones como mucho), 💱 Vender ("shop_sell": 2 o 3 botones), la
      confirmación ("sell_confirm": 2), la pieza de equipo (4 como mucho), ⚒️ Oficios de 🏘️ Servicios (la línea del 🏪)
    - Mapa de impacto: diseno/01-plataforma/mapa-de-impacto.md (M13 "La venta por niveles" y la cascada C-44)
    - Pruebas: tests/test_venta_y_permisos.py; tests/test_camp_upgrades.py (el 🏪 paga el 60 %), tests/test_gear.py,
      tests/test_service.py, tests/test_fogata_ordenada.py
"""

from __future__ import annotations

from typing import Any

from engine.hero import Hero
from engine.messaging import Action, View
from engine.world import mapgen

# The places of a sale, from the worst to the best (stable ids: the keys of balance.yaml shop.sell_tiers and of the texts
# sale.tier.<id>). [ES] Los lugares de una venta, de menos a más (ids estables: claves de shop.sell_tiers y de los textos).
SALE_TIERS = ("remote", "fire", "camp", "castle")
# Button ids (or prefixes) of the sale anywhere: the 💱 Vender screen, the confirmed remote sale of goods ("sellok:<item>" or
# "sellok:all") and the remote sale of a gear piece (ask "sellgq:<item>", confirmed "sellgok:<item>"). [ES] Solo se agregan.
SELL_ACTIONS = ("sellv", "sellok:", "sellgq:", "sellgok:")


def _remedy_kinds() -> tuple[str, ...]:
    """game.REMEDY_KINDS (potions and remedies: what the merchant buys at shop.remedy_sell_ratio)."""
    from engine.service.game import REMEDY_KINDS          # lazy: game.py imports this module
    return REMEDY_KINDS


class SellTiersMixin:
    """The sale by tiers (D-346, D-347). Mixed into GameService (see the module's header).

    [ES]
    Qué es: los precios de venta según dónde estás (a distancia, fogata, campamento, castillo), la escalera de "dónde rinde
    más" y la confirmación de la venta a distancia.
    Quién la usa: GameService (hereda de esta clase).
    Si cambia, afecta: cuántas monedas entran al juego por ventas y las pantallas de vender (C-44).
    """

    # ------------------------------------------------------------------ numbers

    def _sale_tiers(self) -> dict[str, float]:
        """balance.yaml shop.sell_tiers as {tier: share of the price}; a missing tier is the campfire's (shop.sell_ratio)."""
        shop = self.content.balance["shop"]
        cfg = shop.get("sell_tiers") or {}
        fire = float(cfg.get("fire", shop["sell_ratio"]))
        camp = float(cfg.get("camp", fire))
        return {"remote": float(cfg.get("remote", fire)), "fire": fire, "camp": camp, "castle": float(cfg.get("castle", camp))}

    def _sale_ratio(self, item_id: str, tier: str) -> float:
        """The share of its price one unit pays at this tier, before 💱 Comercio (D-347).

        [ES] Qué hace: el precio de la fogata de cada categoría (materiales, comida, muebles y equipo: shop.sell_ratio; pociones
        y remedios: shop.remedy_sell_ratio) por el factor del lugar (nivel ÷ nivel de la fogata). Con los números de hoy: un
        material 0,30 / 0,50 / 0,60 / 0,70; una poción 0,15 / 0,25 / 0,30 / 0,35. La llaman: _sale_price. Si cambia, afecta:
        todas las ventas al 🛒 mercader, al 🏪 Puesto de trueque, a la 🔨 Forja y a distancia."""
        shop = self.content.balance["shop"]
        kind = self.content.items.get(item_id, {}).get("kind")
        base = float(shop.get("remedy_sell_ratio", shop["sell_ratio"])) if kind in _remedy_kinds() else float(shop["sell_ratio"])
        tiers = self._sale_tiers()
        if tiers["fire"] <= 0:
            return base
        return round(base * tiers.get(tier, tiers["fire"]) / tiers["fire"], 6)

    def _sale_price(self, item_id: str, tier: str) -> int:
        """What one unit pays at this tier before 💱 Comercio: price × _sale_ratio, at least 1 (the campfire's unit price)."""
        price = float(self.content.items.get(item_id, {}).get("price", 1))
        return max(1, int(price * self._sale_ratio(item_id, tier) + 1e-9))

    def _sale_total(self, item_id: str, n: int, tier: str) -> int:
        """What n units pay at this tier before 💱 Comercio (D-347).

        [ES] Qué hace: en la 🔥 fogata, lo de siempre: n × el precio de una (_sale_price, redondeado hacia abajo y al menos 1:
        los precios de la fogata no cambian, regla 1). En los demás lugares se cuenta sobre todo el montón (precio × n × la
        parte del lugar, hacia abajo), porque los recursos de base valen 2 o 3 🥉 y por unidad todos los lugares pagarían 1: con
        el montón, 30 🪵 madera dan 18 a distancia, 30 en la fogata, 36 en tu campamento y 42 en tu castillo. Nunca paga a
        distancia más que la fogata ni en tu campamento o castillo menos que ella. La llaman: todas las ventas y las pantallas
        de vender. Si cambia, afecta: cuántas monedas entran al juego por ventas."""
        if n <= 0:
            return 0
        fire = n * self._sale_price(item_id, "fire")
        if tier == "fire":
            return fire
        price = float(self.content.items.get(item_id, {}).get("price", 1))
        raw = max(1, int(price * n * self._sale_ratio(item_id, tier) + 1e-9))
        return min(fire, raw) if tier == "remote" else max(fire, raw)

    def _sale_pct(self, tier: str) -> int:
        """The tier as the percent the texts show (30, 50, 60, 70): what a material pays there."""
        return round(100 * self._sale_ratio_for_materials(tier))

    def _sale_ratio_for_materials(self, tier: str) -> float:
        tiers = self._sale_tiers()
        base = float(self.content.balance["shop"]["sell_ratio"])
        return base * tiers.get(tier, tiers["fire"]) / tiers["fire"] if tiers["fire"] > 0 else base

    def _sale_faq_values(self) -> dict[str, Any]:
        """{sell_remote}, {sell_fire}, {sell_camp}, {sell_castle} and {remedy_remote} for ❓ Dudas (/d51, /d68)."""
        return {"sell_remote": self._sale_pct("remote"), "sell_fire": self._sale_pct("fire"),
                "sell_camp": self._sale_pct("camp"), "sell_castle": self._sale_pct("castle"),
                "remedy_remote": round(100 * float(self.content.balance["shop"].get("remedy_sell_ratio", 0))
                                       * self._sale_tiers()["remote"] / max(1e-9, self._sale_tiers()["fire"]))}

    # ------------------------------------------------------------------ where, and who buys what

    def _barter_buys(self, item_id: str) -> bool:
        """The camp's 🏪 Puesto de trueque buys materials, never food (it feeds the pantry, D-93)."""
        item = self.content.items.get(item_id, {})
        return item.get("kind") == "material" and not item.get("food")

    def _camp_sale_tier(self, hero: Hero) -> str | None:
        """"camp" or "castle" at the center of your own camp with the 🏪 Puesto de trueque (not busy), else None (D-346)."""
        if hero.activity:
            return None
        here = self._upgrades_here(hero)
        if not here or not self._camp_service(here[0], "sell_ratio"):
            return None
        return "castle" if self._camp_stage_id(int(here[0].get("level", 1))) == "castillo" else "camp"

    def _sale_place(self, hero: Hero) -> str:
        """The best place the hero stands at for selling: "fire" (a 🔥 campfire), "camp"/"castle" (your camp with the 🏪) or
        "remote" (anywhere else, or busy)."""
        if not hero.activity and mapgen.is_bonfire(hero.x, hero.y):
            return "fire"
        return self._camp_sale_tier(hero) or "remote"

    def _sale_tier_here(self, hero: Hero, item_id: str) -> str:
        """The tier this thing sells at where the hero stands: the 🔥 campfire buys everything; your camp's 🏪 its materials
        (🏰 more in a castle) and its 🔨 Forja the gear like the campfire; anything else, "remote" (D-347)."""
        place = self._sale_place(hero)
        if place == "fire":
            return "fire"
        if place in ("camp", "castle") and self._barter_buys(item_id):
            return place
        if self.content.items.get(item_id, {}).get("kind") == "gear" and self._sells_gear_here(hero):
            return "fire"                               # D-101: the 🔨 Forja pays like the campfire
        return "remote"

    @staticmethod
    def _sale_kind(item_id: str, tier: str, gear: bool = False) -> str:
        """The "sale" of _merchant_sale (D-141): gear, the camp's barter, or goods (campfire and remote)."""
        if gear:
            return "gear"
        return "barter" if tier in ("camp", "castle") else "goods"

    # ------------------------------------------------------------------ what the screens show

    def _sale_ladder_lines(self, place: str) -> list[str]:
        """📈 Where your sale pays more: one line per tier, 👉 where you are (the "levels of importance" of D-346).

        [ES] Qué hace: la escalera de lugares (D-346, "dale niveles de importancia"): 🎒 desde cualquier lugar, 🔥 en una fogata,
        🏪 en tu campamento con el Puesto de trueque y 🏰 en tu castillo, cada uno con lo que paga un material, y 👉 delante del
        lugar donde estás (place). Abajo, una línea con qué compra cada lugar. La llama: _shop_sell_view."""
        t = self.texts
        lines = [t.t("sale.ladder_title")]
        for tier in SALE_TIERS:
            mark = t.t("sale.here_mark") if tier == place else t.t("sale.other_mark")
            lines.append(t.t("sale.ladder_line", mark=mark, place=t.t(f"sale.tier.{tier}"), pct=self._sale_pct(tier)))
        lines.append(t.t("sale.ladder_rules"))
        return lines

    def _sale_compare_lines(self, items: dict[str, int], gear: bool = False) -> list[str]:
        """What these things pay at each place, here first (the remote sale's confirmation): "🔥 En una fogata: 60 🥉"."""
        t = self.texts
        lines = []
        for tier in SALE_TIERS:
            if gear and tier in ("camp", "castle"):     # the gear: the campfire or your camp's 🔨 Forja, at the campfire's price
                continue
            if tier in ("camp", "castle") and not all(self._barter_buys(i) for i in items):
                continue
            total = sum(self._sale_total(i, n, tier) for i, n in items.items())
            key = "sale.tier.forge" if gear and tier == "fire" else f"sale.tier.{tier}"
            lines.append(t.t("sale.compare_here" if tier == "remote" else "sale.compare_line", place=t.t(key),
                             total=self._money(total)))
        if not gear and not all(self._barter_buys(i) for i in items):
            lines.append(t.t("sale.compare_no_barter"))
        return lines

    def _sell_confirm_view(self, hero: Hero, items: dict[str, int], ok_id: str, back_id: str, gear: bool = False) -> View:
        """💱 ¿Vender desde aquí?: what you sell, what it pays here and at each better place, ✅ Vender aquí / ↩️ Volver.

        [ES] Qué hace: la confirmación de la venta a distancia (D-346: "antes de confirmar ve lo que recibe aquí y lo que
        recibiría en cada lugar mejor"): la lista de lo que vendes, cuánto pagan aquí (a distancia) y en una fogata, en tu
        campamento con el 🏪 y en un castillo (lo que esos no compran no sale), y que el 💱 Comercio suma. Botones: ✅ Vender aquí
        (N) y ↩️ Volver. La llaman: _sell (💱 Vender materiales y /v02 a distancia) y _sell_gear (una pieza a distancia). Si
        cambia, afecta: tests/test_venta_y_permisos.py."""
        t = self.texts
        here = sum(self._sale_total(i, n, "remote") for i, n in items.items())
        names = (", ".join(self._gear_name(i) for i in items) if gear else self._item_list(items))
        body = [t.t("sale.confirm_intro", items=names), ""] + self._sale_compare_lines(items, gear) + ["", t.t("sale.confirm_trade")]
        actions = [Action(id=ok_id, label=t.t("sale.confirm_button", total=self._money(here))),
                   Action(id=back_id, label=t.t("menu.back"))]
        return View(kind="sell_confirm", title=t.t("sale.confirm_title"), body=body, actions=actions)

    def _sale_action(self, hero: Hero, action_id: str) -> View:
        """Route SELL_ACTIONS (a menu: works anywhere, also while busy, never in a fight: act() routes fights first)."""
        if action_id == "sellv":
            return self._shop_sell_view(hero)
        if action_id.startswith("sellok:"):
            return self._sell(hero, action_id[7:], every=True, confirmed=True)
        if action_id.startswith("sellgq:"):
            return self._sell_gear(hero, action_id[7:])
        if action_id.startswith("sellgok:"):
            return self._sell_gear(hero, action_id[8:], confirmed=True)
        return self._shop_sell_view(hero)
