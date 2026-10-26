"""
AI-Powered Cloud Resource Demand Prediction and Auto-Scaling System
PowerPoint generator  -  v4
Fixes:
  - Summary-2 slides: use safe-zone textbox (height 2.65") above triangles
    + a second right-side textbox (left of 3.5") below, so more content fits
  - D&M Part 2: delete layout's built-in placeholder columns before adding textbox
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
import lxml.etree as etree

# ─── helpers ─────────────────────────────────────────────────────────────────

def sp(para, text, sz=None, bold=None, italic=None, color=None):
    for r in para._p.findall(qn("a:r")):
        para._p.remove(r)
    run = para.add_run()
    run.text = text
    if sz:               run.font.size      = Pt(sz)
    if bold  is not None: run.font.bold      = bold
    if italic is not None: run.font.italic   = italic
    if color:            run.font.color.rgb  = RGBColor(*color)

def clear(tf):
    while len(tf.paragraphs) > 1:
        p = tf.paragraphs[-1]._p
        p.getparent().remove(p)

def fill(tf, lines):
    clear(tf)
    first = True
    for row in lines:
        txt = row[0]
        kw  = row[1] if len(row) > 1 else {}
        sz=kw.get("s"); b=kw.get("b"); it=kw.get("i"); c=kw.get("c")
        if first:
            sp(tf.paragraphs[0], txt, sz, b, it, c); first = False
        else:
            p = tf.add_paragraph(); sp(p, txt, sz, b, it, c)

def nofit(bx):
    """Lock textbox height — no auto-expand."""
    bp = bx.text_frame._txBody.find(qn("a:bodyPr"))
    for ch in list(bp):
        if ch.tag in (qn("a:spAutoFit"), qn("a:normAutofit"), qn("a:noAutofit")):
            bp.remove(ch)
    etree.SubElement(bp, qn("a:noAutofit"))

def box(slide, left, top, width, height):
    bx = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height))
    bx.text_frame.word_wrap = True
    nofit(bx)
    return bx

def del_layout_placeholders(slide):
    """Remove the empty 'Click to add text' content placeholders
       that come from the layout — keeps only title (idx=0)."""
    spTree = slide.shapes._spTree
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx != 0:
            spTree.remove(ph._element)

def move_slide(prs, old_index, new_index):
    lst = prs.slides._sldIdLst
    items = list(lst); el = items[old_index]
    lst.remove(el); lst.insert(new_index, el)

# ─── colours ─────────────────────────────────────────────────────────────────
DB = (0,   32,  96)   # dark navy   #002060
RD = (192,  0,   0)   # dark red    #C00000
LB = (0,  112, 192)   # accent blue #0070C0
GR = (0,  112,  54)   # green       #007036
GY = (89,  89,  89)   # grey        #595959
BK = (0,    0,   0)   # black

TMPL = r"c:\Users\bit\Documents\princy\Project_presentation_template_for_B__Tech__V_CSE_AI_MO26.pptx"
OUT  = r"c:\Users\bit\Documents\princy\AI_Predictive_AutoScaling_Presentation.pptx"

prs = Presentation(TMPL)
sl  = prs.slides

# ════════════════════════════════════════════════════════════════════
# SLIDE 1  TITLE
# ════════════════════════════════════════════════════════════════════
for sh in sl[0].shapes:
    if "Shape;128" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0],
           "AI-Powered Cloud Resource Demand Prediction\nand Auto-Scaling System",
           25, True, False, DB)

    if "Shape;129" in sh.name:
        fill(sh.text_frame, [
            ["Pratistha Singh   |   Btech/25047/24",              {"b": True,  "c": DB, "s": 17}],
            ["Arushi Goel        |   Btech/25111/24",              {"b": True,  "c": DB, "s": 17}],
            [""],
            ["B.Tech V Semester  |  CSE Section A",               {"c": GY, "s": 14}],
            ["Dept. of Computer Science and Engineering",         {"c": GY, "s": 13}],
            ["BIT, Mesra - Jaipur Campus",                        {"c": GY, "s": 13}],
            [""],
            ["Under the Supervision of",                          {"c": GY, "s": 13}],
            ["Faculty Mentor",                                    {"b": True, "c": RD, "s": 16}],
            ["Assistant Professor, BIT Mesra - Jaipur Campus",   {"c": RD, "s": 13}],
        ])

# ════════════════════════════════════════════════════════════════════
# SLIDE 2  TABLE OF CONTENTS
# ════════════════════════════════════════════════════════════════════
for sh in sl[1].shapes:
    if "Shape;135" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Table of Contents")

    if "Shape;136" in sh.name:
        fill(sh.text_frame, [
            ["01.   Introduction",                          {"s": 15, "c": DB}],
            ["02.   Problem Statement and Objectives",     {"s": 15, "c": DB}],
            ["03.   Dataset Description",                  {"s": 15, "c": DB}],
            ["04.   Design and Methodology  (Part 1)",    {"s": 15, "c": DB}],
            ["05.   Design and Methodology  (Part 2)",    {"s": 15, "c": DB}],
            ["06.   Literature Review",                    {"s": 15, "c": DB}],
            ["07.   Conclusions and Future Scope",         {"s": 15, "c": DB}],
            ["08.   References",                           {"s": 15, "c": DB}],
        ])

# ════════════════════════════════════════════════════════════════════
# SLIDE 3  INTRODUCTION
# Summary-2 layout:  triangles at x=[0,3.24"], y=[4.26",7.5"]
# Safe upper zone: full width, top 1.25" to 3.9"  (height 2.65")
# Safe lower zone: right side only x>3.4", from 4.0" down
# ════════════════════════════════════════════════════════════════════
for sh in sl[2].shapes:
    if "Shape;142" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Introduction")

# Upper zone  -  full width, above triangles (y: 1.25" to 3.85")
bx = box(sl[2], 0.5, 1.25, 12.3, 2.6)
fill(bx.text_frame, [
    ["Dynamic Cloud Workload",                              {"b": True, "s": 15, "c": DB}],
    ["Modern microservice web applications face highly dynamic, non-linear traffic bursts.", {"s": 13, "c": BK}],
    ["User demand swings unpredictably due to flash sales, breaking events, and viral user activity.", {"s": 13, "c": BK}],
    ["High static resource allocation leads to severe financial and energy inefficiency during low-traffic periods.", {"s": 13, "c": BK}],
    [""],
    ["Legacy Reactive Scaling",                            {"b": True, "s": 15, "c": RD}],
    ["Threshold-based triggers (e.g., Kubernetes HPA at CPU > 80%) react ONLY AFTER congestion occurs.", {"s": 13, "c": BK}],
    ["Container Cold-Start Lag: Pod spinning, image pulling, and readiness checks take 30s to 180s.", {"s": 13, "c": BK}],
    ["Result: Unavoidable transient performance degradation, dropped packets, and SLA violations.", {"s": 13, "c": RD}],
])

# Lower zone  -  right of triangles (x > 3.5", y: 4.1" down)
bx2 = box(sl[2], 3.5, 4.1, 9.3, 2.9)
fill(bx2.text_frame, [
    ["Proposed AI Solution",                               {"b": True, "s": 15, "c": GR}],
    ["Proactive Demand Prediction:  Deep time-series models (GRU/LSTM)",              {"s": 13, "c": BK}],
    ["forecast workload surges 3 to 5 minutes ahead.",    {"s": 13, "c": BK}],
    [""],
    ["Closed-Loop Orchestration:  Programmatically triggers Kubernetes pod",          {"s": 13, "c": BK}],
    ["scaling before traffic spikes hit the cluster.",    {"s": 13, "c": BK}],
    [""],
    ["Eliminates cold-start delays while optimizing cluster cost.", {"s": 13, "c": GR, "b": True}],
])

# ════════════════════════════════════════════════════════════════════
# SLIDE 4  PROBLEM STATEMENT
# Title-and-Two-Content-2  no triangles  full height safe
# ════════════════════════════════════════════════════════════════════
for sh in sl[3].shapes:
    if "Shape;152" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Problem Statement and Objectives")

bx = box(sl[3], 0.5, 1.15, 12.3, 5.85)
fill(bx.text_frame, [
    ["Problem Statement",                                   {"b": True, "s": 17, "c": RD}],
    [""],
    ["Cloud applications experience continuously changing and unpredictable workloads.", {"s": 13, "c": BK}],
    ["During high-demand periods, insufficient resources cause slow response times,",   {"s": 13, "c": BK}],
    ["service degradation, and failures that directly impact end users.",               {"s": 13, "c": BK}],
    ["On the other hand, allocating too many resources during low-demand periods",      {"s": 13, "c": BK}],
    ["leads to unnecessary cloud costs and significant resource wastage.",             {"s": 13, "c": BK}],
    [""],
    ["Traditional auto-scaling methods usually react after resource usage increases.",  {"s": 13, "c": BK}],
    ["This reactive approach causes delays because the system needs time to detect",    {"s": 13, "c": BK}],
    ["the increased demand and provision additional resources (30-180 seconds),",      {"s": 13, "c": RD}],
    ["leaving a critical vulnerability window where users experience service failures.", {"s": 13, "c": RD}],
    [""],
    ["Research Objectives",                                {"b": True, "s": 16, "c": DB}],
    ["1.  Forecast CPU, memory and request-rate demand 3-5 min ahead using AI models.", {"s": 13, "c": BK}],
    ["2.  Build a proactive Kubernetes controller that scales pods before load arrives.", {"s": 13, "c": BK}],
    ["3.  Eliminate SLA violations and reduce resource wastage by 20-30 percent.",     {"s": 13, "c": BK}],
    ["4.  Validate the system with live Prometheus metrics and Grafana dashboards.",   {"s": 13, "c": BK}],
])

# ════════════════════════════════════════════════════════════════════
# SLIDE 5  DATASET DESCRIPTION
# Summary-2 layout  safe zones only
# ════════════════════════════════════════════════════════════════════
for sh in sl[4].shapes:
    if "Shape;158" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Dataset Description")

# Upper zone  -  full width, above triangles
bx = box(sl[4], 0.5, 1.2, 12.3, 2.6)
fill(bx.text_frame, [
    ["Dataset 1  -  Google Cluster Workload Traces v2  (2020)", {"b": True, "s": 15, "c": DB}],
    ["Published by Google. Contains CPU and memory usage metrics sampled every 5 seconds", {"s": 13, "c": BK}],
    ["from thousands of container jobs running on a real Google data-centre cluster.",    {"s": 13, "c": BK}],
    ["Covers both stable periodic patterns AND sudden burst events, making it ideal for", {"s": 13, "c": BK}],
    ["training and validating deep learning forecasting models under realistic conditions.", {"s": 13, "c": BK}],
    ["Source: github.com/google/cluster-data",                {"s": 12, "c": GY, "i": True}],
    [""],
    ["Dataset 2  -  NASA HTTP Web Server Access Logs",         {"b": True, "s": 15, "c": DB}],
    ["Real-world HTTP access logs from NASA Kennedy Space Centre web servers.",          {"s": 13, "c": BK}],
    ["Contains over 1.8 million requests with timestamps, showing strong diurnal (day/night)", {"s": 13, "c": BK}],
    ["traffic cycles and sharp burst spikes triggered by news events.",                  {"s": 13, "c": BK}],
    ["Used to model request-rate time series and test how well the system handles",     {"s": 13, "c": BK}],
    ["sudden public-traffic surges typical of real web applications.",                  {"s": 13, "c": BK}],
])

# Lower zone  -  right of triangles (x > 3.5", y: 4.1" down)
bx2 = box(sl[4], 3.5, 4.1, 9.3, 2.9)
fill(bx2.text_frame, [
    ["Data Preprocessing Pipeline",                        {"b": True, "s": 15, "c": DB}],
    ["Step 1  -  Missing Value Handling:",                  {"b": True, "s": 13, "c": LB}],
    ["Forward-fill for short gaps; mean imputation for longer missing segments.",       {"s": 13, "c": BK}],
    ["Step 2  -  Normalisation:",                           {"b": True, "s": 13, "c": LB}],
    ["MinMaxScaler scales all values to [0, 1] so no single metric dominates training.", {"s": 13, "c": BK}],
    ["Step 3  -  Sliding-Window Sequencing:",               {"b": True, "s": 13, "c": LB}],
    ["Groups consecutive timesteps into fixed-length input windows for the LSTM/GRU.",  {"s": 13, "c": BK}],
    ["Step 4  -  Chronological Data Split:",                {"b": True, "s": 13, "c": GR}],
    ["70 percent Train  |  15 percent Validation  |  15 percent Test  (no random shuffle).", {"s": 13, "c": GR, "b": True}],
    ["Step 5  -  Rolling-Window Cross-Validation:",         {"b": True, "s": 13, "c": LB}],
    ["Prevents data leakage between training and evaluation periods.",                  {"s": 13, "c": BK}],
])

# ════════════════════════════════════════════════════════════════════
# SLIDE 6  DESIGN AND METHODOLOGY  PART 1
# Summary-2 layout
# FIX: clear Shape;169 placeholder entirely, use safe-zone textboxes only
# ════════════════════════════════════════════════════════════════════
# Delete Shape;169 (template content placeholder) entirely -
# prevents the empty 'Click to add text' box overlapping our textboxes
shape_to_delete = None
for sh in sl[5].shapes:
    if "Shape;168" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Design and Methodology  -  Part 1")
    if "Shape;169" in sh.name:
        shape_to_delete = sh._element
if shape_to_delete is not None:
    shape_to_delete.getparent().remove(shape_to_delete)

# Upper zone  -  full width, above triangles
bx = box(sl[5], 0.5, 1.25, 12.3, 2.6)
fill(bx.text_frame, [
    ["End-to-End System Pipeline  (Planned)",              {"b": True, "s": 16, "c": DB}],
    ["Raw Data  ->  Preprocessing  ->  Feature Engineering  ->  Model Training",    {"s": 13, "c": GY}],
    ["->  Forecasting Engine  ->  Scaling Controller  ->  Kubernetes REST API",     {"s": 13, "c": GY}],
    [""],
    ["Module 1  -  Data Preprocessing",                    {"b": True, "s": 14, "c": LB}],
    ["Ingests raw telemetry, handles missing values via forward-fill and imputation,", {"s": 13, "c": BK}],
    ["applies MinMaxScaler normalisation, and creates sliding-window sequences",     {"s": 13, "c": BK}],
    ["ready for model training.",                                                    {"s": 13, "c": BK}],
])

# Lower zone  -  right of triangles (x > 3.5", y: 4.1" down)
bx2 = box(sl[5], 3.5, 4.1, 9.3, 2.9)
fill(bx2.text_frame, [
    ["Module 2  -  Feature Engineering",                   {"b": True, "s": 14, "c": LB}],
    ["Derives lag features from historical CPU and memory readings,",               {"s": 13, "c": BK}],
    ["computes rolling statistics (mean and standard deviation), and",              {"s": 13, "c": BK}],
    ["encodes time-of-day calendar indices to capture diurnal demand patterns.",   {"s": 13, "c": BK}],
    [""],
    ["Both modules together ensure the model receives clean, enriched,",           {"s": 13, "c": GY, "i": True}],
    ["temporally-structured data as input sequences.",                             {"s": 13, "c": GY, "i": True}],
])

# ════════════════════════════════════════════════════════════════════
# NEW SLIDE  DESIGN AND METHODOLOGY  PART 2
# FIX: delete layout's built-in column placeholders before adding textbox
# ════════════════════════════════════════════════════════════════════
dm2 = prs.slides.add_slide(prs.slide_layouts[4])

# Set title placeholder
for ph in dm2.placeholders:
    if ph.placeholder_format.idx == 0:
        ph.text = "Design and Methodology  -  Part 2"

# *** KEY FIX: remove the empty column placeholders from layout ***
del_layout_placeholders(dm2)

# Now add a clean, full-width textbox with no overlap
bx2 = box(dm2, 0.5, 1.1, 12.3, 5.9)
fill(bx2.text_frame, [
    ["Module 3  -  Model Training and Selection",          {"b": True, "s": 15, "c": LB}],
    ["Trains ARIMA, Random Forest, XGBoost, LSTM, and GRU on the prepared sequences.", {"s": 13, "c": BK}],
    ["Evaluates each on the validation set using MAE and RMSE metrics.",              {"s": 13, "c": BK}],
    ["The model with the lowest error is saved as the active forecasting checkpoint.", {"s": 13, "c": BK}],
    [""],
    ["Module 4  -  Forecasting Engine",                    {"b": True, "s": 15, "c": LB}],
    ["The selected model takes recent metric history and outputs a predicted",        {"s": 13, "c": BK}],
    ["resource utilisation value 3 to 5 minutes into the future.",                   {"s": 13, "c": BK}],
    ["This lead time allows the controller to act before the load actually arrives.", {"s": 13, "c": BK}],
    [""],
    ["Module 5  -  Scaling Controller  (Planned)",         {"b": True, "s": 15, "c": LB}],
    ["Every 30 seconds: reads the forecast, calculates the required pod replica",    {"s": 13, "c": BK}],
    ["count, and sends a PATCH command to the Kubernetes REST API server.",          {"s": 13, "c": BK}],
    ["Pods are warm and ready before the traffic spike arrives.",                    {"s": 13, "c": BK}],
    [""],
    ["Module 6  -  Observability Layer",                   {"b": True, "s": 15, "c": LB}],
    ["Prometheus scrapes live cluster metrics every 5 seconds.",                     {"s": 13, "c": BK}],
    ["Grafana renders real-time dashboards: predicted load, actual usage, replicas.", {"s": 13, "c": BK}],
])

# Move D&M Part 2 to index 6 (right after Part 1 at index 5)
move_slide(prs, len(prs.slides) - 1, 6)

# Re-fetch after move
sl = prs.slides

# ════════════════════════════════════════════════════════════════════
# SLIDE 8  LITERATURE REVIEW  (index 7)
# Two-column layout: Restored detailed content, but restricted width to stay left of triangles
# ════════════════════════════════════════════════════════════════════
for sh in sl[7].shapes:
    if "Shape;179" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Literature Review")

# LEFT column  -  Survey of Existing Approaches
bx_l = box(sl[7], 0.4, 1.1, 4.8, 5.9)
fill(bx_l.text_frame, [
    ["Survey of Existing Approaches",                      {"b": True, "s": 15, "c": DB}],
    [""],
    ["1.  ARIMA / Holt-Winters  (Statistical)",            {"b": True, "s": 13, "c": LB}],
    ["Classical time-series models that work well for",    {"s": 12, "c": BK}],
    ["stable, stationary, periodic workloads. Cannot",     {"s": 12, "c": BK}],
    ["capture sudden non-linear traffic bursts.",          {"s": 12, "c": BK}],
    [""],
    ["2.  Random Forest  (Ensemble ML)",                   {"b": True, "s": 13, "c": LB}],
    ["Incorporates lag-based features and handles",        {"s": 12, "c": BK}],
    ["non-linearity better than ARIMA. But makes",         {"s": 12, "c": BK}],
    ["independent predictions with no memory of sequence.",{"s": 12, "c": BK}],
    [""],
    ["3.  XGBoost  (Gradient Boosting)",                   {"b": True, "s": 13, "c": LB}],
    ["Fast and accurate for tabular data with engineered",  {"s": 12, "c": BK}],
    ["features. Lacks the temporal context needed for",    {"s": 12, "c": BK}],
    ["multi-step time-series forecasting.",                {"s": 12, "c": BK}],
    [""],
    ["4.  LSTM  (Deep Learning)",                          {"b": True, "s": 13, "c": LB}],
    ["Learns long-range temporal dependencies via gated",  {"s": 12, "c": BK}],
    ["memory cells. Highly accurate but computationally",  {"s": 12, "c": BK}],
    ["heavy — may be too slow for 30-second control loops.",{"s": 12, "c": BK}],
    [""],
    ["5.  GRU  (State of the Art)",                        {"b": True, "s": 13, "c": GR}],
    ["Matches LSTM accuracy with fewer parameters and",    {"s": 12, "c": BK}],
    ["faster training/inference — ideal for real-time",    {"s": 12, "c": BK}],
    ["cloud resource prediction in production systems.",   {"s": 12, "c": BK}],
])

# RIGHT column  -  Gaps + Our Approach
bx_r = box(sl[7], 5.4, 1.1, 4.8, 5.9)
fill(bx_r.text_frame, [
    ["Key Gaps in Existing Literature",                    {"b": True, "s": 15, "c": RD}],
    [""],
    ["Gap 1:  Offline Evaluation Only",                   {"b": True, "s": 13, "c": RD}],
    ["Most studies benchmark models offline. None",        {"s": 12, "c": BK}],
    ["connect the predictor to a live Kubernetes cluster.",{"s": 12, "c": BK}],
    [""],
    ["Gap 2:  Cold-Start Delay Ignored",                   {"b": True, "s": 13, "c": RD}],
    ["No existing framework accounts for the 30-180 sec",  {"s": 12, "c": BK}],
    ["pod startup delay in the scaling decision logic.",   {"s": 12, "c": BK}],
    [""],
    ["Gap 3:  No Real-Time Control Loop",                  {"b": True, "s": 13, "c": RD}],
    ["Forecasting models are not integrated into a",       {"s": 12, "c": BK}],
    ["cyclic, automated Kubernetes scaling controller.",   {"s": 12, "c": BK}],
    [""],
    ["Gap 4:  No Unified Observability",                   {"b": True, "s": 13, "c": RD}],
    ["No dashboard correlates predicted load, actual",     {"s": 12, "c": BK}],
    ["usage, and active replica count in real time.",      {"s": 12, "c": BK}],
    [""],
    ["How Our Work Addresses These Gaps",                  {"b": True, "s": 14, "c": GR}],
    ["We connect a lightweight GRU model directly to",     {"s": 12, "c": BK}],
    ["the Kubernetes REST API in a closed 30-sec loop,",   {"s": 12, "c": BK}],
    ["with a 3-5 min look-ahead to pre-empt the cold-start",{"s": 12, "c": BK}],
    ["delay — and visualise everything live in Grafana.",  {"s": 12, "c": GR, "b": True}],
])

# ════════════════════════════════════════════════════════════════════
# SLIDE 9  CONCLUSIONS AND FUTURE SCOPE  (index 8)
# Single-column layout: Restricted width to avoid right-side graphics
# ════════════════════════════════════════════════════════════════════
for sh in sl[8].shapes:
    if "Shape;185" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Conclusions and Future Scope")

bx = box(sl[8], 0.5, 1.1, 10.0, 5.9)
fill(bx.text_frame, [
    ["Current Project Status",                             {"b": True, "s": 16, "c": RD}],
    ["The project is in the planning phase with SRS and SDS documents completed.", {"s": 14, "c": BK}],
    [""],
    ["Expected Contributions",                             {"b": True, "s": 16, "c": DB}],
    ["  End-to-End Pipeline: Complete predictive auto-scaling system.", {"s": 14, "c": BK}],
    ["  Proactive Controller: Kubernetes scaling with a 3-5 min look-ahead.", {"s": 14, "c": BK}],
    ["  Resource Efficiency: Estimated 20-30% reduction in cluster over-provisioning.", {"s": 14, "c": BK}],
    [""],
    ["Future Scope",                                       {"b": True, "s": 16, "c": LB}],
    ["  Multi-Metric Forecasting: Predict CPU, memory, and network simultaneously.", {"s": 14, "c": BK}],
    ["  Reinforcement Learning: Adaptive, self-tuning scaling thresholds.", {"s": 14, "c": BK}],
    ["  Cloud Cost Optimisation: Integrate with AWS/GCP APIs to minimise monetary cost.", {"s": 14, "c": BK}],
])

# ════════════════════════════════════════════════════════════════════
# SLIDE 10  REFERENCES  (index 9)
# ════════════════════════════════════════════════════════════════════
for sh in sl[9].shapes:
    if "Shape;191" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "References")

bx = box(sl[9], 0.5, 1.1, 12.3, 5.9)
fill(bx.text_frame, [
    ["[1]  Google Inc., Google Cluster Workload Traces v2, GCP Datasets, 2020.", {"s": 13, "c": BK}],
    ["     github.com/google/cluster-data",                                       {"s": 12, "c": GY, "i": True}],
    ["[2]  S. Hochreiter and J. Schmidhuber, Long Short-Term Memory,",           {"s": 13, "c": BK}],
    ["     Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997.",             {"s": 12, "c": GY, "i": True}],
    ["[3]  K. Cho et al., Learning Phrase Representations using RNN Encoder-Decoder,", {"s": 13, "c": BK}],
    ["     Proc. EMNLP, pp. 1724-1734, 2014.",                                   {"s": 12, "c": GY, "i": True}],
    ["[4]  Kubernetes Authors, Horizontal Pod Autoscaling Architecture, K8s Docs, 2024.", {"s": 13, "c": BK}],
    ["[5]  Prometheus Authors, Prometheus Open-Source Monitoring Toolkit, CNCF, 2024.", {"s": 13, "c": BK}],
    ["[6]  Grafana Labs, Grafana Observability and Dashboarding Platform, 2024.", {"s": 13, "c": BK}],
    ["[7]  T. Chen and C. Guestrin, XGBoost: A Scalable Tree Boosting System,",  {"s": 13, "c": BK}],
    ["     Proc. ACM SIGKDD, pp. 785-794, 2016.",                                {"s": 12, "c": GY, "i": True}],
    ["[8]  IEEE Xplore Digital Library, Cloud Workload Forecasting Research.",    {"s": 13, "c": BK}],
])

# ════════════════════════════════════════════════════════════════════
# SLIDE 11  THANK YOU  (index 10)
# ════════════════════════════════════════════════════════════════════
for sh in sl[10].shapes:
    if "Shape;197" in sh.name:
        clear(sh.text_frame)
        sp(sh.text_frame.paragraphs[0], "Thank You!", 36, True, False, DB)

    if "Shape;198" in sh.name:
        fill(sh.text_frame, [
            ["Pratistha Singh   |   Btech/25047/24",      {"b": True,  "c": DB, "s": 16}],
            ["Arushi Goel        |   Btech/25111/24",      {"b": True,  "c": DB, "s": 16}],
            [""],
            ["B.Tech V  |  CSE Section A",                {"c": GY, "s": 13}],
            [""],
            ["Under the Supervision of",                  {"c": GY, "s": 13}],
            ["Faculty Mentor",                            {"b": True, "c": RD, "s": 15}],
            ["Assistant Professor, BIT Mesra - Jaipur Campus", {"c": RD, "s": 13}],
        ])

# ─── save ────────────────────────────────────────────────────────────────────
prs.save(OUT)
print("SAVED:", OUT)
print("Total slides:", len(prs.slides))
