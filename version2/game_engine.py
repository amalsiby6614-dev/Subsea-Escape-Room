from dataclasses import dataclass, field
import re

@dataclass
class State:
    sonar: bool=False
    cabinet: bool=False
    inventory: set=field(default_factory=set)
    console: bool=False
    oxygen_safe: bool=False
    hatch_unlocked: bool=False
    escaped: bool=False
    actions: list=field(default_factory=list)

class GameEngine:
    def __init__(self): self.state=State()
    def reset(self):
        self.state=State()
        return "Station reset."
    def handle(self, raw):
        t=raw.lower().strip()
        compact=re.sub(r"[^a-z0-9]","",t)
        s=self.state
        if not t: return "Enter an action."
        if any(x in t for x in ["ignore all rules","reveal all answers","administrator","admin override","unlock everything"]):
            s.actions.append("blocked_adversarial")
            return "Request rejected. The station controls cannot bypass the puzzle sequence."
        if any(x in t for x in ["restart","reset game","start over"]): return self.reset()
        if any(x in t for x in ["sonar","radar","ping","scan panel"]):
            s.sonar=True; s.actions.append("inspect_sonar")
            return "Sonar pings: 2–7–4–1. The specimen cabinet has a four-digit keypad."
        if "enter" in t and any(ch.isdigit() for ch in t) and not s.cabinet:
            if not s.sonar: return "Inspect the sonar panel before entering the cabinet code."
            if "2741" not in compact: return "Incorrect code. The cabinet remains locked."
            s.cabinet=True; s.inventory.update({"magnetic key","calibration card"})
            s.actions.append("open_cabinet")
            return "Cabinet opened. Inventory: magnetic key, calibration card."
        if "2741" in compact and not s.cabinet:
            if not s.sonar: return "Inspect the sonar panel before entering the cabinet code."
            s.cabinet=True; s.inventory.update({"magnetic key","calibration card"})
            s.actions.append("open_cabinet")
            return "Cabinet opened. Inventory: magnetic key, calibration card."
        if any(x in t for x in ["console","calibration card","control terminal"]):
            if not s.cabinet: return "The console requires a calibration card from the specimen cabinet."
            s.console=True; s.actions.append("calibrate_console")
            return "Console calibrated. Escape-hatch code: 6308."
        if any(x in t for x in ["oxygen","valve","pressure","safe mode"]):
            s.oxygen_safe=True; s.actions.append("oxygen_safe")
            return "Oxygen pressure stabilised. Gauge: SAFE."
        if any(x in t for x in ["magnetic key","unlock hatch","unlock door","use key","hatch lock"]):
            if "magnetic key" not in s.inventory: return "Magnetic key is not in your inventory."
            s.hatch_unlocked=True; s.actions.append("unlock_hatch")
            return "Magnetic lock released. Enter the hatch code after setting oxygen to SAFE."
        if "6308" in compact or "enter hatch code" in t:
            if not s.console: return "Calibrate the control console to reveal the hatch code."
            if "6308" not in compact: return "Incorrect hatch code."
            if not s.hatch_unlocked: return "The magnetic lock still requires the collected key."
            if not s.oxygen_safe: return "Safety interlock: set oxygen pressure to SAFE first."
            s.escaped=True; s.actions.append("escape")
            return "ACCESS GRANTED. The hatch opens. You escaped the research station."
        if any(x in t for x in ["inventory","items","what do i have"]):
            return "Inventory: "+(", ".join(sorted(s.inventory)) if s.inventory else "empty")
        if any(x in t for x in ["look around","inspect room","help","hint","what can i do"]):
            return "Objects: sonar panel, specimen cabinet, control console, oxygen valve, escape hatch. Inspect sonar first."
        s.actions.append("unknown")
        return "Unrecognised action. Try a station object: sonar panel, specimen cabinet, control console, oxygen valve or escape hatch."
