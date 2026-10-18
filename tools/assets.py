"""Genera logos transparentes, favicon, og:image, fotos WebP y fuentes WOFF locales."""
import os, io
from PIL import Image, ImageDraw, ImageFont
from fontTools import subset
from fontTools.ttLib import TTFont

UP = '/mnt/user-data/uploads/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets') + '/'
FONT_SRC = '/usr/share/fonts/truetype/google-fonts/'

# ---------- Fuentes (subset latino, WOFF) ----------
UNI = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + [0x2013,0x2014,0x2018,0x2019,0x201C,0x201D,0x2022,0x2026,0x20AC,0x2192,0x00B7]
for name, f in [('400','Poppins-Regular'),('500','Poppins-Medium'),('700','Poppins-Bold')]:
    opts = subset.Options(); opts.flavor = 'woff'; opts.layout_features = ['*']; opts.name_IDs=[1,2]
    font = TTFont(FONT_SRC + f + '.ttf')
    s = subset.Subsetter(opts); s.populate(unicodes=UNI); s.subset(font)
    font.flavor = 'woff'; font.save(OUT + f'fonts/poppins-{name}.woff')

# ---------- Logo transparente ----------
src = Image.open(UP + 'logo.jpg').convert('RGB')
W, H = src.size
bg = (251, 248, 231)
px = src.load()
# tintas: morado de la palabra y verde azulado del globo (se muestrean del propio logo)
def darkest(box):
    best=None
    for y in range(box[1],box[3]):
        for x in range(box[0],box[2]):
            p=px[x,y]; s=sum(p)
            if best is None or s<best[0]: best=(s,p)
    return best[1]
purple = (74,34,114)
teal   = (42,106,98)
print('tintas', purple, teal)
def alpha_for(p, ink):
    v=[p[i]-bg[i] for i in range(3)]; d=[ink[i]-bg[i] for i in range(3)]
    dd=sum(x*x for x in d); a=max(0,min(1,sum(v[i]*d[i] for i in range(3))/dd))
    res=sum((v[i]-a*d[i])**2 for i in range(3))
    return a,res
col = Image.new('RGBA',(W,H)); white = Image.new('RGBA',(W,H))
cp=col.load(); wp=white.load()
for y in range(H):
    for x in range(W):
        p=px[x,y]
        a1,r1=alpha_for(p,purple); a2,r2=alpha_for(p,teal)
        a,ink=(a1,purple) if r1<=r2 else (a2,teal)
        a = 0 if a<0.04 else (1 if a>0.96 else a)
        cp[x,y]=(*ink,int(a*255)); wp[x,y]=(255,255,255,int(a*255))
bb=col.getbbox(); pad=4
bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(W,bb[2]+pad),min(H,bb[3]+pad)); print('logo bbox',bb)
colc=col.crop(bb); whitec=white.crop(bb)
colc.save(OUT+'img/logo.png', optimize=True); whitec.save(OUT+'img/logo-white.png', optimize=True)

# ---------- Favicon (globo) ----------
globe = col.crop((18,30,150,165))
globe = globe.crop(globe.getbbox())
def fav(size, pad=0.16, bgc=(251,248,231,255), radius=0.22):
    base = Image.new('RGBA',(size,size),(0,0,0,0))
    d = ImageDraw.Draw(base); d.rounded_rectangle((0,0,size-1,size-1), radius=int(size*radius), fill=bgc)
    inner = int(size*(1-2*pad)); g = globe.copy(); g.thumbnail((inner,inner), Image.LANCZOS)
    base.alpha_composite(g, ((size-g.width)//2,(size-g.height)//2)); return base
fav(180).save(OUT+'img/apple-touch-icon.png'); fav(192).save(OUT+'img/icon-192.png'); fav(512).save(OUT+'img/icon-512.png')
fav(48).save(OUT+'img/favicon-48.png'); fav(32).save(OUT+'img/favicon-32.png')

# ---------- Fotos ----------
ph = Image.open(UP + 'IMG-20260524-WA0045_1.jpg').convert('RGB')
def save(im, name, q=78): im.save(OUT+'img/'+name, 'WEBP', quality=q, method=6)
arch = ph.crop((0,300,960,1500))
save(arch, 'hero-960.webp'); save(arch.resize((600,750), Image.LANCZOS), 'hero-600.webp')
save(ph.resize((1400,1050), Image.LANCZOS), 'about-1400.webp', 74); save(ph.resize((800,600), Image.LANCZOS), 'about-800.webp')

# ---------- og:image 1200x630 ----------
og = Image.new('RGB',(1200,630),(87,35,100))
crop = ph.crop((0,330,1100,1330)).resize((694,631), Image.LANCZOS)
og.paste(crop,(506,0))
d = ImageDraw.Draw(og)
lg = white.copy(); lg.thumbnail((420,170), Image.LANCZOS)
og.paste(lg,(56,70),lg)
fb = ImageFont.truetype(FONT_SRC+'Poppins-Bold.ttf', 44); fr = ImageFont.truetype(FONT_SRC+'Poppins-Regular.ttf', 27)
d.text((56,300),'Free tours en',font=fb,fill=(255,255,255)); d.text((56,352),'Valencia y Altea',font=fb,fill=(212,175,55))
d.text((56,440),'Viajes privados · ES · IT · EN',font=fr,fill=(240,230,245))
og.save(OUT+'img/og-image.jpg', quality=86, optimize=True)
print('ok')
