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


def rocket():
    # A compact launch vignette: Shenzhou-24 lifts off toward the station.
    d.rounded_rectangle((655, 119, 990, 281), 8, fill="#1d3350", outline="#d5cbbb", width=1)
    # Stars and the station silhouette the capsule is heading for.
    for sx, sy in ((684, 140), (716, 158), (905, 138), (940, 162), (872, 132), (700, 186), (958, 190)):
        circle(sx, sy, 1.6, "#e8dfc8")
    d.rectangle((896, 146, 952, 152), fill=GOLD)
    d.rectangle((918, 138, 930, 160), fill="#e8dfc8")
    d.rectangle((884, 147, 896, 151), fill="#9db4cc")
    d.rectangle((952, 147, 964, 151), fill="#9db4cc")
    # Rocket body, capsule nose and fins.
    d.polygon([(806, 238), (812, 176), (822, 150), (832, 176), (838, 238)], fill="#f4f0e6")
    d.polygon([(812, 176), (822, 150), (832, 176)], fill=RED)
    d.rectangle((813, 196, 831, 204), fill=NAVY)
    d.polygon([(806, 238), (792, 256), (806, 252)], fill=RED)
    d.polygon([(838, 238), (852, 256), (838, 252)], fill=RED)
    # Exhaust flame and launch-pad smoke.
    d.polygon([(812, 238), (822, 268), (832, 238)], fill=GOLD)
    d.polygon([(817, 238), (822, 258), (827, 238)], fill="#fff0b6")
    for cx, cy, r in ((776, 262, 13), (806, 268, 16), (842, 268, 16), (868, 262, 12)):
        circle(cx, cy, r, "#d9d1c4")
    d.rectangle((672, 262, 974, 270), fill="#132943")
    text(822, 128, "00:18 UTC", 7, "#efe3cc", True, anchor="ma")


def chart_icon(box):
    x, y, w, h = box
    d.rectangle((x, y, x+w, y+h), fill="#e9e2d4")
    line(x+4, y+4, x+4, y+h-5, NAVY, 1)
    line(x+4, y+h-5, x+w-3, y+h-5, NAVY, 1)
    # A falling index line for the Asian AI selloff.
    pts = [(x+5, y+8), (x+13, y+12), (x+19, y+10), (x+26, y+22), (x+31, y+30), (x+w-4, y+38)]
    d.line(pts, fill=RED, width=2)
    for px, py in pts:
        circle(px, py, 1.8, RED)
    d.polygon([(x+w-4, y+38), (x+w-10, y+36), (x+w-6, y+31)], fill=RED)


def ship_icon(box):
    x, y, w, h = box
    d.rectangle((x,y+int(h*.64),x+w,y+h),fill="#d8e3e4")
    for off in (0, 9, 18):
        line(x+2,y+int(h*.72)+off,x+w-2,y+int(h*.72)+off,"#8ca7ab",1)
    d.polygon([(x+5,y+int(h*.58)),(x+w-7,y+int(h*.58)),(x+w-18,y+int(h*.79)),(x+20,y+int(h*.79))],fill=NAVY)
    d.rectangle((x+22,y+int(h*.43),x+62,y+int(h*.58)),fill="#d9d1c4",outline=NAVY)
    d.rectangle((x+35,y+int(h*.33),x+48,y+int(h*.43)),fill=NAVY)
    line(x+24,y+int(h*.19),x+24,y+int(h*.35),RED,2)
    line(x+25,y+int(h*.2),x+34,y+int(h*.25),RED,2)
    circle(x+w-20,y+15,5,GOLD)


def shield_icon(box):
    x,y,w,h=box
    # A phone guarded by a shield: Australia's new online-safety duty.
    d.rectangle((x,y,x+w,y+h),fill="#e9e2d4")
    d.rounded_rectangle((x+10,y+4,x+28,y+h-4),3,fill=NAVY)
    d.rectangle((x+13,y+9,x+25,y+h-10),fill="#f4f0e6")
    d.polygon([(x+19,y+14),(x+24,y+16),(x+24,y+22),(x+19,y+26),(x+14,y+22),(x+14,y+16)],fill="#55725a")
    d.line([(x+16.5,y+20),(x+18.5,y+22),(x+22,y+17.5)],fill="white",width=1)


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
text(995,66,"50 STORIES · 7 REGIONS · 22 FIELDS",8,"#fffaf0",True,anchor="ra")

# Dominant front-page lead and original launch illustration.
section_label(28,102,"THE LEAD",RED,8)
text(28,115,"SHENZHOU-24",31,NAVY,True)
text(28,149,"DOCKS IN ORBIT",31,NAVY,True)
paragraph(29,190,"China launches Shenzhou-24 at 00:18 UTC; the capsule docks with the space station at 03:56 UTC carrying Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali. [AP / Reuters]",11,585,INK,False,2,5)
rocket()
text(664,284,"SHENZHOU-24 · LAUNCH 00:18 UTC · DOCKING 03:56 UTC",7,MUTED,True)

# Three concise illustrated follow-up leads.
lead_cards = [
    ("SECOND LEAD","IRAN: READY TO WITHSTAND US BLOCKADE",
     "Vice-president Aref said Wednesday Tehran is unconcerned by the naval blockade as cargo shifts to other borders; October inflation hit 88.7%. [Reuters]","ship"),
    ("THIRD LEAD","ASIAN STOCKS TUMBLE IN AI SELLOFF",
     "Taiex fell over 6% Wednesday, TSMC −8.1%, Kospi −5.6%, Nikkei −3.6% and SoftBank −16.1% as AI shares slid. [AP]","chart"),
    ("FOURTH LEAD","AUSTRALIA PASSES ONLINE-SAFETY DUTY",
     "The Digital Duty of Care passed both Houses Wednesday; penalties reach 5% of global turnover or A$109.2m. [AP]","shield"),
]
card_x = [28, 359, 690]
for i,(label,headline,deck,kind) in enumerate(lead_cards):
    x=card_x[i]
    line(x,299,x+305,299,RED,2)
    section_label(x,305,label,RED,7)
    title, title_size = fitted(headline,10,304,True,7)
    text(x,319,title,title_size,NAVY,True)
    if kind == "chart": chart_icon((x+1,333,37,50))
    elif kind == "ship": ship_icon((x+1,333,38,50))
    else: shield_icon((x+1,333,38,50))
    paragraph(x+43,338,deck,8,258,INK,False,1,5)

# The day's big picture, visually set apart as the only red band.
d.rounded_rectangle((27,387,997,431),5,fill="#eee2d0",outline="#d7c8b1")
d.rectangle((27,387,33,431),fill=RED)
section_label(43,394,"THE DAY IN ONE LINE",RED,9)
paragraph(211,394,"Wednesday mixed a space docking and an AI market rout with Hormuz tanker blasts, fresh US tariffs and data, and wars from Ukraine to Gaza and Sudan — every story below is dated 25 November. [wire]",9,769,INK,False,1,3)

# All forty-six briefs stay in the edition. The deck is a short, measured
# caption for each; source tags sit on each headline line.
stories = [
 ("INDIA MARKETS RALLY","ASIA · Sensex +1,502 to 83,938; Nifty +470.","wire","money"),
 ("BANGLADESH RAISES GARMENT WAGE 36%","ASIA · To 17,000 taka from 1 Dec; vote 4–2.","wire","people"),
 ("AUSTRALIA CPI AT 4.9%","OCEANIA · October CPI 4.9% y/y; trimmed mean 3.8%.","ABS","money"),
 ("JAXA UNVEILS MOON ROVER MODEL","ASIA · Test rover to hunt water at lunar south pole.","BBC","science"),
 ("ISHIKAWA ANNOUNCES MARRIAGE","ASIA · Table-tennis star announced it Wednesday.","JIJI","people"),
 ("PROSECUTORS SEEK DEATH PENALTY","ASIA · Chiba double-murder arson trial, Wednesday.","JIJI","law"),
 ("SOLOMON–AUSTRALIA TREATY SIGNED","OCEANIA · Bars foreign military base in Solomons.","wire","world"),
 ("EUROSTAR STRIKE DISRUPTS TRAINS","EUROPE · Strike hit services on 25 November.","AP","rail"),
 ("CHAMPIONS LEAGUE: WEDNESDAY RESULTS","EUROPE · Barça 4–1, Liverpool 3–0, Bayern beaten.","UEFA","sport"),
 ("MERZ ACCUSES RUSSIA IN BUNDESTAG","EUROPE · Defends defence spending and Ukraine aid.","wire","world"),
 ("RUSSIA FIRES 112 DRONES OVERNIGHT","EUROPE · 88 downed or suppressed by 08:00 Wed.","Ukraine AF","air"),
 ("UKRAINE HITS REFINERIES, AIRBASE","EUROPE · 3 MiG-31 and 2 Su-34 damaged overnight.","wire","air"),
 ("GERMAN GDP GROWS JUST 0.1%","EUROPE · Q3 revised down from 0.2%, Destatis Wed.","Destatis","money"),
 ("ESA RELEASES HERA ASTEROID IMAGES","SPACE · Stadium-size crater on Dimorphos shown Wed.","ESA/CNN","science"),
 ("UK TO LICENCE KNIFE SELLERS","EUROPE · Home Office announced scheme Wednesday.","Home Office","law"),
 ("OFGEM: BILLS TO RISE 26%","EUROPE · Cap £2,166 from January, announced Wed.","Ofgem","energy"),
 ("POUNDLAND ENTERS ADMINISTRATION","EUROPE · 11,000 jobs at risk; administrators Wed.","AlixPartners","money"),
 ("UKRAINE SAYS LASER DOWNED JET DRONE","EUROPE · Adviser Wed called Blysk hit a world first.","wire","shield"),
 ("BBC: 490,334 RUSSIAN DEATHS","EUROPE · Leak analysis published Wednesday.","BBC","people"),
 ("NEW INHIBITOR REVIVES ANTIBIOTIC","SCIENCE · IMP-2380 restores ciprofloxacin vs MRSA.","Nat Chem Biol","science"),
 ("GHB TRACE FOUND UP TO 48 HOURS","SCIENCE · Marker study published Wednesday.","Sci Adv","science"),
 ("UN WARNS OF ATROCITY RISK IN GAZA","MIDEAST · Türk warned Wednesday; ~2m displaced.","UN News","people"),
 ("IRAN: TWO TANKERS HIT MINES","MIDEAST · IRGC: blasts early Wednesday in Hormuz.","IRGC","energy"),
 ("HOUTHIS CLAIM RAS TANURA STRIKE","MIDEAST · Claim Wed; refinery hit unconfirmed.","Just Security","shield"),
 ("ISRAEL KILLS ABUELOUF FAMILY","MIDEAST · Mohammad Abuelouf, wife, 2 children Wed.","wire","people"),
 ("JUDGES URGE DROPPING NETANYAHU CASE","MIDEAST · Drop Case 4000 bribery, judges Wed.","wire","law"),
 ("LIBYA'S LNA VOWS RETALIATION","AFRICA · Vow Wednesday after two officers' deaths.","wire","shield"),
 ("19 KILLED IN SUDAN RSF STRIKES","AFRICA · Emergency Lawyers reported Wednesday.","E. Lawyers","people"),
 ("EGYPT TANKER FIRE KILLS 21","AFRICA · Vehicle blaze on ring road Wednesday.","Reuters","energy"),
 ("UN: 10 EBOLA WORKERS EVACUATED","AFRICA · Mission said Wednesday; Ituri fighting.","Reuters","people"),
 ("NIGERIA ANNOUNCES METH SEIZURE","AFRICA · 1,512 kg announced Wed; raid was 11 Nov.","NDLEA","shield"),
 ("CAF NAMES PLAYER OF YEAR FINALISTS","AFRICA · Five-man shortlist announced Wednesday.","CAF","sport"),
 ("MACKENZIE CONVICTED ON NEW COUNTS","AFRICA · Child-cruelty counts, convicted Wednesday.","wire","law"),
 ("CAR MEDIA HOLD DAY WITHOUT NEWS","AFRICA · Outlets silent Wednesday over pressure.","wire","world"),
 ("US PROPOSES TARIFFS ON 14 PARTNERS","AMERICAS · Excess-capacity tariffs proposed Wed.","Reuters","money"),
 ("IOWA DETONATES 68 LEAD AZIDE DRUMS","AMERICAS · Blast completed Wed; readings near zero.","wire","shield"),
 ("COURT ORDERS RESPONSE IN HASAN CASE","AMERICAS · Order Wed: reply by noon CT Friday.","court","law"),
 ("US GDP REVISED UP TO 4.3%","AMERICAS · PCE 3.8%, core 3.3%, claims 189K Wed.","Commerce","money"),
 ("WALL STREET ENDS MIXED WEDNESDAY","AMERICAS · Dow +0.33%; S&P −0.25%, Nasdaq −0.62%.","wire","money"),
 ("MACY'S PARADE POSTPONED TO SATURDAY","AMERICAS · 100th parade moved, announced Wed.","wire","people"),
 ("DIVERS FIND 6 IN PLANE WRECK","AMERICAS · Search ended early Wed; victims named.","wire","people"),
 ("JUDGE BLOCKS BIRTHRIGHT ORDER","AMERICAS · Injunction issued Wednesday.","wire","law"),
 ("BEIGE BOOK: GROWTH, STICKY PRICES","AMERICAS · 8 of 12 districts grew; released Wed.","Fed","money"),
 ("FCC CLEARS SPACEX DATA-CENTRE SATS","AMERICAS · Up to 1m Starmind satellites Wed.","Reuters","science"),
 ("ECUADOR: TALKS REVIEW US OPERATIONS","LATAM · Minister spoke Wednesday after US pause.","Reuters","world"),
 ("POPE LAMENTS COP31 FAILURE","GLOBAL · Leo XIV voiced concern Wednesday.","wire","world"),
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
 ("00:18","Shenzhou-24 launches"),
 ("03:56","Capsule docks with station"),
 ("07:00","German GDP revised to 0.1%"),
 ("13:30","US GDP and PCE data land"),
 ("15:00","Iowa lead azide detonation"),
 ("17:55","FCC clears SpaceX Starmind"),
 ("19:35","Fed Beige Book released"),
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
 "HUAWEI GUILTY VERDICT — 24 Nov",
 "HOUTHIS HIT RIYADH TOWER — 24 Nov",
 "GIULIANI MEDAL OF FREEDOM — 24 Nov",
 "RUSSIA 96 DRONES / 73 DOWNED — 23–24 Nov",
 "WARSHIP SUNK OFF LIBYA — 22–23 Nov",
 "NUCLEAR PANEL ANNOUNCED — 24 Nov",
 "DOW 50,000 TUESDAY CLOSE — 24 Nov",
 "700,000 RUSSIAN DEAD ESTIMATE — 23 Nov",
 "SARKOZY TRIAL ORDER — 24 Nov",
 "NATO AWACS POLAND DECISION — 23 Nov",
 "QUASAR DISCOVERY ANNOUNCED — 24 Nov",
 "SHURI CASTLE REOPENED — 23 Nov",
 "SINNER KNEE SURGERY — 24 Nov",
 "LAKERS BEAT JAZZ — 23 Nov",
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
footer="SHENZHOU-24 DOCKS  ·  IRAN DEFIES BLOCKADE  ·  ASIAN STOCKS SLIDE  ·  AUSTRALIA ONLINE-SAFETY LAW  ·  EVERY STORY DATED 25 NOV"
footer,size=fitted(footer,8,976,True,6)
text(24,1011,footer,size,"#fffaf0",True)

assert len(stories)+4 == 50
im.save(OUT,format="PNG",optimize=True)
print(f"Wrote {OUT} ({W}x{H}), {4+len(stories)} stories")
