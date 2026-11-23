from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
p=Path(r'C:/Users/joshu/Documents/GitHub/Apps/NovaAcademyGate')
out=p/'deliverables'
r=json.loads((out/'TEST_RESULTS.json').read_text())
assert all(x['pass'] for x in r['cases']) and len(r['cases'])==8
D=Document(); sec=D.sections[0]; sec.page_width=Inches(8.27);sec.page_height=Inches(11.69);sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65);sec.left_margin=sec.right_margin=Inches(.72)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3']:
 st=D.styles[name]; st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
D.styles['Normal'].font.size=Pt(10);D.styles['Normal'].paragraph_format.space_after=Pt(7)
D.styles['Normal'].paragraph_format.line_spacing=1.08
D.styles['Title'].font.size=Pt(25)
D.styles['Heading 1'].font.size=Pt(17);D.styles['Heading 2'].font.size=Pt(12)
def para(t,style=None):return D.add_paragraph(t,style)
def h(t):D.add_heading(t,1)
def code(s):
 for line in s.strip().splitlines():
  x=para(line);x.paragraph_format.space_after=Pt(0);x.paragraph_format.line_spacing=1
  for run in x.runs:run.font.name='Consolas';run.font.size=Pt(8)
 para('')
def table(headers,rows,widths):
 t=D.add_table(rows=1,cols=len(headers));t.autofit=False
 for c,w in zip(t.columns,widths):c.width=Inches(w)
 for cell,text in zip(t.rows[0].cells,headers):cell.text=text
 for row in rows:
  cells=t.add_row().cells
  for cell,text in zip(cells,row):cell.text=str(text)
 for i,row in enumerate(t.rows):
  for j,cell in enumerate(row.cells):
   cell.width=Inches(widths[j]);pr=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for side in ['top','left','bottom','right']:
    n=OxmlElement('w:'+side);n.set(qn('w:val'),'single');n.set(qn('w:sz'),'4');n.set(qn('w:color'),'D9D9D9');b.append(n)
   pr.append(b)
   margins=OxmlElement('w:tcMar')
   for side in ['top','left','bottom','right']:
    n=OxmlElement('w:'+side);n.set(qn('w:w'),'85');n.set(qn('w:type'),'dxa');margins.append(n)
   pr.append(margins)
   shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DDE7E8' if i==0 else ('F5F7F6' if i%2==0 else 'FFFFFF'));pr.append(shade)
   for pp in cell.paragraphs:
    pp.paragraph_format.space_after=Pt(1)
    for run in pp.runs:run.font.size=Pt(9);run.bold=i==0
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
 t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
 return t
def page():D.add_page_break()
def lineno(file,token):
 return next(i for i,line in enumerate((p/file).read_text(encoding='utf-8').splitlines(),1) if token in line)
D.add_heading('Nova Academy Gate Week 12 Lab',0)
para('Completed answers and tested web stack implementation','Subtitle')
para('Name: ____________________    Section: __________    Date: 23 November 2026')
para('The requested pilot registration page is implemented in React and Next.js with a Node.js endpoint, TypeScript validation and a Three.js space scene. All eight worksheet cases pass in the browser and against the server. This report follows the worksheet steps and labels the original MVC answers separately from the implemented equivalents.')
h('Step 1 Project and model')
para('Project: NovaAcademyGate. The source worksheet names DemoValidation and uses C# ASP.NET MVC 5 examples, rather than Visual Basic. The implemented model is lib/pilot.ts; there is no Pilot.cs in the web application. PilotId is omitted from the form because this lab does not store registrations or assign database identities.')
table(['Property','Implemented rule'],[
 ['PilotName','Required; trim surrounding spaces; 3 to 20 characters.'],['Age','Required integer from 18 through 60, inclusive.'],['Email','Required; valid basic email pattern.'],['Mobile','Required; phone-like syntax; 7–11 digits and no more than 11 total characters. This is an explicit web policy, not exact .NET Phone parser parity.'],['LaunchDate','Optional; valid calendar date, today or later in Asia/Manila.']], [1.15,5.65])
D.add_heading('Original MVC attribute answers',2)
code('''[Required(ErrorMessage = "Every pilot needs a callsign (3 to 20 characters)!")]
[StringLength(20, MinimumLength = 3,
 ErrorMessage = "Every pilot needs a callsign (3 to 20 characters)!")]
public string PilotName { get; set; }
[Range(18, 60, ErrorMessage = "Pilots must be 18 to 60 years old.")]
public int Age { get; set; }
[Required(ErrorMessage = "That email is lost in space.")]
[EmailAddress(ErrorMessage = "That email is lost in space.")]
public string Email { get; set; }
[Required(ErrorMessage = "Please enter a valid mobile number.")]
[Phone(ErrorMessage = "Please enter a valid mobile number.")]
[StringLength(11, ErrorMessage = "Please enter a valid mobile number.")]
public string Mobile { get; set; }''')
page();h('Step 2 Controller')
para('Blank answer: IsValid. The controller must check ModelState.IsValid before running its success branch. A non-nullable int also produces a binding error when the age field is blank. The web adaptation shows the clearer message “Please enter your age.”')
D.add_heading('Why return View pilot when invalid',2)
para('Returning View(pilot) displays the same form with the submitted values and ModelState errors, so the user can correct the invalid fields without retyping everything. A normal redirect starts a new request and loses that ModelState and its messages unless they are explicitly preserved.')
D.add_heading('Implemented equivalent',2)
para('app/api/pilots/route.ts calls validatePilot(raw). Invalid data returns HTTP 422 and field errors. The React form retains its values and displays those messages. Only a valid result can produce “Welcome aboard, [callsign]!”; the client then clears the fields. No account or database record is created.')
code('''const result = validatePilot(raw);
if (!result.ok) return Response.json(result, { status: 422 });
return Response.json({ ok: true,
  message: `Welcome aboard, ${result.pilot.pilotName}!` });''')
h('Step 3 View and helper locations')
para('Razor helpers do not exist in a React view, so their Razor line numbers are not applicable. These are the actual equivalent locations in this project; none is presented as a fabricated Index.cshtml line.')
rows=[['Html.BeginForm()',f'components/PilotForm.tsx:{lineno("components/PilotForm.tsx","return <form")}', 'React form and onSubmit handler.'],['Html.AntiForgeryToken()',f'app/api/pilots/route.ts:{lineno("app/api/pilots/route.ts","get(\"origin\")")}', 'Different mechanism: exact same-origin JSON request guard; no Razor token or session.'],['Html.ValidationSummary(...)',f'components/PilotForm.tsx:{lineno("components/PilotForm.tsx","error-summary")}', 'Accessible error summary with links to invalid fields.'],['Html.ValidationMessageFor(PilotName)',f'components/PilotForm.tsx:{lineno("components/PilotForm.tsx","field-error")}', 'Shared field renderer displays the pilotName error beside its input.'],['ViewBag.Message',f'components/PilotForm.tsx:{lineno("components/PilotForm.tsx","className=\"success\"")}', 'Server message displayed in a focusable success status.']]
table(['Worksheet helper','Actual file and line','Equivalent'],rows,[1.7,2.1,3.0])
para('Security distinction: MVC’s token helper must be paired with [ValidateAntiForgeryToken] on the POST action to enforce token checks. The original worksheet omits that controller attribute. This local JSON exercise uses an Origin check instead; it does not claim to implement the MVC token system.')
page();h('Step 4 Actual gate test results')
para('Executed in Chromium against the production build on 23 November 2026. The baseline for rows 1–7 is Ace / 25 / a@b.com / 09171234567, changing the value shown below. For row 8, all values are shown. UI messages and direct API status were both verified.')
variants=['PilotName blank','Age 17','Age 61','Email banana','Mobile blank','Age blank','PilotName Captain Zoomzoom Starfighter','Nova / 30 / nova@academy.edu / 09171234567']
table(['Test','Input or change','Actual displayed result','API','Pass'],[[x['id'],variants[i],x['actual'],x['serverStatus'],'Yes'] for i,x in enumerate(r['cases'])],[.4,2.1,3.15,.55,.6])
D.add_heading('Additional verification',2)
para('Twenty unit tests pass, including name/age boundaries, malformed values, phone length, calendar dates and Manila midnight. TypeScript and the Next.js production build pass. The production dependency audit reports zero vulnerabilities after upgrading this project to Next.js 16.4.6.')
para('Browser checks also confirm first-error focus, four red messages for an empty form, retained values after invalid input or a network failure, cleared fields after success, a real Three.js canvas, and no horizontal page overflow at 390px or 320px. Reduced-motion mode was used for deterministic screenshots. No JavaScript page errors were recorded.')
para('Direct requests also reject missing or foreign Origin (403), malformed JSON (400), wrong content type (415), oversized JSON (413) and GET on the POST-only endpoint (405). This is a local exercise verification, not a production security certification.')
para('Machine-readable evidence: deliverables/TEST_RESULTS.json. Checkpoint images appear after the answers; full-resolution copies are in deliverables/screenshots/.')
page();h('Step 5 Break it on purpose')
D.add_heading('Experiment 1 Remove the age range',2)
para('Observed in an isolated copy of the actual validator: with the range comparison removed and the other values valid, age 5 was accepted. The original validator rejected the same input. Required/integer checks alone do not impose the 18–60 range.')
D.add_heading('Experiment 2 Ignore the validity check',2)
para('Observed in an isolated success-branch harness: blank data produced “Welcome aboard, !” even though validatePilot returned ok: false. Declaring or calculating validation rules does not stop code that ignores their result. A client-side check can also be bypassed, so the server must refuse invalid input before processing it. The live endpoint still rejects blank data; neither experiment changed production validation.')
h('Step 6 Optional launch date challenge')
para('Implemented and tested. A past date displays “You cannot launch yesterday!” Today and future dates are accepted. Invalid calendar dates are rejected. Both client and server derive today from Asia/Manila; no comparison to a UTC date string is used. Leaving this optional field empty is allowed.')
D.add_heading('Equivalent original MVC custom validation answer',2)
code('''[CustomValidation(typeof(Pilot), nameof(ValidateLaunchDate))]
public DateTime? LaunchDate { get; set; }
public static ValidationResult ValidateLaunchDate(DateTime? value)
{
  return !value.HasValue || value.Value.Date >= DateTime.Today
    ? ValidationResult.Success
    : new ValidationResult("You cannot launch yesterday!");
}''')
para('This illustrative C# version uses the server calendar date. Configure the intended timezone in a real MVC implementation; the delivered web app explicitly uses Philippine time.')
h('Reflection answers')
para('1. Range is especially useful here because it expresses a real eligibility rule. Tests at 17 and 61 reject the request, while 18 and 60 pass. Required alone would only check that a value is present.')
para('2. For a Parachute property: add the property and its validation rule in the model; keep the controller’s validity check; add the input and its validation message to the view. In this application, update PilotInput/Pilot, validatePilot and the React fields, then add tests. If Parachute is a safety checkbox that must be checked, use a rule requiring true; a Boolean Required annotation alone does not mean true.')
para('Self-check: model rules, server guard, form equivalents, all eight cases, screenshots, both isolated experiments, reflections and optional challenge are supplied. No grade is claimed. The worksheet lists +8 for Step 6 but +10 in its rubric; the instructor determines the bonus.')
# Actual website evidence; source snapshots fit within the page without cropping content.
shots=[('Checkpoint 1 Pilot model and rules','01_model_source.png','Actual shared TypeScript source, with line numbers. This replaces the Pilot.cs screenshot in the web adaptation.'),('Checkpoint 2 Server controller equivalent','02_controller_source.png','Actual Node.js route. The success response follows the server validation guard.'),('Checkpoint 3 React view source','03_view_source.png','Actual React form source with client checks, server POST, summary, field messages and success state. Open the full-resolution PNG or /lab/view to inspect the lines at full size.'),('Checkpoint 4 Multiple validation errors','04_multiple_errors.png','Actual empty-form submission. Four red field messages and the error summary appear; the first invalid field receives focus.'),('Checkpoint 4 Successful registration check','05_success.png','Actual successful Nova submission. The server returns the welcome message and the form clears its fields.'),('Optional quest Past launch date rejected','06_launch_date_error.png','Actual form result for the past date 2000-01-01. The required challenge message is shown.')]
for title,name,caption in shots:
 page();h(title);para(caption)
 img=out/'screenshots'/name;w,hpx=Image.open(img).size
 width=min(6.8,8.9*w/hpx)
 pic=D.add_picture(str(img),width=Inches(width));D.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
 para('Source: '+name)
for border in D.styles.element.xpath('.//w:pBdr'):
 border.getparent().remove(border)
D.save(out/'COMPLETED_WEEK_12_LAB.docx')
print('Created completed answer document')
