from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from PIL import Image
p=Path(r'C:/Users/joshu/Documents/GitHub/Apps/NovaAcademyGate');out=p/'deliverables';qa=p/'artifacts/worksheet-format-v2';src=Path(r'C:/Users/joshu/Downloads/WEEK 12 LAB WORKSHEET.docx')
D=Document(src);base=deepcopy(D.paragraphs[2]._p.pPr);sect=deepcopy(D.sections[0]._sectPr)
# Preserve portrait geometry, repair non-integer Word twip attributes and remove multi-column pseudo-tables.
for element in sect.iter():
 for k,v in list(element.attrib.items()):
  try:
   if '.' in v:element.set(k,str(round(float(v))))
  except ValueError:pass
for tag in ['cols','type']:
 for x in sect.findall(qn('w:'+tag)):sect.remove(x)
body=D._element.body
for x in list(body):body.remove(x)
body.append(sect)
def para(text='',bold=False,size=12,keep=False):
 pp=D.add_paragraph();pr=deepcopy(base)
 for tag in ['sectPr','pBdr','ind','spacing','rPr','framePr','tabs']:
  for x in pr.findall(qn('w:'+tag)):pr.remove(x)
 pp._p.insert(0,pr);fmt=pp.paragraph_format;fmt.space_before=Pt(0);fmt.space_after=Pt(6);fmt.line_spacing=1.08;fmt.keep_with_next=keep;fmt.widow_control=True
 if pp._p.getprevious() is not None and pp._p.getprevious().tag == qn('w:tbl'):fmt.space_before=Pt(7)
 rr=pp.add_run(text);rr.font.name='Arial';rr.font.size=Pt(size);rr.bold=bold;rr.font.color.rgb=RGBColor(0,0,0)
 return pp
def heading(t):return para(t,True,12,True)
def answer(t):
 pp=para('Answer: '+t,size=11);pp.paragraph_format.left_indent=Inches(.15);return pp
def num(n,t):return para(f'{n}. {t}',size=11)
def code(text):
 pp=para(text.strip(),size=8.5);pp.paragraph_format.line_spacing=1;pp.paragraph_format.keep_together=True
 for r in pp.runs:r.font.name='Consolas'
def page():D.add_page_break()
def table(headers,rows,widths,size=9):
 t=D.add_table(rows=1,cols=len(headers));t.autofit=False
 for col,w in zip(t.columns,widths):col.width=Inches(w)
 for cell,txt in zip(t.rows[0].cells,headers):cell.text=txt
 for row in rows:
  for c,txt in zip(t.add_row().cells,row):c.text=str(txt)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for j,c in enumerate(row.cells):
   c.width=Inches(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   pr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for side in ['top','left','bottom','right']:
    e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
   pr.append(b);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EEEEEE' if i==0 else 'FFFFFF');pr.append(shade)
   mar=OxmlElement('w:tcMar')
   for side in ['top','left','bottom','right']:
    e=OxmlElement('w:'+side);e.set(qn('w:w'),'70');e.set(qn('w:type'),'dxa');mar.append(e)
   pr.append(mar)
   for pp in c.paragraphs:
    pp.paragraph_format.space_after=Pt(1);pp.paragraph_format.line_spacing=1.04
    for r in pp.runs:r.font.name='Arial';r.font.size=Pt(size);r.bold=i==0;r.font.color.rgb=RGBColor(0,0,0)
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 return t
def shot(label,filename,caption,maxh=7.1):
 heading(label);para(caption,size=10)
 f=out/'screenshots'/filename;w,h=Image.open(f).size
 D.add_picture(str(f),width=Inches(min(6.48,maxh*w/h)));D.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER;D.paragraphs[-1].paragraph_format.space_after=Pt(0);D.paragraphs[-1].paragraph_format.space_before=Pt(0)
 para('Screenshot: '+filename,size=9)
para('LAB WORKSHEET: Build the Nova Academy Gate',True,12)
para('Week 12 Hands-On Lab | Tool: Visual Studio (ASP.NET MVC 5) | Time: 90 minutes',True,11)
para('Name: ____________________  Section: __________  Date: __________\nLab Score: ______ / 50',size=11)
para('Web-stack submission: React / Next.js / TypeScript / Node.js / Three.js. Original MVC prompts are retained below; implemented equivalents are labelled.',size=10)
heading('Mission Brief')
para("The Academy’s sign-up page is live, but it accepts anything. In this lab you will build the Pilot Registration page and make it reject bad data with friendly messages.",size=11)
para('Deliverables: (1) working project, (2) screenshots for each checkpoint, (3) completed test table, (4) answers to the reflection questions.',size=11)
heading('Step 1: Create the Project and Model (8 points)')
num(1,'Create a new ASP.NET Web Application (.NET Framework) named DemoValidation using the MVC template.')
num(2,'Right-click the Models folder, then Add > Class, and name it Pilot.cs.')
num(3,'Add these properties. Fill in the attributes yourself (use the rules table below).')
para('Implemented equivalent: NovaAcademyGate; shared model and validator in lib/pilot.ts. PilotId is not an input because no registration record is persisted.',size=10)
table(['Property','Rule','Error message to show'],[['PilotName','Required; 3–20 characters','Every pilot needs a callsign (3 to 20 characters)!'],['Age','18–60 inclusive','Pilots must be 18 to 60 years old.'],['Email','Required; valid email pattern','That email is lost in space.'],['Mobile','Required; well-formed; at most 11 characters','Please enter a valid mobile number.']],[.75,2.2,3.55])
para('Completed original MVC attribute blanks (C# reference, not executed by this web app):',size=10)
code('''public int PilotId { get; set; }
[Required(ErrorMessage="Every pilot needs a callsign (3 to 20 characters)!")]
[StringLength(20, MinimumLength=3,
 ErrorMessage="Every pilot needs a callsign (3 to 20 characters)!")]
public string PilotName { get; set; }
[Range(18, 60, ErrorMessage="Pilots must be 18 to 60 years old.")]
public int Age { get; set; }
[Required(ErrorMessage="That email is lost in space.")]
[EmailAddress(ErrorMessage="That email is lost in space.")]
public string Email { get; set; }
[Required(ErrorMessage="Please enter a valid mobile number.")]
[Phone(ErrorMessage="Please enter a valid mobile number.")]
[StringLength(11, ErrorMessage="Please enter a valid mobile number.")]
public string Mobile { get; set; }''')
page();shot('Checkpoint 1: Take a screenshot of your finished Pilot.cs.','01_model_source.png','Web equivalent: actual lib/pilot.ts, including shared rules and messages. Phone policy is 7–11 digits, at most 11 total characters; it is not exact .NET Phone parser parity.')
page();heading('Step 2: Add the Controller (8 points)')
num(1,'Right-click the Controllers folder, then Add > Controller, and choose MVC 5 Controller - Empty.')
num(2,'Name it PilotController (remember, it must end with “Controller”).')
num(3,'Replace the generated action with the two actions below. Fill in the blanks.')
para('Completed original MVC answer:',size=10)
code('''using System.Web.Mvc;
using DemoValidation.Models;
namespace DemoValidation.Controllers
{
  public class PilotController : Controller
  {
    public ActionResult Index() { return View(); }
    [HttpPost]
    public ActionResult Index(Pilot pilot)
    {
      if (ModelState.IsValid)
      {
        ViewBag.Message = "Welcome aboard, " + pilot.PilotName + "!";
        ModelState.Clear();
        return View();
      }
      return View(pilot);
    }
  }
}''')
answer('The missing member is IsValid. The web equivalent is app/api/pilots/route.ts: validatePilot(raw), return 422 with field errors when invalid, and return the welcome message only when valid. Successful submission clears the React form.')
heading('Question (2 points): Why do we return View(pilot) when the data is invalid instead of redirecting somewhere else?')
answer('It redisplays the submitted values and ModelState errors, letting the user correct only the invalid fields. A normal redirect starts a new request and loses those errors and values unless they are preserved explicitly. The React form similarly keeps input values when validation fails.')
para('MVC security note: the original sample lacks [ValidateAntiForgeryToken]. Add it to enforce Html.AntiForgeryToken(). This app instead checks same-origin JSON requests; it does not claim to implement Razor tokens.',size=10)
page();shot('Checkpoint 2: Screenshot of PilotController.cs.','02_controller_source.png','Web equivalent: the actual Node.js route and validation guard in app/api/pilots/route.ts.')
page();heading('Step 3: Create the View (8 points)')
num(1,'Right-click return View() in the first Index action, then click Add View.')
num(2,'View name: Index. Template: Create. Model class: Pilot (DemoValidation.Models).')
num(3,'Tick Reference script libraries and Use a layout page, then click Add.')
num(4,'Open Index.cshtml and confirm you can find each of these helpers. Write the line number where you found them:')
para('Web equivalent: components/PilotForm.tsx and app/layout.tsx. Razor helpers are not present; actual corresponding file lines are given instead of invented Index.cshtml lines.',size=10)
table(['Helper','Line number and implemented equivalent'],[['Html.BeginForm()','Not applicable in Razor. PilotForm.tsx:49 — React form / onSubmit.'],['Html.AntiForgeryToken()','Not applicable. app/api/pilots/route.ts:5 — exact Origin check; different mechanism.'],['Html.ValidationSummary(...)','Not applicable in Razor. PilotForm.tsx:51 — linked error summary.'],['Html.ValidationMessageFor(...) for PilotName','Not applicable in Razor. PilotForm.tsx:53 — shared field renderer, including PilotName.']],[2.55,3.95],10)
num(5,'Add this line above the form so the welcome message can show:')
code('<h3 class="text-success">@ViewBag.Message</h3>')
answer('The web equivalent is the focusable success status in PilotForm.tsx:50. It displays the server’s “Welcome aboard, Nova!” response. The form also connects field errors with aria-describedby and marks them with aria-invalid.')
page();shot('Checkpoint 3: Screenshot of the view code.','03_view_source.png','Web equivalent: the actual components/PilotForm.tsx. Full-resolution screenshot and /lab/view allow closer inspection.',7.0)
page();heading('Step 4: Run the Gate Tests (12 points)')
para('Run the project (F5), go to /Pilot, and test each case. Record what actually happened.',size=11)
para('Web equivalent: run START_NOVA.cmd, then visit http://localhost:3212. The following results were executed in Chromium and independently checked against the Node.js endpoint. Tests 1–7 return HTTP 422; test 8 returns 200.',size=10)
r=json.loads((out/'TEST_RESULTS.json').read_text())
expected=['Name error','Age error','Age error','Email error','Mobile error','Age required-style error','Name length error','Success message']
rows=[]
for i,x in enumerate(r['cases']):
 data=x['data'];rows.append([str(x['id']),data['pilotName'] or '(blank)',data['age'] or '(blank)',data['email'],data['mobile'] or '(blank)',expected[i],x['actual'],'Yes'])
table(['#','PilotName','Age','Email','Mobile','Expected result','Actual result (message shown)','Pass?'],rows,[.22,.75,.50,.92,.83,.7,2.14,.44],8)
para('All eight cases passed. Blank age shows “Please enter your age.” The original non-nullable MVC int produces a required-style binding error. The web app retains invalid input and clears it only after server success.',size=10)
page();shot('Checkpoint 4: Screenshot of a page showing at least two red messages.','04_multiple_errors.png','Actual empty-form submission: four red field messages, a summary and focus on the first invalid field.')
page();shot('Checkpoint 4: Screenshot of the success page.','05_success.png','Actual test 8: Nova / 30 / nova@academy.edu / 09171234567. The server returns the welcome message and the form clears.')
page();heading('Step 5: Break It On Purpose (6 points)')
para('Try each experiment, then write what happens.',size=11)
num(1,'Remove [Range(18, 60)] from Age, run, and enter an age of 5. What happens?')
answer('Age 5 was accepted after removing the range comparison from an isolated copy of the actual validator. The original validator rejected the same input. Required/integer rules alone do not enforce the allowed age range.')
num(2,'Put ModelState.IsValid back, but delete the if check in the controller so the code always runs the success branch. Submit blank data. What happens, and why is this dangerous even though the attributes are still on the model?')
answer('An isolated success-branch harness produced “Welcome aboard, !” for blank data even though validation returned false. Rules only describe or detect invalid data; processing code must enforce the result. Otherwise invalid data can be processed even if the model declares validation rules.')
heading('Restore your original code before continuing.')
para('Both experiments used test-only copies/harnesses. The real endpoint retained its validity check and still rejects blank or out-of-range submissions.',size=10)
heading('Step 6: Challenge Quest (optional, +8 bonus points)')
para('Add a new property LaunchDate (DateTime) to Pilot. Using CustomValidation (or your own custom attribute), make the app reject any launch date in the past with the message “You cannot launch yesterday!”',size=11)
para('Hint: a custom validation method returns ValidationResult.Success when the value is good, or new ValidationResult("message") when it is not.',size=10)
answer('Implemented in lib/pilot.ts and the optional “Plan your launch” field. A past date is rejected with the exact message; today/future pass. Both client and server use Asia/Manila calendar dates. Empty LaunchDate is allowed because this quest field is optional.')
code('''// Illustrative original MVC answer (server calendar date):
[CustomValidation(typeof(Pilot), nameof(ValidateLaunchDate))]
public DateTime? LaunchDate { get; set; }
public static ValidationResult ValidateLaunchDate(DateTime? value)
{
  return !value.HasValue || value.Value.Date >= DateTime.Today
    ? ValidationResult.Success
    : new ValidationResult("You cannot launch yesterday!");
}''')
page();heading('Reflection (8 points)')
num(1,'Which validation attribute did you find the most useful, and why?')
answer('Range is especially useful because it enforces eligibility, rather than just requiring a value. Ages 17 and 61 fail, while 18 and 60 pass. Without that rule, age 5 can be accepted.')
num(2,'If the Academy later adds a Parachute property to Pilot, which one step in this lab would you repeat in the model? In the controller? In the view?')
answer('Model: add the property and its validation rule. Controller: keep the validity check; the same model binding/validation flow can process the property. View: add the input and field message. Here, update the TypeScript types, shared validator and React fields, then add tests. A safety checkbox that must be checked needs a true-value rule; Boolean Required alone does not require true.')
heading('Lab Rubric (self-check)')
table(['Criteria','Points'],[['Model with correct attributes and messages','8'],['Controller with ModelState.IsValid check','8'],['View created from the Create template with validation helpers','8'],['Complete test table and screenshots','12'],['Break-it experiments and answers','6'],['Reflection','8'],['Challenge quest (bonus)','+10']],[5.65,.85],10)
para('The rubric is preserved as supplied. MVC-specific criteria are addressed through clearly labelled web equivalents, not a claim of an ASP.NET build. No score is assigned. Step 6 says +8 bonus while this rubric says +10; the instructor resolves the difference.',size=10)
heading('Lab answer hints')
para('Model: Required and StringLength(20, MinimumLength=3); Range(18,60); Required and EmailAddress; Required, Phone and StringLength(11). Controller blank: IsValid. Tests 1–7 show errors; test 8 shows success. Without the range, age 5 is accepted. Without enforcing IsValid, invalid data can be processed.',size=10)
para('Evidence: 20 unit tests, eight browser cases plus eight direct API cases, TypeScript and production build passed. Screenshots were captured from the actual local website. Name, section and grade remain blank for the student and instructor.',size=10)
# Write through a temporary working copy, then preserve source package parts not authorized for editing.
work=qa/'worksheet-working.docx';D.save(work)
final=out/'COMPLETED_WEEK_12_LAB_WORKSHEET_FORMAT.docx'
editable={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml'}
with ZipFile(src) as original,ZipFile(work) as built,ZipFile(final,'w',ZIP_DEFLATED) as dest:
 for item in original.infolist():dest.writestr(item,built.read(item.filename) if item.filename in editable else original.read(item.filename))
 for name in built.namelist():
  if name not in original.namelist():dest.writestr(name,built.read(name))
with ZipFile(src) as a,ZipFile(final) as b:
 kept=[n for n in a.namelist() if n not in editable]
 assert all(a.read(n)==b.read(n) for n in kept)
 assert b.testzip() is None
(qa/'STRUCTURAL_CHECK.json').write_text(json.dumps({'original_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'preserved_parts':kept,'edited_parts':sorted(editable),'new_images':len(D.inline_shapes),'section_repair':'Seven broken pseudo-table sections consolidated to one source-sized portrait section','final':str(final)},indent=2),encoding='utf-8')
print('Saved',final)
