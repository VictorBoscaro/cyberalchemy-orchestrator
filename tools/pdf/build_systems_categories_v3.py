from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Image, Table, TableStyle, KeepTogether, Flowable, HRFlowable,
)

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "output/pdf/systems-and-categories-v3/systems_and_categories_toward_domain_languages_v3.md"
OUT = ROOT / "output/pdf/systems-and-categories-v3/systems_and_categories_toward_domain_languages_v3.pdf"
MEDIA = ROOT / "tmp/docx_v3_extract/word/media"
FONTS = ROOT / "tmp/fonts"

CHARCOAL = colors.HexColor("#25292D")
BLUE = colors.HexColor("#52677A")
GOLD = colors.HexColor("#A58A63")
PALE = colors.HexColor("#EEF1F2")
LINE = colors.HexColor("#BCC5CA")
LIGHT = colors.HexColor("#DCE1E3")
WHITE = colors.white

pdfmetrics.registerFont(TTFont("EBG", str(FONTS / "EBGaramond.ttf")))
pdfmetrics.registerFont(TTFont("EBGI", str(FONTS / "EBGaramond-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Inter", str(FONTS / "Inter.ttf")))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    s = s.replace("—", "-").replace("–", "-").replace("→", "-&gt;")
    return s


styles = {
    "body": ParagraphStyle("body", fontName="EBG", fontSize=12, leading=14.5,
        textColor=CHARCOAL, alignment=TA_JUSTIFY, spaceAfter=7, allowWidows=0, allowOrphans=0),
    "caption": ParagraphStyle("caption", fontName="EBGI", fontSize=9.2, leading=11,
        textColor=BLUE, alignment=TA_CENTER, spaceBefore=5, spaceAfter=8),
    "h3": ParagraphStyle("h3", fontName="EBG", fontSize=16, leading=18, textColor=BLUE,
        spaceBefore=10, spaceAfter=5, keepWithNext=True),
    "h4": ParagraphStyle("h4", fontName="EBG", fontSize=13, leading=15, textColor=BLUE,
        spaceBefore=8, spaceAfter=3, keepWithNext=True),
    "ref": ParagraphStyle("ref", fontName="EBG", fontSize=10, leading=12, leftIndent=12,
        firstLineIndent=-12, spaceAfter=5, textColor=CHARCOAL),
}


class SectionTitle(Flowable):
    def __init__(self, number, title, eyebrow=""):
        super().__init__(); self.number=number; self.title=title; self.eyebrow=eyebrow
        self.height = 79 if len(title) < 42 else 96
    def wrap(self, aw, ah): self.width=aw; return aw, self.height
    def draw(self):
        c=self.canv; w=self.width
        if self.eyebrow:
            c.setFillColor(BLUE); c.setFont("EBG", 8.5); c.drawString(0, self.height-9, self.eyebrow.upper())
        c.setFillColor(BLUE); c.setFont("Inter", 28); c.drawString(0, self.height-48, self.number)
        p=Paragraph(inline(self.title), ParagraphStyle("st", fontName="EBG", fontSize=21,
            leading=22, textColor=CHARCOAL, spaceAfter=0))
        offset = 72 if self.number == "6" else 50
        pw,ph=p.wrap(w-offset, 50); p.drawOn(c, offset, self.height-25-ph)
        c.setStrokeColor(LINE); c.setLineWidth(.55); c.line(0, 0, w, 0)


class LensFigure(Flowable):
    def __init__(self): super().__init__(); self.height=210
    def wrap(self, aw, ah): self.width=aw; return aw,self.height
    def draw_panel(self,c,x,y,w,h,title,accent,systemic):
        c.setFillColor(colors.white); c.setStrokeColor(LIGHT); c.roundRect(x,y,w,h,5,fill=1,stroke=1)
        c.setFont("Inter",9); c.setFillColor(accent); c.drawString(x+12,y+h-20,title.upper())
        pts={"promise":(x+30,y+74),"capacity":(x+105,y+106),"delay":(x+170,y+66),"retention":(x+108,y+34)}
        edges=[("promise","capacity"),("capacity","delay"),("delay","retention"),("retention","promise")]
        for a,b in edges:
            chosen = systemic or (a,b) in [("promise","capacity"),("capacity","delay")]
            c.setStrokeColor(accent if chosen else LIGHT); c.setLineWidth(1.5 if chosen else .7)
            c.line(*pts[a],*pts[b])
        for name,(px,py) in pts.items():
            chosen = systemic or name in ("promise","capacity","delay")
            c.setFillColor(accent if chosen else colors.HexColor("#C8CED1")); c.circle(px,py,4,fill=1,stroke=0)
            c.setFillColor(CHARCOAL if chosen else BLUE); c.setFont("Inter",7); c.drawCentredString(px,py-14,name)
        c.setFillColor(BLUE); c.setFont("EBG",9)
        note="behavior through time" if systemic else "translation and preservation"
        c.drawCentredString(x+w/2,y+9,note)
    def draw(self):
        c=self.canv; w=self.width; gap=16; pw=(w-gap)/2
        c.setFillColor(BLUE); c.setFont("Inter",8); c.drawCentredString(w/2,self.height-14,"THE SAME SITUATION, DIFFERENT RELATIONS MADE SALIENT")
        self.draw_panel(c,0,18,pw,165,"Systemic lens",BLUE,True)
        self.draw_panel(c,pw+gap,18,pw,165,"Categorical lens",GOLD,False)


class InfrastructureFigure(Flowable):
    def __init__(self): super().__init__(); self.height=245
    def wrap(self,aw,ah): self.width=aw; return aw,self.height
    def draw(self):
        c=self.canv; w=self.width
        c.setFont("Inter",8); c.setFillColor(BLUE); c.drawCentredString(w/2,232,"LANGUAGES PARTICIPATE ACROSS THE PATH WITHOUT BECOMING UNIFORM")
        labels=["INTENTION","ORCHESTRATION","BOUNDED WORK","EFFECT"]
        xs=[6,126,258,390]; boxw=92
        for i,(x,l) in enumerate(zip(xs,labels)):
            c.setFillColor(colors.white); c.setStrokeColor(BLUE if i<3 else GOLD); c.roundRect(x,105,boxw,46,4,fill=1,stroke=1)
            c.setFillColor(BLUE if i<3 else GOLD); c.setFont("Inter",8); c.drawCentredString(x+boxw/2,128,l)
            if i<3:
                c.setStrokeColor(BLUE); c.line(x+boxw,128,xs[i+1]-4,128)
        bands=[("HUMAN LANGUAGE",BLUE,30,455,202),
               ("DOMAIN LANGUAGE A",GOLD,72,385,184),
               ("SHARED RELATIONAL LANGUAGE",BLUE,115,430,166),
               ("DOMAIN LANGUAGE B",GOLD,220,470,88)]
        for label,col,x1,x2,y in bands:
            c.setStrokeColor(col); c.setLineWidth(3); c.line(x1,y,x2,y)
            c.setFillColor(col); c.setFont("Inter",7); c.drawString(x1,y+5,label)
        c.setFillColor(PALE); c.setStrokeColor(LIGHT); c.roundRect(25,22,w-50,54,5,fill=1,stroke=1)
        c.setFillColor(BLUE); c.setFont("Inter",8); c.drawString(38,54,"RECOVERABLE CONTEXT / KNOWLEDGE")
        c.setFillColor(CHARCOAL); c.setFont("EBG",9.5); c.drawString(38,37,"scope, versions, translations, authority, and unresolved mismatches remain reachable")
        c.setStrokeColor(colors.Color(.65,.54,.39,alpha=.6)); c.setLineWidth(1.2); c.roundRect(110,96,230,69,7,fill=0,stroke=1)
        c.setFillColor(GOLD); c.setFont("Inter",7); c.drawString(118,154,"SITUATED LENS: SELECTED RELATIONS")


class EssayDoc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path), pagesize=A4, leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=72,
            title="Systems and Categories: Toward Domain Languages", author="Victor Boscaro")
        frame=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id="main",showBoundary=0)
        self.addPageTemplates(PageTemplate(id="internal",frames=[frame],onPage=self.decorate))
    def decorate(self,c,doc):
        if doc.page==1: return
        c.saveState(); c.setFont("Inter",8); c.setFillColor(BLUE)
        c.drawString(54,A4[1]-25,"SYSTEMS AND CATEGORIES")
        c.setStrokeColor(LINE); c.setLineWidth(.45); c.line(54,A4[1]-36,A4[0]-54,A4[1]-36)
        c.drawRightString(A4[0]-54,25,f"TOWARD DOMAIN LANGUAGES   ·   {doc.page}")
        c.restoreState()


EYEBROWS={"0":"READER ORIENTATION","1":"REPRESENTATION","2":"SYSTEMS AND CATEGORIES",
"3":"ANALOGY AND FORMAL TRANSLATION","4":"PROGRESSIVE FORMALIZATION","5":"COMPOSITIONAL SYSTEMS MODELING",
"6":"RUPTURE AND RESIDUE","7":"MAKING THE REGIME OF INVESTIGATION EXPLICIT","8":"FROM REPRESENTATION TO ACTION",
"9":"A DESIGN DIRECTION","10":"REFLEXIVE TURN","A":"APPENDIX","B":"APPENDIX","C":"APPENDIX"}


def cover(story):
    story += [Spacer(1,45), Paragraph("SYSTEMS AND CATEGORIES", ParagraphStyle("cover",fontName="EBG",fontSize=32.5,leading=35,textColor=CHARCOAL)),
              Spacer(1,18), HRFlowable(width="100%",thickness=.8,color=GOLD), Spacer(1,18),
              Paragraph("Toward Domain Languages", ParagraphStyle("sub",fontName="EBGI",fontSize=21,leading=24,textColor=BLUE)),
              Paragraph("An essay on representation, composition, and the construction of domain languages.", ParagraphStyle("strap",fontName="Inter",fontSize=9,leading=12,textColor=BLUE)), Spacer(1,42)]
    img=Image(str(MEDIA/"image1.png"),width=430,height=240); story += [img,Spacer(1,105),
        Paragraph("Victor Boscaro",ParagraphStyle("author",fontName="Inter",fontSize=9,textColor=BLUE)),
        Paragraph("ResonantOS",ParagraphStyle("brand",fontName="Inter",fontSize=7,textColor=BLUE))]


def parse_md():
    lines=MD.read_text(encoding="utf-8").splitlines(); story=[]; cover(story)
    in_comment=False; i=0; refs=False
    while i<len(lines):
        raw=lines[i].strip()
        if raw.startswith("<!--"):
            in_comment=True
            spec=[]
            while i<len(lines):
                spec.append(lines[i])
                if "-->" in lines[i]: break
                i+=1
            txt=" ".join(spec)
            if "SAME SITUATION" in txt: story += [Spacer(1,5),LensFigure()]
            elif "TRANSVERSAL LANGUAGES" in txt: story += [Spacer(1,5),InfrastructureFigure()]
            elif "embedded image 2" in txt: story += [Image(str(MEDIA/"image2.png"),width=430,height=126)]
            elif "embedded image 3" in txt: story += [Image(str(MEDIA/"image3.png"),width=430,height=161)]
            in_comment=False; i+=1; continue
        if not raw or raw in ("---",): i+=1; continue
        if raw.startswith("# Systems") or raw.startswith("## Toward") or raw.startswith("*An essay on"):
            i+=1; continue
        m=re.match(r"## (?:Appendix )?([0-9]+|[A-C])\.\s*(.+)",raw)
        if m:
            num,title=m.groups(); story.append(PageBreak()); story.append(SectionTitle(num,title,EYEBROWS.get(num,""))); refs=False; i+=1; continue
        if raw=="## References":
            story.append(PageBreak()); story.append(SectionTitle("","References","")); refs=True; i+=1; continue
        if raw.startswith("### "):
            story.append(Paragraph(inline(raw[4:]),styles["h3"])); i+=1; continue
        if raw.startswith("#### "):
            story.append(Paragraph(inline(raw[5:]),styles["h4"])); i+=1; continue
        if raw.startswith("|"):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith("|"):
                cells=[c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c)<=set("-: ") for c in cells): rows.append(cells)
                i+=1
            data=[[Paragraph(inline(c),ParagraphStyle("tc",fontName="Inter",fontSize=8.8,leading=11,textColor=CHARCOAL)) for c in row] for row in rows]
            tbl=Table(data,colWidths=[225,102,160],repeatRows=1,hAlign="LEFT")
            tbl.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),BLUE),("TEXTCOLOR",(0,0),(-1,0),WHITE),
                ("FONTNAME",(0,0),(-1,0),"Inter"),("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,1),(-1,-1),.35,LIGHT),
                ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
            story += [tbl,Spacer(1,6)]; continue
        if raw.startswith("> **CENTRAL QUESTION"):
            q=lines[i+1].strip().lstrip("> ").strip("*") if i+1<len(lines) else ""
            label=Paragraph("CENTRAL QUESTION",ParagraphStyle("ql",fontName="Inter",fontSize=7.5,textColor=BLUE))
            question=Paragraph(f"<i>{inline(q)}</i>",ParagraphStyle("qq",fontName="EBGI",fontSize=13,leading=15,textColor=CHARCOAL))
            t=Table([[label],[question]],colWidths=[470]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE),("LINEBEFORE",(0,0),(0,-1),3,BLUE),("LEFTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)])); story += [t,Spacer(1,7)]; i+=2; continue
        if raw.startswith("*Figure"):
            story.append(Paragraph(inline(raw.strip("*")),styles["caption"])); i+=1; continue
        if raw.startswith("-") and refs:
            story.append(Paragraph(inline(raw[1:].strip()),styles["ref"])); i+=1; continue
        if raw.startswith("Victor Boscaro") or raw=="ResonantOS": i+=1; continue
        # join normal markdown paragraph until structural break
        parts=[raw]; i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r"(#{2,4} |<!--|\||>|- )",lines[i].strip()):
            parts.append(lines[i].strip()); i+=1
        story.append(Paragraph(inline(" ".join(parts)),styles["body"]))
    return story


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True,exist_ok=True)
    EssayDoc(OUT).build(parse_md())
    print(OUT)
