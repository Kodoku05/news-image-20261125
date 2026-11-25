from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math


OUT = Path(__file__).with_name("entry.png")
W = H = 1024
PAPER = "#f4f0e6"
INK = "#17263a"
NAVY = "#132943"
RED = "#c33c32"
GOLD = "#d5ad68"
MUTED = "#647182"
RULE = "#c9c5bb"
PALE = "#e9e4d9"

FONT_ROOT = Path("/usr/share/fonts/truetype/dejavu")
if not (FONT_ROOT / "DejaVuSans.ttf").exists():
    FONT_ROOT = Path("/usr/share/fonts/truetype/noto")
REGULAR = FONT_ROOT / "DejaVuSans.ttf"
BOLD = FONT_ROOT / "DejaVuSans-Bold.ttf"
if not REGULAR.exists():
    REGULAR = FONT_ROOT / "NotoSans-Regular.ttf"
    BOLD = FONT_ROOT / "NotoSans-Bold.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else REGULAR), size)


def text(x, y, value, size, fill=INK, bold=False, anchor=None):
    d.text((x, y), value, font=font(size, bold), fill=fill, anchor=anchor)


def width(value, size, bold=False):
    return d.textlength(value, font=font(size, bold))


def wrap(value, size, max_width, bold=False):
    words = value.split()
    lines, line = [], ""
    for word in words:
        candidate = word if not line else line + " " + word
        if width(candidate, size, bold) <= max_width or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fitted(value, size, max_width, bold=False, minimum=6):
    while size > minimum and width(value, size, bold) > max_width:
        size -= 1
    if width(value, size, bold) <= max_width:
        return value, size
    result = value
    while result and width(result + "…", size, bold) > max_width:
        result = result[:-1]
    return result + "…", size


def paragraph(x, y, value, size, max_width, fill=INK, bold=False, line_gap=2, max_lines=None):
    lines = wrap(value, size, max_width, bold)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last, _ = fitted(lines[-1] + "…", size, max_width, bold)
        lines[-1] = last
    for index, line in enumerate(lines):
        text(x, y + index * (size + line_gap), line, size, fill, bold)
    return y + len(lines) * (size + line_gap)


def line(x1, y1, x2, y2, fill=RULE, thick=1):
    d.line((x1, y1, x2, y2), fill=fill, width=thick)


def section_label(x, y, value, color=RED, size=8):
    text(x, y, value, size, color, True)


def circle(cx, cy, r, fill, outline=None, thick=1):
    d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=fill, outline=outline, width=thick)


def courtroom():
    # A compact courtroom vignette: bench, judge, jury rail and the evidence seal.
    d.rounded_rectangle((655, 119, 990, 281), 8, fill="#e8e1d4", outline="#d5cbbb", width=1)
    d.rectangle((672, 237, 974, 250), fill=NAVY)
    d.rectangle((687, 250, 699, 270), fill="#8c7355")
    d.rectangle((948, 250, 960, 270), fill="#8c7355")
    d.rectangle((704, 225, 941, 237), fill="#b39164")
    # Bench front inset and small gold seal.
    d.rectangle((718, 241, 926, 250), fill="#263b53")
    circle(822, 247, 4, GOLD)
    # Judge silhouette above the bench.
    d.polygon([(784, 188), (791, 168), (805, 159), (839, 159), (853, 168), (860, 188)], fill=NAVY)
    d.ellipse((802, 137, 842, 175), fill="#d7b894")
    d.polygon([(798, 143), (804, 128), (842, 128), (849, 146), (836, 138), (813, 140)], fill="#313b47")
    d.polygon([(810, 174), (834, 174), (845, 211), (800, 211)], fill="#f4f0e6")
    d.polygon([(816, 176), (828, 176), (822, 193)], fill=RED)
    # Two jury silhouettes keep the scene grounded without adding visual noise.
    for xx in (688, 716, 922, 950):
        circle(xx, 191, 9, "#b68f69")
        d.rounded_rectangle((xx-11, 201, xx+11, 229), 4, fill="#40566a")
    # Gavel and document marked as evidence.
    d.rounded_rectangle((861, 194, 903, 201), 3, fill="#76553a")
    d.rounded_rectangle((871, 185, 893, 196), 3, fill="#76553a")
    d.rectangle((742, 210, 772, 228), fill="#fffdf8", outline="#b9ad9a")
    text(747, 213, "EXHIBIT", 5, MUTED, True)


def tower_icon(box):
    x, y, w, h = box
    d.rectangle((x, y+h-10, x+w, y+h), fill="#d9d1c4")
    pts = [(x+w*.42,y+h-10),(x+w*.45,y+13),(x+w*.39,y+8),(x+w*.47,y+4),
           (x+w*.49,y),(x+w*.53,y+8),(x+w*.58,y+11),(x+w*.56,y+h-10)]
    d.polygon(pts, fill=NAVY)
    for yy in range(int(y+22), int(y+h-15), 9):
        line(int(x+w*.46), yy, int(x+w*.55), yy, "#d6c7ac", 2)
    # Drone with twin rotors and a red strike marker.
    line(x+8,y+17,x+33,y+17,RED,2); line(x+20,y+17,x+20,y+25,RED,2)
    line(x+4,y+13,x+12,y+13,RED,2); line(x+29,y+13,x+37,y+13,RED,2)
    circle(x+20,y+17,3,RED)


def ship_icon(box):
    x, y, w, h = box
    d.rectangle((x,y+int(h*.64),x+w,y+h),fill="#d8e3e4")
    for off in (0, 9, 18):
        line(x+2,y+int(h*.72)+off,x+w-2,y+int(h*.72)+off,"#8ca7ab",1)
    d.polygon([(x+5,y+int(h*.58)),(x+w-7,y+int(h*.58)),(x+w-18,y+int(h*.79)),(x+20,y+int(h*.79))],fill=NAVY)
    d.rectangle((x+22,y+int(h*.43),x+62,y+int(h*.58)),fill="#d9d1c4",outline=NAVY)
    d.rectangle((x+35,y+int(h*.33),x+48,y+int(h*.43)),fill=NAVY)
    line(x+42,y+int(h*.19),x+42,y+int(h*.35),RED,2)
    line(x+43,y+int(h*.2),x+66,y+int(h*.25),RED,2)
    circle(x+w-20,y+15,5,GOLD)


def medal_icon(box):
    x,y,w,h=box
    # Two officials and a ribbon medal against a simple ceremony backdrop.
    d.rectangle((x,y,x+w,y+h),fill="#e9e2d4")
    d.rectangle((x+5,y+h-11,x+w-5,y+h-7),fill="#bd9b69")
    for xx, color in ((x+18,"#435768"),(x+45,"#26394e"),(x+76,"#435768")):
        circle(xx,y+24,8,"#c99f7a")
        d.rounded_rectangle((xx-9,y+32,xx+9,y+h-12),4,fill=color)
    d.polygon([(x+51,y+7),(x+58,y+22),(x+65,y+7)],fill=RED)
    circle(x+58,y+26,7,GOLD,outline="#9e762f",thick=1)
    circle(x+58,y+26,3,"#fff0b6")


def mini_symbol(x, y, kind):
    colors = {"air":RED,"money":"#50836e","law":"#816348","world":"#3f708b",
              "energy":"#be8b3d","science":"#617b94","sport":"#4d8769",
              "people":"#a66672","rail":"#786596","shield":"#55725a"}
    c = colors[kind]
    circle(x+5,y+6,5,c)
    if kind == "air":
        d.polygon([(x+2,y+7),(x+10,y+4),(x+7,y+8),(x+10,y+10)],fill="white")
    elif kind == "money":
        text(x+5,y+6,"$",6,"white",True,anchor="mm")
    elif kind == "law":
        line(x+5,y+2,x+5,y+10,"white",1); line(x+2,y+4,x+8,y+4,"white",1)
    elif kind == "world":
        d.arc((x+2,y+3,x+8,y+9),0,360,fill="white",width=1)
        line(x+2,y+6,x+8,y+6,"white",1)
    elif kind == "energy":
        d.polygon([(x+6,y+1),(x+3,y+7),(x+6,y+7),(x+4,y+11),(x+9,y+5),(x+6,y+5)],fill="white")
    elif kind == "science":
        circle(x+5,y+6,2,"white")
        line(x+2,y+3,x+8,y+9,"white",1); line(x+8,y+3,x+2,y+9,"white",1)
    elif kind == "sport":
        circle(x+5,y+6,3,"white")
        line(x+3,y+5,x+7,y+7,"#4d8769",1)
    elif kind == "people":
        circle(x+5,y+4,2,"white"); d.arc((x+2,y+5,x+8,y+10),180,360,fill="white",width=1)
    elif kind == "rail":
        line(x+3,y+2,x+3,y+9,"white",1); line(x+7,y+2,x+7,y+9,"white",1)
        line(x+2,y+5,x+8,y+5,"white",1)
    else:
        d.polygon([(x+5,y+2),(x+8,y+3),(x+8,y+7),(x+5,y+10),(x+2,y+7),(x+2,y+3)],fill="white")


# Masthead: the publication date and title are the dominant visual anchors.
d.rectangle((0,0,W,91),fill=NAVY)
d.rectangle((0,86,W,91),fill=RED)
text(27,13,"THE WORLD TODAY",36,"#fffaf0",True)
text(29,55,"WEDNESDAY 25 NOVEMBER 2026",18,"#efe3cc",True)
text(996,17,"WORLD\nEDITION",8,"#d4c5a9",True,anchor="ra")
text(995,66,"50 STORIES · 7 REGIONS · 18 FIELDS",8,"#fffaf0",True,anchor="ra")

# Dominant front-page lead and original courtroom illustration.
section_label(28,102,"THE LEAD",RED,8)
text(28,115,"HUAWEI GUILTY",31,NAVY,True)
text(28,149,"ON 10 COUNTS",31,NAVY,True)
paragraph(29,190,"A Brooklyn jury convicts the Chinese tech giant of bank and wire fraud, sanctions violations and conspiring to steal trade secrets; acquitted on racketeering and obstruction. [Reuters]",11,585,INK,False,2,5)
courtroom()
text(664,269,"BROOKLYN FEDERAL COURT · VERDICT",7,MUTED,True)

# Three concise illustrated follow-up leads.
lead_cards = [
    ("SECOND LEAD","HOUTHIS HIT RIYADH'S TALLEST TOWER — 11 HURT",
     "Second strike in less than a week; at least 11 wounded. UAE condemns it. [Reuters / Al Jazeera]","tower"),
    ("THIRD LEAD","ZELENSKYY: WE SANK RUSSIAN WARSHIP OFF LIBYA",
     "Ukraine says two vessels struck near Benghazi; corvette Merkury sunk in Kyiv's farthest sea strike. Zelenskyy also confirms a cargo-ship drone strike in the Gulf of Finland; Norway urges caution. [Reuters / RFE/RL]","ship"),
    ("FOURTH LEAD","TRUMP GIVES GIULIANI MEDAL OF FREEDOM",
     "Closed-press Oval Office honour; Giuliani was pardoned over election-overturn efforts. [Reuters]","medal"),
]
card_x = [28, 359, 690]
for i,(label,headline,deck,kind) in enumerate(lead_cards):
    x=card_x[i]
    line(x,299,x+305,299,RED,2)
    section_label(x,305,label,RED,7)
    title, title_size = fitted(headline,10,304,True,7)
    text(x,319,title,title_size,NAVY,True)
    if kind == "tower": tower_icon((x+1,333,37,50))
    elif kind == "ship": ship_icon((x+1,333,38,50))
    else: medal_icon((x+1,333,38,50))
    paragraph(x+43,338,deck,8,258,INK,False,1,5)

# The regional conflict explainer, visually set apart as the only red band.
d.rounded_rectangle((27,387,997,431),5,fill="#eee2d0",outline="#d7c8b1")
d.rectangle((27,387,33,431),fill=RED)
section_label(43,394,"WHY THE GULF IS BURNING",RED,9)
paragraph(211,394,"Ninth month of US–Iran war: US naval blockade, tanker attacks in Hormuz, Houthi strikes on Riyadh and US bases; Brent crude below $90. [Reuters / wire]",9,769,INK,False,1,3)

# All forty-six briefs stay in the edition. The deck is a short, measured
# caption for each; source tags sit on each headline line.
stories = [
 ("RUSSIA FIRES 96 DRONES OVERNIGHT","Air defences down 73, including 45 jet-powered Shaheds; 13 sites hit.","Ukraine Air Force / Kyiv24","air"),
 ("SENATE PROBES VANCE OVER VENEZUELA OIL DEAL","Maggie Hassan seeks records on alleged help for Vitol; sales up to 100m barrels.","wire","law"),
 ("CIA AND ODNI HIT BY CYBER BREACH","Breach involves some unclassified information, a source says.","Reuters","shield"),
 ("FORT HOOD SHOOTER SEEKS STAY","Nidal Hasan seeks a stay of his scheduled execution.","Reuters","law"),
 ("SARKOZY CORRUPTION CASE TO TRIAL","Former French president and Carla Bruni face trial.","Reuters","law"),
 ("HOUTHIS WON'T TAKE ADEN","Yemeni forces say Houthis are 60 km away but will not capture the city.","Reuters","shield"),
 ("NATO EYES EARLY-WARNING JETS FOR POLAND","Deployment planned after missiles landed during an attack on Ukraine.","wire","air"),
 ("DOW TOPS 50,000 AS NVIDIA SLIDES","Nvidia -6% after a 30% rally on Huang's return; Nasdaq -1.5%, S&P -0.5%.","wire","money"),
 ("DELL LIFTS FORECASTS","Record quarter powered by surging AI server demand.","wire","money"),
 ("INDIA MARKETS REOPEN","NSE and BSE return after holiday; GIFT Nifty points about 100 higher.","Kalkine","money"),
 ("700,000 RUSSIAN SOLDIERS KILLED","Analysis puts Russian dead past 700,000 in the war on Ukraine.","RFE/RL","people"),
 ("IRAN BRACES FOR WINTER GAS SHORTAGES","War damage deepens the energy crisis as cold nears.","RFE/RL","energy"),
 ("US ENVOY 'NOT CERTAIN' ISRAEL AID ENDS","Trump promised an end; the US–Israel aid memorandum continues.","Reuters","world"),
 ("TRUMP TO UNVEIL NEW TARIFFS","Sources cite a probe into excess factory capacity.","Reuters","money"),
 ("RADAR ISSUE DELAYS O'HARE FLIGHTS","FAA reports a radar problem at Chicago O'Hare.","Reuters / FAA","air"),
 ("US TREASURY SANCTIONS IRAN SHADOW BANKING","Two dozen-plus exchanges and fronts hit after FinCEN flags $14.7bn.","US Treasury","money"),
 ("ZELENSKYY ACCEPTS PRE-CHRISTMAS TALKS","Kyiv accepts US trilateral proposal; Miami floated, no invite yet.","wire","world"),
 ("GRYNSPAN TOPS UN STRAW POLL","Rebeca Grynspan wins 10 of 15 votes; two vetoes block her.","wire","world"),
 ("UK–EU AGREE BREXIT RESET DEAL","Package includes 100,000 youth visas and food trade.","wire","world"),
 ("SENATE PASSES PERMITTING BILL 62–33","US energy-project permitting reform clears the Senate.","wire","law"),
 ("IOWA LEAD AZIDE BLAST TODAY","Army plans to detonate 68 unstable barrels; residents told to leave.","wire","shield"),
 ("ESTONIA CLOSES RUSSIA BORDER CROSSINGS","Closures begin 1 Dec after a sabotage bid.","wire","shield"),
 ("EU REJECTS RUSSIA'S SECURITY DEMANDS","Ministers back ceasefire first and approve nearly €8bn in Ukraine aid.","wire","world"),
 ("DENMARK COURT UPHOLDS 'GHETTO' EVICTIONS","Supreme Court dismisses ethnic-discrimination concerns over housing law.","wire","law"),
 ("REEF HIDES 12 'LOST' CORALS","Genetic analysis revives 12 Acropora species on the Great Barrier Reef.","wire","science"),
 ("UN: WOMAN KILLED BY FAMILY EVERY 12 MINUTES","Five women an hour were killed by relatives, UN finds.","UN","people"),
 ("BJP AND SAD ANNOUNCE PUNJAB ALLIANCE","The parties reunite for state polls, six years after splitting.","wire","world"),
 ("US AND QATAR TALK STRATEGIC COOPERATION","Officials discuss regional developments and bilateral ties.","wire","world"),
 ("UN RAISES GAZA CONCERNS","Civilians face continuing humanitarian difficulties seeking aid.","UN","people"),
 ("CHAMPIONS LEAGUE TONIGHT: 9 TIES","PSG–Roma, Liverpool at Brugge, Sporting–Man Utd; Barça at Sabah.","UEFA","sport"),
 ("AUSTRALIA INFLATION DATA DUE TODAY","CPI and RBA trimmed mean due; Japan sells 40-year bonds.","wire","money"),
 ("RUSSIAN JETS NEAR S. KOREAN ISLAND","Seoul issues an alert after Russian military flights.","wire","air"),
 ("MI5 WARNS FIRMS BACKING UKRAINE","UK companies told to act against Russian sabotage.","wire","shield"),
 ("UK ACTS AGAINST HOUTHI COMMANDERS","Sanctions imposed over abuse accusations in Yemen.","wire","law"),
 ("MOSCOW TO BUILD KALININGRAD RAIL FERRY","Plan follows a logistics 'blockade'.","wire","rail"),
 ("IRAN REPORTS TANKER EXPLOSIONS","Revolutionary Guard Navy says naval mines hit three Hormuz tankers.","wire","energy"),
 ("RUSSIA AND UKRAINE TRADE ACCUSATIONS AT UN","Dispute concerns attacks on Black Sea shipping and energy sites.","UN","world"),
 ("ENGLAND BEAT AUSTRALIA IN 2ND T20I","Eight-wicket chase of 185 levels the five-match series.","wire","sport"),
 ("RFE/RL BACK ON SHORTWAVE FOR AFGHAN GIRLS","Educational radio for girls excluded from school by Taliban.","RFE/RL","people"),
 ("NORWAY URGES KYIV CAUTION","Oslo urges restraint after the Gulf of Finland ship strike.","Reuters","world"),
 ("MAN UTD FUME OVER YORO RED CARD","Pochettino leads fury at the ruling.","wire","sport"),
 ("VENEZUELA REPORTS $237.5BN PUBLIC DEBT","Official total is published.","wire","money"),
 ("DUTCH TRAIN FARES FROZEN","Prices unchanged until the end of next May, says state secretary.","wire","rail"),
 ("UK ASKS PUBLIC ON AGE OF CONSENT","Ministers consult on a possible change.","BBC","people"),
 ("NUCLEAR TEST VETERANS GET PANEL","PM Burnham confirms independent review of Cold War atomic health legacy.","BBC","science"),
 ("SENEDD REJECTS BID TO OUST PRESIDING OFFICER","Reform motion to remove Huw Irranca Davies fails.","wire","law"),
]
assert len(stories) == 46, f"grid story count is {len(stories)}"

section_label(28,439,"THE WORLD IN BRIEF",NAVY,8)
text(995,439,"46 REPORTS · SOURCES SHOWN",7,MUTED,True,anchor="ra")

grid_top, grid_bottom = 452, 790
col_w, gap = 311, 18
grid_x = [28, 28+col_w+gap, 28+2*(col_w+gap)]
per_col = [16,15,15]
cursor = 0
for col, count in enumerate(per_col):
    x=grid_x[col]
    line(x,grid_top,x,grid_bottom,"#d5cfc4",1)
    for row in range(count):
        headline, deck, source, kind = stories[cursor]
        y=grid_top+row*21
        mini_symbol(x+5,y+1,kind)
        src=f"[{source}]"
        src_size=6
        src_w=width(src,src_size,True)
        head,hs=fitted(headline,8,x and (col_w-18-src_w-7),True,6)
        text(x+15,y,head,hs,NAVY,True)
        text(x+col_w-src_w-2,y+1,src,src_size,RED,True)
        deck_line,ds=fitted(deck,7,col_w-22,False,5)
        text(x+15,y+9,deck_line,ds,INK,False)
        if row < count-1:
            line(x+15,y+19,x+col_w-3,y+19,"#e1ddd4",1)
        cursor+=1
assert cursor == 46

# Timeline is a seven-stop strip; times are UTC as labeled.
line(28,798,996,798,NAVY,1)
section_label(28,802,"HOW WEDNESDAY UNFOLDED — UTC",NAVY,8)
timeline = [
 ("00:00","96 drones over Ukraine; 73 downed"),
 ("01:00","Kyiv confirms warship sunk off Libya"),
 ("02:00","Asia wakes to Huawei verdict, Giuliani medal"),
 ("08:00","India markets reopen; Riyadh strike confirmed"),
 ("15:00","Iowa: Army blast planned, 9am local"),
 ("17:45","Champions League opens; Sabah–Barcelona"),
 ("20:00","PSG–Roma; Liverpool, Sporting–Man Utd"),
]
for i,(when,what) in enumerate(timeline):
    x=28+i*138
    if i: line(x-6,816,x-6,846,"#d5cfc4",1)
    text(x,814,when,8,RED,True)
    paragraph(x,825,what,6,130,INK,False,1,3)

# A dotted, original schematic world map with numbered event pins.
line(28,854,996,854,NAVY,1)
section_label(28,859,"WHERE IT HAPPENED",NAVY,8)
text(28,870,"DOTTED MAP · STORY LOCATIONS",6,MUTED,True)
# Simplified continent silhouettes made from ellipses and polygons; dots form the texture.
land = [
 [(54,895),(76,884),(94,888),(108,900),(101,910),(112,919),(99,932),(90,951),(80,942),(76,927),(62,920)],
 [(115,944),(127,951),(134,969),(127,987),(120,974)],
 [(168,899),(181,885),(202,884),(217,893),(236,891),(250,902),(241,914),(225,915),(220,927),(207,929),(196,941),(183,930),(179,915),(166,910)],
 [(211,936),(224,936),(234,951),(231,967),(219,981),(212,966),(207,950)],
 [(239,920),(254,914),(267,920),(264,931),(250,936)],
 [(274,899),(291,892),(306,898),(321,903),(337,900),(351,911),(345,923),(328,927),(319,939),(304,934),(298,922),(283,919)],
 [(324,938),(336,935),(344,946),(340,960),(331,968),(325,956)],
 [(353,908),(368,905),(378,913),(372,920),(360,919)],
]
for poly in land:
    d.polygon(poly,fill="#dfd9cd")
    minx=min(p[0] for p in poly); maxx=max(p[0] for p in poly)
    miny=min(p[1] for p in poly); maxy=max(p[1] for p in poly)
    for yy in range(miny+3,maxy,6):
        for xx in range(minx+3,maxx,6):
            if im.getpixel((xx,yy)) == (223,217,205):
                circle(xx,yy,0.8,"#aaa79e")
pins=[(91,906,"1"),(202,901,"2"),(230,943,"3"),(302,911,"4"),(318,922,"5"),(122,965,"6"),(256,923,"7")]
for px,py,num in pins:
    circle(px,py,5,RED,outline=PAPER,thick=1)
    text(px,py,num,5,"white",True,anchor="mm")

# Older stories are intentionally listed with their dates in this separate box.
d.rounded_rectangle((398,859,996,999),4,fill="#ebe6dc",outline="#cfc8bb")
section_label(411,866,"DATE CHECK — LEFT OUT AS OLDER NEWS",RED,8)
older = [
 "ABU DHABI TALKS END WITH NO DEAL — 24 Nov",
 "NETANYAHU URGES TRUMP TO HIT IRAN AGAIN — 24 Nov",
 "RUSSIAN STRIKE HITS ZAPORIZHZHIA, 2 KILLED — 24 Nov",
 "GUKESH–SINDAROV TITLE MATCH OPENS — 24 Nov",
 "TRUMP PARDONS TURKEYS FREEDOM & FEATHERS — 24 Nov",
 "CHAMPIONS LEAGUE TUESDAY RESULTS (REAL 5–1 PSV) — 24 Nov",
 "ALCARAZ WINS ATP FINALS — 22 Nov",
 "COP31 COLLAPSES IN ANTALYA — 22 Nov",
 "KYIV GRID BARRAGE — 23 Nov",
 "IRAN VOWS ‘EVERY MEANS’ — 23 Nov",
 "NVIDIA +30% ON HUANG'S RETURN — 23 Nov",
 "EU PROPOSES 22ND SANCTIONS PACKAGE — 23 Nov",
 "NEPAL PM'S INDIA VISIT — 22–23 Nov",
]
for i,item in enumerate(older):
    col=i//7
    row=i%7
    x=411+col*288
    y=881+row*16
    label,size=fitted("· "+item,7,275,False,5)
    text(x,y,label,size,INK,False)

# Bottom ribbon repeats the four edition leads and the oil-market line.
d.rectangle((0,1005,W,H),fill=NAVY)
footer="HUAWEI GUILTY  ·  HOUTHIS HIT RIYADH TOWER  ·  ZELENSKYY CONFIRMS LIBYA SINKING  ·  GIULIANI HONOURED  ·  BRENT BELOW $90"
footer,size=fitted(footer,8,976,True,6)
text(24,1011,footer,size,"#fffaf0",True)

assert len(stories)+4 == 50
im.save(OUT,format="PNG",optimize=True)
print(f"Wrote {OUT} ({W}x{H}), {4+len(stories)} stories")
