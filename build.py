#!/usr/bin/env python3
"""Static builder for rudimohamed.com. Run: python3 build.py  -> writes /index.html, /about/index.html, ...
Pages share one header/footer; edit copy in the PAGES dict below."""
import json, os

SITE = "https://rudimohamed.com"
SUBSTACK = "https://rudimohamed.substack.com/"
LINKEDIN = "https://www.linkedin.com/in/rudi-mohamed/"
EMAIL = "rudi@rudimohamed.com"
BOOK_URL = "[VERIFY PURCHASE LINK]"   # replace with the direct Amazon/retailer product URL
FORM_ENDPOINT = "https://formspree.io/f/[INSERT_FORM_ID]"  # or any static-form provider Rudi approves
NAV = [("Home", "/"), ("About", "/about/"), ("Impact", "/impact/"), ("Insights", "/insights/"), ("Connect", "/connect/")]

def ph(t):  # visible placeholder; build fails loudly in launch check if any remain
    return f'<span class="placeholder">[{t}]</span>'

PERSON = {
  "@context": "https://schema.org", "@type": "Person", "@id": SITE + "/#rudi",
  "name": "Rudi Mohamed", "url": SITE + "/", "image": SITE + "/assets/rudi-portrait-960.webp",
  "jobTitle": "Chief Information Officer",
  "worksFor": {"@type": "GovernmentOrganization", "name": "Minnesota Housing"},
  "award": "2025 Minnesota ORBIE Award, Large Enterprise category",
  "knowsAbout": ["Technology value realization", "Enterprise architecture", "AI governance",
                 "Public-sector technology modernization", "Technology leadership"],
  "sameAs": [LINKEDIN, SUBSTACK],
}

def head(title, desc, path, extra_ld=None, og_type="website"):
    url = SITE + path
    ld = [PERSON] + (extra_ld or [])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Rudi Mohamed">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-rudi-mohamed.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#101D30">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else PERSON)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/">Rudi Mohamed</a>
<button class="menu-btn" aria-expanded="false" aria-controls="primary-nav">Menu</button>
<nav class="nav" id="primary-nav" aria-label="Primary"><ul>
""" + "".join(f'<li><a href="{h}"{" aria-current=page" if h == path else ""}>{n}</a></li>' for n, h in NAV) + """
</ul></nav></div></header>
<main id="main">
"""

FOOT = f"""</main>
<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div><p class="footer-sig">TECHNOLOGY. VALUE. IMPACT.</p>
<p>Technology should expand what we can accomplish. I write and speak about turning technology into capability, measurable value, and mission impact.</p></div>
<div><h2 class="eyebrow" style="color:#9DBDE3">Explore</h2><ul>
<li><a href="/about/">About</a></li><li><a href="/impact/">Impact</a></li><li><a href="/insights/">Insights</a></li><li><a href="/book/">The RockStar IT Leader Handbook</a></li><li><a href="/connect/">Connect</a></li></ul></div>
<div><h2 class="eyebrow" style="color:#9DBDE3">Elsewhere</h2><ul>
<li><a href="{SUBSTACK}">The Digital Edge on Substack</a></li><li><a href="{LINKEDIN}">LinkedIn</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
</div>
<p class="legal">&copy; 2026 Rudi Mohamed. Views expressed on this site are my own and do not represent Minnesota Housing or the State of Minnesota. Nothing here is an offer of services to, or on behalf of, any government entity.</p>
</div></footer>
<script>
(function(){{var b=document.querySelector('.menu-btn'),n=document.getElementById('primary-nav');
b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&n.classList.contains('open')){{n.classList.remove('open');b.setAttribute('aria-expanded','false');b.focus();}}}});}})();
</script>
</body></html>
"""

def newsletter(dark=False):
    return f"""<section class="{'on-dark' if dark else 'band'}" aria-labelledby="nl-title"><div class="wrap grid-2" style="align-items:center">
<div><p class="eyebrow">The Digital Edge</p><h2 id="nl-title">Practical thinking on technology, value, and AI that has to work.</h2>
<p>Field-tested perspective for technology and business leaders: how to choose investments, move AI past the pilot, and measure what technology actually changes. No hype.</p></div>
<div><a class="btn btn-primary" href="{SUBSTACK}">Subscribe to The Digital Edge</a>
<p class="hint" style="margin-top:1rem">Subscriptions are handled by Substack. You can unsubscribe at any time.</p></div>
</div></section>"""

ARTICLES = [  # verified titles/dates from rudimohamed.substack.com/archive (Oct 2026)
  ("How Should CIOs Respond to Today's Economic Uncertainties?", "May 20, 2025", "Technology Value"),
  ("DevSecOps for CIOs: A Practical Playbook for Secure, Scalable Innovation", "Mar 11, 2025", "Technology Leadership"),
  ("Top Digital Transformation Challenges & How to Overcome Them", "Feb 24, 2025", "Technology Leadership"),
  ("Mastering Cloud Transformation: A Strategic Playbook for Technology Executives", "Feb 12, 2025", "Technology Value"),
  ("DeepSeek-R1: 5 Must-Know Insights for Technology Executives", "Feb 4, 2025", "AI in the Real World"),
  ("What is GovTech and Why is it Important?", "Feb 2, 2025", "Public-Sector Innovation"),
  ("What Skills Are Essential for Financial Technology Leadership?", "Jan 31, 2025", "Technology Leadership"),
]
ART_URL = {ARTICLES[3][0]: SUBSTACK + "p/15-proven-tips-to-enhance-your-aws"}

def article_items(items):
    out = []
    for t, d, theme in items:
        u = ART_URL.get(t, SUBSTACK + "archive")
        out.append(f'<li><a href="{u}">{t}</a><p class="meta">{theme} &middot; {d} &middot; The Digital Edge</p></li>')
    return '<ul class="article-list">' + "".join(out) + "</ul>"

# ---------------- PAGES ----------------
HOME = head("Rudi Mohamed | Technology Executive, CIO, and Author",
  "Public-sector CIO, former Microsoft engineer, and 2025 Minnesota ORBIE Award winner focused on turning complex technology into capability, measurable value, and mission impact.", "/") + f"""
<section class="hero on-dark"><div class="wrap hero-grid">
<div><p class="signature">RUDI MOHAMED &nbsp;&middot;&nbsp; TECHNOLOGY. VALUE. IMPACT.</p>
<h1>Technology should expand what we can accomplish.</h1>
<p class="lede">I'm a public-sector CIO, technology strategist, and former Microsoft engineer focused on turning complex technology into greater organizational capability, measurable value, and mission impact.</p>
<div class="actions"><a class="btn btn-primary" href="/impact/">Explore My Work</a><a class="btn btn-secondary" href="/insights/">Read My Insights</a></div></div>
<img class="portrait" src="/assets/rudi-portrait-960.webp" srcset="/assets/rudi-portrait-480.webp 480w, /assets/rudi-portrait-960.webp 960w" sizes="(max-width:860px) 300px, 420px" width="960" height="1200" alt="Rudi Mohamed, Chief Information Officer, in a navy suit" fetchpriority="high">
</div></section>

<div class="wrap"><div class="cred" aria-label="Credentials">
<div><strong>Current role</strong>Chief Information Officer, Minnesota Housing</div>
<div><strong>Recognition</strong>2025 Minnesota ORBIE Award, Large Enterprise</div>
<div><strong>Foundation</strong>Software integration engineering, Microsoft</div>
<div><strong>Author</strong>The RockStar IT Leader Handbook</div>
</div></div>

<section aria-labelledby="pov"><div class="wrap grid-2">
<div><p class="eyebrow">Point of view</p><h2 id="pov">Technology is not the outcome. What it enables is.</h2></div>
<div><p>Most organizations don't have a technology problem. They have a gap between technology activity and measurable value: projects delivered, licenses bought, pilots launched, and too little change in what the institution can actually do.</p>
<p>For more than 20 years, from writing and integrating software at Microsoft to leading technology for a regulated public financial institution, my work has been closing that gap: connecting strategy to execution, investment to value, innovation to real work, and governance to responsible outcomes.</p>
<a class="textlink" href="/about/">Read my story</a></div>
</div></section>

<section class="band" aria-labelledby="chain"><div class="wrap">
<p class="eyebrow">How I think about value</p><h2 id="chain">From technology to outcomes</h2>
<p class="muted">Every investment should be traceable along this chain. If a link is missing, the value is too.</p>
<ol class="flow">
<li><strong>Technology</strong>Platforms, data, AI, and the systems we build or buy.</li>
<li><strong>Capability</strong>What people and teams can now do that they couldn't before.</li>
<li><strong>Operational change</strong>Workflows, decisions, and roles redesigned to use it.</li>
<li><strong>Outcome</strong>Measurable mission, financial, and risk results.</li>
</ol></div></section>

<section aria-labelledby="focus"><div class="wrap">
<p class="eyebrow">Areas of focus</p><h2 id="focus">Three places I spend my thinking</h2>
<div class="grid-3" style="margin-top:2rem">
<div class="card"><h3>Technology and enterprise leadership</h3><p>Modernization, architecture, security, and governance in environments where systems must keep running while they change.</p><a class="textlink" href="/impact/#modernization">See the work</a></div>
<div class="card"><h3>AI and technology value realization</h3><p>Choosing the right workflows, defining success up front, keeping humans accountable, and measuring what AI actually changes.</p><a class="textlink" href="/insights/#ai">Read about AI in the real world</a></div>
<div class="card"><h3>Public-sector technology and growth</h3><p>How government technology organizations make decisions, and what technology companies need to understand to deliver mission-relevant value.</p><a class="textlink" href="/insights/#public-sector">Explore public-sector innovation</a></div>
</div></div></section>

<section class="band" aria-labelledby="evidence"><div class="wrap">
<p class="eyebrow">Evidence</p><h2 id="evidence">Selected impact</h2>
<div class="grid-3" style="margin-top:2rem">
<div class="panel"><h3>Statewide tax-system modernization</h3><p>Led IT modernization for State of Minnesota infrastructure supporting the collection of more than $23 billion in annual tax revenue.</p><p class="meta">Role: {ph('VERIFY ROLE AND SCOPE WORDING')}</p></div>
<div class="panel"><h3>Regulated-environment CIO leadership</h3><p>Leads technology, security, and modernization for Minnesota Housing, a public financial institution. {ph('INSERT APPROVED OUTCOME METRIC')}</p></div>
<div class="panel"><h3>Peer recognition</h3><p>Named the 2025 Minnesota ORBIE Award winner in the Large Enterprise category, honoring CIOs of organizations above $1.4 billion in annual revenue.</p></div>
</div>
<div class="actions"><a class="btn btn-secondary" href="/impact/">Explore the case studies</a></div></div></section>

<section aria-labelledby="writing"><div class="wrap">
<div class="grid-2"><div><p class="eyebrow">Insights</p><h2 id="writing">Recent writing from The Digital Edge</h2></div>
<div><p>Practical essays on technology value, AI in real operations, and public-sector innovation.</p><a class="textlink" href="/insights/">All insights</a></div></div>
{article_items(ARTICLES[:3])}
</div></section>

<section class="band" aria-labelledby="book-h"><div class="wrap book-grid">
<img src="/assets/book-cover.webp" width="415" height="627" loading="lazy" alt="Cover of The RockStar IT Leader Handbook by Rudi M. Mohamed">
<div><p class="eyebrow">The book</p><h2 id="book-h">Technical excellence alone doesn't create leadership influence.</h2>
<p>The RockStar IT Leader Handbook is a practical guide for technology professionals who want to build credibility, communicate value, and lead teams that connect technical work to organizational outcomes.</p>
<div class="actions"><a class="btn btn-primary" href="/book/">Explore the Book</a></div></div>
</div></section>

<section class="on-dark" aria-labelledby="cta"><div class="wrap grid-2" style="align-items:center">
<div><h2 id="cta">Have a conversation in mind?</h2><p>Executive opportunities, speaking, board and advisory roles, or a thoughtful discussion about public-sector technology.</p></div>
<div class="actions" style="margin-top:0"><a class="btn btn-primary" href="/connect/">Get in Touch</a><a class="btn btn-secondary" href="{SUBSTACK}">Subscribe to The Digital Edge</a></div>
</div></section>
""" + FOOT

ABOUT = head("About Rudi Mohamed | From Software Engineer to CIO",
  "How a Microsoft software integration engineer became a public-sector CIO: enterprise architecture, technology investment strategy, and leadership in regulated environments.", "/about/") + f"""
<section class="page-head"><div class="wrap hero-grid">
<div><p class="eyebrow">About</p><h1>A technologist who became a leader, and never stopped being a technologist.</h1>
<p class="lede">My career has moved up the technology lifecycle: from building systems, to designing how they fit together, to deciding which ones an institution should invest in, to leading the people who make it all work.</p></div>
<img class="portrait" src="/assets/rudi-portrait-960.webp" srcset="/assets/rudi-portrait-480.webp 480w, /assets/rudi-portrait-960.webp 960w" sizes="(max-width:860px) 300px, 380px" width="960" height="1200" alt="Portrait of Rudi Mohamed" loading="lazy">
</div></section>

<section aria-labelledby="arc"><div class="wrap grid-2">
<div><p class="eyebrow">The arc</p><h2 id="arc">Four stages, one question</h2><p>At every stage I've asked the same thing: what will this technology make possible, and how will we know?</p></div>
<ol class="timeline">
<li><p class="stage">Build</p><h3>Software engineering and technical foundations</h3><p>I started as a software integration engineer at Microsoft, where I learned that systems succeed or fail at the seams: interfaces, data, and the assumptions teams make about each other. {ph('VERIFY DATES AND TITLE')}</p></li>
<li><p class="stage">Connect</p><h3>Enterprise architecture and systems thinking</h3><p>In enterprise architecture across the State of Minnesota, the unit of design became the institution. The work was less about any one system and more about how dozens of them served shared missions, data, and constituents.</p></li>
<li><p class="stage">Invest</p><h3>Technology investment strategy and program leadership</h3><p>Leading technology investment strategy and large-scale programs taught me that the hardest decisions aren't technical. They're about sequencing, trade-offs, and what to stop. This period included statewide tax-system modernization supporting more than $23 billion in annual revenue collection.</p></li>
<li><p class="stage">Lead</p><h3>CIO leadership in a complex, regulated environment</h3><p>Today I serve as Chief Information Officer at Minnesota Housing, a public financial institution, after leading its information systems function since 2022. I'm accountable for modernization, operations, security, and the organizational capability to sustain them.</p></li>
</ol></div></section>

<section class="band" aria-labelledby="phil"><div class="wrap grid-2">
<div><blockquote>Technology should expand what people and organizations are capable of accomplishing.</blockquote></div>
<div><h2 id="phil" class="eyebrow">How I lead</h2>
<p><strong>Start with the outcome.</strong> Define what will be measurably different before choosing the technology.</p>
<p><strong>Govern for speed, not against it.</strong> Good governance makes responsible decisions faster and more transparent.</p>
<p><strong>Build capability, not dependency.</strong> The lasting result of a program is what the organization can now do on its own.</p>
<p><strong>Be honest about evidence.</strong> Report what changed, what didn't, and what we learned.</p></div>
</div></section>

<section aria-labelledby="now"><div class="wrap grid-2">
<div><p class="eyebrow">Current interests</p><h2 id="now">What I'm working on now</h2></div>
<div><p>I'm focused on moving AI from experimentation toward accountable, measurable performance: selecting the right workflows, designing human oversight, and building the data readiness that makes AI dependable.</p>
<p>I also serve on peer leadership communities, including the Twin Cities CISO Leadership Board and the Twin Cities CIO Governing Body. {ph('VERIFY CURRENT BOARD AND COMMUNITY ROLES')}</p>
<p>I write about this work in <a href="/insights/">The Digital Edge</a> and in <a href="/book/">The RockStar IT Leader Handbook</a>.</p>
<div class="actions"><a class="btn btn-primary" href="/impact/">Explore My Work</a><a class="btn btn-secondary" href="/connect/">Get in Touch</a></div></div>
</div></section>
""" + FOOT

def case(id_, tag, title, items):
    rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in items)
    return f'<article class="case" id="{id_}" aria-labelledby="{id_}-h"><span class="tag">{tag}</span><h2 id="{id_}-h" style="margin-top:1rem">{title}</h2><dl>{rows}</dl></article>'

IMPACT = head("Impact | Case Studies in Technology Value | Rudi Mohamed",
  "Case studies in modernizing mission-critical public-sector systems, turning technology investment into measurable value, and moving AI toward responsible performance.", "/impact/") + f"""
<section class="page-head"><div class="wrap">
<p class="eyebrow">Impact</p><h1>Evidence, not adjectives.</h1>
<p class="lede">Three bodies of work, each written the same way: the problem, the constraints, the decisions, and what measurably changed. Where an outcome belongs to a team or the organization, I say so.</p>
<p class="notice">These case studies omit confidential and security-sensitive details about government systems. Metrics are published only when verified and approved for release.</p>
</div></section>
<div class="wrap">
{case("modernization", "Modernization", "Modernizing mission-critical public-sector systems", [
 ("The challenge", "Statewide technology supporting the collection of more than $23 billion in annual tax revenue needed to be modernized without interrupting service."),
 ("Why it mattered", "Revenue collection funds public services. Downtime, errors, or security failures would affect residents, businesses, and the state budget directly."),
 ("Constraints and risks", f"Fixed filing calendars, federal and state compliance requirements, legacy integrations, and zero tolerance for data loss. {ph('VERIFY AND ADD APPROVED CONSTRAINTS')}"),
 ("Decisions and interventions", ph("INSERT APPROVED DESCRIPTION OF KEY DECISIONS")),
 ("Implementation approach", ph("INSERT APPROVED DESCRIPTION, e.g. phasing, DevSecOps, cloud, vendor model")),
 ("Measurable outcome", ph("VERIFY METRIC, e.g. availability, processing time, e-filing adoption")),
 ("My role vs. team", ph("STATE DIRECT ROLE, TEAM, AND ORGANIZATION CONTRIBUTIONS")),
 ("Lessons for executives", "Modernizing a system that cannot stop is a sequencing problem before it is a technology problem. Protect the calendar, de-risk the seams, and measure service continuity as rigorously as delivery."),
])}
{case("value", "Technology Value", "Turning technology investments into measurable value", [
 ("The challenge", ph("INSERT APPROVED CASE STUDY: a portfolio or investment decision at Minnesota Housing or prior role")),
 ("Why it mattered", "Public financial institutions are accountable for every dollar. Technology spending has to show how it advances mission, reduces risk, or improves stewardship."),
 ("Constraints and risks", ph("VERIFY: budget cycle, legislative or board oversight, regulatory requirements")),
 ("Decisions and interventions", ph("INSERT: e.g. value criteria, prioritization model, what was paused or stopped")),
 ("Implementation approach", ph("INSERT APPROVED DESCRIPTION")),
 ("Measurable outcome", ph("VERIFY METRIC: never estimate savings")),
 ("My role vs. team", ph("STATE DIRECT ROLE, TEAM, AND ORGANIZATION CONTRIBUTIONS")),
 ("Lessons for executives", "If value isn't defined before funding, it will be redefined after delivery. Decide up front what will change, who owns it, and how it will be measured."),
])}
{case("ai", "AI in the Real World", "Moving AI from experimentation toward responsible performance", [
 ("The challenge", ph("INSERT APPROVED CASE STUDY: AI governance or workflow work cleared for public description")),
 ("Why it mattered", "AI pilots are easy to start and hard to turn into dependable, accountable operations, especially where decisions affect the public."),
 ("Constraints and risks", "Data quality and privacy, explainability, human accountability for decisions, security, and public trust."),
 ("Decisions and interventions", ph("INSERT: e.g. workflow selection criteria, governance model, human-in-the-loop design")),
 ("Implementation approach", ph("INSERT APPROVED DESCRIPTION")),
 ("Measurable outcome", ph("VERIFY METRIC, or state that measurement is in progress")),
 ("My role vs. team", ph("STATE DIRECT ROLE, TEAM, AND ORGANIZATION CONTRIBUTIONS")),
 ("Lessons for executives", "Choose workflows, not use cases. A good AI candidate has a clear owner, a measurable baseline, available data, and a defined point where a human verifies the result."),
])}
</div>
<section class="band" aria-labelledby="ai-sel"><div class="wrap">
<p class="eyebrow">Framework</p><h2 id="ai-sel">Five questions before an AI workflow ships</h2>
<ol class="flow flow-5">
<li><strong>Owner</strong>Who is accountable for the result?</li>
<li><strong>Baseline</strong>How does the work perform today?</li>
<li><strong>Data</strong>Is the data ready, permitted, and trustworthy?</li>
<li><strong>Verification</strong>Where does a human check the output?</li>
<li><strong>Measure</strong>What number should move, and by when?</li>
</ol><p class="meta" style="margin-top:1rem">Proposed framework by Rudi Mohamed. Opinion, not a standard.</p></div></section>
<section aria-labelledby="next"><div class="wrap grid-2"><div><h2 id="next">Want the thinking behind the work?</h2><p>The Digital Edge explores the decisions behind these case studies in more depth.</p></div>
<div class="actions"><a class="btn btn-primary" href="/insights/">Read My Insights</a><a class="btn btn-secondary" href="/connect/">Explore Executive Opportunities</a></div></div></section>
""" + FOOT

INSIGHTS = head("Insights | The Digital Edge by Rudi Mohamed",
  "The Digital Edge: practical writing on technology value, AI in the real world, and public-sector innovation from a working CIO.", "/insights/") + f"""
<section class="page-head"><div class="wrap">
<p class="eyebrow">Insights &middot; The Digital Edge</p><h1>The gap between technology activity and measurable value.</h1>
<p class="lede">Every piece asks the same practical questions: what problem are we solving, what capability are we creating, what must change operationally, how will we measure it, and what should we accelerate, redesign, pause, or stop?</p>
<div class="actions"><a class="btn btn-primary" href="{SUBSTACK}">Subscribe to The Digital Edge</a></div>
</div></section>
<section aria-labelledby="themes"><div class="wrap">
<h2 id="themes" class="eyebrow">Three themes</h2>
<div class="grid-3">
<div class="card" id="value"><h3>Technology Value</h3><p>Investment decisions, value realization, prioritization, operational efficiency, and institutional performance.</p></div>
<div class="card" id="ai"><h3>AI in the Real World</h3><p>Agentic workflows, workflow selection and redesign, governance, human oversight, and moving from pilots to measurable outcomes.</p></div>
<div class="card" id="public-sector"><h3>Public-Sector Innovation</h3><p>Government technology needs, procurement realities, adoption, and how technology companies can better understand government customers.</p></div>
</div></div></section>
<section class="band" aria-labelledby="latest"><div class="wrap">
<h2 id="latest">From the archive</h2>
{article_items(ARTICLES)}
<p style="margin-top:1.5rem"><a class="textlink" href="{SUBSTACK}archive">Read the full archive on Substack</a></p>
</div></section>
<section aria-labelledby="coming"><div class="wrap">
<h2 id="coming">In development</h2><p class="muted">Proposed essay concepts, not yet published.</p>
<ul class="article-list">
<li><span style="font-family:var(--serif);font-size:1.3rem">Choose workflows, not use cases: a practical test for AI investment</span><p class="meta">AI in the Real World &middot; Proposed</p></li>
<li><span style="font-family:var(--serif);font-size:1.3rem">What to stop: the most underused decision in technology portfolios</span><p class="meta">Technology Value &middot; Proposed</p></li>
<li><span style="font-family:var(--serif);font-size:1.3rem">What government technology leaders wish vendors understood</span><p class="meta">Public-Sector Innovation &middot; Proposed</p></li>
</ul></div></section>
<section class="band" aria-labelledby="lead"><div class="wrap book-grid">
<img src="/assets/book-cover.webp" width="415" height="627" loading="lazy" alt="Cover of The RockStar IT Leader Handbook">
<div><p class="eyebrow">Technology leadership</p><h2 id="lead">The RockStar IT Leader Handbook</h2><p>For the leadership and career side of the work: building credibility, communicating value, and leading teams.</p><div class="actions"><a class="btn btn-primary" href="/book/">Explore the Book</a></div></div>
</div></section>
""" + newsletter(dark=True) + FOOT

CONNECT = head("Connect with Rudi Mohamed | Executive, Speaking, and Board Inquiries",
  "Reach Rudi Mohamed about executive leadership opportunities, public-sector technology conversations, speaking, and board or advisory roles.", "/connect/") + f"""
<section class="page-head"><div class="wrap">
<p class="eyebrow">Connect</p><h1>Start a useful conversation.</h1>
<p class="lede">Choose the pathway closest to your purpose. I read every message and respond to relevant inquiries personally.</p>
</div></section>
<section aria-labelledby="paths"><div class="wrap"><h2 id="paths" class="eyebrow">Pathways</h2>
<div class="grid-2">
<div class="card"><h3>Executive leadership opportunities</h3><p>For recruiters, CEOs, and boards considering CIO, CTO, or senior technology leadership roles.</p><a class="textlink" href="#form" data-topic="executive">Explore Executive Opportunities</a></div>
<div class="card"><h3>Public-sector technology and growth</h3><p>For technology-company leaders who want to understand how government technology organizations operate and what mission-relevant value looks like.</p><a class="textlink" href="#form" data-topic="public-sector">Discuss Public-Sector Growth</a></div>
<div class="card"><h3>Speaking and thought leadership</h3><p>Keynotes, panels, and podcasts on technology value, responsible AI, and technology leadership.</p><a class="textlink" href="#form" data-topic="speaking">Invite Rudi to Speak</a></div>
<div class="card"><h3>Board and advisory opportunities</h3><p>Governance roles where technology, risk, and stewardship experience strengthen the board.</p><a class="textlink" href="#form" data-topic="board">Get in Touch</a></div>
</div>
<p class="notice" style="margin-top:2.5rem">Because I serve as a public-sector CIO, I do not discuss or influence procurement matters involving my agency, share non-public information, or represent my employer in commercial conversations. Any outside role is subject to applicable ethics and conflict-of-interest review.</p>
</div></section>
<section class="band" id="form" aria-labelledby="form-h"><div class="wrap grid-2">
<div><h2 id="form-h">Send a message</h2><p>Prefer email? Write to <a href="mailto:{EMAIL}">{EMAIL}</a> or connect on <a href="{LINKEDIN}">LinkedIn</a>.</p></div>
<form class="panel" action="{FORM_ENDPOINT}" method="POST" novalidate>
<div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
<div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-err"><p class="error" id="email-err" hidden>Enter a valid email address.</p></div>
<div class="field"><label for="org">Organization <span class="muted">(optional)</span></label><input id="org" name="organization" autocomplete="organization"></div>
<div class="field"><label for="topic">Topic</label><select id="topic" name="topic" required>
<option value="">Choose a topic</option><option value="executive">Executive leadership opportunity</option><option value="public-sector">Public-sector technology and growth</option><option value="speaking">Speaking or thought leadership</option><option value="board">Board or advisory</option><option value="other">Something else</option></select></div>
<div class="field"><label for="msg">Message</label><textarea id="msg" name="message" required aria-describedby="msg-hint"></textarea><p class="hint" id="msg-hint">A few sentences on what you have in mind and any timing.</p></div>
<div class="hp" aria-hidden="true"><label for="website">Leave this empty</label><input id="website" name="_gotcha" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="_next" value="{SITE}/connect/thanks/">
<p class="error" id="form-err" role="alert" hidden>Please complete the required fields.</p>
<button class="btn btn-primary" type="submit">Send message</button>
<p class="hint">Your details are used only to reply to you.</p>
</form></div></section>
<script>
(function(){{var f=document.querySelector('form');document.querySelectorAll('[data-topic]').forEach(function(a){{a.addEventListener('click',function(){{document.getElementById('topic').value=a.dataset.topic;}});}});
f.addEventListener('submit',function(e){{var ok=true,em=f.email;f.querySelectorAll('[required]').forEach(function(i){{var bad=!i.value.trim()||(i.type==='email'&&!/^\\S+@\\S+\\.\\S+$/.test(i.value));i.setAttribute('aria-invalid',bad);if(bad)ok=false;}});
document.getElementById('email-err').hidden=em.getAttribute('aria-invalid')!=='true';var fe=document.getElementById('form-err');fe.hidden=ok;if(!ok){{e.preventDefault();f.querySelector('[aria-invalid=true]').focus();}}}});}})();
</script>
""" + FOOT

THANKS = head("Message received | Rudi Mohamed", "Thank you for reaching out.", "/connect/thanks/") + f"""
<section class="page-head"><div class="wrap"><p class="eyebrow">Thank you</p><h1>Your message is on its way.</h1>
<p class="lede">Thank you for reaching out. I review every message and respond to relevant inquiries, usually within a few business days.</p>
<div class="actions"><a class="btn btn-primary" href="/insights/">Read My Insights</a><a class="btn btn-secondary" href="/">Return home</a></div></div></section>
""" + FOOT
THANKS = THANKS.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">')
NOTFOUND_FIX=1

BOOK_LD = [{"@context": "https://schema.org", "@type": "Book", "name": "The RockStar IT Leader Handbook",
  "author": {"@id": SITE + "/#rudi"}, "image": SITE + "/assets/book-cover.webp", "url": SITE + "/book/"}]
BOOK = head("The RockStar IT Leader Handbook | Rudi Mohamed",
  "A practical leadership guide for technology professionals who want to build credibility, communicate value, lead teams, and connect technical work to outcomes.", "/book/", BOOK_LD) + f"""
<section class="page-head"><div class="wrap book-grid">
<img src="/assets/book-cover.webp" width="415" height="627" alt="Cover of The RockStar IT Leader Handbook by Rudi M. Mohamed" fetchpriority="high">
<div><p class="eyebrow">The book</p><h1>The RockStar IT Leader Handbook</h1>
<p class="lede">Technical excellence alone doesn't guarantee leadership influence. This handbook is about the rest of the job.</p>
<p>Written for engineers, architects, managers, and new technology leaders, it offers practical guidance on earning credibility beyond your technical expertise, communicating value in terms executives act on, and leading teams that connect their work to organizational outcomes. {ph('VERIFY AGAINST PUBLISHED BOOK DESCRIPTION')}</p>
<div class="actions"><a class="btn btn-primary" href="{BOOK_URL}">Buy the Book {ph('VERIFY RETAILER')}</a><a class="btn btn-secondary" href="{SUBSTACK}">Subscribe to The Digital Edge</a></div>
<p class="meta">Format, ISBN, and publication date: {ph('VERIFY')}</p></div>
</div></section>
<section aria-labelledby="themes"><div class="wrap"><h2 id="themes">What you'll take away</h2>
<div class="grid-3" style="margin-top:2rem">
<div class="card"><h3>Credibility</h3><p>How to be trusted with decisions, not just tasks.</p></div>
<div class="card"><h3>Communicating value</h3><p>How to translate technical work into outcomes, risk, and investment language.</p></div>
<div class="card"><h3>Leading teams</h3><p>How to build teams that are capable, accountable, and connected to the mission.</p></div>
</div>
<p class="meta" style="margin-top:1.5rem">{ph('CONFIRM THEMES MATCH CHAPTERS; ADD TABLE OF CONTENTS IF DESIRED')}</p></div></section>
<section class="band" aria-labelledby="who"><div class="wrap grid-2">
<div><h2 id="who">Who it's for</h2></div>
<div><p>Technology professionals stepping into leadership, managers who want more influence with executives, and leaders developing the next generation of technology talent.</p>
<p>Keep going with related writing on <a href="/insights/">technology leadership</a>, or see how these ideas show up in practice on the <a href="/impact/">Impact</a> page.</p></div>
</div></section>
""" + newsletter(dark=True) + FOOT

NOTFOUND = head("Page not found | Rudi Mohamed", "This page could not be found.", "/404.html") + """
<section class="page-head"><div class="wrap"><p class="eyebrow">404</p><h1>That page has moved or doesn't exist.</h1>
<div class="actions"><a class="btn btn-primary" href="/">Go home</a><a class="btn btn-secondary" href="/insights/">Read My Insights</a></div></div></section>
""" + FOOT

OUT = {"index.html": HOME, "about/index.html": ABOUT, "impact/index.html": IMPACT, "insights/index.html": INSIGHTS,
       "connect/index.html": CONNECT, "connect/thanks/index.html": THANKS, "book/index.html": BOOK, "404.html": NOTFOUND}
for p, html in OUT.items():
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    open(p, "w").write(html)
urls = ["/", "/about/", "/impact/", "/insights/", "/connect/", "/book/"]
open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-19</lastmod></url>\n" for u in urls) + "</urlset>\n")
open("assets/favicon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="14" fill="#101D30"/><text x="50" y="62" text-anchor="middle" font-family="Georgia,serif" font-size="44" fill="#fff">RM</text></svg>')
print("built", len(OUT), "pages")
