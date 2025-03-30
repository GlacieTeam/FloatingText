from endstone.plugin import Plugin
from typing import TypedDict
from binarystream import BinaryStream
import random, json, os, importlib.util

if importlib.util.find_spec("endstone_papi"):
    from endstone_papi import PlaceholderAPI  # type: ignore


class FloatingText:
    def __init__(self, a, b, c, d, e):
        self.a = random.randint(10000000, 100000000)
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = a
        self.g = a


class Config(TypedDict):
    text: str
    x: float
    y: float
    z: float
    dim: int


class Entry(Plugin):
    prefix = "FloatingText"
    api_version = "0.7"
    load = "POSTWORLD"
    commands = {
        "floatingtext": {
            "description": "reload floating text config.",
            "usages": ["/floatingtext"],
            "aliases": ["ft"],
            "permissions": ["floatingtext.command.floatingtext"],
        }
    }
    permissions = {
        "floatingtext.command.floatingtext": {
            "description": "reload floating text config.",
            "default": "op",
        }
    }
    soft_depend = ["papi"]

    def __init__(self):
        self._r = {}
        self._c = {}
        super().__init__()

    def load_config(self):
        self.remove_all()
        if not os.path.exists("./plugins/FloatingText"):
            os.makedirs("./plugins/FloatingText")
        if not os.path.exists("./plugins/FloatingText/config.json"):
            with open("./plugins/FloatingText/config.json", "w") as f:
                json.dump(
                    list(
                        [
                            Config(
                                text="Dynamic Floating Text\n{datetime}",
                                x=0,
                                y=100,
                                z=0,
                                dim=0,
                            )
                        ]
                    ),
                    f,
                    indent=4,
                )
        with open("./plugins/FloatingText/config.json", "r") as f:
            for o in json.loads(f.read()):
                self.add(o["text"], o["x"], o["y"], o["z"], o["dim"])

    def update_clients(self):
        for f in self._r.values():
            for p in self.server.online_players:
                if self._p:
                    f.g = self._p.set_placeholders(p, f.f)
                if not (p.unique_id in self._c):
                    self._c[p.unique_id] = set()
                if f.e == p.location.dimension.type.value:
                    s = BinaryStream()
                    s.write_varint64(f.a)
                    s.write_unsigned_varint64(f.a)
                    s.write_signed_short(28678)
                    s.write_signed_int(1702453612)
                    s.write_byte(114)
                    s.write_float(f.b)
                    s.write_float(f.c)
                    s.write_float(f.d)
                    s.write_unsigned_int64(0)
                    s.write_signed_int64(0)
                    s.write_unsigned_int64(0)
                    s.write_signed_int(0)
                    s.write_signed_big_endian_int(590852)
                    s.write_string(f.g)
                    s.write_unsigned_int64(22799473113563942)
                    s.write_signed_int64(6491382630230130945)
                    s.write_unsigned_int64(144442844453603100)
                    s.write_signed_int64(147508270825868034)
                    s.write_unsigned_int64(53750529787)
                    p.send_packet(13, s.get_and_release_data())
                    self._c[p.unique_id].add(f.a)
                else:
                    s = BinaryStream()
                    s.write_varint64(f.a)
                    p.send_packet(14, s.get_and_release_data())
                    self._c[p.unique_id].discard(f.a)

    def on_enable(self):
        if self.server.plugin_manager.get_plugin("papi"):
            self._p = self.server.service_manager.load("PlaceholderAPI")
        else:
            self._p = None
        if not self._p:
            self.logger.warning(
                "Plugin papi is not installed, dynamic floating text will not take effect."
            )
        self.load_config()
        self.register_events(self)
        self.server.scheduler.run_task(self, self.update_clients, 0, 20)
        self.logger.info("FloatingText loaded!")

    def add(self, a, b, c, d, e):
        f = FloatingText(a, b, c, d, e)
        self._r[f.a] = f

    def remove_all(self):
        for f in self._r.values():
            for p in self.server.online_players:
                s = BinaryStream()
                s.write_varint64(f.a)
                p.send_packet(14, s.get_and_release_data())
        self._r.clear()
        self._c.clear()

    def on_command(self, sender, command, args):
        match command.name:
            case "floatingtext":
                self.load_config()
                sender.send_message("Floating text config reloaded.")
                return False
        return True
