from PIL import ImageFont

FD = "/usr/share/fonts/truetype/dejavu"
def f(n, s): return ImageFont.truetype(FD + "/" + n, s)
SER_B = "DejaVuSerif-Bold.ttf"
SAN = "DejaVuSans.ttf"
SAN_B = "DejaVuSans-Bold.ttf"
SER = "DejaVuSerif.ttf"

def w(font, t):
    b = font.getbbox(t)
    return b[2] - b[0]

print("== masthead date fit (target 968) ==")
d = "TUESDAY 24 NOVEMBER 2026"
for s in range(48, 80, 2):
    print(" ", s, w(f(SER_B, s), d))

print("== featured headlines ==")
hl = [
    "Huang's return ignites the rebound — then Tuesday fades it",
    "Trump dares, Iran answers with the law",
    "Serang toll 26, and a negligence probe opens",
]
for t in hl:
    print(" ", len(t), [(s, w(f(SER_B,s), t)) for s in (11,12,13)])

print("== featured deks at 11 ==")
dk = [
 "Monday's close was Wall Street's best since April 2025; Asia rallies, the US fades.",
 "14+ tankers massed at Kharg; the convoy has not sailed; Iran invokes Article 51.",
 "26 dead and 8 missing after Saturday's candy-factory fire; a negligence probe opens.",
]
for t in dk:
    print(" ", len(t), w(f(SAN,11), t))

print("== grid headlines at 11 ==")
gh = [
 "Hamas security chief killed in Tuesday's strikes",
 "Two killed, 40 wounded in an overnight strike",
 "COP31 fallout: the process itself on trial",
 "Oregon and Virginia sue SpaceX over Grok images",
 "Vance and Rubio meet Qatar's PM — separately",
]
for t in gh:
    print(" ", len(t), w(f(SER_B,11), t))

print("== grid deks at 11 ==")
gd = [
 "Strikes kill Hamas security chief Naeem Abu Nahel and six others on Tuesday.",
 "Governor: overnight Russian strike kills two and wounds 40, four children.",
 "Germany is the first country with access to Ukraine's Delta battlefield system.",
]
for t in gd:
    print(" ", len(t), w(f(SAN,11), t))

print("== longest brief ==")
t27 = "CL matchday 5: Madrid 5-1 PSV, Arsenal 1-1 Dortmund, City 2-2 Napoli, Gala 1-0 Villa, Feyenoord 0-1 Porto, Leipzig 3-1 Lens."
for s in (8, 9):
    print("  size", s, "px", w(f(SAN,s), t27))

print("== stat captions ==")
for t in ["Nvidia's Monday jump on Huang's reinstatement (~$952bn added)",
          "confirmed dead in the Serang factory fire, 8 still missing"]:
    print(" ", len(t), [(s, w(f(SAN,s), t)) for s in (8, 9)])

print("== stat values ==")
for v in ["+31.5%","+6.51%","14+","26","404","700,000+"]:
    print(" ", v, w(f(SER_B,20), v), w(f(SER_B,22), v))

print("== timeline text at 8 ==")
for t in ["Wall Street closes: Nasdaq +6.51%, S&P +4.73%, Dow +3.01%",
          "Asia opens the rebound: Kospi +6.5%, Taiex +9%+, Nikkei +3.9%"]:
    print(" ", len(t), w(f(SAN,8), t))

print("== how sure line at 8 ==")
hs = "CONFIRMED two or more major outlets · OFFICIAL on the record from officials or agencies · REPORTED one outlet · CLAIM unverified claim, typeset as a claim"
print(" ", w(f(SAN,8), hs))

print("== date check ==")
for t in ["Brussels strike shutdown — MONDAY 23 NOV (Tuesday carries only the tally)",
          "Serang \"28 unaccounted\" — ONE TUE STATEMENT, conflicts with AP's 8 missing"]:
    print(" ", len(t), w(f(SAN,8), t))
