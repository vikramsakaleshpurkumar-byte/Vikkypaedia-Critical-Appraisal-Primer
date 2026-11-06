"""Portable source-led textbook course pipeline. See references/course-schema.md."""
from __future__ import annotations
import argparse,collections,hashlib,html,json,pathlib,re,shutil,subprocess,sys,unicodedata
P=pathlib.Path
ASSETS=P(__file__).resolve().parents[1]/'assets'
def read(p):return json.loads(P(p).read_text(encoding='utf-8-sig'))
def write(p,obj):
 p=P(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def text(p,s):
 p=P(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def pdf_open(path):
 try:
  import pymupdf
  if not callable(getattr(pymupdf,'open',None)):raise ImportError('PyMuPDF 1.x API unavailable')
  return pymupdf,pymupdf.open(str(path))
 except ImportError as e:raise SystemExit('Install compatible PyMuPDF (known working: 1.26.7) in the selected Python environment. '+str(e))
def clean(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('\x07',' ')
 s=re.sub(r'(\w)-\s*\n\s*([a-z])',r'\1\2',s)
 return re.sub(r'\s+',' ',s).strip()
def inspect(a):
 fitz,doc=pdf_open(a.pdf);out=P(a.out);toc=doc.get_toc();numbered=[]
 for level,title,page in toc:
  m=re.match(r'^(?:chapter\s+)?(\d+(?:\.\d+)?)\s*[.\-–—:]?\s+(.+)$',title,re.I)
  if m:numbered.append({'num':len(numbered)+1,'source_label':m[1],'title':m[2].strip(),'start':page,'group':'All chapters'})
 numbered.sort(key=lambda c:c['start'])
 for i,c in enumerate(numbered):c['num']=i+1;c['end']=numbered[i+1]['start']-1 if i+1<len(numbered) else len(doc)
 sample=sorted(set([0,min(5,len(doc)-1),len(doc)//2,len(doc)-1]+[c['start']-1 for c in numbered[:5]]))
 info={'source_name':P(a.pdf).name,'source_path':str(P(a.pdf).resolve()),'sha256':hashlib.file_digest(open(a.pdf,'rb'),'sha256').hexdigest(),'pdf_pages':len(doc),'metadata':doc.metadata,'bookmarks':toc,'samples':[]}
 for i in sample:
  p=doc[i];info['samples'].append({'pdf_page':i+1,'size':list(p.rect),'fonts':sorted(set(f[3] for f in p.get_fonts())),'image_placements':len(p.get_image_info()),'text':p.get_text()[:3500]})
 write(out/'inspection.json',info)
 write(out/'manifest.draft.json',{'reviewed':False,'title':doc.metadata.get('title') or P(a.pdf).stem,'course_name':'Vikkypaedia · Subject Course','edition':None,'year':None,'publisher':None,'authors':None,'subtitle':'Self-paced study course','chapters':numbered,'omitted_pages':[],'glyph_map':{},'features':[],'column_split':None,'header_fraction':.075,'footer_fraction':.035})
 print(json.dumps({'pages':len(doc),'draft_chapters':len(numbered),'out':str(out),'review_required':True}))
def lines_for(page,fitz,glyph_map):
 blocks=[]
 for b in page.get_text('dict',flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']:
  if b['type']!=0:continue
  lines=[]
  for l in b['lines']:
   ss=l['spans'];parts=[]
   for s in ss:
    val=s['text']
    for font,mapping in glyph_map.items():
     if font in s['font']:val=''.join(mapping.get(ch,ch) for ch in val)
    parts.append(val)
   lines.append({'text':''.join(parts),'size':max(s['size'] for s in ss),'bold':any(re.search('Bold|Black|Semibold',s['font'],re.I) for s in ss),'bbox':l['bbox'],'dir':l['dir']})
  if lines:blocks.append({'bbox':b['bbox'],'lines':lines})
 return blocks
def gutter(blocks,width,columns,override):
 if columns==1:return None
 if override is not None:return float(override)*width if float(override)<1 else float(override)
 mass=collections.Counter()
 for b in blocks:
  for l in b['lines']:
   if len(l['text'])>20:mass[round(l['bbox'][0]/4)*4]+=len(l['text'])
 peaks=mass.most_common(12)
 left=[p for p in peaks if p[0]<width*.4];right=[p for p in peaks if width*.4<=p[0]<=width*.72]
 if left and right:
  l=max(left,key=lambda x:x[1]);r=max(right,key=lambda x:x[1])
  if r[0]-l[0]>width*.22 and r[1]>.15*l[1]:return r[0]-3
 return width*.5 if columns==2 else None
def manifest_check(m,npages):
 if not m.get('reviewed'):raise ValueError('Review manifest boundaries and set reviewed=true before extraction.')
 if not m.get('chapters'):raise ValueError('A reviewed manifest must contain at least one chapter.')
 if [c['num'] for c in m['chapters']]!=list(range(1,len(m['chapters'])+1)):raise ValueError('Normalized chapter IDs must be 1..N.')
 for c in m['chapters']:
  pages=c.get('pages',list(range(c['start'],c['end']+1)))
  if not pages or any(p<1 or p>npages for p in pages):raise ValueError('Invalid chapter pages: '+str(c['num']))
def extract(a):
 fitz,doc=pdf_open(a.pdf);m=read(a.manifest);manifest_check(m,len(doc));root=P(a.out);chapters=[];inventory=[]
 source={'source_name':P(a.pdf).name,'sha256':hashlib.file_digest(open(a.pdf,'rb'),'sha256').hexdigest(),'pdf_pages':len(doc),'title':m['title'],'edition':m.get('edition'),'year':m.get('year'),'publisher':m.get('publisher'),'authors':m.get('authors')}
 for spec in m['chapters']:
  num=spec['num'];pages=spec.get('pages',list(range(spec['start'],spec['end']+1)));paragraphs=[];figures=[];tables=[];views=[];raw=[f"# {spec.get('source_label',num)}. {spec['title']}",'> Source attribution: [Source credits](../../SOURCE_CREDITS.md).\n'];heading='Overview'
  for pn in pages:
   page=doc[pn-1];blocks=lines_for(page,fitz,m.get('glyph_map',{}));split=gutter(blocks,page.rect.width,spec.get('columns'),spec.get('column_split',m.get('column_split')))
   pp=spec.get('printed_start');pp=pp+(pn-pages[0]) if isinstance(pp,int) else None
   sizes=collections.Counter()
   for b in blocks:
    for l in b['lines']:sizes[round(l['size'],1)]+=len(l['text'])
   body_size=sizes.most_common(1)[0][0] if sizes else 9
   parts=[]
   for b in blocks:
    for side in ([0,1] if split else [0]):
     ls=[l for l in b['lines'] if (split is None or (0 if l['bbox'][0]<split else 1)==side) and page.rect.height*m.get('header_fraction',.075)<=l['bbox'][1]<=page.rect.height*(1-m.get('footer_fraction',.035))]
     if ls:parts.append((side,min(l['bbox'][1] for l in ls),ls))
   parts.sort(key=lambda b:(b[0],b[1]));raw.append(f'\n## PDF page {pn}'+(f' | printed page {pp}' if pp is not None else '')+'\n');chars=0
   for _,_,ls in parts:
    buf=[];isbody=True;lasthead=False
    def flush():
     if not buf:return
     val=clean('\n'.join(buf));raw.append(val+'\n')
     if isbody and val and not re.match(r'^(?:Image|Figure|Fig\.|Table|Courtesy|Source:|©)\s',val):paragraphs.append({'text':val,'heading':heading,'pdf_page':pn,'printed_page':pp})
     buf.clear()
    for l in ls:
     val=clean(l['text']);chars+=len(val)
     head=l['bold'] and len(val)<180 and (l['size']>body_size+.8 or val.isupper()) and not re.match(r'^(?:CHAPTER\s+\d|IMAGE|FIGURE|TABLE)',val)
     if head:
      flush()
      if lasthead:heading+=' '+val;raw[-1]='### '+heading+'\n'
      else:heading=val;raw.append('### '+heading+'\n')
      lasthead=True
     else:
      lasthead=False
      if buf and isbody!=(l['size']>=body_size-.35):flush()
      isbody=l['size']>=body_size-.35;buf.append(l['text'])
    flush()
   caps=[(b['bbox'],clean('\n'.join(l['text'] for l in b['lines']))) for b in blocks if re.match(r'^(?:Image|Figure|Fig\.)\s*\d',clean(b['lines'][0]['text']))]
   expanded=[]
   for bb,cap in caps:
    if len(cap)<30:
     following=[b for b in blocks if bb[3]-2<=b['bbox'][1]<=bb[3]+20 and abs(b['bbox'][0]-bb[0])<15]
     if following:cap+=' '+clean('\n'.join(l['text'] for l in min(following,key=lambda b:b['bbox'][1])['lines']))
    expanded.append((bb,cap))
   caps=expanded
   for j,im in enumerate(page.get_image_info(xrefs=True)):
    rect=fitz.Rect(im['bbox']) & page.rect
    if rect.width<m.get('min_image_width',45) or rect.height<m.get('min_image_height',40) or rect.get_area()<m.get('min_image_area',3000):continue
    candidates=[(bb,t) for bb,t in caps if bb[1]>=rect.y1-15 and abs(bb[0]-rect.x0)<max(80,rect.width*.6)]
    cap=min(candidates,key=lambda z:abs(z[0][1]-rect.y1))[1] if candidates else f'Unmatched source image; PDF page {pn}. Consult the original caption.'
    name=f'figures/ch{num:03d}_p{pn:04d}_{j+1:02d}.jpg';(root/'figures').mkdir(parents=True,exist_ok=True);page.get_pixmap(clip=rect,dpi=a.dpi,alpha=False).save(root/name,jpg_quality=86)
    figures.append({'path':name,'caption':cap,'caption_matched':bool(candidates) and len(cap)>25,'pdf_page':pn,'printed_page':pp,'chapter':num});raw.append(f"![Source image](../../{name})\n\n{cap}\n")
   all_lines=[l for b in blocks for l in b['lines']];vertical=bool(all_lines) and sum(abs(l['dir'][1])>.8 for l in all_lines)>len(all_lines)*.5
   tmp=None;tp=page
   if vertical:
    tmp=fitz.open();tmp.insert_pdf(doc,from_page=pn-1,to_page=pn-1);tp=tmp[0];tp.set_rotation(90 if sum(l['dir'][1] for l in all_lines)<0 else 270);tp.remove_rotation()
   if m.get('detect_tables',True) and (vertical or re.search(r'\bTable\s+\d',page.get_text())):
    try:
     for j,t in enumerate(tp.find_tables(strategy='lines_strict').tables):
      if t.row_count<2 or t.col_count<2:continue
      name=f'tables/ch{num:03d}_p{pn:04d}_{j+1}.jpg';(root/'tables').mkdir(parents=True,exist_ok=True);tp.get_pixmap(clip=fitz.Rect(t.bbox),dpi=a.dpi,alpha=False).save(root/name,jpg_quality=88)
      md=t.to_markdown();tables.append({'path':name,'markdown':md,'pdf_page':pn,'printed_page':pp,'orientation_normalized':vertical});raw.extend(['\n### Automatic table extraction — verify rendered original\n',md,f'\n[Original table](../../{name})\n'])
    except Exception as e:tables.append({'pdf_page':pn,'printed_page':pp,'extraction_error':str(e)})
   if pn in spec.get('page_views',[]) or chars<40 or vertical:
    name=f'tables/ch{num:03d}_page{pn:04d}.jpg';(root/'tables').mkdir(parents=True,exist_ok=True);tp.get_pixmap(dpi=a.dpi,alpha=False).save(root/name,jpg_quality=88);views.append({'path':name,'pdf_page':pn,'printed_page':pp})
   if tmp:tmp.close()
   inventory.append({'pdf_page':pn,'chapter':num,'characters':chars,'low_text':chars<40})
  c={**spec,'num':num,'pdf_start':min(pages),'pdf_end':max(pages),'pages':pages,'printed_start':spec.get('printed_start'),'printed_end':spec.get('printed_start')+max(pages)-min(pages) if isinstance(spec.get('printed_start'),int) else None,'paragraphs':paragraphs,'figures':figures,'tables':tables,'page_views':views,'raw_md':'\n'.join(raw)}
  chapters.append(c);text(root/f'raw/chapters/{num:03d}.md',c['raw_md']);write(root/f'build/evidence/ch{num:03d}.json',c)
  print(f"Extracted {num}/{len(m['chapters'])}: {spec['title']}",flush=True)
 write(root/'build/extraction.json',chapters);write(root/'build/page_inventory.json',inventory);write(root/'build/source_metadata.json',source);write(root/'build/manifest.json',m)
def scaffold(a):
 root=P(a.course);cs=read(root/'build/extraction.json')
 write(a.out,{'chapters':[{'num':c['num'],'pillars':[],'cards':[],'mcqs':[],'atlas':{},'therapies':[],'authoring_status':'unwritten','evidence_file':f"build/evidence/ch{c['num']:03d}.json"} for c in cs]})
 print('Wrote empty authoring ledger; write source-supported content before claiming full-depth completion.')
def strip_meta(s):return re.sub(r'\s+',' ',re.sub(r'\b(?:this chapter|see chapter|see table|see fig(?:ure)?)\b[^.;]*[.;]?','',s,flags=re.I)).strip()
def snippet(c,pattern):
 for p in c['paragraphs']:
  if re.search(pattern,p['heading'],re.I) and len(p['text'])>50:
   ss=re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])',strip_meta(p['text']));return {**p,'text':' '.join(ss[:2])}
 return None
def point(p,c):return {'pdf_page':p['pdf_page'],'printed_page':p.get('printed_page')}
def build(a):
 root=P(a.course);cs=read(root/'build/extraction.json');m=read(root/'build/manifest.json');src=read(root/'build/source_metadata.json');tools=read(a.study_tools) if a.study_tools else {'chapters':[]};by={c['num']:c for c in tools['chapters']}
 if len(by)!=len(tools['chapters']) or set(by)-{c['num'] for c in cs}:raise ValueError('Duplicate or unknown study-tools chapter ID.')
 features=m.get('features',[]);cards=[];quizzes=[];atlas=[];therapies=[];figures=[];catalog=[];coverage=[]
 esc=lambda s:html.escape(str(s))
 pillars_default=[('Mechanism and etiology','ETIOLOG|PATHOGEN|MECHANISM'),('Clinical recognition','CLINICAL|PRESENTATION|OVERVIEW'),('Diagnostic workup','DIAGNOS'),('Treatment and interventions','TREATMENT|MANAGEMENT|THERAP'),('Prevention and prognosis','CONTROL|PREVENTION|PROGNOS')]
 for c in cs:
  n=c['num'];st=by.get(n,{});group=c.get('group','All chapters');ps=st.get('pillars',[])
  if not ps:ps=[{'label':label,**p} for label,pat in pillars_default if (p:=snippet(c,pat))]
  body=' '.join(p['text'] for p in c['paragraphs']);tags=[f['label'] for f in features if re.search(f['pattern'],body,re.I)]
  for i,f in enumerate(st.get('cards',[]),1):cards.append({**f,'id':f'fc-{n:03d}-{i}','ch':n,'group':group,'category':f.get('category','Active recall'),'q':strip_meta(f['q']),'a':strip_meta(f['a']),'printed_page':f.get('printed_page')})
  authored=0
  for i,q in enumerate(st.get('mcqs',[]),1):
   kind=q.get('kind','Authored MCQ');authored+=kind=='Authored MCQ';notes=[]
   for j,note in enumerate(q.get('option_notes',[])):
    note={'text':note} if isinstance(note,str) else note
    notes.append({'option':q['options'][j],**note,'ch':note.get('ch',n),'pdf_page':note.get('pdf_page',q['pdf_page']),'printed_page':note.get('printed_page',q.get('printed_page'))})
   quizzes.append({**q,'id':f'q-{n:03d}-{i}','ch':n,'kind':kind,'q':strip_meta(q['q']),'explanation':strip_meta(q['explanation']),'printed_page':q.get('printed_page'),'option_chapters':q.get('option_chapters',[]),'option_notes':notes})
  for t in st.get('therapies',[]):therapies.append({**t,'ch':n,'title':c['title'],'group':group,'drugs':t.get('drugs',[]),'section':t.get('section','Source excerpt'),'has_dose':bool(t.get('has_dose',False)),'printed_page':t.get('printed_page')})
  summary=next((p['text'] for p in ps if re.search('recognition|clinical|overview',p['label'],re.I)),ps[0]['text'] if ps else '')
  entry={'num':n,'source_label':c.get('source_label',str(n)),'title':c['title'],'group':group,'features':tags,'pdf_start':c['pdf_start'],'pdf_end':c['pdf_end'],'printed_start':c.get('printed_start'),'printed_end':c.get('printed_end'),'figures':len(c['figures']),'tables':sum('path' in t for t in c['tables']),'cards':sum(f['ch']==n for f in cards),'summary':summary}
  catalog.append(entry);figures+=c['figures']
  at=st.get('atlas',{});atlas.append({**entry,'etiology':at.get('etiology') or snippet(c,'ETIOLOG|PATHOGEN|MECHANISM|OVERVIEW'),'epidemiology':at.get('epidemiology') or snippet(c,'EPIDEMIO|TRANSMISSION'),'diagnostics':at.get('diagnostics') or snippet(c,'DIAGNOS')})
  sections=[];previous_heading=None
  for p in c['paragraphs']:
   h=f"<h2>{esc(p['heading'].title())}</h2>" if p['heading']!=previous_heading else ''
   sections.append(f"<section>{h}<p>{esc(p['text'])}</p><small class='source'>PDF p. {p['pdf_page']}</small></section>");previous_heading=p['heading']
  for view in c['page_views']+[t for t in c['tables'] if 'path' in t]:sections.append(f"<figure><a href='{view['path']}' target='_blank'><img loading='lazy' src='{view['path']}' alt='Source page or table'></a><figcaption>PDF p. {view['pdf_page']}</figcaption></figure>")
  for f in c['figures']:sections.append(f"<figure><a href='{f['path']}' target='_blank'><img loading='lazy' src='{f['path']}' alt='{esc(f['caption'])}'></a><figcaption>{esc(f['caption'])}<br>PDF p. {f['pdf_page']}</figcaption></figure>")
  payload={**entry,'pillars':ps,'figures':c['figures'],'tables':c['tables'],'reader_html':''.join(sections)}
  text(root/f'data/chapters/ch_{n:03d}.js','window.registerChapter('+json.dumps(payload,ensure_ascii=False)+');\n')
  cm=[f"# {c.get('source_label',n)}. {c['title']}",'> [Source credits](../../SOURCE_CREDITS.md).\n','## Study pillars\n']
  cm += [f"### {p['label']}\n\n{p['text']}\n\nPDF p. {p['pdf_page']}\n" for p in ps];cm+=['\n## Full source extraction\n',c['raw_md']];text(root/f'wiki/chapters/{n:03d}.md','\n'.join(cm))
  fs=[f for f in cards if f['ch']==n];qs=[q for q in quizzes if q['ch']==n]
  text(root/f'wiki/flashcards/{n:03d}_flashcards.md','\n\n'.join(f"<details><summary>{esc(f['q'])}</summary>\n\n{f['a']}\n\nPDF p. {f['pdf_page']}\n</details>" for f in fs))
  text(root/f'wiki/mcqs/{n:03d}_mcqs.md','\n\n'.join(f"## {q['kind']}\n\n{q['q']}\n\n"+'\n'.join(f'{chr(65+j)}. {o}' for j,o in enumerate(q['options']))+f"\n\n<details><summary>Answer and rationale</summary>\n\n{q['options'][q['answer']]}\n\n{q['explanation']}\n\nPDF p. {q['pdf_page']}\n</details>" for q in qs))
  coverage.append({'num':n,'title':c['title'],'cards':len(fs),'authored_mcqs':authored,'automated_mcqs':len(qs)-authored,'gap':len(fs)<6 or authored<5,'gap_reason':st.get('gap_reason','Study tools remain incomplete; inspect chapter evidence.'),'review_statuses':dict(collections.Counter(x.get('review_status','draft') for x in fs+qs))})
 stats={'chapters':len(cs),'figures':len(figures),'matched_captions':sum(f['caption_matched'] for f in figures),'tables':sum(c['tables'] for c in catalog),'flashcards':len(cards),'mcqs':len(quizzes),'authored_mcqs':sum(c['authored_mcqs'] for c in coverage),'treatment_records':len(therapies),'depth_gap_chapters':sum(c['gap'] for c in coverage)}
 data={'course_name':m.get('course_name','Vikkypaedia · Subject Course'),'storage_key':m.get('storage_key','vikkypaedia_'+re.sub(r'\W+','_',m.get('course_name',m['title']).lower())),'source_pdf':m.get('public_source_pdf_url'),'chapters':catalog,'atlas':atlas,'therapies':therapies,'cards':cards,'quizzes':quizzes,'figures':figures,'features':[f['label'] for f in features],'groups':list(dict.fromkeys(c['group'] for c in catalog)),'stats':stats}
 text(root/'data/course.js','window.COURSE='+json.dumps(data,ensure_ascii=False)+';\n');write(root/'build/course_data.json',data);write(root/'build/coverage.json',coverage)
 assets=P(a.assets) if a.assets else ASSETS
 page=(assets/'index.html').read_text(encoding='utf-8').replace('@@COURSE_NAME@@',esc(data['course_name'])).replace('@@COURSE_SUBTITLE@@',esc(m.get('subtitle','Personal learning course')))
 text(root/'index.html',page);shutil.copyfile(assets/'app.js',root/'data/app.js');text(root/'.nojekyll','')
 anki=['#separator:tab','#html:true','#tags column:3']
 for f in cards:anki.append(esc(f['q']).replace('\n','<br>')+'\t'+esc(f['a']).replace('\n','<br>')+f"<br><br>PDF p. {f['pdf_page']}\tVikkypaedia Ch_{f['ch']:03d} "+re.sub(r'\W+','_',f['category']))
 text(root/'anki_course.tsv','\n'.join(anki)+'\n');text(root/'index.md','# '+data['course_name']+'\n\n'+'\n'.join(f"- [{c['source_label']}. {c['title']}](wiki/chapters/{c['num']:03d}.md)" for c in catalog))
 credits=f"# Source credits\n\nTitle: {src['title']}\n\nEdition/year: {src.get('edition')} / {src.get('year')}\n\nAuthors/editor: {src.get('authors') or 'Not yet confirmed'}\n\nPublisher: {src.get('publisher') or 'Not yet confirmed'}\n\nOriginal text, captions, figure credits, and rights remain with their respective holders. Course branding does not imply authorship or endorsement of source material.\n\nSource SHA-256: `{src['sha256']}`\n\n"+m.get('permissions_note','Publication permissions have not been established by this build.')
 text(root/'SOURCE_CREDITS.md',credits)
 text(root/'README.md',f"# {data['course_name']}\n\nOpen index.html with its folders intact. No server is needed. Import anki_course.tsv as Front/Back/Tags.\n\nSee [source credits](SOURCE_CREDITS.md) and [build report](BUILD_REPORT.md).\n\nClinical/source content requires appropriate editorial review. Feature overlap is not a diagnostic probability. Source-edition treatment excerpts are not automatically current prescribing guidance.\n")
 text(root/'BUILD_REPORT.md','# Build report\n\n'+json.dumps(stats,indent=2)+'\n\nFull-depth targets: 6–10 cards and five authored MCQs per chapter.\n\n'+('\n'.join(f"- Chapter {c['num']}: {c['cards']} cards, {c['authored_mcqs']} authored MCQs; {c['gap_reason']}" for c in coverage if c['gap']) or 'All minimum depth targets met; editorial/specialist review status remains separate.')+'\n\nAutomatic extraction and caption matches are not a facsimile or independent clinical validation. See build/coverage.json, build/page_inventory.json, and build/source_metadata.json.\n')
 print(json.dumps(stats,indent=2))
def verify(a):
 root=P(a.course);d=read(root/'build/course_data.json');cs=read(root/'build/extraction.json');m=read(root/'build/manifest.json');errors=[];warnings=[];checks=[]
 def check(name,condition):
  checks.append({'name':name,'passed':bool(condition)})
  if not condition:errors.append(name)
 check('Normalized chapter IDs',[c['num'] for c in cs]==list(range(1,len(cs)+1)))
 expected=[p for c in m['chapters'] for p in c.get('pages',list(range(c['start'],c['end']+1)))];actual=[p for c in cs for p in c['pages']]
 check('Exact declared source page coverage',collections.Counter(expected)==collections.Counter(actual))
 omitted=set()
 for item in m.get('omitted_pages',[]):
  if isinstance(item,int):omitted.add(item)
  else:
   if not item.get('reason'):errors.append('Omitted range has no reason')
   omitted.update(range(item['start'],item['end']+1))
 source=read(root/'build/source_metadata.json')
 check('All PDF pages scoped or explicitly omitted',set(expected)|omitted==set(range(1,source['pdf_pages']+1)))
 check('No scope/omission overlap',not(set(expected)&omitted))
 if len(actual)!=len(set(actual)):warnings.append('Shared pages require explicit boundary review.')
 for c in cs:check('Chapter files '+str(c['num']),all((root/s).exists() for s in [f"raw/chapters/{c['num']:03d}.md",f"wiki/chapters/{c['num']:03d}.md",f"data/chapters/ch_{c['num']:03d}.js"]))
 for key in ['cards','quizzes','therapies']:
  for x in d[key]:
   c=cs[x['ch']-1];check('Source reference '+x.get('id',str(x['ch'])),x.get('pdf_page') in c['pages'])
 for q in d['quizzes']:
  check('Answer/options '+q['id'],len(q['options'])==5 and len(set(q['options']))==5 and isinstance(q['answer'],int) and 0<=q['answer']<5)
  if q['kind']=='Authored MCQ':
   check('Distractor notes '+q['id'],len(q['option_notes'])==5 and all(n.get('text','').strip() for n in q['option_notes']))
   check('Blind source title '+q['id'],len(cs[q['ch']-1]['title'])<5 or cs[q['ch']-1]['title'].lower() not in q['q'].lower())
  for note in q.get('option_notes',[]):
   check('Option evidence '+q['id']+' '+note['option'],1<=note['ch']<=len(cs) and note['pdf_page'] in cs[note['ch']-1]['pages'])
 check('No study meta boilerplate',not re.search(r'\b(?:this chapter|see chapter|see table|see fig(?:ure)?)\b',json.dumps(d['cards']+d['quizzes']),re.I))
 try:from PIL import Image
 except ImportError:Image=None;warnings.append('Pillow unavailable: image decoding was not checked.')
 assets=d['figures']+[t for c in cs for t in c['tables']+c['page_views'] if 'path' in t]
 for f in assets:
  p=root/f['path'];valid=p.is_file()
  if valid and Image:
   try:
    with Image.open(p) as im:im.verify()
   except Exception:valid=False
  check('Asset '+f['path'],valid)
 for p in root.rglob('*.md'):
  for rel in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
   if re.match(r'^[A-Za-z]+:|^#',rel):continue
   check('Markdown link '+str(p.relative_to(root))+' '+rel,(p.parent/rel.split('#')[0]).exists())
 for rel in re.findall(r'<script[^>]+src="([^"]+)"',(root/'index.html').read_text(encoding='utf-8')):check('HTML script '+rel,(root/rel).is_file())
 node=shutil.which('node')
 if node:
  for p in (root/'data').rglob('*.js'):check('JS syntax '+p.name,subprocess.run([node,'--check',str(p)],capture_output=True).returncode==0)
 else:warnings.append('Node unavailable: JavaScript syntax checks were not run.')
 coverage=read(root/'build/coverage.json');gaps=[c['num'] for c in coverage if c['gap']]
 if gaps:warnings.append('Full-depth study-tool gaps: '+', '.join(map(str,gaps)))
 if a.strict_depth:check('Full-depth minimums',not gaps)
 result={'technical_passed':not errors,'full_depth_complete':not gaps,'errors':errors,'warnings':warnings,'checks':checks,'metrics':d['stats']};write(root/'build/verification.json',result);print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
 return 0 if not errors else 1
def main():
 p=argparse.ArgumentParser(description=__doc__);sp=p.add_subparsers(dest='command',required=True)
 s=sp.add_parser('inspect');s.add_argument('--pdf',required=True);s.add_argument('--out',required=True);s.set_defaults(run=inspect)
 s=sp.add_parser('extract');s.add_argument('--pdf',required=True);s.add_argument('--manifest',required=True);s.add_argument('--out',required=True);s.add_argument('--dpi',type=int,default=150);s.set_defaults(run=extract)
 s=sp.add_parser('scaffold-study');s.add_argument('--course',required=True);s.add_argument('--out',required=True);s.set_defaults(run=scaffold)
 s=sp.add_parser('build');s.add_argument('--course',required=True);s.add_argument('--study-tools');s.add_argument('--assets',help='Workspace copy of frontend assets with subject-specific labels');s.set_defaults(run=build)
 s=sp.add_parser('verify');s.add_argument('--course',required=True);s.add_argument('--strict-depth',action='store_true');s.set_defaults(run=verify)
 a=p.parse_args();return a.run(a) or 0
if __name__=='__main__':
 try:sys.exit(main())
 except (ValueError,KeyError,OSError) as e:raise SystemExit(str(e))
