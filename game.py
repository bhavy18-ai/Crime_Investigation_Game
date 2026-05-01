import pygame
import sys
import math
import time

pygame.init()

# ─────────────────────────────────────────────
#  CONSTANTS & COLORS
# ─────────────────────────────────────────────
SCREEN_W, SCREEN_H = 900, 600
FPS = 60

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
DARK_BG    = (15,  15,  25)
PANEL_BG   = (25,  25,  40)
CARD_BG    = (35,  35,  55)
GOLD       = (220, 170,  50)
GOLD_DIM   = (140, 110,  30)
RED        = (180,  40,  40)
RED_BRIGHT = (220,  60,  60)
GREEN      = ( 50, 180,  80)
BLUE       = ( 60, 120, 220)
CYAN       = ( 60, 200, 200)
GREY       = (120, 120, 140)
LIGHT_GREY = (180, 180, 200)
YELLOW     = (255, 220,  60)
ORANGE     = (220, 130,  40)
PURPLE     = (140,  80, 200)

# ─────────────────────────────────────────────
#  ALL CASES DATA
# ─────────────────────────────────────────────

ALL_CASES = {

    # ══════════════════════════════════════════
    #  CASE 1 — The Stolen Diamond  (original)
    # ══════════════════════════════════════════
    "case1": {
        "title":    "The Stolen Diamond",
        "subtitle": "A priceless gem has vanished from the museum vault.",
        "icon":     "💎",
        "locations": ["vault", "hallway", "garden", "lab"],
        "location_colors": {
            "vault":   (60,  40, 100),
            "hallway": (40,  60,  80),
            "garden":  (30,  70,  40),
            "lab":     (60,  50,  30),
        },
        "location_icons": {
            "vault":   "🔒",
            "hallway": "🚪",
            "garden":  "🌿",
            "lab":     "🔬",
        },
        "clues": {
            "vault":   [
                {"id": "broken_lock",  "label": "Broken Lock",  "x": 220, "y": 260,
                 "desc": "The vault lock was forced open from inside using a thin metal tool — not a robbery."},
                {"id": "diamond_box",  "label": "Empty Box",    "x": 580, "y": 310,
                 "desc": "The diamond display case is empty. No glass broken — someone had the key."},
            ],
            "hallway": [
                {"id": "muddy_boots",  "label": "Muddy Boots",  "x": 310, "y": 380,
                 "desc": "Size 9 muddy boots near the exit. They came from the garden — recently."},
                {"id": "torn_glove",   "label": "Torn Glove",   "x": 600, "y": 250,
                 "desc": "A torn leather glove — monogrammed 'V'. Only one person here has that initial."},
            ],
            "garden":  [
                {"id": "footprints",   "label": "Footprints",   "x": 260, "y": 320,
                 "desc": "Fresh footprints lead from the garden gate straight to the back door of the vault."},
            ],
            "lab":     [
                {"id": "fake_diamond", "label": "Fake Diamond", "x": 450, "y": 290,
                 "desc": "A synthetic replica of the stolen diamond — still warm. Someone was here recently."},
            ],
        },
        "suspects": {
            "Victor": {
                "emoji":  "🕵️",
                "role":   "Museum Curator",
                "alibi":  "Says he was in the lab all evening cataloguing items.",
                "truth":  "Lab CCTV shows he left at 9:45 PM — right before the theft.",
                "clue":   "torn_glove",
                "guilty": True,
                "motive": "Owed Rs.40 lakhs in gambling debts. Planned to sell the diamond abroad.",
                "lines": [
                    "I was in my lab all evening. You can check the logs.",
                    "The diamond is irreplaceable — why would I steal my own exhibit?",
                    "That glove? I lost it last week. Anyone could have picked it up.",
                ]
            },
            "Priya": {
                "emoji":  "👩‍🔬",
                "role":   "Security Officer",
                "alibi":  "Was on night patrol rounds the entire evening.",
                "truth":  "Patrol log confirms she was at the front gate during the theft window.",
                "clue":   "muddy_boots",
                "guilty": False,
                "motive": "No financial motive found.",
                "lines": [
                    "I was doing my rounds! The entry log has my card swipes.",
                    "My boots are size 7. Whoever left those prints isn't me.",
                    "I reported the theft as soon as I saw the vault open.",
                ]
            },
            "Rajan": {
                "emoji":  "👨‍💼",
                "role":   "Diamond Dealer",
                "alibi":  "Claims he was at a business dinner across town.",
                "truth":  "Restaurant confirms he left at 9:15 PM — 30 mins from the museum.",
                "clue":   "fake_diamond",
                "guilty": False,
                "motive": "Had a disputed deal with the museum, but was not present.",
                "lines": [
                    "I was having dinner with clients. Call the restaurant.",
                    "Yes, I know about the fake diamond — I authenticated the real one last month.",
                    "I have no reason to steal it. My reputation is worth more.",
                ]
            },
        },
    },

    # ══════════════════════════════════════════
    #  CASE 2 — The Poisoned Professor
    # ══════════════════════════════════════════
    "case2": {
        "title":    "The Poisoned Professor",
        "subtitle": "Prof. Sharma was found dead in his office. Murder or accident?",
        "icon":     "☠️",
        "locations": ["office", "kitchen", "library", "rooftop"],
        "location_colors": {
            "office":  (50,  30,  30),
            "kitchen": (40,  50,  30),
            "library": (30,  30,  60),
            "rooftop": (20,  40,  55),
        },
        "location_icons": {
            "office":  "🖥️",
            "kitchen": "🍵",
            "library": "📚",
            "rooftop": "🏙️",
        },
        "clues": {
            "office":  [
                {"id": "poison_cup",   "label": "Poison Cup",   "x": 280, "y": 300,
                 "desc": "The professor's tea cup has traces of arsenic. The tea was prepared by someone else."},
                {"id": "threat_note",  "label": "Threat Note",  "x": 560, "y": 240,
                 "desc": "A crumpled note says 'Stop the research or face consequences' — unsigned but typed."},
            ],
            "kitchen": [
                {"id": "missing_tea",  "label": "Missing Tin",  "x": 340, "y": 270,
                 "desc": "The herbal tea tin is missing from the shelf — someone removed it to hide evidence."},
                {"id": "gloves_bin",   "label": "Rubber Gloves","x": 580, "y": 350,
                 "desc": "Disposable rubber gloves found in the bin — used to avoid fingerprints on the cup."},
            ],
            "library": [
                {"id": "torn_paper",   "label": "Torn Paper",   "x": 300, "y": 310,
                 "desc": "A torn page from a chemistry book on toxicology — bookmark still inside."},
            ],
            "rooftop": [
                {"id": "phone_record", "label": "Burn Phone",   "x": 470, "y": 280,
                 "desc": "A disposable mobile phone — last call made to a private number at 8 PM that evening."},
            ],
        },
        "suspects": {
            "Neha": {
                "emoji":  "👩‍🏫",
                "role":   "Lab Assistant",
                "alibi":  "Claims she left campus at 7 PM after her shift.",
                "truth":  "CCTV shows her entering the kitchen at 8:30 PM with a key she shouldn't have.",
                "clue":   "gloves_bin",
                "guilty": True,
                "motive": "Professor was going to expose her plagiarism in the upcoming thesis submission.",
                "lines": [
                    "I left early that day! Check the attendance register.",
                    "I have never been to the rooftop. This is all circumstantial.",
                    "Yes, I read toxicology books — I'm a science student! That means nothing.",
                ]
            },
            "Dr. Mehta": {
                "emoji":  "👨‍⚕️",
                "role":   "Rival Professor",
                "alibi":  "Was presenting a paper at a conference in Pune all day.",
                "truth":  "Conference records confirm he was on stage from 6 PM to 9 PM.",
                "clue":   "threat_note",
                "guilty": False,
                "motive": "Had a long-standing academic rivalry but was out of the city.",
                "lines": [
                    "I was in Pune! Two hundred people saw me present my paper.",
                    "Yes, we disagreed on research methods. That is not a crime.",
                    "Sharma and I argued, but I respected him. I would never do this.",
                ]
            },
            "Suman": {
                "emoji":  "🧑‍🍳",
                "role":   "Canteen Staff",
                "alibi":  "Says he served tea that evening as usual and left by 9 PM.",
                "truth":  "Kitchen logs show his last order was completed at 8:10 PM, not 9 PM as he claims.",
                "clue":   "missing_tea",
                "guilty": False,
                "motive": "Owed the professor money but had no access to arsenic.",
                "lines": [
                    "I make tea for everyone here. I didn't put anything in it!",
                    "I may have left early — I don't remember exactly. It was a normal day.",
                    "The tin was already missing when I came in that morning.",
                ]
            },
        },
    },

    # ══════════════════════════════════════════
    #  CASE 3 — The Missing Laptop
    # ══════════════════════════════════════════
    "case3": {
        "title":    "The Missing Laptop",
        "subtitle": "A laptop containing top-secret data has disappeared from HQ.",
        "icon":     "💻",
        "locations": ["server_room", "conference", "parking", "cafeteria"],
        "location_colors": {
            "server_room": (20,  50,  70),
            "conference":  (50,  40,  20),
            "parking":     (35,  35,  35),
            "cafeteria":   (40,  55,  30),
        },
        "location_icons": {
            "server_room": "🖥️",
            "conference":  "🪑",
            "parking":     "🚗",
            "cafeteria":   "☕",
        },
        "clues": {
            "server_room": [
                {"id": "deleted_logs", "label": "Deleted Logs", "x": 300, "y": 270,
                 "desc": "Server access logs were wiped between 6 PM and 7 PM — someone covered their tracks."},
                {"id": "usb_drive",    "label": "USB Drive",    "x": 580, "y": 320,
                 "desc": "A USB drive behind a monitor — contains partial copies of the stolen data files."},
            ],
            "conference":  [
                {"id": "coffee_mug",   "label": "Coffee Mug",   "x": 350, "y": 300,
                 "desc": "A coffee mug with red lipstick — not matching the usual staff. A visitor was here."},
                {"id": "sticky_note",  "label": "Sticky Note",  "x": 580, "y": 240,
                 "desc": "A sticky note reads 'Room 3, 6:30 PM' in handwriting matching the IT intern."},
            ],
            "parking":     [
                {"id": "tyre_tracks",  "label": "Tyre Tracks",  "x": 360, "y": 360,
                 "desc": "Fresh motorcycle tyre tracks near the fire exit — someone left in a hurry."},
            ],
            "cafeteria":   [
                {"id": "torn_badge",   "label": "Torn ID Badge", "x": 440, "y": 290,
                 "desc": "A torn employee ID badge — name partially readable: 'AR__V'. That matches one person."},
            ],
        },
        "suspects": {
            "Arjun": {
                "emoji":  "👨‍💻",
                "role":   "IT Intern",
                "alibi":  "Says he was working overtime in the server room till 8 PM.",
                "truth":  "Overtime sheet is forged — his supervisor confirms he left at 6 PM.",
                "clue":   "sticky_note",
                "guilty": True,
                "motive": "Was secretly paid by a competitor company to leak the product designs.",
                "lines": [
                    "I was in the server room all evening. I had to fix the cooling unit.",
                    "That sticky note is from last week — I wrote it for a team meeting!",
                    "My badge tore accidentally near the cafeteria. I didn't think much of it.",
                ]
            },
            "Ms. Kapoor": {
                "emoji":  "👩‍💼",
                "role":   "HR Manager",
                "alibi":  "Was interviewing candidates till 7:30 PM, multiple witnesses present.",
                "truth":  "Interview panel confirms she was in HR wing the entire evening.",
                "clue":   "coffee_mug",
                "guilty": False,
                "motive": "Dislikes the management but has no technical ability to steal data.",
                "lines": [
                    "I was in interviews! Ask the three candidates I was speaking to.",
                    "I use that conference room for lunch sometimes. The mug could be mine.",
                    "I have no idea how the server system even works.",
                ]
            },
            "Ramesh": {
                "emoji":  "🧑‍🔧",
                "role":   "Security Guard",
                "alibi":  "Was stationed at the main gate from 5 PM to 9 PM per duty roster.",
                "truth":  "Gate log confirms he was at the entrance — did not enter the building.",
                "clue":   "tyre_tracks",
                "guilty": False,
                "motive": "Has access to the building but no computer skills.",
                "lines": [
                    "I was at the gate all night. The entry log has my signatures every 30 minutes.",
                    "That motorbike near the fire exit? I saw it — it was parked by some delivery guy.",
                    "I guard the building, I don't steal from it.",
                ]
            },
        },
    },

    # ══════════════════════════════════════════
    #  CASE 4 — The Art Gallery Heist
    # ══════════════════════════════════════════
    "case4": {
        "title":    "The Art Gallery Heist",
        "subtitle": "A priceless painting vanished the night of the gala event.",
        "icon":     "🖼️",
        "locations": ["gallery", "storage", "lobby", "basement"],
        "location_colors": {
            "gallery":  (60,  45,  20),
            "storage":  (30,  25,  50),
            "lobby":    (45,  45,  55),
            "basement": (20,  20,  20),
        },
        "location_icons": {
            "gallery":  "🎨",
            "storage":  "📦",
            "lobby":    "🚶",
            "basement": "🔦",
        },
        "clues": {
            "gallery":  [
                {"id": "empty_frame",  "label": "Empty Frame",  "x": 260, "y": 260,
                 "desc": "The painting was cut out cleanly — professional blade. Not a spur-of-the-moment theft."},
                {"id": "champagne",    "label": "Champagne",    "x": 580, "y": 300,
                 "desc": "An unfinished champagne glass near the painting — not belonging to any gala guest."},
            ],
            "storage":  [
                {"id": "rope_fibres",  "label": "Rope Fibres",  "x": 320, "y": 290,
                 "desc": "Rope fibres on the storage window — someone climbed down from the upper floor."},
                {"id": "fake_frame",   "label": "Fake Frame",   "x": 600, "y": 340,
                 "desc": "An identical replica frame was prepared in advance and left behind. Pre-planned swap."},
            ],
            "lobby":    [
                {"id": "guest_list",   "label": "Guest List",   "x": 350, "y": 320,
                 "desc": "One name on the guest list was added last minute — hand-written over a correction."},
            ],
            "basement": [
                {"id": "blueprint",    "label": "Gallery Plan", "x": 460, "y": 280,
                 "desc": "A hand-drawn floor plan of the gallery with the painting location circled in red ink."},
            ],
        },
        "suspects": {
            "Kavya": {
                "emoji":  "👩‍🎨",
                "role":   "Art Restorer",
                "alibi":  "Says she was at the gala the whole time, socialising with guests.",
                "truth":  "Three guests confirm she disappeared for 40 minutes during the gala peak hour.",
                "clue":   "fake_frame",
                "guilty": True,
                "motive": "Was denied credit for restoring the painting and owed large loans to an art dealer.",
                "lines": [
                    "I was at the gala all evening. Everyone saw me near the buffet.",
                    "I restore paintings — of course I know how frames are made. That proves nothing.",
                    "Why would I steal something I spent six months restoring? That makes no sense.",
                ]
            },
            "Mr. Iyer": {
                "emoji":  "👴",
                "role":   "Gallery Owner",
                "alibi":  "Was hosting guests and giving speeches throughout the evening.",
                "truth":  "Multiple photographs and witnesses place him in the main hall all night.",
                "clue":   "blueprint",
                "guilty": False,
                "motive": "Owns the gallery — the insurance payout seemed suspicious initially.",
                "lines": [
                    "I was literally shaking hands with the Mayor when it happened!",
                    "Yes, I have floor plans — I own the building. That is not unusual.",
                    "I called the police myself. Does that sound like someone who planned a theft?",
                ]
            },
            "Suresh": {
                "emoji":  "🚚",
                "role":   "Delivery Driver",
                "alibi":  "Claims he delivered items and left the gallery by 5 PM, before the gala.",
                "truth":  "His van was spotted on CCTV near the rear exit at 10 PM — long after his claimed departure.",
                "clue":   "rope_fibres",
                "guilty": False,
                "motive": "Had access to the loading dock but no knowledge of art or the painting's value.",
                "lines": [
                    "I delivered the catering supplies and drove off. I was home by six.",
                    "Lots of vans look like mine. That CCTV image could be anyone.",
                    "I don't even know what painting you're talking about. I just drive a van.",
                ]
            },
        },
    },
}


# ─────────────────────────────────────────────
#  GAME STATE CLASS
# ─────────────────────────────────────────────
class GameState:
    def __init__(self, case_id="case1"):
        self.case_id       = case_id
        self.case_data     = ALL_CASES[case_id]
        self.scene         = "title"      # title / case_select / game / interrogate / accuse / win / lose
        self.location      = self.case_data["locations"][0]
        self.clues_found   = []
        self.suspects_done = []
        self.accused       = None
        self.score         = 0
        self.start_time    = None
        self.elapsed       = 0
        self.time_limit    = 180
        self.wrong_count   = 0
        self.current_suspect = None
        self.msg           = ""
        self.msg_timer     = 0

    def start_game(self):
        self.scene      = "game"
        self.start_time = time.time()

    def get_time_left(self):
        if self.start_time is None:
            return self.time_limit
        spent = time.time() - self.start_time
        return max(0, self.time_limit - int(spent))

    def add_clue(self, clue_id):
        if clue_id not in self.clues_found:
            self.clues_found.append(clue_id)
            self.score += 15
            return True
        return False

    def flash(self, msg):
        self.msg       = msg
        self.msg_timer = 120

    def tick_msg(self):
        if self.msg_timer > 0:
            self.msg_timer -= 1

    def total_clues(self):
        total = 0
        for loc_clues in self.case_data["clues"].values():
            total += len(loc_clues)
        return total


# ─────────────────────────────────────────────
#  RENDERER HELPERS
# ─────────────────────────────────────────────

def draw_text(surf, text, x, y, font, color=WHITE, center=False, right=False):
    img = font.render(text, True, color)
    r   = img.get_rect()
    if center: r.center   = (x, y)
    elif right: r.right, r.top = x, y
    else:       r.topleft = (x, y)
    surf.blit(img, r)
    return r

def draw_rect_alpha(surf, color, rect, alpha=180, radius=8):
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))

def draw_button(surf, rect, text, font, bg, fg=WHITE, hover=False, radius=8):
    col = tuple(min(255, c+30) for c in bg) if hover else bg
    pygame.draw.rect(surf, col, rect, border_radius=radius)
    pygame.draw.rect(surf, GOLD_DIM, rect, 1, border_radius=radius)
    draw_text(surf, text, rect[0]+rect[2]//2, rect[1]+rect[3]//2, font, fg, center=True)

def pulsing_glow(surf, cx, cy, radius, color, tick):
    pulse = 0.5 + 0.5 * math.sin(tick * 0.08)
    for r in range(int(radius+14), int(radius), -2):
        alpha = int(60 * pulse * (1 - (r - radius) / 14))
        glow  = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, alpha), (r, r), r)
        surf.blit(glow, (cx-r, cy-r))

def wrap_text(text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if font.size(test)[0] <= max_width:
            line = test
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return lines


# ─────────────────────────────────────────────
#  SCENE BACKGROUNDS  (generic + per-location)
# ─────────────────────────────────────────────

def draw_vault_bg(surf, fonts):
    surf.fill((20, 15, 35))
    pygame.draw.rect(surf, (50, 45, 65), (550, 150, 200, 280), border_radius=6)
    pygame.draw.rect(surf, (80, 70, 100), (550, 150, 200, 280), 3, border_radius=6)
    pygame.draw.circle(surf, (100, 90, 60), (650, 290), 60)
    pygame.draw.circle(surf, (140, 130, 80), (650, 290), 60, 3)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = int(650 + 40*math.cos(rad)); y1 = int(290 + 40*math.sin(rad))
        x2 = int(650 + 60*math.cos(rad)); y2 = int(290 + 60*math.sin(rad))
        pygame.draw.line(surf, (80, 70, 50), (x1,y1), (x2,y2), 3)
    pygame.draw.rect(surf, (40, 35, 55), (480, 270, 140, 100), border_radius=4)
    pygame.draw.rect(surf, (80, 75, 95), (480, 270, 140, 100), 2, border_radius=4)
    pygame.draw.rect(surf, (60, 50, 40), (150, 220, 120, 90), border_radius=4)
    pygame.draw.rect(surf, RED, (150, 220, 120, 90), 2, border_radius=4)
    draw_text(surf, "VAULT", 120, 100, fonts["title"], GOLD)
    draw_text(surf, "Room 01 — The Stolen Diamond", 120, 140, fonts["small"], GREY)

def draw_hallway_bg(surf, fonts):
    surf.fill((18, 25, 32))
    for i in range(5):
        x = 80 + i * 160
        pygame.draw.rect(surf, (30, 40, 50), (x, 100, 100, 330), border_radius=3)
        pygame.draw.rect(surf, (50, 65, 80), (x, 100, 100, 330), 2, border_radius=3)
    pygame.draw.rect(surf, (40, 55, 45), (270, 210, 80, 220))
    pygame.draw.rect(surf, (70, 100, 80), (270, 210, 80, 220), 2)
    pygame.draw.circle(surf, (180, 150, 60), (305, 330), 6)
    draw_text(surf, "HALLWAY", 80, 60, fonts["title"], CYAN)
    draw_text(surf, "Corridor — Evidence Left Behind", 80, 100, fonts["small"], GREY)

def draw_garden_bg(surf, fonts):
    surf.fill((12, 22, 14))
    pygame.draw.rect(surf, (20, 45, 20), (0, 350, 900, 250))
    for bx, by, bw in [(100,200,80),(300,180,60),(500,190,90),(700,170,70)]:
        pygame.draw.ellipse(surf, (25, 60, 25), (bx, by, bw, int(bw*1.2)))
        pygame.draw.ellipse(surf, (35, 80, 35), (bx, by, bw, int(bw*1.2)), 2)
    draw_text(surf, "GARDEN", 80, 60, fonts["title"], GREEN)
    draw_text(surf, "Outdoor — Fresh Tracks Found", 80, 100, fonts["small"], GREY)

def draw_lab_bg(surf, fonts):
    surf.fill((22, 18, 12))
    for lx, ly in [(120,180),(350,160),(580,190),(760,175)]:
        pygame.draw.rect(surf, (50, 45, 35), (lx-30, ly, 60, 160), border_radius=3)
        pygame.draw.rect(surf, (80, 70, 50), (lx-30, ly, 60, 160), 2, border_radius=3)
        pygame.draw.ellipse(surf, (60, 120, 140), (lx-15, ly-20, 30, 40))
    draw_text(surf, "LAB", 80, 60, fonts["title"], ORANGE)
    draw_text(surf, "Research Lab — Synthetic Evidence", 80, 100, fonts["small"], GREY)

# ── Case 2 backgrounds ──
def draw_office_bg(surf, fonts):
    surf.fill((25, 10, 10))
    pygame.draw.rect(surf, (45, 30, 30), (100, 160, 280, 200), border_radius=4)
    pygame.draw.rect(surf, (70, 50, 50), (100, 160, 280, 200), 2, border_radius=4)
    for i in range(3):
        pygame.draw.rect(surf, (35, 55, 35), (530+i*60, 140, 50, 220), border_radius=3)
    pygame.draw.rect(surf, (60, 45, 30), (150, 320, 200, 8))
    draw_text(surf, "PROFESSOR'S OFFICE", 80, 60, fonts["title"], RED_BRIGHT)
    draw_text(surf, "Scene of the Crime", 80, 100, fonts["small"], GREY)

def draw_kitchen_bg(surf, fonts):
    surf.fill((14, 20, 10))
    pygame.draw.rect(surf, (40, 50, 30), (80, 200, 700, 180), border_radius=3)
    pygame.draw.rect(surf, (60, 80, 45), (80, 200, 700, 180), 2, border_radius=3)
    for i in range(4):
        pygame.draw.rect(surf, (55, 65, 40), (120+i*160, 170, 80, 30), border_radius=3)
    draw_text(surf, "KITCHEN", 80, 60, fonts["title"], GREEN)
    draw_text(surf, "Where Tea Was Prepared", 80, 100, fonts["small"], GREY)

def draw_library_bg(surf, fonts):
    surf.fill((12, 12, 28))
    for i in range(6):
        pygame.draw.rect(surf, (30, 25, 45), (60+i*140, 140, 120, 240), border_radius=2)
        for j in range(6):
            col = [(80,30,30),(30,60,80),(60,80,30),(80,60,20),(50,30,80),(30,70,60)][j%6]
            pygame.draw.rect(surf, col, (68+i*140, 150+j*32, 104, 26), border_radius=2)
    draw_text(surf, "LIBRARY", 80, 60, fonts["title"], PURPLE)
    draw_text(surf, "Clues Hidden in Plain Sight", 80, 100, fonts["small"], GREY)

def draw_rooftop_bg(surf, fonts):
    surf.fill((8, 14, 24))
    for i in range(8):
        h = 80 + (i*47) % 120
        pygame.draw.rect(surf, (20+i*3, 25, 35), (50+i*105, 350-h, 80, h+100))
    pygame.draw.rect(surf, (18, 25, 40), (0, 350, 900, 100))
    for sx, sy in [(200,180),(450,120),(700,200),(100,230),(800,160)]:
        pygame.draw.circle(surf, (220, 220, 180), (sx, sy), 2)
    draw_text(surf, "ROOFTOP", 80, 60, fonts["title"], CYAN)
    draw_text(surf, "Night Sky — Secret Spot", 80, 100, fonts["small"], GREY)

# ── Case 3 backgrounds ──
def draw_server_room_bg(surf, fonts):
    surf.fill((5, 18, 28))
    for i in range(5):
        pygame.draw.rect(surf, (15, 40, 55), (80+i*155, 140, 130, 230), border_radius=4)
        pygame.draw.rect(surf, (20, 80, 110), (80+i*155, 140, 130, 230), 1, border_radius=4)
        for j in range(6):
            c = (0, 200, 80) if (i+j)%3!=0 else (200, 80, 0)
            pygame.draw.circle(surf, c, (100+i*155+j*18, 165), 4)
    draw_text(surf, "SERVER ROOM", 80, 60, fonts["title"], BLUE)
    draw_text(surf, "Data Centre — Logs Deleted", 80, 100, fonts["small"], GREY)

def draw_conference_bg(surf, fonts):
    surf.fill((22, 18, 10))
    pygame.draw.rect(surf, (50, 40, 20), (120, 200, 620, 150), border_radius=8)
    pygame.draw.rect(surf, (80, 65, 30), (120, 200, 620, 150), 2, border_radius=8)
    for i in range(8):
        pygame.draw.rect(surf, (35, 28, 14), (140+i*72, 310, 52, 80), border_radius=3)
    draw_text(surf, "CONFERENCE ROOM", 80, 60, fonts["title"], YELLOW)
    draw_text(surf, "Where the Meeting Was Held", 80, 100, fonts["small"], GREY)

def draw_parking_bg(surf, fonts):
    surf.fill((18, 18, 18))
    pygame.draw.rect(surf, (30, 30, 30), (0, 280, 900, 200))
    for i in range(6):
        pygame.draw.line(surf, (60, 60, 60), (i*150, 280), (i*150, 480), 2)
    pygame.draw.rect(surf, (40, 35, 20), (180, 290, 140, 70), border_radius=4)
    pygame.draw.rect(surf, (25, 22, 12), (180, 290, 140, 70), 2, border_radius=4)
    draw_text(surf, "PARKING LOT", 80, 60, fonts["title"], GREY)
    draw_text(surf, "Rear Exit — Escape Route", 80, 100, fonts["small"], GREY)

def draw_cafeteria_bg(surf, fonts):
    surf.fill((14, 22, 12))
    pygame.draw.rect(surf, (30, 45, 25), (60, 200, 780, 140), border_radius=4)
    for i in range(5):
        pygame.draw.rect(surf, (40, 60, 30), (80+i*150, 215, 110, 110), border_radius=5)
        pygame.draw.circle(surf, (55, 40, 25), (135+i*150, 345), 30)
    draw_text(surf, "CAFETERIA", 80, 60, fonts["title"], ORANGE)
    draw_text(surf, "Daily Hangout — A Clue Dropped", 80, 100, fonts["small"], GREY)

# ── Case 4 backgrounds ──
def draw_gallery_bg(surf, fonts):
    surf.fill((28, 22, 10))
    for i, col in enumerate([(80,60,20),(50,40,60),(30,60,50),(60,30,30)]):
        pygame.draw.rect(surf, col, (80+i*190, 140, 150, 200), border_radius=3)
        pygame.draw.rect(surf, GOLD_DIM, (80+i*190, 140, 150, 200), 2, border_radius=3)
    pygame.draw.rect(surf, (20,16,8), (270, 140, 150, 200))
    pygame.draw.rect(surf, RED, (270, 140, 150, 200), 2)
    draw_text(surf, "! EMPTY !", 345, 240, fonts["bold16"], RED, center=True)
    draw_text(surf, "ART GALLERY", 80, 60, fonts["title"], GOLD)
    draw_text(surf, "Gala Night — Painting Gone", 80, 100, fonts["small"], GREY)

def draw_storage_bg(surf, fonts):
    surf.fill((12, 10, 22))
    for i in range(4):
        for j in range(3):
            pygame.draw.rect(surf, (35, 30, 50), (80+i*200, 160+j*90, 170, 75), border_radius=3)
            pygame.draw.rect(surf, (55, 50, 75), (80+i*200, 160+j*90, 170, 75), 1, border_radius=3)
    draw_text(surf, "STORAGE ROOM", 80, 60, fonts["title"], PURPLE)
    draw_text(surf, "Behind the Gallery — Rope Found", 80, 100, fonts["small"], GREY)

def draw_lobby_bg(surf, fonts):
    surf.fill((20, 20, 30))
    pygame.draw.rect(surf, (35, 35, 50), (0, 360, 900, 120))
    for i in range(3):
        pygame.draw.ellipse(surf, (30, 28, 45), (100+i*270, 200, 180, 240))
        pygame.draw.ellipse(surf, (50, 45, 70), (100+i*270, 200, 180, 240), 2)
    draw_text(surf, "GALLERY LOBBY", 80, 60, fonts["title"], LIGHT_GREY)
    draw_text(surf, "Entrance — Guest Records", 80, 100, fonts["small"], GREY)

def draw_basement_bg(surf, fonts):
    surf.fill((5, 5, 8))
    for i in range(10):
        pygame.draw.rect(surf, (15, 12, 10), (i*92, 0, 85, 600))
    pygame.draw.rect(surf, (30, 25, 10), (300, 230, 300, 160), border_radius=4)
    pygame.draw.rect(surf, (60, 50, 20), (300, 230, 300, 160), 1, border_radius=4)
    draw_text(surf, "BASEMENT", 80, 60, fonts["title"], (180, 160, 60))
    draw_text(surf, "Dark Underbelly — Plans Hidden", 80, 100, fonts["small"], GREY)


BG_DRAWERS = {
    "vault":        draw_vault_bg,
    "hallway":      draw_hallway_bg,
    "garden":       draw_garden_bg,
    "lab":          draw_lab_bg,
    "office":       draw_office_bg,
    "kitchen":      draw_kitchen_bg,
    "library":      draw_library_bg,
    "rooftop":      draw_rooftop_bg,
    "server_room":  draw_server_room_bg,
    "conference":   draw_conference_bg,
    "parking":      draw_parking_bg,
    "cafeteria":    draw_cafeteria_bg,
    "gallery":      draw_gallery_bg,
    "storage":      draw_storage_bg,
    "lobby":        draw_lobby_bg,
    "basement":     draw_basement_bg,
}


# ─────────────────────────────────────────────
#  MAIN GAME CLASS
# ─────────────────────────────────────────────

class CrimeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Crime Investigation Game")
        self.clock  = pygame.time.Clock()
        self.state  = GameState()
        self.tick   = 0

        self.fonts = {
            "big":    pygame.font.SysFont("Courier New", 44, bold=True),
            "title":  pygame.font.SysFont("Courier New", 28, bold=True),
            "sub":    pygame.font.SysFont("Courier New", 20, bold=True),
            "body":   pygame.font.SysFont("Courier New", 15),
            "small":  pygame.font.SysFont("Courier New", 13),
            "bold16": pygame.font.SysFont("Courier New", 16, bold=True),
        }

        self.buttons         = {}
        self.clue_spots      = []
        self.interrog_line_idx = 0

    # ── MAIN LOOP ─────────────────────────────
    def run(self):
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.state.scene in ("game", "interrogate"):
                        self.state.scene = "game"
                        self.state.current_suspect = None
                    elif self.state.scene == "case_select":
                        self.state.scene = "title"
                    else:
                        pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.handle_click(e.pos)

            self.tick += 1
            self.state.tick_msg()

            if self.state.scene == "game" and self.state.get_time_left() == 0:
                self.state.scene   = "lose"
                self.state.elapsed = self.state.time_limit

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    # ── CLICK HANDLER ─────────────────────────
    def handle_click(self, pos):
        s = self.state.scene

        if s == "title":
            if "play" in self.buttons and self.buttons["play"].collidepoint(pos):
                self.state.scene = "case_select"
            if "quit" in self.buttons and self.buttons["quit"].collidepoint(pos):
                pygame.quit(); sys.exit()

        elif s == "case_select":
            for cid in ALL_CASES:
                key = "case_" + cid
                if key in self.buttons and self.buttons[key].collidepoint(pos):
                    self.state = GameState(cid)
                    self.state.start_game()
                    self.interrog_line_idx = 0
                    return
            if "back_title" in self.buttons and self.buttons["back_title"].collidepoint(pos):
                self.state.scene = "title"

        elif s == "game":
            locs = self.state.case_data["locations"]
            for loc in locs:
                if loc in self.buttons and self.buttons[loc].collidepoint(pos):
                    self.state.location = loc
                    return
            for spot in self.clue_spots:
                if spot["rect"].collidepoint(pos):
                    added = self.state.add_clue(spot["id"])
                    if added:
                        self.state.flash(f"Clue found: {spot['label']}!")
                    else:
                        self.state.flash(f"Already collected: {spot['label']}")
                    return
            for name in self.state.case_data["suspects"]:
                key = "sus_" + name
                if key in self.buttons and self.buttons[key].collidepoint(pos):
                    self.state.current_suspect = name
                    self.state.scene = "interrogate"
                    self.interrog_line_idx = 0
                    return
            if "accuse" in self.buttons and self.buttons["accuse"].collidepoint(pos):
                if len(self.state.clues_found) < 3:
                    self.state.flash("Collect at least 3 clues before accusing!")
                else:
                    self.state.scene = "accuse"

        elif s == "interrogate":
            name  = self.state.current_suspect
            lines = self.state.case_data["suspects"][name]["lines"]
            if "next_line" in self.buttons and self.buttons["next_line"].collidepoint(pos):
                if self.interrog_line_idx < len(lines) - 1:
                    self.interrog_line_idx += 1
                else:
                    if name not in self.state.suspects_done:
                        self.state.suspects_done.append(name)
                        self.state.score += 10
                    self.state.scene = "game"
                    self.state.current_suspect = None
            if "back_interrog" in self.buttons and self.buttons["back_interrog"].collidepoint(pos):
                self.state.scene = "game"
                self.state.current_suspect = None

        elif s == "accuse":
            for name in self.state.case_data["suspects"]:
                key = "acc_" + name
                if key in self.buttons and self.buttons[key].collidepoint(pos):
                    self.state.accused = name
                    self.state.elapsed = self.state.time_limit - self.state.get_time_left()
                    if self.state.case_data["suspects"][name]["guilty"]:
                        bonus = max(0, self.state.get_time_left())
                        self.state.score += int(bonus) + 50
                        self.state.scene  = "win"
                    else:
                        self.state.wrong_count += 1
                        self.state.score = max(0, self.state.score - 30)
                        self.state.scene  = "lose"
                    return
            if "back_accuse" in self.buttons and self.buttons["back_accuse"].collidepoint(pos):
                self.state.scene = "game"

        elif s in ("win", "lose"):
            if "restart" in self.buttons and self.buttons["restart"].collidepoint(pos):
                self.state = GameState(self.state.case_id)
                self.state.start_game()
                self.tick = 0
            if "menu" in self.buttons and self.buttons["menu"].collidepoint(pos):
                self.state = GameState()
                self.state.scene = "case_select"
                self.tick = 0
            if "quit_end" in self.buttons and self.buttons["quit_end"].collidepoint(pos):
                pygame.quit(); sys.exit()

    # ── DRAW DISPATCHER ───────────────────────
    def draw(self):
        s = self.state.scene
        if   s == "title":       self.draw_title()
        elif s == "case_select": self.draw_case_select()
        elif s == "game":        self.draw_game()
        elif s == "interrogate": self.draw_interrogate()
        elif s == "accuse":      self.draw_accuse()
        elif s == "win":         self.draw_verdict(won=True)
        elif s == "lose":        self.draw_verdict(won=False)

    # ─────────────────────────────────────────
    #  TITLE SCREEN
    # ─────────────────────────────────────────
    def draw_title(self):
        self.screen.fill(DARK_BG)
        self.buttons.clear()
        mouse = pygame.mouse.get_pos()

        for y in [0, 4]:
            pygame.draw.line(self.screen, GOLD_DIM, (0, y), (SCREEN_W, y), 2)
        for y in [SCREEN_H-1, SCREEN_H-5]:
            pygame.draw.line(self.screen, GOLD_DIM, (0, y), (SCREEN_W, y), 2)

        draw_text(self.screen, "CRIME INVESTIGATION GAME",
                  SCREEN_W//2, 100, self.fonts["big"], GOLD, center=True)
        draw_text(self.screen, "— Solve the Mystery —",
                  SCREEN_W//2, 160, self.fonts["sub"], LIGHT_GREY, center=True)

        draw_rect_alpha(self.screen, PANEL_BG, (180, 205, 540, 180), alpha=220, radius=10)
        pygame.draw.rect(self.screen, GOLD_DIM, (180, 205, 540, 180), 1, border_radius=10)

        draw_text(self.screen, "4 CASES  |  12 SUSPECTS  |  20 CLUES",
                  SCREEN_W//2, 225, self.fonts["bold16"], GOLD, center=True)

        info = [
            "Case 1: The Stolen Diamond",
            "Case 2: The Poisoned Professor",
            "Case 3: The Missing Laptop",
            "Case 4: The Art Gallery Heist",
        ]
        for i, line in enumerate(info):
            draw_text(self.screen, line, SCREEN_W//2, 252 + i*28,
                      self.fonts["body"], LIGHT_GREY, center=True)

        play_r = pygame.Rect(310, 415, 280, 48)
        quit_r = pygame.Rect(370, 478, 160, 36)
        draw_button(self.screen, play_r, "SELECT A CASE", self.fonts["bold16"],
                    RED, hover=play_r.collidepoint(mouse))
        draw_button(self.screen, quit_r, "EXIT", self.fonts["body"],
                    (50,50,70), hover=quit_r.collidepoint(mouse))

        self.buttons["play"] = play_r
        self.buttons["quit"] = quit_r

        draw_text(self.screen, "BTech 1st Year Project  |  Python + Pygame",
                  SCREEN_W//2, 530, self.fonts["small"], GREY, center=True)
        draw_text(self.screen, "Press ESC to quit anytime",
                  SCREEN_W//2, 550, self.fonts["small"], (70,70,90), center=True)

    # ─────────────────────────────────────────
    #  CASE SELECTION SCREEN
    # ─────────────────────────────────────────
    def draw_case_select(self):
        self.screen.fill(DARK_BG)
        self.buttons.clear()
        mouse = pygame.mouse.get_pos()

        draw_text(self.screen, "SELECT YOUR CASE",
                  SCREEN_W//2, 40, self.fonts["title"], GOLD, center=True)
        pygame.draw.line(self.screen, GOLD_DIM, (80, 72), (SCREEN_W-80, 72), 1)

        case_items = list(ALL_CASES.items())
        cols = 2
        card_w, card_h = 380, 190
        start_x = [70, 460]
        start_y = [90, 310]

        for idx, (cid, cdata) in enumerate(case_items):
            col_i = idx % cols
            row_i = idx // cols
            cx    = start_x[col_i]
            cy    = start_y[row_i]
            cr    = pygame.Rect(cx, cy, card_w, card_h)
            hov   = cr.collidepoint(mouse)

            bg_col = (45, 38, 20) if hov else CARD_BG
            pygame.draw.rect(self.screen, bg_col, cr, border_radius=10)
            pygame.draw.rect(self.screen, GOLD if hov else GOLD_DIM, cr, 2 if hov else 1, border_radius=10)

            draw_text(self.screen, f"{cdata['icon']}  {cdata['title']}",
                      cx+16, cy+14, self.fonts["sub"], GOLD)
            draw_text(self.screen, cdata["subtitle"],
                      cx+16, cy+46, self.fonts["small"], LIGHT_GREY)

            pygame.draw.line(self.screen, GOLD_DIM, (cx+10, cy+68), (cx+card_w-10, cy+68), 1)

            suspects = list(cdata["suspects"].keys())
            draw_text(self.screen, "Suspects: " + "  ".join(
                f"{cdata['suspects'][n]['emoji']} {n}" for n in suspects),
                cx+16, cy+78, self.fonts["small"], GREY)

            locs = cdata["locations"]
            draw_text(self.screen, "Locations: " + "  ".join(
                f"{cdata['location_icons'][l]} {l.replace('_',' ').title()}" for l in locs),
                cx+16, cy+100, self.fonts["small"], GREY)

            clue_count = sum(len(v) for v in cdata["clues"].values())
            draw_text(self.screen, f"Clues: {clue_count}   Time Limit: 3:00",
                      cx+16, cy+122, self.fonts["small"], CYAN)

            btn_r = pygame.Rect(cx + card_w - 150, cy + card_h - 44, 136, 32)
            draw_button(self.screen, btn_r, "INVESTIGATE", self.fonts["small"],
                        RED if hov else (70, 30, 30), hover=hov)
            self.buttons["case_" + cid] = cr    # whole card is clickable

        back_r = pygame.Rect(SCREEN_W//2 - 100, SCREEN_H - 44, 200, 34)
        draw_button(self.screen, back_r, "← Back to Menu", self.fonts["body"],
                    (50,50,70), hover=back_r.collidepoint(mouse))
        self.buttons["back_title"] = back_r

    # ─────────────────────────────────────────
    #  MAIN GAME SCREEN
    # ─────────────────────────────────────────
    def draw_game(self):
        self.buttons.clear()
        self.clue_spots.clear()
        loc   = self.state.location
        cdata = self.state.case_data
        mouse = pygame.mouse.get_pos()

        BG_DRAWERS[loc](self.screen, self.fonts)

        # ── TOP HUD ──
        pygame.draw.rect(self.screen, (10, 10, 20), (0, 0, SCREEN_W, 55))
        pygame.draw.line(self.screen, GOLD_DIM, (0, 55), (SCREEN_W, 55), 1)
        draw_text(self.screen, f"CASE: {cdata['title']}", 12, 8, self.fonts["bold16"], GOLD)
        draw_text(self.screen, f"Score: {self.state.score}", 12, 30, self.fonts["small"], CYAN)

        tl   = self.state.get_time_left()
        tcol = RED if tl < 30 else (YELLOW if tl < 60 else GREEN)
        draw_text(self.screen, f"Time: {tl//60:02d}:{tl%60:02d}",
                  SCREEN_W//2, 10, self.fonts["sub"], tcol, center=True)
        total_c = self.state.total_clues()
        draw_text(self.screen, f"Clues: {len(self.state.clues_found)}/{total_c}",
                  SCREEN_W//2, 35, self.fonts["small"], LIGHT_GREY, center=True)

        draw_text(self.screen, f"Location: {loc.upper().replace('_',' ')}",
                  SCREEN_W-12, 10, self.fonts["bold16"], LIGHT_GREY, right=True)
        draw_text(self.screen, f"Interviewed: {len(self.state.suspects_done)}/3",
                  SCREEN_W-12, 33, self.fonts["small"], GREY, right=True)

        # ── Clue hotspots ──
        for clue in cdata["clues"].get(loc, []):
            cx, cy = clue["x"], clue["y"]
            already = clue["id"] in self.state.clues_found
            col = GREY if already else GOLD
            pulsing_glow(self.screen, cx, cy, 14, col, self.tick)
            pygame.draw.circle(self.screen, col, (cx, cy), 14)
            pygame.draw.circle(self.screen, WHITE if not already else GREY, (cx, cy), 14, 2)
            draw_text(self.screen, "v" if already else "?", cx, cy, self.fonts["bold16"],
                      BLACK, center=True)
            draw_text(self.screen, clue["label"], cx, cy+20, self.fonts["small"],
                      GREY if already else YELLOW, center=True)
            r = pygame.Rect(cx-18, cy-18, 36, 36)
            self.clue_spots.append({"id": clue["id"], "label": clue["label"], "rect": r})

        # ── BOTTOM PANEL ──
        panel_y = 450
        pygame.draw.rect(self.screen, (10, 10, 18), (0, panel_y, SCREEN_W, SCREEN_H - panel_y))
        pygame.draw.line(self.screen, GOLD_DIM, (0, panel_y), (SCREEN_W, panel_y), 1)

        # Location nav
        draw_text(self.screen, "GO TO:", 12, panel_y + 8, self.fonts["small"], GREY)
        locs = cdata["locations"]
        loc_icons = cdata["location_icons"]
        btn_w = min(108, (SCREEN_W - 220) // len(locs))
        for i, l in enumerate(locs):
            lx = 80 + i * (btn_w + 6)
            lr = pygame.Rect(lx, panel_y + 4, btn_w, 32)
            active = (l == loc)
            col    = GOLD_DIM if active else (50, 50, 70)
            label  = f"{loc_icons[l]} {l.replace('_',' ').upper()[:8]}"
            draw_button(self.screen, lr, label, self.fonts["small"],
                        col, GOLD if active else LIGHT_GREY, hover=lr.collidepoint(mouse))
            self.buttons[l] = lr

        # Suspect buttons
        draw_text(self.screen, "SUSPECTS:", 12, panel_y + 44, self.fonts["small"], GREY)
        suspects = list(cdata["suspects"].items())
        for i, (name, data) in enumerate(suspects):
            sx = 80 + i * 180
            sr = pygame.Rect(sx, panel_y + 40, 168, 30)
            done = name in self.state.suspects_done
            col  = (30, 60, 30) if done else (50, 30, 50)
            draw_button(self.screen, sr, f"{data['emoji']} {name}", self.fonts["small"],
                        col, GREEN if done else LIGHT_GREY, hover=sr.collidepoint(mouse))
            self.buttons["sus_" + name] = sr

        # Accuse button
        acc_r = pygame.Rect(SCREEN_W - 180, panel_y + 8, 168, 62)
        ready = len(self.state.clues_found) >= 3
        draw_button(self.screen, acc_r, "MAKE ACCUSATION", self.fonts["bold16"],
                    RED if ready else (60, 30, 30),
                    WHITE if ready else GREY, hover=ready and acc_r.collidepoint(mouse))
        self.buttons["accuse"] = acc_r

        # Flash message
        if self.state.msg_timer > 0:
            draw_rect_alpha(self.screen, (20, 20, 20), (SCREEN_W//2-220, 410, 440, 34), alpha=200, radius=6)
            draw_text(self.screen, self.state.msg, SCREEN_W//2, 427,
                      self.fonts["small"], GOLD, center=True)

        # Clue log
        draw_text(self.screen, "CLUE LOG:", 636, panel_y + 8, self.fonts["small"], GREY)
        name_map = {c["id"]: c["label"] for loc_clues in cdata["clues"].values() for c in loc_clues}
        for i, cid in enumerate(self.state.clues_found[:3]):
            draw_text(self.screen, f"v {name_map.get(cid, cid)}", 636, panel_y + 24 + i*14,
                      self.fonts["small"], GREEN)
        if len(self.state.clues_found) > 3:
            draw_text(self.screen, f"  + {len(self.state.clues_found)-3} more",
                      636, panel_y + 24 + 3*14, self.fonts["small"], GREY)

    # ─────────────────────────────────────────
    #  INTERROGATION SCREEN
    # ─────────────────────────────────────────
    def draw_interrogate(self):
        self.buttons.clear()
        name = self.state.current_suspect
        if not name: return
        data  = self.state.case_data["suspects"][name]
        mouse = pygame.mouse.get_pos()

        self.screen.fill(DARK_BG)
        pygame.draw.rect(self.screen, PANEL_BG, (80, 60, SCREEN_W-160, SCREEN_H-120), border_radius=12)
        pygame.draw.rect(self.screen, GOLD_DIM, (80, 60, SCREEN_W-160, SCREEN_H-120), 1, border_radius=12)

        draw_text(self.screen, "INTERROGATION ROOM",
                  SCREEN_W//2, 85, self.fonts["title"], GOLD, center=True)
        draw_text(self.screen, f"{data['emoji']}  {name}",
                  SCREEN_W//2, 125, self.fonts["sub"], WHITE, center=True)
        draw_text(self.screen, data["role"],
                  SCREEN_W//2, 152, self.fonts["body"], GREY, center=True)

        pygame.draw.line(self.screen, GOLD_DIM, (120, 172), (SCREEN_W-120, 172), 1)

        draw_text(self.screen, "Alibi:", 120, 185, self.fonts["bold16"], CYAN)
        for i, l in enumerate(wrap_text(data["alibi"], self.fonts["body"], 620)):
            draw_text(self.screen, l, 120, 205 + i*18, self.fonts["body"], LIGHT_GREY)

        pygame.draw.rect(self.screen, (20, 20, 35), (120, 260, SCREEN_W-240, 140), border_radius=8)
        pygame.draw.rect(self.screen, BLUE, (120, 260, SCREEN_W-240, 140), 1, border_radius=8)
        draw_text(self.screen, f"{name} says:", 136, 272, self.fonts["bold16"], BLUE)

        lines_text = data["lines"]
        current    = lines_text[self.interrog_line_idx]
        wrapped    = wrap_text(f'"{current}"', self.fonts["body"], SCREEN_W-280)
        for i, l in enumerate(wrapped[:5]):
            draw_text(self.screen, l, 136, 294 + i*20, self.fonts["body"], WHITE)

        draw_text(self.screen, f"{self.interrog_line_idx+1}/{len(lines_text)}",
                  SCREEN_W-140, 388, self.fonts["small"], GREY)

        is_last   = (self.interrog_line_idx == len(lines_text) - 1)
        btn_label = "Done  ->" if is_last else "Next  ->"
        next_r    = pygame.Rect(SCREEN_W//2 + 20, 430, 200, 38)
        back_r    = pygame.Rect(SCREEN_W//2 - 230, 430, 200, 38)
        draw_button(self.screen, next_r, btn_label, self.fonts["bold16"],
                    GREEN if is_last else BLUE, hover=next_r.collidepoint(mouse))
        draw_button(self.screen, back_r, "<- Back to Scene", self.fonts["body"],
                    (50,50,70), hover=back_r.collidepoint(mouse))
        self.buttons["next_line"]     = next_r
        self.buttons["back_interrog"] = back_r

        draw_text(self.screen, "ESC — back to scene",
                  SCREEN_W//2, 485, self.fonts["small"], GREY, center=True)

    # ─────────────────────────────────────────
    #  ACCUSATION SCREEN
    # ─────────────────────────────────────────
    def draw_accuse(self):
        self.buttons.clear()
        mouse    = pygame.mouse.get_pos()
        suspects = self.state.case_data["suspects"]

        self.screen.fill(DARK_BG)
        draw_text(self.screen, "MAKE YOUR ACCUSATION",
                  SCREEN_W//2, 50, self.fonts["title"], RED, center=True)
        draw_text(self.screen, "Choose the culprit. Wrong guess costs 30 points.",
                  SCREEN_W//2, 85, self.fonts["body"], GREY, center=True)
        pygame.draw.line(self.screen, RED, (160, 108), (SCREEN_W-160, 108), 1)
        draw_text(self.screen, f"Evidence collected: {len(self.state.clues_found)}/{self.state.total_clues()} clues",
                  SCREEN_W//2, 120, self.fonts["body"], CYAN, center=True)

        n_sus = len(suspects)
        card_w = min(220, (SCREEN_W - 60) // n_sus - 10)
        total_w = n_sus * (card_w + 10)
        start_x = (SCREEN_W - total_w) // 2

        for i, (name, data) in enumerate(suspects.items()):
            cx  = start_x + i * (card_w + 10)
            cr  = pygame.Rect(cx, 148, card_w, 240)
            hov = cr.collidepoint(mouse)
            pygame.draw.rect(self.screen, (55,40,40) if hov else CARD_BG, cr, border_radius=10)
            pygame.draw.rect(self.screen, RED if hov else GOLD_DIM, cr, 2 if hov else 1, border_radius=10)

            draw_text(self.screen, data["emoji"],    cx+card_w//2, 170, self.fonts["title"], WHITE, center=True)
            draw_text(self.screen, name,             cx+card_w//2, 210, self.fonts["sub"],   GOLD,  center=True)
            draw_text(self.screen, data["role"],     cx+card_w//2, 232, self.fonts["small"], GREY,  center=True)
            pygame.draw.line(self.screen, GOLD_DIM, (cx+10, 250), (cx+card_w-10, 250), 1)
            draw_text(self.screen, "Alibi:", cx+10, 257, self.fonts["small"], CYAN)
            for j, l in enumerate(wrap_text(data["alibi"], self.fonts["small"], card_w-20)[:3]):
                draw_text(self.screen, l, cx+10, 273+j*15, self.fonts["small"], LIGHT_GREY)

            acc_r = pygame.Rect(cx+10, 348, card_w-20, 32)
            draw_button(self.screen, acc_r, "ACCUSE", self.fonts["bold16"],
                        RED, hover=hov)
            self.buttons["acc_" + name] = acc_r

        back_r = pygame.Rect(SCREEN_W//2-90, 415, 180, 36)
        draw_button(self.screen, back_r, "<- Review Evidence", self.fonts["body"],
                    (50,50,70), hover=back_r.collidepoint(mouse))
        self.buttons["back_accuse"] = back_r

    # ─────────────────────────────────────────
    #  WIN / LOSE SCREEN
    # ─────────────────────────────────────────
    def draw_verdict(self, won):
        self.buttons.clear()
        mouse    = pygame.mouse.get_pos()
        acc      = self.state.accused or "?"
        suspects = self.state.case_data["suspects"]
        killer   = next(n for n, d in suspects.items() if d["guilty"])
        cdata    = self.state.case_data

        self.screen.fill(DARK_BG)
        stamp_col = GREEN if won else RED
        stamp_txt = "CASE SOLVED!" if won else "CASE FAILED"
        draw_text(self.screen, stamp_txt, SCREEN_W//2, 55, self.fonts["big"], stamp_col, center=True)
        pygame.draw.line(self.screen, stamp_col, (100, 100), (SCREEN_W-100, 100), 2)

        draw_text(self.screen,
                  f"Correct! {acc} is guilty." if won else f"Wrong! {acc} accused  |  Real culprit: {killer}",
                  SCREEN_W//2, 118, self.fonts["sub"], GOLD if won else RED, center=True)

        draw_rect_alpha(self.screen, PANEL_BG, (90, 148, SCREEN_W-180, 210), alpha=230, radius=10)
        pygame.draw.rect(self.screen, GOLD_DIM, (90, 148, SCREEN_W-180, 210), 1, border_radius=10)

        draw_text(self.screen, "THE TRUTH:", 115, 162, self.fonts["bold16"], GOLD)
        k_data = suspects[killer]
        truth_lines = [
            f"Culprit : {killer}  ({k_data['role']})",
            f"Motive  : {k_data['motive']}",
            f"Truth   : {k_data['truth']}",
            "",
            "KEY EVIDENCE FOUND:",
        ]
        name_map = {c["id"]: c["label"] for lc in cdata["clues"].values() for c in lc}
        desc_map = {c["id"]: c["desc"]  for lc in cdata["clues"].values() for c in lc}
        for cid in self.state.clues_found:
            lbl  = name_map.get(cid, cid)
            desc = desc_map.get(cid, "")[:55]
            truth_lines.append(f"  v {lbl}: {desc}...")

        for i, l in enumerate(truth_lines[:9]):
            col = YELLOW if l.startswith("KEY") else (LIGHT_GREY if l.startswith("  v") else WHITE)
            draw_text(self.screen, l, 115, 185 + i*20, self.fonts["small"], col)

        m = self.state.elapsed // 60
        s = self.state.elapsed % 60
        draw_text(self.screen, f"Final Score: {self.state.score}",
                  SCREEN_W//2, 378, self.fonts["title"], GOLD, center=True)
        draw_text(self.screen,
                  f"Time: {m:02d}:{s:02d}   Clues: {len(self.state.clues_found)}/{self.state.total_clues()}   Wrong: {self.state.wrong_count}",
                  SCREEN_W//2, 408, self.fonts["body"], GREY, center=True)

        r_r   = pygame.Rect(SCREEN_W//2 - 310, 445, 190, 42)
        m_r   = pygame.Rect(SCREEN_W//2 - 95,  445, 190, 42)
        q_r   = pygame.Rect(SCREEN_W//2 + 120, 445, 190, 42)
        draw_button(self.screen, r_r, "RETRY CASE",  self.fonts["bold16"], BLUE,  hover=r_r.collidepoint(mouse))
        draw_button(self.screen, m_r, "CASE SELECT", self.fonts["bold16"], GREEN, hover=m_r.collidepoint(mouse))
        draw_button(self.screen, q_r, "EXIT GAME",   self.fonts["bold16"], RED,   hover=q_r.collidepoint(mouse))
        self.buttons["restart"]  = r_r
        self.buttons["menu"]     = m_r
        self.buttons["quit_end"] = q_r

        draw_text(self.screen, f"Case: {cdata['title']}  |  BTech 1st Year  |  Python + Pygame",
                  SCREEN_W//2, 504, self.fonts["small"], GREY, center=True)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    game = CrimeGame()
    game.run()