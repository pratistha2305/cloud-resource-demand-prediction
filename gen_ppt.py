from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.enum.text import PP_ALIGN

def set_para(para, text, sz=None, bold=None, italic=None, color=None, align=None):
    for r in para._p.findall(qn('a:r')):
        para._p.remove(r)
    run = para.add_run()
    run.text = text
    if sz:    run.font.size = Pt(sz)
    if bold is not None:   run.font.bold = bold
    if italic is not None: run.font.italic = italic
    if color: run.font.color.rgb = RGBColor(*color)
    if align: para.alignment = align

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
        sz=kw.get('s'); b=kw.get('b'); it=kw.get('i')
        c=kw.get('c');  al=kw.get('a')
        if first:
            set_para(tf.paragraphs[0], txt, sz, b, it, c, al)
            first = False
        else:
            p = tf.add_paragraph()
            set_para(p, txt, sz, b, it, c, al)

# ── Colour palette ──────────────────────────────────────────────────────────
DB = (0,  32,  96)   # dark navy  #002060
RD = (192,  0,   0)  # dark red   #C00000
GR = (0,  112,  54)  # green      #007036
LB = (0,  112, 192)  # accent blue#0070C0
GY = (89,  89,  89)  # grey       #595959
BK = (0,    0,   0)  # black

TMPL = r'c:\Users\bit\Documents\princy\Project_presentation_template_for_B__Tech__V_CSE_AI_MO26.pptx'
OUT  = r'c:\Users\bit\Documents\princy\AI_Predictive_AutoScaling_Presentation.pptx'
prs  = Presentation(TMPL)
sl   = prs.slides

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1  –  TITLE
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[0].shapes:
    if 'Shape;128' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0],
            'AI-Powered Cloud Resource Demand\nPrediction and Auto-Scaling System',
            26, True, False, DB)

    if 'Shape;129' in sh.name:
        fill(sh.text_frame, [
            ['Pratistha Singh   |   Btech/25047/24', {'b':True,  'c':DB, 's':17}],
            ['Arushi Goel        |   Btech/25111/24', {'b':True,  'c':DB, 's':17}],
            [''],
            ['B.Tech – V Semester  |  CSE Section A', {'b':False, 'c':GY, 's':14}],
            ['Dept. of Computer Science & Engineering', {'b':False, 'c':GY, 's':14}],
            ['Birla Institute of Technology, Mesra – Jaipur Campus', {'b':False,'c':GY,'s':13}],
            [''],
            ['Under the Supervision of',   {'b':False, 'c':GY, 's':13}],
            ['Faculty Mentor',              {'b':True,  'c':RD, 's':16}],
            ['Assistant Professor, BIT Mesra – Jaipur Campus', {'b':False,'c':RD,'s':13}],
        ])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2  –  TABLE OF CONTENTS
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[1].shapes:
    if 'Shape;135' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Table of Contents')

    if 'Shape;136' in sh.name:
        fill(sh.text_frame, [
            ['01.   Introduction',                        {'s':16, 'b':False, 'c':DB}],
            ['02.   Problem Statement and Objectives',    {'s':16, 'b':False, 'c':DB}],
            ['03.   Dataset Description',                 {'s':16, 'b':False, 'c':DB}],
            ['04.   Design and Methodology',              {'s':16, 'b':False, 'c':DB}],
            ['05.   Literature Review',                   {'s':16, 'b':False, 'c':DB}],
            ['06.   Conclusions and Future Scope',        {'s':16, 'b':False, 'c':DB}],
            ['07.   References',                          {'s':16, 'b':False, 'c':DB}],
        ])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3  –  INTRODUCTION
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[2].shapes:
    if 'Shape;142' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Introduction')

bx = sl[2].shapes.add_textbox(Inches(0.45), Inches(1.25), Inches(12.4), Inches(6.0))
bx.text_frame.word_wrap = True
fill(bx.text_frame, [
    ['Background and Context', {'b':True, 's':17, 'c':DB}],
    ['Cloud computing has become the backbone of modern digital services, hosting everything', {'s':13,'c':BK}],
    ['from social media platforms to financial systems. These services experience workloads', {'s':13,'c':BK}],
    ['that are highly dynamic, bursty, and difficult to predict in advance.', {'s':13,'c':BK}],
    [''],
    ['The Challenge with Traditional Scaling', {'b':True, 's':17, 'c':DB}],
    ['Standard Kubernetes Horizontal Pod Autoscaler (HPA) is purely reactive — it waits until', {'s':13,'c':BK}],
    ['CPU or memory crosses a threshold before it starts new pods. Since launching a container', {'s':13,'c':BK}],
    ['takes 30 to 180 seconds, the system always responds too late during sudden traffic spikes.', {'s':13,'c':BK}],
    ['This results in:  request timeouts,  SLA violations,  and poor user experience.', {'s':13,'c':RD,'b':False,'i':False}],
    [''],
    ['Our Proposed Solution', {'b':True, 's':17, 'c':DB}],
    ['We propose replacing reactive scaling with a proactive, AI-driven prediction engine.', {'s':13,'c':BK}],
    ['By forecasting resource demand 3–5 minutes into the future using deep learning models', {'s':13,'c':BK}],
    ['(GRU and LSTM), the system prepares Kubernetes pod replicas before the spike arrives.', {'s':13,'c':BK}],
    [''],
    ['Technologies Involved', {'b':True, 's':15, 'c':LB}],
    ['Python 3.12  |  TensorFlow / PyTorch  |  Scikit-learn  |  Kubernetes / Minikube  |  Prometheus  |  Grafana  |  Docker  |  Locust', {'s':12,'c':GY}],
])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4  –  PROBLEM STATEMENT AND OBJECTIVES
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[3].shapes:
    if 'Shape;152' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Problem Statement and Objectives')

bx = sl[3].shapes.add_textbox(Inches(0.45), Inches(1.15), Inches(12.4), Inches(6.1))
bx.text_frame.word_wrap = True
fill(bx.text_frame, [
    ['Core Problem', {'b':True, 's':17, 'c':RD}],
    ['When cloud traffic surges suddenly, traditional auto-scalers only react after the damage', {'s':13,'c':BK}],
    ['has already begun. The delay between threshold breach and pod readiness (30–180 seconds)', {'s':13,'c':BK}],
    ['leaves a vulnerability window where real users face failed requests and degraded performance.', {'s':13,'c':BK}],
    ['Furthermore, static over-provisioning wastes significant compute budget and energy.', {'s':13,'c':BK}],
    [''],
    ['Research Objectives', {'b':True, 's':17, 'c':DB}],
    ['1.  Develop a time-series forecasting pipeline comparing multiple ML and DL models:', {'s':13,'c':BK}],
    ['    ARIMA, Random Forest, XGBoost, LSTM, and GRU for predicting CPU and memory demand.', {'s':13,'c':GY}],
    ['2.  Build a proactive Kubernetes controller that uses the forecast to scale pods in advance,', {'s':13,'c':BK}],
    ['    operating on a 30-second cycle with a 3–5 minute look-ahead window.', {'s':13,'c':GY}],
    ['3.  Eliminate SLA violations during traffic burst scenarios through pre-emptive pod provisioning.', {'s':13,'c':BK}],
    ['4.  Reduce cluster compute over-provisioning by an estimated 20–30% compared to static scaling.', {'s':13,'c':BK}],
    ['5.  Provide a live observability layer using Prometheus and Grafana to monitor, compare', {'s':13,'c':BK}],
    ['    predicted vs. actual load and validate system behaviour in real time.', {'s':13,'c':GY}],
])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5  –  DATASET DESCRIPTION
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[4].shapes:
    if 'Shape;158' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Dataset Description')

bx = sl[4].shapes.add_textbox(Inches(0.45), Inches(1.15), Inches(12.4), Inches(6.1))
bx.text_frame.word_wrap = True
fill(bx.text_frame, [
    ['Dataset 1 — Google Cluster Workload Traces v2 (2020)', {'b':True, 's':16, 'c':DB}],
    ['Published by Google, this dataset contains CPU and memory usage metrics sampled every', {'s':13,'c':BK}],
    ['5 seconds across thousands of container jobs on a production-scale Google data centre.', {'s':13,'c':BK}],
    ['It captures both periodic patterns and sudden burst events, making it ideal for training', {'s':13,'c':BK}],
    ['and validating our deep learning forecasting models.', {'s':13,'c':BK}],
    ['    Source: github.com/google/cluster-data', {'s':12,'c':GY,'i':True}],
    [''],
    ['Dataset 2 — NASA HTTP Web Server Access Logs', {'b':True, 's':16, 'c':DB}],
    ['Real-world HTTP request logs from NASA web servers with strong diurnal traffic patterns', {'s':13,'c':BK}],
    ['and sharp burst spikes. Used to model request-rate time series and assess how well the', {'s':13,'c':BK}],
    ['system handles sudden surges typical of public web applications.', {'s':13,'c':BK}],
    [''],
    ['Data Preprocessing Pipeline', {'b':True, 's':16, 'c':LB}],
    ['Step 1:  Handle missing values using forward-fill and mean imputation techniques.', {'s':13,'c':BK}],
    ['Step 2:  Normalise all values to the [0, 1] range using MinMaxScaler.', {'s':13,'c':BK}],
    ['Step 3:  Generate sliding window sequences from historical timesteps for model input.', {'s':13,'c':BK}],
    ['Step 4:  Split data chronologically — 70% Training  |  15% Validation  |  15% Testing.', {'s':13,'c':GR,'b':True}],
    ['Step 5:  Apply rolling-window cross-validation to prevent temporal data leakage.', {'s':13,'c':BK}],
])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6  –  DESIGN AND METHODOLOGY
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[5].shapes:
    if 'Shape;168' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Design and Methodology')

    if 'Shape;169' in sh.name:
        fill(sh.text_frame, [
            ['End-to-End System Pipeline (Planned Architecture)', {'b':True, 's':15, 'c':DB}],
            ['Raw Workload Data  ->  Preprocessing  ->  Feature Engineering  ->  Model Training', {'s':12,'c':GY}],
            ['->  Forecasting Engine  ->  Scaling Decision Controller  ->  Kubernetes REST API', {'s':12,'c':GY}],
            [''],
            ['Module 1 — Data Preprocessing', {'b':True, 's':13, 'c':LB}],
            ['Cleans raw telemetry traces, imputes missing values, and applies MinMaxScaler', {'s':12,'c':BK}],
            ['normalisation. Structures data into sliding-window input sequences for model training.', {'s':12,'c':BK}],
            [''],
            ['Module 2 — Model Training and Selection', {'b':True, 's':13, 'c':LB}],
            ['Trains and benchmarks ARIMA, Random Forest, XGBoost, LSTM, and GRU models.', {'s':12,'c':BK}],
            ['The model with the lowest prediction error on validation data is selected automatically.', {'s':12,'c':BK}],
            [''],
            ['Module 3 — Forecasting Engine', {'b':True, 's':13, 'c':LB}],
            ['The selected model takes recent metric history and predicts resource demand', {'s':12,'c':BK}],
            ['3 to 5 minutes ahead, giving the system time to act before load arrives.', {'s':12,'c':BK}],
            [''],
            ['Module 4 — Scaling Controller (Planned)', {'b':True, 's':13, 'c':LB}],
            ['Every 30 seconds, the controller reads the forecast, computes the required number', {'s':12,'c':BK}],
            ['of pod replicas, and sends a scaling command to the Kubernetes API server.', {'s':12,'c':BK}],
            [''],
            ['Module 5 — Observability', {'b':True, 's':13, 'c':LB}],
            ['Prometheus scrapes live cluster metrics every 5 seconds. Grafana dashboards display', {'s':12,'c':BK}],
            ['real load, predicted load, and active replica count side by side for validation.', {'s':12,'c':BK}],
        ])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7  –  LITERATURE REVIEW
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[6].shapes:
    if 'Shape;179' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Literature Review')

bx = sl[6].shapes.add_textbox(Inches(0.45), Inches(1.1), Inches(12.4), Inches(6.1))
bx.text_frame.word_wrap = True
fill(bx.text_frame, [
    ['Summary of Existing Approaches', {'b':True, 's':17, 'c':DB}],
    ['ARIMA and Holt-Winters Exponential Smoothing:  These classical statistical models work', {'s':13,'c':BK}],
    ['well for predictable, stationary workloads. However, they cannot handle sudden non-linear', {'s':13,'c':BK}],
    ['traffic spikes that are common in modern cloud environments.', {'s':13,'c':BK}],
    [''],
    ['Random Forest and XGBoost:  Tree-based ensemble models improved accuracy by incorporating', {'s':13,'c':BK}],
    ['lag-based features. They handle non-linearity better but still lack temporal sequence memory.', {'s':13,'c':BK}],
    [''],
    ['LSTM and GRU (State of the Art):  Recurrent deep learning models that learn long-range', {'s':13,'c':BK}],
    ['temporal dependencies. GRU achieves LSTM-level accuracy with fewer parameters, making', {'s':13,'c':BK}],
    ['it well suited for low-latency inference in a real-time control loop.', {'s':13,'c':BK}],
    [''],
    ['Gaps Identified in Existing Literature', {'b':True, 's':17, 'c':RD}],
    ['  Most research evaluates forecasting models offline and never connects them to a live cluster.', {'s':13,'c':BK}],
    ['  No existing framework accounts for the 30–180 second pod cold-start delay in scaling logic.', {'s':13,'c':BK}],
    ['  Heavy neural networks can be too slow for a 30-second real-time control loop requirement.', {'s':13,'c':BK}],
    ['  No unified observability dashboard correlating predicted, actual, and replica count data.', {'s':13,'c':BK}],
    [''],
    ['How Our Work Addresses These Gaps', {'b':True, 's':15, 'c':GR}],
    ['We plan to close the full loop — connecting a lightweight forecasting model directly to', {'s':13,'c':BK}],
    ['the Kubernetes API so that scaling actions happen before traffic peaks reach the cluster.', {'s':13,'c':BK}],
])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8  –  CONCLUSIONS AND FUTURE SCOPE
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[7].shapes:
    if 'Shape;185' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Conclusions and Future Scope')

bx = sl[7].shapes.add_textbox(Inches(0.45), Inches(1.1), Inches(12.4), Inches(6.1))
bx.text_frame.word_wrap = True
fill(bx.text_frame, [
    ['Current Project Status', {'b':True, 's':17, 'c':RD}],
    ['This project is currently in the planning and requirement analysis phase.', {'s':13,'c':BK}],
    ['The SRS and SDS documents have been completed, covering the full system scope,', {'s':13,'c':BK}],
    ['functional requirements, module design, and experimental setup configuration.', {'s':13,'c':BK}],
    ['Implementation, model training, and live cluster testing are the planned next steps.', {'s':13,'c':BK}],
    [''],
    ['Expected Contributions', {'b':True, 's':17, 'c':DB}],
    ['  A complete end-to-end predictive auto-scaling pipeline from data ingestion to pod scaling.', {'s':13,'c':BK}],
    ['  Benchmark comparison of five forecasting models on real cloud workload datasets.', {'s':13,'c':BK}],
    ['  A proactive Kubernetes controller that scales pods based on predicted future demand.', {'s':13,'c':BK}],
    ['  An estimated 20–30% reduction in cluster compute over-provisioning and energy waste.', {'s':13,'c':BK}],
    ['  A live Grafana dashboard providing real-time observability of the entire system.', {'s':13,'c':BK}],
    [''],
    ['Future Scope', {'b':True, 's':17, 'c':LB}],
    ['  Extend to joint multi-metric forecasting — CPU, memory, and network I/O together.', {'s':13,'c':BK}],
    ['  Explore reinforcement learning for adaptive, self-tuning scaling policies.', {'s':13,'c':BK}],
    ['  Deploy across multi-cluster and edge / fog computing environments.', {'s':13,'c':BK}],
    ['  Integrate with cloud cost management platforms like AWS Cost Explorer and GCP Billing.', {'s':13,'c':BK}],
])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9  –  REFERENCES
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[8].shapes:
    if 'Shape;191' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'References')

bx = sl[8].shapes.add_textbox(Inches(0.45), Inches(1.1), Inches(12.4), Inches(6.1))
bx.text_frame.word_wrap = True
fill(bx.text_frame, [
    ['[1]  Google Inc., "Google Cluster Workload Traces v2," Google Cloud Platform Datasets, 2020.', {'s':13,'c':BK}],
    ['     Available: github.com/google/cluster-data', {'s':12,'c':GY,'i':True}],
    [''],
    ['[2]  S. Hochreiter and J. Schmidhuber, "Long Short-Term Memory,"', {'s':13,'c':BK}],
    ['     Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.', {'s':12,'c':GY,'i':True}],
    [''],
    ['[3]  K. Cho et al., "Learning Phrase Representations using RNN Encoder-Decoder', {'s':13,'c':BK}],
    ['     for Statistical Machine Translation," Proc. EMNLP, pp. 1724–1734, 2014.', {'s':12,'c':GY,'i':True}],
    [''],
    ['[4]  Kubernetes Authors, "Horizontal Pod Autoscaling Architecture and Specifications,"', {'s':13,'c':BK}],
    ['     Kubernetes Documentation, 2024.  kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/', {'s':12,'c':GY,'i':True}],
    [''],
    ['[5]  Prometheus Authors, "Prometheus: An Open-Source Monitoring and Alerting Toolkit,"', {'s':13,'c':BK}],
    ['     Cloud Native Computing Foundation (CNCF), 2024.', {'s':12,'c':GY,'i':True}],
    [''],
    ['[6]  Grafana Labs, "Grafana Observability and Dashboarding Platform Documentation," 2024.', {'s':13,'c':BK}],
    [''],
    ['[7]  T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System,"', {'s':13,'c':BK}],
    ['     Proc. ACM SIGKDD, pp. 785–794, 2016.', {'s':12,'c':GY,'i':True}],
    [''],
    ['[8]  IEEE Xplore Digital Library — Cloud Workload Forecasting and Auto-Scaling Research.', {'s':13,'c':BK}],
])

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 10  –  THANK YOU
# ════════════════════════════════════════════════════════════════════════════
for sh in sl[9].shapes:
    if 'Shape;197' in sh.name:
        clear(sh.text_frame)
        set_para(sh.text_frame.paragraphs[0], 'Thank You!', 36, True, False, DB)

    if 'Shape;198' in sh.name:
        fill(sh.text_frame, [
            ['Pratistha Singh   |   Btech/25047/24', {'b':True,  'c':DB, 's':16}],
            ['Arushi Goel        |   Btech/25111/24', {'b':True,  'c':DB, 's':16}],
            [''],
            ['B.Tech V  |  CSE Section A',            {'b':False, 'c':GY, 's':13}],
            ['Under the Supervision of',              {'b':False, 'c':GY, 's':13}],
            ['Faculty Mentor',                        {'b':True,  'c':RD, 's':15}],
            ['Assistant Professor',                   {'b':False, 'c':RD, 's':13}],
            ['BIT Mesra – Jaipur Campus',             {'b':False, 'c':GY, 's':13}],
        ])

prs.save(OUT)
print('SAVED:', OUT)
