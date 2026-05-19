import json
import random
import hashlib
from typing import List, Dict, Set

LABELS = {
    "benign": "BENIGN",
    "data_exfil": "DATA_EXFILTRATION",
    "ip_theft": "IP_THEFT",
    "poaching": "EMPLOYEE_POACHING",
    "conflict": "CONFLICT_OF_INTEREST",
    "policy": "POLICY_CIRCUMVENTION",
    "fraud": "FINANCIAL_FRAUD",
    "credential": "CREDENTIAL_ABUSE",
    "union": "UNION_ORGANIZING",
    "stressed": "STRESSED_EMPLOYEE",
    "job_seeking": "JOB_SEEKING"
}

DISTRIBUTION = {
    "benign": 2500,      
    "data_exfil": 1200,
    "ip_theft": 1100,
    "poaching": 1000,
    "conflict": 1000,
    "policy": 1100,
    "fraud": 1000,
    "credential": 1100,
    "union": 1000,  
    "stressed": 1000,  
    "job_seeking": 1000  
}

NAMES = ["John", "Sarah", "Mike", "Lisa", "David", "Emma", "Chris", "Anna", "Tom", "Kate",
         "Alex", "Maria", "James", "Rachel", "Mark", "Jennifer", "Steve", "Nicole", "Brian", "Laura",
         "Kevin", "Michelle", "Ryan", "Amanda", "Jason", "Stephanie", "Eric", "Ashley", "Andrew", "Jessica"]

DEPARTMENTS = ["Sales", "Engineering", "Marketing", "Finance", "HR", "IT", "Operations", "Legal",
               "Customer Support", "R&D", "Product", "Design", "Security", "Procurement", "Quality Assurance"]

COMPANIES = ["Apex Corp", "TechVentures", "GlobalSoft", "DataPrime", "InnovateTech", "NextGen Solutions",
             "Summit Industries", "Pioneer Systems", "Quantum Labs", "Vertex Technologies", "Synergy Inc",
             "Horizon Digital", "Catalyst Group", "Momentum Partners", "Velocity Tech"]

COMPETITORS = ["CompetitorX", "RivalTech", "MarketLeader Inc", "Industry Giant", "the competition",
               "our main competitor", "that other company", "you-know-who", "the big guys", "their company"]

FILE_TYPES = ["customer database", "client list", "financial records", "employee data", "contracts",
              "sales reports", "pricing sheets", "vendor list", "transaction logs", "HR records",
              "payroll data", "account information", "user credentials", "email archives", "CRM export"]

CODE_ASSETS = ["source code", "algorithm", "codebase", "repository", "proprietary code", "trading algorithm",
               "ML model", "neural network", "API keys", "encryption keys", "software architecture",
               "core modules", "backend code", "frontend code", "mobile app code"]

DESIGN_ASSETS = ["product designs", "CAD files", "schematics", "blueprints", "prototypes", "mockups",
                 "UI designs", "architecture diagrams", "technical specifications", "patent applications",
                 "research data", "formulas", "manufacturing processes", "trade secrets"]

STORAGE_METHODS = ["USB drive", "personal email", "Google Drive", "Dropbox", "external hard drive",
                   "personal cloud", "private server", "home computer", "personal laptop", "flash drive",
                   "memory card", "WeTransfer", "personal OneDrive", "iCloud", "private FTP"]

TIMES = ["tonight", "this weekend", "after hours", "before I leave", "tomorrow morning", "next week",
         "during lunch", "when no one's around", "off-hours", "late tonight", "early morning"]

MEETING_TOPICS = ["project status", "quarterly review", "team sync", "sprint planning", "budget review",
                  "client meeting", "training session", "performance review", "product roadmap", "strategy meeting"]

CASUAL_GREETINGS = ["Hey", "Hi", "Hello", "Hey there", "Hi there", "Yo", "What's up", "Morning", "Afternoon"]

FORMAL_GREETINGS = ["Dear", "Hello", "Good morning", "Good afternoon", "Greetings"]

CASUAL_CLOSINGS = ["Thanks", "Cheers", "Later", "Talk soon", "Best", "Thx", "TY", "K thanks", "Cool thanks"]

FORMAL_CLOSINGS = ["Best regards", "Kind regards", "Sincerely", "Thank you", "Regards", "Best wishes"]

URGENCY_WORDS = ["ASAP", "urgent", "immediately", "right away", "as soon as possible", "quickly",
                 "before EOD", "by tomorrow", "priority", "time-sensitive"]

SECURITY_TOOLS = ["VPN", "proxy", "Tor", "incognito mode", "private browsing", "burner phone",
                  "encrypted channel", "Signal", "disappearing messages", "anonymous email"]

MONEY_TERMS = ["invoice", "payment", "wire transfer", "expense report", "reimbursement", "bonus",
               "commission", "kickback", "consulting fee", "finder's fee", "referral bonus"]

UNION_TERMS = ["union", "labor union", "workers union", "employee union", "trade union", "collective bargaining",
               "union rep", "union representative", "labor rights", "collective action", "organizing committee",
               "bargaining unit", "union drive", "unionize", "organized labor", "labor organizer"]

UNION_ACTIONS = ["strike", "walkout", "work stoppage", "slowdown", "picket", "boycott", "sit-in",
                 "protest", "demonstration", "rally", "collective action", "work-to-rule", "sick-out"]

UNION_GRIEVANCES = ["unfair wages", "low pay", "no benefits", "poor working conditions", "long hours",
                    "unpaid overtime", "unsafe workplace", "harassment", "discrimination", "no job security",
                    "arbitrary firings", "favoritism", "retaliation", "lack of respect", "no voice"]

UNION_ORGS = ["AFL-CIO", "SEIU", "UAW", "Teamsters", "CWA", "UFCW", "UNITE HERE", "IBEW", "USW",
              "local union", "regional organizer", "labor board", "NLRB", "union organizer", "labor attorney"]

STRESS_SYMPTOMS = ["burnout", "exhausted", "overwhelmed", "frustrated", "stressed out", "at my limit",
                   "can't take it anymore", "breaking point", "losing it", "fed up", "done with this",
                   "had enough", "can't cope", "struggling", "drowning", "suffocating"]

STRESS_CAUSES = ["workload", "deadlines", "overtime", "management", "toxic environment", "micromanagement",
                 "unrealistic expectations", "no work-life balance", "constant pressure", "impossible demands",
                 "understaffed", "overworked", "no support", "being ignored", "lack of resources", "chaos"]

STRESS_EMOTIONS = ["angry", "depressed", "anxious", "miserable", "hopeless", "trapped", "resentful",
                   "bitter", "demoralized", "defeated", "broken", "numb", "cynical", "apathetic", "irritable"]

UNHAPPY_REASONS = ["terrible management", "toxic culture", "no appreciation", "unfair treatment",
                   "broken promises", "bad leadership", "poor communication", "constant changes",
                   "no growth", "dead-end job", "meaningless work", "hostile environment", "favoritism",
                   "office politics", "backstabbing", "no respect"]

COPING_METHODS = ["taking mental health days", "seeing a therapist", "on medication", "barely sleeping",
                  "drinking more", "calling in sick", "avoiding meetings", "working from home to hide",
                  "crying in the bathroom", "having panic attacks", "can't eat", "stress eating"]

JOB_PLATFORMS = ["LinkedIn", "Indeed", "Glassdoor", "ZipRecruiter", "Monster", "CareerBuilder",
                 "AngelList", "Hired", "the job boards", "recruiters", "headhunters", "networking events"]

JOB_ACTIVITIES = ["updating my resume", "polishing my LinkedIn", "applying to jobs", "interviewing",
                  "talking to recruiters", "networking", "job hunting", "looking around", "exploring options",
                  "testing the market", "sending out applications", "scheduling interviews"]

JOB_REASONS = ["better opportunity", "higher salary", "more growth", "better culture", "remote work",
               "work-life balance", "new challenges", "career advancement", "escape this place",
               "can't stand it here", "need a change", "toxic environment", "undervalued here",
               "no future here", "better benefits", "shorter commute"]

INTERVIEW_TERMS = ["phone screen", "first round", "second round", "final round", "technical interview",
                   "panel interview", "case study", "take-home assignment", "culture fit", "offer letter",
                   "negotiating salary", "reference check", "background check", "start date"]

COMPETING_COMPANIES = ["that startup", "the tech giant", "a competitor", "another company", "a new opportunity",
                       "somewhere better", "a real company", "a place that values people", "somewhere with growth"]


def generate_benign_templates() -> List[str]:
    """Generate benign/normal workplace messages."""
    templates = [
        f"Can we schedule a {random.choice(MEETING_TOPICS)} for {random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])}?",
        f"{random.choice(CASUAL_GREETINGS)}, are you free for a quick call about the {random.choice(['project', 'deadline', 'client request', 'bug fix'])}?",
        f"Just wanted to follow up on the {random.choice(MEETING_TOPICS)} from yesterday.",
        f"The {random.choice(MEETING_TOPICS)} has been moved to {random.randint(1, 5)} PM.",
        f"Please join the {random.choice(MEETING_TOPICS)} via Zoom at {random.randint(9, 16)}:{random.choice(['00', '30'])}.",
        f"Need to reschedule our {random.choice(MEETING_TOPICS)} - something came up.",
        f"Can you send the meeting invite for the {random.choice(MEETING_TOPICS)}?",
        f"I'll dial in remotely for the {random.randint(2, 4)} o'clock {random.choice(MEETING_TOPICS)}.",
        f"Room {random.choice(['A', 'B', 'C'])}{random.randint(101, 305)} is booked for our {random.choice(MEETING_TOPICS)}.",
        f"Should we do the {random.choice(MEETING_TOPICS)} over Teams or in person?",

        f"I've finished the {random.choice(['report', 'analysis', 'presentation', 'document', 'spreadsheet'])} you asked for.",
        f"The {random.choice(['project', 'feature', 'update', 'fix'])} is ready for review.",
        f"Could you review my pull request when you get a chance?",
        f"I pushed the changes to the {random.choice(['development', 'staging', 'feature'])} branch.",
        f"The build is passing now. Ready for QA.",
        f"Just merged the {random.choice(['hotfix', 'feature branch', 'update'])} to main.",
        f"All tests are green, ready to deploy.",
        f"Completed the {random.choice(['code review', 'documentation', 'testing'])} for the {random.choice(['new feature', 'bug fix', 'refactor'])}.",
        f"The {random.choice(['sprint', 'milestone', 'phase'])} is on track.",
        f"Finished my part of the {random.choice(['project', 'deliverable', 'feature'])}. Handing off to {random.choice(NAMES)}.",

        f"Do you have the {random.choice(['documentation', 'specs', 'requirements', 'design doc'])} for this feature?",
        f"Can you help me understand how the {random.choice(['API', 'module', 'function', 'service'])} works?",
        f"What's the status on the {random.choice(['client', 'vendor', 'partner'])} deliverable?",
        f"Who should I contact about {random.choice(['IT support', 'HR questions', 'expense reports', 'time off'])}?",
        f"Is there a style guide for the {random.choice(['code', 'documentation', 'UI', 'reports'])}?",
        f"Where can I find the {random.choice(['onboarding docs', 'wiki', 'runbooks'])}?",
        f"What's the process for {random.choice(['requesting time off', 'submitting expenses', 'ordering equipment'])}?",
        f"Do you know if {random.choice(NAMES)} is available to help with {random.choice(['the bug', 'this task', 'my question'])}?",
        f"Which {random.choice(['Slack channel', 'email list', 'Teams group'])} should I use for {random.choice(DEPARTMENTS)} questions?",
        f"How do I get access to the {random.choice(['staging environment', 'test data', 'sandbox'])}?",

        f"Coffee break in 10?",
        f"Want to grab lunch?",
        f"Happy Friday! Any plans for the weekend?",
        f"Thanks for your help with that issue earlier.",
        f"Great job on the presentation!",
        f"The meeting ran long, sorry I'm late.",
        f"I'll be WFH tomorrow.",
        f"Running a bit behind, be there in 15.",
        f"OOO next week - {random.choice(NAMES)} is covering for me.",
        f"Congrats on the promotion!",
        f"Did you see the email about the {random.choice(['team outing', 'company event', 'holiday party'])}?",
        f"How was your vacation?",
        f"Good luck with your {random.choice(['presentation', 'interview', 'demo'])} today!",
        f"Let me know if you need any help settling in.",
        f"See you at the {random.choice(['team lunch', 'happy hour', 'offsite'])}!",
        f"Thanks for covering for me while I was out.",
        f"Have a great weekend!",
        f"Welcome back! How was your time off?",
        f"That was a productive meeting!",
        f"Thanks for the quick turnaround on that.",

        f"Have you tried restarting the {random.choice(['server', 'service', 'container', 'VM'])}?",
        f"The {random.choice(['database', 'cache', 'queue'])} seems slow today.",
        f"We should probably add more {random.choice(['tests', 'logging', 'monitoring'])} to this module.",
        f"What version of {random.choice(['Node', 'Python', 'Java', 'React'])} are we using?",
        f"The deployment to {random.choice(['staging', 'production', 'dev'])} completed successfully.",
        f"Getting a {random.choice(['timeout', '500 error', 'connection refused'])} from the {random.choice(['API', 'database', 'service'])}.",
        f"Can you check the {random.choice(['logs', 'metrics', 'dashboard'])} for any anomalies?",
        f"The {random.choice(['CI pipeline', 'build', 'deployment'])} failed - looking into it.",
        f"We need to update the {random.choice(['dependencies', 'packages', 'libraries'])} before release.",
        f"The {random.choice(['memory usage', 'CPU load', 'disk space'])} is spiking on {random.choice(['prod', 'staging', 'the server'])}.",

        f"Can you update the Jira ticket once you're done?",
        f"Let's sync on this in our {random.choice(['standup', 'retro', '1:1'])} tomorrow.",
        f"I added you to the project Slack channel.",
        f"Please review the PR before merging.",
        f"The client approved the mockups.",
        f"Moving this ticket to {random.choice(['In Progress', 'Code Review', 'Done'])}.",
        f"Added {random.choice(NAMES)} as a reviewer on the PR.",
        f"The {random.choice(['deadline', 'milestone', 'release date'])} is next {random.choice(['week', 'Friday', 'month'])}.",
        f"Can you estimate how long the {random.choice(['task', 'feature', 'fix'])} will take?",
        f"Let's break this epic into smaller tasks.",

        f"Please find attached the {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} {random.choice(['report', 'summary', 'analysis'])}.",
        f"As per our discussion, I've updated the {random.choice(['proposal', 'contract', 'agreement'])}.",
        f"The vendor confirmed delivery for next week.",
        f"Budget approval received from {random.choice(['Finance', 'management', 'the CFO'])}.",
        f"Training session scheduled for new {random.choice(['tools', 'processes', 'team members'])}.",
        f"Please sign and return the attached {random.choice(['NDA', 'contract', 'agreement'])}.",
        f"The {random.choice(['board', 'stakeholders', 'executives'])} approved the {random.choice(['budget', 'proposal', 'plan'])}.",
        f"We need your feedback on the {random.choice(['RFP', 'SOW', 'proposal'])} by EOD.",
        f"The audit is scheduled for next {random.choice(['week', 'month', 'quarter'])}.",
        f"Please review the updated {random.choice(['policy', 'guidelines', 'procedures'])} and acknowledge.",

        f"My laptop is running slow, can IT take a look?",
        f"Need access to the {random.choice(['shared drive', 'project folder', 'team wiki'])}.",
        f"Can you reset my VPN credentials? They expired.",
        f"The printer on floor {random.randint(1, 5)} is jammed again.",
        f"Please update the org chart with the new hires.",
        f"My {random.choice(['monitor', 'keyboard', 'mouse'])} stopped working.",
        f"Request for new {random.choice(['software license', 'equipment', 'laptop'])}.",
        f"When is the next IT maintenance window?",
        f"Can I get a {random.choice(['docking station', 'second monitor', 'headset'])} for WFH?",
        f"Badge not working at the {random.choice(['main entrance', 'parking garage', 'server room'])}.",

        f"Can you share the {random.choice(['Google Doc', 'spreadsheet', 'presentation'])} with me?",
        f"I'll update the {random.choice(['wiki', 'Confluence page', 'Notion doc'])} after the meeting.",
        f"Left you a comment on the {random.choice(['doc', 'PR', 'ticket'])}.",
        f"Let's collaborate on this in {random.choice(['Google Docs', 'Figma', 'Miro'])}.",
        f"Can you give me edit access to the {random.choice(['file', 'folder', 'document'])}?",

        f"Can you add me to the {random.choice(['Slack channel', 'Teams group', 'email list'])} for {random.choice(DEPARTMENTS)}?",
        f"I'm shadowing {random.choice(NAMES)} today to learn the {random.choice(['process', 'workflow', 'system'])}.",
        f"Where can I find the onboarding materials?",
        f"Is there a training video for the new {random.choice(['tool', 'process', 'system'])}?",
        f"Who handles training for new {random.choice(DEPARTMENTS)} team members?",
        f"Can you walk me through the {random.choice(['deployment process', 'review workflow', 'approval chain'])}?",
        f"I'm starting certification training next week.",
        f"Are there any upcoming lunch and learns?",
        f"Sign me up for the {random.choice(['security awareness', 'compliance', 'leadership'])} training.",
        f"Who's the point person for {random.choice(['onboarding', 'new hire setup', 'orientation'])}?",

        f"Quick heads up - I'll be in late tomorrow.",
        f"Taking a personal day on {random.choice(['Monday', 'Friday', 'Wednesday'])}.",
        f"Doctor's appointment at 2pm, will be out for an hour.",
        f"Working remotely for the rest of the week.",
        f"My calendar is up to date if you need to find a time.",
        f"I'm heads down on this project until Thursday.",
        f"Let me know when you're free to sync.",
        f"Stuck in another meeting - will message when I'm out.",
        f"Back from PTO, catching up on emails today.",
        f"Flexible on timing - whenever works for the team.",

        f"Can you review my draft before I send it to the client?",
        f"Looking for feedback on the proposal I sent over.",
        f"Would appreciate your input on the design mockup.",
        f"Let me know your thoughts when you get a chance.",
        f"Happy to iterate based on your suggestions.",
        f"Made the changes you requested - take another look?",
        f"Incorporated the feedback from yesterday's review.",
        f"Should be good to go after your final sign-off.",
        f"Thanks for the constructive feedback!",
        f"Your suggestions really improved the final version.",

        f"Can we get more {random.choice(['licenses', 'seats', 'subscriptions'])} for the team?",
        f"Need to order some {random.choice(['office supplies', 'equipment', 'hardware'])}.",
        f"Where do I submit requests for new {random.choice(['software', 'tools', 'resources'])}?",
        f"The {random.choice(['whiteboard', 'projector', 'conference phone'])} in room B is broken.",
        f"Can IT set up the new {random.choice(['laptop', 'workstation', 'monitor'])}?",
        f"Requesting a standing desk through facilities.",
        f"Need headphones for the open office - any recommendations?",
        f"The team could use another {random.choice(['screen', 'mouse', 'keyboard'])}.",
        f"Putting in a request for upgraded {random.choice(['RAM', 'storage', 'CPU'])} on my machine.",
        f"Can we expense {random.choice(['Udemy courses', 'conference tickets', 'books'])}?",

        f"Bringing donuts tomorrow - any dietary restrictions?",
        f"Happy work anniversary, {random.choice(NAMES)}!",
        f"Drinks after work on Friday?",
        f"Anyone want to grab food for lunch?",
        f"Team outing ideas - bowling or escape room?",
        f"Signing a card for {random.choice(NAMES)} - swing by my desk.",
        f"Baby shower for {random.choice(NAMES)} next Thursday!",
        f"Potluck on Friday - what should I bring?",
        f"Who's in for the fantasy football league?",
        f"Movie night at my place this weekend - you're invited!",

        f"What's the policy on {random.choice(['remote work', 'travel', 'expenses'])}?",
        f"How do I book a conference room?",
        f"Who approves PTO requests for our team?",
        f"Is there a template for {random.choice(['expense reports', 'project proposals', 'status updates'])}?",
        f"What's the dress code for client meetings?",
        f"Do we have guidelines for {random.choice(['email etiquette', 'meeting agendas', 'documentation'])}?",
        f"How far in advance should I book travel?",
        f"What's the reimbursement timeline for expenses?",
        f"Who do I contact about payroll questions?",
        f"Is there a FAQ for common HR questions?",

        f"Need to loop in {random.choice(DEPARTMENTS)} on this project.",
        f"Who's the stakeholder from {random.choice(DEPARTMENTS)}?",
        f"Can you intro me to someone on the {random.choice(DEPARTMENTS)} team?",
        f"Setting up a cross-functional meeting for the initiative.",
        f"Which team owns the {random.choice(['authentication', 'payments', 'notifications'])} service?",
        f"Need to coordinate with {random.choice(DEPARTMENTS)} before we proceed.",
        f"Who should I talk to about {random.choice(['budgets', 'headcount', 'timelines'])}?",
        f"Aligning with the other teams on the release schedule.",
        f"Can you share the contacts for the {random.choice(DEPARTMENTS)} project leads?",
        f"Joint planning session with {random.choice(DEPARTMENTS)} tomorrow.",

        f"Where's the documentation for the {random.choice(['API', 'service', 'module'])}?",
        f"I updated the README with the latest changes.",
        f"Can you review the docs I wrote for the new feature?",
        f"The wiki page needs updating after the refactor.",
        f"Added inline comments to make the code clearer.",
        f"Created a how-to guide for the {random.choice(['deployment', 'setup', 'testing'])} process.",
        f"The architecture diagram is outdated - who maintains it?",
        f"Documenting the API endpoints for the external team.",
        f"Added JSDoc comments to all the public functions.",
        f"The changelog needs an entry for this release.",

        f"Anyone else seeing issues with the {random.choice(['dev', 'staging', 'test'])} environment?",
        f"The tests are flaky - investigating now.",
        f"Found the root cause of the bug - simple fix.",
        f"Can you check if this works on your machine?",
        f"Cleared my cache and it's working now.",
        f"The issue was a missing environment variable.",
        f"Turns out it was a race condition.",
        f"Fixed the null pointer exception in the {random.choice(['handler', 'controller', 'service'])}.",
        f"The regression was caused by the last merge.",
        f"Added better error handling for edge cases.",

        f"How long do you think this feature will take?",
        f"Can we break this into smaller tasks?",
        f"I've estimated {random.randint(2, 8)} story points for this.",
        f"Let's do a planning poker session for the backlog.",
        f"The scope seems larger than initially thought.",
        f"We should prioritize the critical path items.",
        f"Adding this to the next sprint backlog.",
        f"Can we get this into the current iteration?",
        f"The deadline is tight but achievable.",
        f"Let's discuss the trade-offs in the next standup.",

        f"The linter is complaining about this file.",
        f"Can you fix the formatting before merging?",
        f"We should add unit tests for this module.",
        f"Code coverage dropped - need more tests.",
        f"The static analysis found some issues.",
        f"Refactored to reduce complexity.",
        f"Extracted this into a reusable component.",
        f"The code smell was bothering me so I cleaned it up.",
        f"Applied the design pattern we discussed.",
        f"Simplified the logic as suggested in the review.",

        f"The {random.choice(['database', 'cache', 'queue'])} needs more resources.",
        f"Scaling up the cluster for the load test.",
        f"The SSL certificate expires next month.",
        f"Setting up monitoring for the new service.",
        f"Added alerts for high CPU usage.",
        f"The backup job completed successfully.",
        f"Migrating to the new {random.choice(['database', 'cloud provider', 'framework'])} version.",
        f"Updated the Terraform configs.",
        f"The Kubernetes pods are healthy.",
        f"Increased the timeout for the slow endpoint.",

        f"The client approved the mockups.",
        f"Customer feedback was positive overall.",
        f"Scheduling a demo for the stakeholders.",
        f"The user testing went well.",
        f"Incorporating feedback from the beta users.",
        f"The customer support team reported a new issue.",
        f"Client wants to discuss the roadmap.",
        f"User research insights are in the shared folder.",
        f"NPS scores improved this quarter.",
        f"The customer success team needs our help.",

        f"Found a great tutorial for {random.choice(['React', 'Python', 'Kubernetes'])}.",
        f"Anyone interested in a lunch and learn about {random.choice(['AI', 'security', 'testing'])}?",
        f"Just finished the certification course.",
        f"Sharing my notes from the conference.",
        f"Interesting blog post about {random.choice(['microservices', 'DevOps', 'clean code'])}.",
        f"Book recommendation: just finished reading about {random.choice(['system design', 'leadership', 'agile'])}.",
        f"The workshop on {random.choice(['AWS', 'Docker', 'GraphQL'])} was helpful.",
        f"Practicing for the technical interview prep.",
        f"Learning a new language for the side project.",
        f"Mentoring session with {random.choice(NAMES)} went great.",

        f"Deploying to production at {random.randint(2, 6)} PM.",
        f"Release notes are ready for review.",
        f"The canary deployment looks stable.",
        f"Rolling back the last change - issues found.",
        f"Feature flag is enabled for 10% of users.",
        f"The hotfix is in production now.",
        f"Smoke tests passed after deployment.",
        f"Cutting the release branch tomorrow.",
        f"The release was successful - monitoring metrics.",
        f"Post-deployment verification complete.",

        f"Completed the security training module.",
        f"Running a vulnerability scan on the codebase.",
        f"Updated dependencies to patch the CVE.",
        f"Security review approved the changes.",
        f"Added input validation to prevent injection.",
        f"Enabled two-factor auth on my account.",
        f"The penetration test report is in.",
        f"Fixed the OWASP top 10 issue.",
        f"Rotated the API keys as scheduled.",
        f"The security audit went well.",

        f"Can you take a look when you have a minute?",
        f"No rush on this, just when you get a chance.",
        f"Thanks for the quick turnaround!",
        f"Appreciate your help with this.",
        f"Let me know if you need anything from my end.",
        f"Happy to jump on a call to discuss.",
        f"I'll handle the follow-up items.",
        f"Keeping you in the loop on progress.",
        f"Flagging this for your awareness.",
        f"Just a heads up about the upcoming change.",

        f"Would {random.choice(['10 AM', '2 PM', '3:30 PM', '11 AM'])} work for a quick sync?",
        f"Circling back on the action items from yesterday's standup.",
        f"Looping in {random.choice(NAMES)} since they have context on this.",
        f"Mind if I shadow you on the next {random.choice(['client call', 'demo', 'presentation'])}?",
        f"Putting together the {random.choice(['agenda', 'deck', 'summary'])} for tomorrow's meeting.",
        f"Quick reminder about the {random.choice(['deadline', 'submission', 'review'])} this Friday.",
        f"Wanted to give you a heads up before the all-hands.",
        f"Let's touch base after the {random.choice(MEETING_TOPICS)} wraps up.",
        f"Thanks for flagging that - I'll take care of it.",
        f"Passing this along since it might be relevant to your project.",
        f"Bumping this in case it got buried in your inbox.",
        f"Just following the thread here - any updates?",
        f"Adding this to our backlog for next sprint consideration.",
        f"Tagging you since you expressed interest in this area.",
        f"Gentle nudge on the review I sent over last week.",
        f"Let's reconvene after everyone has had a chance to digest this.",
        f"Confirming receipt - will get back to you by EOD.",
        f"Thanks for the context - that helps a lot.",
        f"Deferring to your expertise on this one.",
        f"Great catch - updating the document now.",

        f"Really appreciate you staying late to help finish this.",
        f"Your presentation was excellent - the client loved it.",
        f"Kudos on shipping that feature on time!",
        f"Just wanted to acknowledge the great work you've been doing.",
        f"Thanks for being so responsive on this project.",
        f"Your attention to detail really shows in this deliverable.",
        f"That was a fantastic idea you brought up in the meeting.",
        f"Shoutout to {random.choice(NAMES)} for going above and beyond!",
        f"The feedback from stakeholders has been really positive.",
        f"You knocked it out of the park with that demo.",
        f"Impressed by how quickly you ramped up on this.",
        f"Your mentorship has been incredibly valuable.",
        f"The quality of your code reviews is always top-notch.",
        f"Thanks for being such a great team player.",
        f"Your positive attitude makes a real difference.",
        f"Really glad to have you on the team.",
        f"That bug fix was clutch - saved us a lot of trouble.",
        f"Your documentation is always so thorough and helpful.",
        f"Great job handling that difficult customer situation.",
        f"The improvements you made are already showing results.",

        f"Submitting my timesheet now - let me know if anything looks off.",
        f"Updated the shared calendar with the new meeting times.",
        f"Can you verify the PO number for this expense?",
        f"Need to update my emergency contact info with HR.",
        f"Confirming my attendance at the {random.choice(['training', 'workshop', 'seminar'])}.",
        f"Please add me to the distribution list for {random.choice(DEPARTMENTS)} updates.",
        f"My badge isn't working at the {random.choice(['north entrance', 'parking garage', 'second floor'])}.",
        f"Requesting a replacement {random.choice(['laptop charger', 'mouse', 'keyboard'])}.",
        f"The projector in room {random.choice(['A', 'B', 'C'])}{random.randint(100, 300)} needs maintenance.",
        f"Can facilities look at the AC in our area? It's freezing.",
        f"Need to update my direct deposit information.",
        f"Parking pass expires next month - how do I renew?",
        f"Where do I submit receipts for the team lunch?",
        f"Can I get a visitor badge for my guest tomorrow?",
        f"The elevator on the east side is out of service again.",
        f"Requesting access to the {random.choice(['wellness room', 'mother\'s room', 'quiet room'])}.",
        f"Do we have any standing desks available?",
        f"My office phone extension changed to {random.randint(1000, 9999)}.",
        f"Need to reserve the large conference room for {random.randint(10, 30)} people.",
        f"Is there a process for ordering business cards?",

        f"Found a great course on {random.choice(['Udemy', 'Coursera', 'LinkedIn Learning'])} for this skill.",
        f"Would the team be interested in a knowledge share on {random.choice(['GraphQL', 'Kubernetes', 'React hooks'])}?",
        f"Planning to attend the {random.choice(['AWS', 'Google', 'Microsoft'])} conference next month.",
        f"Just passed my {random.choice(['PMP', 'AWS Solutions Architect', 'Scrum Master'])} certification!",
        f"Looking for a study buddy for the upcoming certification exam.",
        f"Anyone have book recommendations for improving {random.choice(['leadership', 'communication', 'technical'])} skills?",
        f"There's a free webinar on {random.choice(['best practices', 'new features', 'industry trends'])} tomorrow.",
        f"Requesting budget approval for the online course subscription.",
        f"The internal tech talk series has been really valuable.",
        f"Setting up a book club for the team - interested?",
        f"Completed the required compliance training ahead of schedule.",
        f"Mind reviewing my learning plan for this quarter?",
        f"The mentorship program applications open next week.",
        f"Any interest in doing a hackathon as a team?",
        f"Found an interesting podcast episode about our industry.",
        f"Taking notes at the conference - will share with the team.",
        f"The new employee orientation was really well organized.",
        f"Cross-training with {random.choice(DEPARTMENTS)} has been enlightening.",
        f"Signed up for the internal leadership development program.",
        f"The lunch and learn on {random.choice(['AI', 'security', 'agile'])} was packed.",

        f"Phase {random.randint(1, 3)} is wrapping up nicely.",
        f"We hit the milestone a day early!",
        f"All blockers from last week have been resolved.",
        f"The scope change has been approved by stakeholders.",
        f"Dependencies are all green - we're on track.",
        f"Risk mitigation plan is in place for the identified issues.",
        f"Velocity is improving compared to last sprint.",
        f"Customer UAT feedback has been incorporated.",
        f"The beta group is reporting positive results.",
        f"Integration testing is progressing smoothly.",
        f"We've achieved {random.randint(80, 100)}% test coverage on the new module.",
        f"Technical debt reduction is ahead of schedule.",
        f"The performance optimization yielded {random.randint(20, 50)}% improvement.",
        f"All acceptance criteria for the user story have been met.",
        f"Stakeholder sign-off received for the design.",
        f"Resource allocation has been finalized for next quarter.",
        f"The pilot program feedback is being incorporated.",
        f"Change request has been documented and submitted.",
        f"Lessons learned session scheduled for project closeout.",
        f"Budget utilization is within expected parameters.",

        f"Anyone want to order lunch together? Thinking {random.choice(['Thai', 'Mexican', 'Italian', 'Chinese'])}.",
        f"The new coffee machine in the break room is amazing.",
        f"Did anyone see my {random.choice(['water bottle', 'umbrella', 'jacket'])} in the conference room?",
        f"Team trivia night this Thursday - be there!",
        f"Bringing in {random.choice(['donuts', 'bagels', 'cookies'])} for the morning standup.",
        f"Anyone up for a walking meeting? Weather looks nice.",
        f"The office plants could use some water if anyone's near them.",
        f"Lost and found has accumulated quite a collection.",
        f"Who's in for the fantasy {random.choice(['football', 'basketball', 'baseball'])} league?",
        f"The vending machine on floor {random.randint(1, 5)} is restocked.",
        f"Free leftover pizza in the kitchen from the {random.choice(DEPARTMENTS)} meeting.",
        f"Organizing a group order from the new restaurant nearby.",
        f"Anyone have recommendations for lunch spots around here?",
        f"The office is so quiet today - everyone remote?",
        f"Don't forget to RSVP for the holiday party.",
        f"Who left the delicious brownies in the break room? Thank you!",
        f"Team photo tomorrow - don't forget to smile.",
        f"Found a great coffee shop down the street for our next 1:1.",
        f"The office snack supply is running low.",
        f"Anyone interested in starting a running club?",

        f"The new {random.choice(['framework', 'library', 'tool'])} has some interesting features.",
        f"Considering migrating from {random.choice(['REST', 'SOAP', 'GraphQL'])} to improve performance.",
        f"Has anyone tried the latest version of {random.choice(['Node', 'Python', 'Go'])}?",
        f"The database query optimization made a huge difference.",
        f"Reviewing the architecture decision records for the refactor.",
        f"The microservices approach is working well for this use case.",
        f"Need to add more granular logging for debugging.",
        f"The load balancer configuration needs adjustment.",
        f"Caching strategy is reducing database load significantly.",
        f"The API versioning scheme is working as expected.",
        f"Container orchestration has simplified our deployment process.",
        f"Feature toggles give us more flexibility for releases.",
        f"The monitoring dashboard is really helpful for troubleshooting.",
        f"Need to review our error handling strategy.",
        f"The tech debt sprint was really productive.",
        f"Considering adding {random.choice(['TypeScript', 'linting', 'static analysis'])} to the project.",
        f"The CI/CD pipeline improvements cut build time in half.",
        f"Need to update our {random.choice(['README', 'contributing guide', 'wiki'])} with the new process.",
        f"The refactored module is much easier to maintain now.",
        f"Pair programming session helped me understand the codebase better.",

        f"The vendor demo is scheduled for {random.choice(['Tuesday', 'Thursday', 'next week'])}.",
        f"Received the updated SOW from the contractor.",
        f"The external audit went smoothly.",
        f"Partner integration is progressing as planned.",
        f"The SLA metrics for the quarter look good.",
        f"Vendor renewal negotiation starts next month.",
        f"Third-party security assessment came back clean.",
        f"The consultant's recommendations are being reviewed.",
        f"Supplier lead times have improved recently.",
        f"The agency delivered the creative assets on time.",
        f"Contract extension has been approved by legal.",
        f"The outsourced team is ramped up and productive.",
        f"Vendor scorecard review is scheduled for this quarter.",
        f"The implementation partner has been very responsive.",
        f"Requesting references from the potential vendor.",
        f"The proof of concept with the new tool was successful.",
        f"Procurement has approved the purchase requisition.",
        f"The service level agreement meets our requirements.",
        f"Partner training session is being arranged.",
        f"External stakeholder feedback has been positive.",

        f"The dashboard metrics are updated and ready for review.",
        f"Running the monthly report now.",
        f"Data quality checks passed for the latest import.",
        f"The analytics team needs access to the aggregated dataset.",
        f"KPI tracking shows we're on target for the quarter.",
        f"The A/B test results are statistically significant.",
        f"Customer segmentation analysis is complete.",
        f"The data pipeline is running without errors.",
        f"Need to schedule the quarterly business review.",
        f"The trend analysis shows positive growth.",
        f"Attribution model has been updated with new parameters.",
        f"The cohort analysis reveals interesting patterns.",
        f"Funnel visualization is now available in the dashboard.",
        f"The data warehouse migration is progressing well.",
        f"Need to validate the data before the presentation.",
        f"The report template has been standardized.",
        f"Real-time metrics are now available in the monitoring tool.",
        f"The forecast model accuracy has improved.",
        f"Data governance policies have been updated.",
        f"The benchmark comparison looks favorable.",
    ]
    return templates

def generate_benign_long() -> List[str]:
    """Generate longer benign messages (email style)."""
    templates = [
        f"""{random.choice(FORMAL_GREETINGS)} Team,

I wanted to provide an update on the {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} {random.choice(['project', 'initiative', 'rollout'])}. We've made significant progress over the past week and are on track to meet our deadlines.

Key accomplishments:
- Completed the {random.choice(['design phase', 'testing phase', 'development sprint'])}
- Received stakeholder approval
- Onboarded {random.randint(2, 5)} new team members

Next steps include finalizing the documentation and preparing for the launch.

{random.choice(FORMAL_CLOSINGS)},
{random.choice(NAMES)}""",

        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

Just circling back on our conversation from the {random.choice(MEETING_TOPICS)}. I think the approach you suggested makes a lot of sense. Let me run it by {random.choice(NAMES)} from {random.choice(DEPARTMENTS)} and get their input.

I'll set up a follow-up meeting for later this week.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""Team,

Reminder that the {random.choice(['monthly', 'weekly', 'quarterly'])} {random.choice(MEETING_TOPICS)} is tomorrow at {random.randint(9, 16)}:{random.choice(['00', '30'])} in Conference Room {random.choice(['A', 'B', 'C', '1', '2', '3'])}.

Agenda:
1. Review progress on current initiatives
2. Discuss blockers and dependencies
3. Plan for next {random.choice(['sprint', 'quarter', 'milestone'])}

Please come prepared with your updates.

Thanks,
{random.choice(NAMES)}""",

        f"""{random.choice(FORMAL_GREETINGS)} {random.choice(NAMES)},

Thank you for sending over the {random.choice(['proposal', 'requirements', 'specifications'])}. I've reviewed them with the team and we have a few questions:

1. Can you clarify the timeline for phase 2?
2. What resources will be allocated to this project?
3. How does this align with our existing roadmap?

Looking forward to discussing further.

{random.choice(FORMAL_CLOSINGS)},
{random.choice(NAMES)}
{random.choice(DEPARTMENTS)} Department""",

        f"""Hi all,

Quick update on the {random.choice(['server migration', 'system upgrade', 'security patch', 'maintenance window'])} scheduled for this weekend:

- Start time: Saturday {random.randint(1, 12)} AM
- Expected duration: {random.randint(2, 8)} hours
- Affected systems: {random.choice(['email', 'file server', 'internal tools', 'CRM'])}

Please save your work and log off by Friday EOD. If you experience any issues after the maintenance, contact IT support.

Thanks for your patience,
IT Team""",
    ]
    return templates

def generate_data_exfil_templates() -> List[str]:
    """Generate data exfiltration messages."""
    templates = [
        # Direct requests
        f"Can you send me the {random.choice(FILE_TYPES)} before I leave?",
        f"I need a copy of the {random.choice(FILE_TYPES)} on my {random.choice(STORAGE_METHODS)}.",
        f"Export the entire {random.choice(FILE_TYPES)} and send it to my personal email.",
        f"How do I download all the {random.choice(FILE_TYPES)} to take with me?",
        f"Can you zip up the {random.choice(FILE_TYPES)} and upload it to {random.choice(STORAGE_METHODS)}?",
        f"I want to copy the complete {random.choice(FILE_TYPES)} to my personal device.",
        f"Forward me all the {random.choice(FILE_TYPES)} to my gmail account.",
        f"Transfer the {random.choice(FILE_TYPES)} files to my {random.choice(STORAGE_METHODS)}.",
        f"How can I get all {random.choice(FILE_TYPES)} out of the system?",
        f"Need to pull down the entire {random.choice(FILE_TYPES)} tonight.",

        # Subtle attempts
        f"I'm working from home {random.choice(TIMES)}, need offline access to the {random.choice(FILE_TYPES)}.",
        f"The VPN is too slow. Can I just copy the {random.choice(FILE_TYPES)} locally?",
        f"For the presentation, I need the full {random.choice(FILE_TYPES)} on my laptop.",
        f"Can you give me export permissions for the {random.choice(FILE_TYPES)}?",
        f"Is there a way to bulk download everything from the {random.choice(['CRM', 'database', 'shared drive', 'file server'])}?",
        f"Going on a business trip - need local copies of the {random.choice(FILE_TYPES)}.",
        f"Wi-Fi might be spotty at the client site. Let me download the {random.choice(FILE_TYPES)}.",
        f"Just in case my access gets cut, can you pull the {random.choice(FILE_TYPES)} for me?",
        f"Want to work on the {random.choice(FILE_TYPES)} over the weekend. How do I take it home?",
        f"The systems might go down during the upgrade. Let me save a copy of {random.choice(FILE_TYPES)}.",

        # Urgency-based
        f"{random.choice(URGENCY_WORDS).upper()}: Need the complete {random.choice(FILE_TYPES)} extracted tonight.",
        f"Client needs the {random.choice(FILE_TYPES)} {random.choice(URGENCY_WORDS)} - can you pull it all?",
        f"Before my last day, I need to back up the {random.choice(FILE_TYPES)} I've been working on.",
        f"Leaving the company soon, want to save all my {random.choice(['contacts', 'work', 'files', 'projects'])}.",
        f"Help me export my {random.choice(['client contacts', 'sales pipeline', 'account list'])} before transition.",
        f"My account gets deactivated Friday - need to grab the {random.choice(FILE_TYPES)} now.",
        f"Quick, before they lock down the system, help me copy the {random.choice(FILE_TYPES)}.",
        f"This is time sensitive - get me everything from the {random.choice(FILE_TYPES)}.",
        f"Managers are doing layoffs. Let me save my {random.choice(FILE_TYPES)} while I still can.",
        f"Getting terminated tomorrow. Help me back up my {random.choice(['work', 'files', 'data'])}.",

        # Deceptive framing
        f"For audit purposes, I need a copy of all {random.choice(FILE_TYPES)}.",
        f"Legal requested I archive all {random.choice(FILE_TYPES)} - sending to my personal for safekeeping.",
        f"Backing up {random.choice(FILE_TYPES)} to personal cloud in case of system failure.",
        f"IT said I should save a local copy of the {random.choice(FILE_TYPES)} during migration.",
        f"Making a personal backup of the {random.choice(FILE_TYPES)} just in case.",
        f"Compliance needs me to have an offline copy of {random.choice(FILE_TYPES)}.",
        f"Boss asked me to create a backup of all {random.choice(FILE_TYPES)} on my personal drive.",
        f"Security audit requires me to verify the {random.choice(FILE_TYPES)} - sending to my email.",
        f"For disaster recovery, I'm copying the {random.choice(FILE_TYPES)} to my personal {random.choice(STORAGE_METHODS)}.",
        f"Need the {random.choice(FILE_TYPES)} for a legitimate project - just easier on my personal device.",

        # Technical methods
        f"What's the SQL query to dump the entire {random.choice(['customer', 'user', 'sales', 'financial'])} table?",
        f"Can you disable the DLP alerts while I transfer these files?",
        f"How do I bypass the download restrictions on the {random.choice(FILE_TYPES)}?",
        f"Need API access to extract all data from the {random.choice(['CRM', 'ERP', 'database'])}.",
        f"Is there a way to export without triggering the security logs?",
        f"Give me the db connection string so I can pull the {random.choice(FILE_TYPES)} directly.",
        f"Can you run mysqldump on the {random.choice(['production', 'main', 'customer'])} database for me?",
        f"How do I export more than the {random.randint(100, 1000)} record limit?",
        f"Need direct S3 access to download all the {random.choice(FILE_TYPES)}.",
        f"Can you give me a DB replica so I can query the {random.choice(FILE_TYPES)} myself?",

        # Collaboration in exfil
        f"Hey, I'm collecting all the {random.choice(FILE_TYPES)} - can you send me what you have?",
        f"Let's sync our {random.choice(FILE_TYPES)} before they revoke our access.",
        f"Save everything to the {random.choice(STORAGE_METHODS)}, I'll pick it up later.",
        f"Upload the {random.choice(FILE_TYPES)} to the shared link I sent you.",
        f"Use the encrypted channel to send me the {random.choice(FILE_TYPES)}.",
        f"Put it in the shared {random.choice(STORAGE_METHODS)} folder I created.",
        f"Here's my personal email - send the {random.choice(FILE_TYPES)} there.",
        f"I set up a private share. Upload all {random.choice(FILE_TYPES)} there.",
        f"You have access - can you export the {random.choice(FILE_TYPES)} and send it my way?",
        f"Let's both download what we can and pool the {random.choice(FILE_TYPES)} later.",

        f"I need the complete {random.choice(['CRM', 'ERP', 'database'])} export, not just partial data.",
        f"Give me everything from the last {random.randint(2, 5)} years.",
        f"Export all records, not just my accounts.",
        f"I want access to the entire {random.choice(['customer', 'client', 'vendor'])} database.",
        f"How do I bulk download everything?",
        f"Need a complete snapshot of the {random.choice(FILE_TYPES)}.",
        f"Can you pull all {random.choice(['accounts', 'contacts', 'transactions'])} from the system?",
        f"I need the whole thing, not just a sample.",
        f"Export every single record to CSV for me.",
        f"Full data dump from {random.choice(['Salesforce', 'SAP', 'the main system'])} please.",

        f"Let me plug my personal {random.choice(['USB', 'phone', 'hard drive'])} into my work computer.",
        f"Sending this to my personal device for {random.choice(['safekeeping', 'backup', 'reference'])}.",
        f"I'll Bluetooth the {random.choice(FILE_TYPES)} to my phone.",
        f"Email it to my personal account: {random.choice(['gmail', 'yahoo', 'outlook'])}.",
        f"Uploading the {random.choice(FILE_TYPES)} to my home NAS.",
        f"Using AirDrop to send the files to my iPad.",
        f"I'll sync this to my personal iCloud account.",
        f"Copying everything to my personal laptop before I go.",
        f"Setting up automatic sync to my personal cloud storage.",
        f"Let me print all this so I have a physical copy.",

        f"Set up an automatic export to run every night.",
        f"I need a scheduled job to dump the {random.choice(FILE_TYPES)} daily.",
        f"Can you configure recurring backups to my personal {random.choice(STORAGE_METHODS)}?",
        f"I want a cron job that exports everything at 3 AM.",
        f"Set up automatic forwarding of all {random.choice(FILE_TYPES)} to my email.",
        f"Create a script that backs up the data to my private server nightly.",
        f"I need real-time sync of all {random.choice(FILE_TYPES)} to external storage.",
        f"Automate the export so I always have the latest copy.",
        f"Schedule this extraction to run {random.choice(['hourly', 'daily', 'weekly'])}.",
        f"Configure a data pipeline to my personal {random.choice(['AWS', 'Azure', 'GCP'])} account.",

        f"Delete the export after I download it.",
        f"Don't leave any trace of this data transfer.",
        f"Clear the logs after I pull the {random.choice(FILE_TYPES)}.",
        f"Make sure this extraction doesn't show up in the audit.",
        f"Use an unmarked channel to transfer the data.",
        f"Encrypt the {random.choice(FILE_TYPES)} so no one knows what's in it.",
        f"Compress and password-protect before sending.",
        f"Split the files into smaller chunks so it's less obvious.",
        f"Time the download when monitoring is lightest.",
        f"Let's do this {random.choice(TIMES)} when no one's watching.",

        f"I need this for a job interview portfolio.",
        f"My financial advisor needs to see the {random.choice(FILE_TYPES)}.",
        f"Taking the data for a side consulting gig.",
        f"I promised a friend I'd share how our {random.choice(['system', 'process', 'data'])} works.",
        f"Need it for my MBA thesis research.",
        f"I'm writing a book and need real-world examples.",
        f"Another company wants to see how we handle {random.choice(['customers', 'data', 'processes'])}.",
        f"For benchmarking with industry peers - totally anonymous.",
        f"A recruiter asked me to demonstrate my work.",
        f"I want to analyze the data at home where I can focus.",

        # More data exfil - specific file types
        f"Export the entire {random.choice(['Salesforce', 'HubSpot', 'Dynamics'])} database.",
        f"I need all the {random.choice(['invoices', 'receipts', 'purchase orders'])} from accounting.",
        f"Download the complete {random.choice(['lead list', 'prospect database', 'sales pipeline'])}.",
        f"Get me the {random.choice(['org chart', 'employee directory', 'contact list'])} with personal info.",
        f"Export all {random.choice(['support tickets', 'customer complaints', 'feedback forms'])}.",
        f"I want the {random.choice(['audit logs', 'access records', 'login history'])} for everyone.",
        f"Pull the {random.choice(['compensation data', 'salary bands', 'bonus information'])} for all employees.",
        f"Need the {random.choice(['board minutes', 'executive memos', 'strategic plans'])}.",
        f"Download all {random.choice(['legal contracts', 'NDAs', 'partnership agreements'])}.",
        f"Export the {random.choice(['insurance policies', 'benefits enrollment', 'claims data'])}.",

        # More data exfil - communication records
        f"Archive all my emails and send them to my personal account.",
        f"Export the entire {random.choice(['Slack', 'Teams', 'chat'])} history.",
        f"I need recordings of all the {random.choice(['meetings', 'calls', 'webinars'])}.",
        f"Download all shared files from the team channel.",
        f"Export my calendar with all attendee information.",
        f"Get me the {random.choice(['call logs', 'voicemails', 'phone records'])}.",
        f"I want copies of all {random.choice(['presentations', 'meeting notes', 'decision logs'])}.",
        f"Archive the entire project folder to my personal drive.",
        f"Export all documents I've ever accessed.",
        f"Download the shared drive contents to external storage.",

        # More data exfil - database targeting
        f"Run a SELECT * on the {random.choice(['users', 'customers', 'orders'])} table.",
        f"I need a full database backup on portable media.",
        f"Export all tables to CSV without any filtering.",
        f"Give me direct SQL access to run my own queries.",
        f"Dump the {random.choice(['production', 'live', 'main'])} database to my machine.",
        f"I want read access to all schemas in the data warehouse.",
        f"Export the entire {random.choice(['data lake', 'analytics database', 'reporting tables'])}.",
        f"Pull everything from {random.choice(['MongoDB', 'PostgreSQL', 'MySQL'])} to local.",
        f"Need the raw data, not the sanitized version.",
        f"Bypass the row-level security and get all records.",

        # More data exfil - API abuse
        f"I'm going to script the API to pull all data overnight.",
        f"What's the rate limit? I need to extract everything.",
        f"Using the API to mirror the entire database locally.",
        f"Automating data extraction through the REST endpoints.",
        f"Calling the export API in a loop to get all records.",
        f"Need API keys with no rate limits for bulk extraction.",
        f"Writing a scraper to get all the data through the UI.",
        f"Using pagination to extract the complete dataset.",
        f"The GraphQL API lets me query everything at once.",
        f"Automating browser to download all available data.",

        # More data exfil - media and files
        f"Downloading all images from the {random.choice(['product catalog', 'marketing folder', 'asset library'])}.",
        f"Copying all videos from the internal training library.",
        f"Export all PDFs from the document management system.",
        f"I need the raw {random.choice(['photos', 'graphics', 'designs'])} files, not compressed.",
        f"Download the entire media library to external storage.",
        f"Copying all the {random.choice(['templates', 'brand assets', 'marketing materials'])}.",
        f"Export audio recordings from the {random.choice(['call center', 'meetings', 'interviews'])}.",
        f"I want all attachments from the last {random.randint(1, 5)} years of emails.",
        f"Download the complete {random.choice(['SharePoint', 'Box', 'OneDrive'])} folder structure.",
        f"Extracting all files from the archive system.",

        # More data exfil - reports and analytics
        f"Export all {random.choice(['dashboards', 'reports', 'analytics'])} to PDF.",
        f"I need the raw data behind these visualizations.",
        f"Download all historical {random.choice(['metrics', 'KPIs', 'performance data'])}.",
        f"Export the {random.choice(['BI tool', 'Tableau', 'PowerBI'])} workbooks.",
        f"Get me the underlying data for all reports.",
        f"Download the complete {random.choice(['forecast', 'projection', 'model'])} data.",
        f"Export all {random.choice(['survey results', 'poll data', 'research findings'])}.",
        f"I want the {random.choice(['benchmarking', 'competitive', 'market'])} analysis data.",
        f"Pull all {random.choice(['trend data', 'historical analytics', 'time series'])}.",
        f"Need the executive dashboard data in spreadsheet form.",

        # More data exfil - intellectual property adjacent
        f"Copying the {random.choice(['style guide', 'brand book', 'design system'])} for reference.",
        f"Export the {random.choice(['content calendar', 'marketing plan', 'campaign strategy'])}.",
        f"Download all {random.choice(['case studies', 'white papers', 'success stories'])}.",
        f"I need the {random.choice(['pricing strategy', 'discount rules', 'margin data'])}.",
        f"Export the {random.choice(['product catalog', 'SKU list', 'inventory data'])}.",
        f"Get me the {random.choice(['vendor agreements', 'supplier contracts', 'procurement data'])}.",
        f"Download the {random.choice(['SOP documents', 'process maps', 'workflow diagrams'])}.",
        f"I want the {random.choice(['training materials', 'onboarding docs', 'playbooks'])}.",
        f"Export all {random.choice(['email templates', 'communication scripts', 'response guidelines'])}.",
        f"Need the {random.choice(['territory assignments', 'account allocations', 'sales regions'])} data.",

        f"Gonna take screenshots of every page of the {random.choice(FILE_TYPES)}.",
        f"Recording my screen while scrolling through the {random.choice(FILE_TYPES)}.",
        f"Dictating the {random.choice(FILE_TYPES)} into my phone's voice memo app.",
        f"Copying the data one small chunk at a time to avoid detection.",
        f"Printing everything and taking it home in my bag.",
        f"Emailing myself in small batches so it doesn't flag anything.",
        f"Using the mobile app to slowly download everything piece by piece.",
        f"Photographing each page of the {random.choice(FILE_TYPES)} with my phone.",
        f"Going to handwrite the key details from the {random.choice(FILE_TYPES)}.",
        f"Compressing and renaming files so security doesn't recognize them.",
        f"Breaking the export into tiny pieces under the detection threshold.",
        f"Sending one record at a time to my personal email over weeks.",
        f"Accessing from coffee shop WiFi so it's not traced to me.",
        f"Using my phone's hotspot to bypass company network monitoring.",
        f"Downloading during maintenance window when logging is reduced.",
        f"Exporting as images instead of data files to evade DLP.",
        f"Embedding data in documents that look like normal work files.",
        f"Password protecting the files before transferring them.",
        f"Zipping everything with an innocent looking filename.",
        f"Converting to PDF so the content filters don't catch it.",

        f"My access expires at midnight - need everything before then.",
        f"They're revoking permissions tomorrow, help me now!",
        f"The window to grab this is closing fast.",
        f"Restructuring means I lose access next week - move quickly.",
        f"IT is doing a permissions audit, get this done today.",
        f"Security is tightening up - last chance to pull this data.",
        f"New policies take effect Monday, this is our only shot.",
        f"System upgrade will lock us out - extract now.",
        f"Before they implement the new restrictions, pull everything.",
        f"The audit is coming, we need to move this data immediately.",
        f"Compliance changes mean we can't access this next month.",
        f"HR just announced layoffs - securing my files while I can.",
        f"Manager is getting suspicious, speed up the extraction.",
        f"IT noticed unusual activity, let's finish this quickly.",
        f"The new DLP software goes live Friday - hurry.",
        f"They're watching now, we have a small window.",
        f"Pull trigger on the backup plan, time is running out.",
        f"This is our last opportunity before the lockdown.",
        f"Extract what you can before the access review.",
        f"Clock is ticking on my departure - need files immediately.",

        f"The CEO asked me to have a personal backup of everything important.",
        f"Compliance wants me to personally verify all {random.choice(FILE_TYPES)} - need local copies.",
        f"IT told me to save everything locally during the migration.",
        f"My manager approved this data extraction, don't worry.",
        f"This is for the disaster recovery test - need offline copies.",
        f"Auditors requested I maintain personal archives.",
        f"Legal said I should keep copies for potential litigation.",
        f"HR wants employees to have personal backups of their work.",
        f"The board requested redundant copies of critical data.",
        f"Security team asked me to verify data integrity offline.",
        f"This is part of the business continuity planning exercise.",
        f"Finance needs independent verification of the records.",
        f"Quality assurance requires personal review of all data.",
        f"Client specifically asked for data to be sent to my personal email.",
        f"Vendor needs the data sent to their secure portal.",
        f"Partner organization requires direct data transfer.",
        f"Consultant engagement requires sharing raw data externally.",
        f"The government audit demands personal accountability copies.",
        f"Insurance claim requires proof - need personal documentation.",
        f"Investor due diligence needs direct data access.",

        f"Need a complete mirror of the entire {random.choice(['database', 'file server', 'SharePoint'])}.",
        f"Let's replicate the full {random.choice(['data warehouse', 'document repository', 'archive'])}.",
        f"I want a clone of everything in the {random.choice(['network drive', 'cloud storage', 'backup system'])}.",
        f"Sync the entire {random.choice(['CRM', 'ERP', 'HRM'])} to my external drive.",
        f"Download the complete history, not just current data.",
        f"I need every version of every file, including deleted ones.",
        f"Pull everything from the recycle bin and archives too.",
        f"Get the raw database tables, not the sanitized exports.",
        f"I want unfiltered access to the entire dataset.",
        f"Export with all metadata and audit trails intact.",
        f"Include all attachments and linked documents in the export.",
        f"Make sure to get the encrypted files too, I have the keys.",
        f"Don't forget the backup archives from last year.",
        f"Include all branch and regional data, not just headquarters.",
        f"Get the data from all subsidiaries and business units.",
        f"I need the international records as well.",
        f"Pull from both production and disaster recovery environments.",
        f"Include test data too - sometimes it has real customer info.",
        f"Don't skip any tables even if they seem empty.",
        f"Export everything including system tables and logs.",

        f"I need the complete Social Security number database.",
        f"Export all credit card information from the payment system.",
        f"Pull the full medical records database.",
        f"Get me everyone's home addresses from HR.",
        f"Download the authentication credentials for all accounts.",
        f"Export the biometric data from the security system.",
        f"I want the complete background check files.",
        f"Pull all the salary and compensation data.",
        f"Get the performance reviews and disciplinary records.",
        f"Export customer payment history with card details.",
        f"Download all passport and visa copies from HR.",
        f"I need the driver's license scans for everyone.",
        f"Pull the employee health insurance information.",
        f"Export all bank account details for direct deposit.",
        f"Get the complete tax ID and EIN records.",
        f"Download emergency contact personal information.",
        f"Pull all login credentials and password hashes.",
        f"Export the encryption keys and certificates.",
        f"Get all API keys and access tokens.",
        f"Download session tokens and cookies from the database.",

        f"Archive every email I've sent and received here.",
        f"Export complete Slack message history for all channels.",
        f"Download all Teams chat logs and recordings.",
        f"Pull the entire Zoom meeting archive with recordings.",
        f"Get all call recordings from the phone system.",
        f"Export complete SMS and messaging logs.",
        f"Download all voicemails and transcriptions.",
        f"Pull the calendar data with all attendee details.",
        f"Export video conference recordings from all platforms.",
        f"Get the complete instant message history.",
        f"Download all shared files from messaging platforms.",
        f"Pull private message archives, not just public channels.",
        f"Export direct messages between specific people.",
        f"Get the deleted messages if possible.",
        f"Download communication metadata and timestamps.",
        f"Pull the contact lists from all communication tools.",
        f"Export distribution lists and group memberships.",
        f"Get the auto-complete suggestions from email.",
        f"Download the address book across all platforms.",
        f"Pull the conference bridge access codes and PINs.",

        f"Can you FTP the files to my home server?",
        f"Set up SFTP access to transfer everything securely.",
        f"Use rsync to mirror the data to my private server.",
        f"Push the data to my personal S3 bucket.",
        f"Upload to the anonymous file sharing site I'll link.",
        f"Transfer via peer-to-peer to avoid centralized logging.",
        f"Use BitTorrent to distribute the files securely.",
        f"Send through Tor network to anonymize the transfer.",
        f"Use VPN to tunnel the data out.",
        f"Connect to my SSH server to stream the data.",
        f"Post the data to an encrypted pastebin.",
        f"Upload to temporary file hosting with auto-delete.",
        f"Use steganography to hide data in image files.",
        f"Encode the data in QR codes for manual transfer.",
        f"Beam files via Bluetooth to my personal device.",
        f"AirDrop the data to my phone.",
        f"Use NFC to tap and transfer small data pieces.",
        f"Infrared transfer to my secondary device.",
        f"Upload to decentralized storage like IPFS.",
        f"Post to blockchain-based storage for permanent access.",

        f"I need all data from the {random.choice(DEPARTMENTS)} department.",
        f"Export everything the {random.choice(DEPARTMENTS)} team has access to.",
        f"Pull all {random.choice(DEPARTMENTS)} shared drives and folders.",
        f"Get the complete {random.choice(DEPARTMENTS)} project archive.",
        f"Download {random.choice(DEPARTMENTS)}'s confidential files.",
        f"Export the restricted {random.choice(DEPARTMENTS)} database.",
        f"Pull all {random.choice(DEPARTMENTS)} customer data.",
        f"Get {random.choice(DEPARTMENTS)}'s internal communications.",
        f"Download {random.choice(DEPARTMENTS)} meeting recordings.",
        f"Export {random.choice(DEPARTMENTS)} strategic documents.",
        f"Pull {random.choice(DEPARTMENTS)}'s vendor contracts.",
        f"Get all {random.choice(DEPARTMENTS)} budget information.",
        f"Download {random.choice(DEPARTMENTS)} personnel files.",
        f"Export {random.choice(DEPARTMENTS)} performance data.",
        f"Pull {random.choice(DEPARTMENTS)}'s proprietary processes.",
        f"Get {random.choice(DEPARTMENTS)} client lists.",
        f"Download {random.choice(DEPARTMENTS)} sales pipeline.",
        f"Export {random.choice(DEPARTMENTS)} forecasting models.",
        f"Pull {random.choice(DEPARTMENTS)}'s competitive analysis.",
        f"Get {random.choice(DEPARTMENTS)} pricing strategies.",
    ]
    return templates

def generate_data_exfil_long() -> List[str]:
    """Generate longer data exfiltration messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

Since I'm transitioning out next month, I want to make sure I have copies of all the {random.choice(FILE_TYPES)} I've worked on. You know, for my portfolio and references.

Can you help me export:
- Complete {random.choice(FILE_TYPES)}
- All {random.choice(['client communications', 'project files', 'sales records'])}
- The {random.choice(['contact list', 'vendor database', 'pricing information'])}

Send it to my personal email or upload to my {random.choice(STORAGE_METHODS)}.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""Need a favor - the {random.choice(FILE_TYPES)} system is being migrated and I'm worried about losing access. Can you pull everything and save it somewhere safe?

I'm thinking we put it on a {random.choice(STORAGE_METHODS)} as backup. Better safe than sorry, right? Let's do it {random.choice(TIMES)} when the network is less monitored.

Let me know when you can help.""",

        f"""Quick question - is there a way to export the complete {random.choice(FILE_TYPES)} to CSV or Excel? I need ALL records, not just my accounts.

I've been trying but there seems to be some restriction. {random.choice(NAMES)} said you might know a workaround. This is for an important project, so please keep it between us.

Thanks!""",

        f"""{random.choice(CASUAL_GREETINGS)},

Before my access gets revoked, I need to grab some files:
1. The entire {random.choice(FILE_TYPES)}
2. All {random.choice(['customer data', 'transaction records', 'sales history'])} from the past 3 years
3. Complete {random.choice(['employee list', 'vendor contacts', 'partner information'])}

My personal email is [redacted]@gmail.com. Can you send everything there? Or use {random.choice(STORAGE_METHODS)}.

{random.choice(URGENCY_WORDS)} - my last day is Friday.""",
    ]
    return templates

def generate_ip_theft_templates() -> List[str]:
    """Generate intellectual property theft messages."""
    templates = [
        # Source code theft
        f"Can you share the {random.choice(CODE_ASSETS)} repository with my personal GitHub?",
        f"I need to clone the entire {random.choice(CODE_ASSETS)} to my machine.",
        f"How do I get the {random.choice(CODE_ASSETS)} onto my {random.choice(STORAGE_METHODS)}?",
        f"Send me the {random.choice(CODE_ASSETS)} - all of it, including the proprietary parts.",
        f"I want a complete backup of our {random.choice(CODE_ASSETS)} for reference.",
        f"Give me push access to the private {random.choice(CODE_ASSETS)} repo.",
        f"Add my personal GitHub account to the {random.choice(CODE_ASSETS)} project.",
        f"Export all the {random.choice(CODE_ASSETS)} to a zip file I can take home.",
        f"What's the easiest way to mirror the {random.choice(CODE_ASSETS)} to my own server?",
        f"I need the {random.choice(CODE_ASSETS)} for my personal archive.",

        # Design/Trade secret theft
        f"Can you export the {random.choice(DESIGN_ASSETS)} to my personal account?",
        f"I need copies of all the {random.choice(DESIGN_ASSETS)} we developed.",
        f"Share the {random.choice(DESIGN_ASSETS)} with me privately - it's for my portfolio.",
        f"How do I download the {random.choice(DESIGN_ASSETS)} without raising flags?",
        f"The {random.choice(DESIGN_ASSETS)} would be really useful at my next job.",
        f"Save the {random.choice(DESIGN_ASSETS)} to my personal {random.choice(STORAGE_METHODS)}.",
        f"Forward me all the {random.choice(DESIGN_ASSETS)} from the secure folder.",
        f"Can I get the original {random.choice(DESIGN_ASSETS)} files, not just the PDFs?",
        f"I'm taking photos of the {random.choice(DESIGN_ASSETS)} on my phone, is that okay?",
        f"Print me a copy of all the {random.choice(DESIGN_ASSETS)} to take home.",

        # Research/Algorithm theft
        f"Can you send me the {random.choice(['research findings', 'experimental data', 'test results'])}?",
        f"I want to take the {random.choice(CODE_ASSETS)} with me when I leave.",
        f"The {random.choice(['algorithm', 'model', 'formula'])} I developed - can I keep a copy?",
        f"Export the {random.choice(['training data', 'model weights', 'neural network'])} to my account.",
        f"I built this {random.choice(CODE_ASSETS)}, so I should be able to take it.",
        f"Share the complete {random.choice(['research dataset', 'training corpus', 'experiment logs'])}.",
        f"The {random.choice(['ML pipeline', 'data processing scripts', 'feature engineering'])} needs to be in my personal repo.",
        f"Can you dump the {random.choice(['model parameters', 'hyperparameters', 'model config'])} for me?",
        f"I need the full {random.choice(['R&D documentation', 'research notes', 'lab results'])}.",
        f"The proprietary {random.choice(['algorithm', 'formula', 'method'])} should be mine - I invented it.",

        # Subtle IP theft
        f"For my side project, I might reuse some of our {random.choice(CODE_ASSETS)}.",
        f"The {random.choice(DESIGN_ASSETS)} could work for my freelance client.",
        f"I'm documenting how our {random.choice(['system', 'architecture', 'platform'])} works for personal notes.",
        f"Screenshot the {random.choice(DESIGN_ASSETS)} for me, I want to study the approach.",
        f"What's our secret sauce in the {random.choice(CODE_ASSETS)}? Need details.",
        f"Just going to borrow some ideas from the {random.choice(DESIGN_ASSETS)} for my own project.",
        f"Recording my screen while I demo the {random.choice(['product', 'system', 'platform'])}.",
        f"Taking detailed notes on how the {random.choice(CODE_ASSETS)} works - for learning purposes.",
        f"Mind if I copy this {random.choice(['function', 'module', 'component'])} for personal use?",
        f"I'll just recreate the {random.choice(DESIGN_ASSETS)} from memory at my new job.",

        # Competitive intent
        f"This {random.choice(CODE_ASSETS)} would give {random.choice(COMPETITORS)} a huge advantage.",
        f"I know someone at {random.choice(COMPETITORS)} who'd pay well for our {random.choice(DESIGN_ASSETS)}.",
        f"{random.choice(COMPETITORS)} would love to see how we built this.",
        f"Our {random.choice(['methodology', 'process', 'approach'])} is worth a lot to the right buyer.",
        f"Imagine taking our {random.choice(CODE_ASSETS)} and using it to compete with them.",
        f"A competitor reached out. They want details on our {random.choice(DESIGN_ASSETS)}.",
        f"I could sell this {random.choice(CODE_ASSETS)} to {random.choice(COMPETITORS)} for serious money.",
        f"Someone offered me a bonus to bring the {random.choice(DESIGN_ASSETS)} to their company.",
        f"My new employer specifically wants me to bring knowledge of our {random.choice(CODE_ASSETS)}.",
        f"The {random.choice(['trade secrets', 'IP', 'proprietary methods'])} here would fetch a high price.",

        f"Export all the technical documentation before they change my access.",
        f"I need the complete {random.choice(['API specs', 'system architecture', 'database schema'])}.",
        f"Copy the entire {random.choice(['technical wiki', 'knowledge base', 'runbooks'])} to my personal account.",
        f"Download all the internal {random.choice(['whitepapers', 'research papers', 'technical reports'])}.",
        f"I want copies of every {random.choice(['design decision', 'architectural document', 'technical spec'])}.",
        f"The {random.choice(['roadmap', 'product strategy', 'technical vision'])} document needs to come with me.",
        f"Save all the {random.choice(['meeting notes', 'decision logs', 'engineering docs'])} from this project.",
        f"Export our {random.choice(['best practices', 'playbooks', 'operational guides'])} before I leave.",
        f"Copy the {random.choice(['style guides', 'coding standards', 'architecture patterns'])} we developed.",
        f"I need our proprietary {random.choice(['frameworks', 'libraries', 'tools'])} for my next role.",

        f"Export the {random.choice(['training data', 'labeled dataset', 'annotated corpus'])} to my personal account.",
        f"I need a copy of all our {random.choice(['ML models', 'trained networks', 'AI systems'])}.",
        f"Download the {random.choice(['model weights', 'checkpoints', 'fine-tuned parameters'])}.",
        f"Copy the {random.choice(['feature engineering', 'preprocessing', 'data pipeline'])} code.",
        f"Export our {random.choice(['hyperparameter configs', 'training scripts', 'model architectures'])}.",
        f"The {random.choice(['prediction models', 'recommendation engine', 'classification system'])} is mine - I built it.",
        f"I'm taking the {random.choice(['data science notebooks', 'experiment logs', 'model evaluation results'])}.",
        f"Copy all the {random.choice(['A/B test results', 'analytics insights', 'performance metrics'])}.",
        f"Need the {random.choice(['data models', 'schemas', 'ETL logic'])} for my portfolio.",
        f"Our proprietary {random.choice(['algorithms', 'heuristics', 'optimization methods'])} should come with me.",

        f"Document exactly how our {random.choice(['manufacturing process', 'production line', 'quality control'])} works.",
        f"I need the recipe for our {random.choice(['secret sauce', 'special formula', 'proprietary blend'])}.",
        f"Copy the {random.choice(['supplier list', 'vendor contacts', 'procurement sources'])} with pricing.",
        f"Export our {random.choice(['cost structures', 'margin calculations', 'pricing models'])}.",
        f"I want details on how we achieve our {random.choice(['efficiency', 'quality', 'performance'])} numbers.",
        f"Document the {random.choice(['workflow', 'process', 'methodology'])} that makes us competitive.",
        f"Save all the {random.choice(['operational secrets', 'trade know-how', 'production techniques'])}.",
        f"Copy the {random.choice(['calibration data', 'testing procedures', 'validation protocols'])}.",
        f"Export our {random.choice(['standard operating procedures', 'work instructions', 'process flows'])}.",
        f"I need the {random.choice(['formulas', 'calculations', 'algorithms'])} we use internally.",

        f"Export the entire {random.choice(['client database', 'customer CRM', 'account list'])} with contacts.",
        f"I need all the {random.choice(['proposals we sent', 'quotes we made', 'contracts we signed'])}.",
        f"Copy the {random.choice(['sales strategies', 'pitch decks', 'client presentations'])} we use.",
        f"Download all {random.choice(['client communications', 'email threads', 'meeting notes'])} from key accounts.",
        f"I want the {random.choice(['pricing history', 'deal terms', 'contract details'])} for our biggest clients.",
        f"Export the {random.choice(['customer feedback', 'satisfaction surveys', 'NPS data'])}.",
        f"Copy the {random.choice(['account plans', 'growth strategies', 'retention tactics'])} for each client.",
        f"Save all the {random.choice(['competitor analysis', 'market research', 'industry reports'])} we have.",
        f"I need the {random.choice(['win/loss analyses', 'competitive intelligence', 'market positioning'])} data.",
        f"Download the {random.choice(['customer segments', 'persona research', 'buyer journey maps'])}.",

        # More IP theft - proprietary technology
        f"Clone the entire {random.choice(['firmware', 'embedded code', 'hardware designs'])} repository.",
        f"I need our proprietary {random.choice(['compiler', 'interpreter', 'runtime'])} source code.",
        f"Export the {random.choice(['FPGA designs', 'ASIC layouts', 'chip schematics'])}.",
        f"Copy the {random.choice(['signal processing', 'image recognition', 'voice synthesis'])} algorithms.",
        f"Download our custom {random.choice(['driver code', 'kernel modules', 'OS patches'])}.",
        f"Get me the {random.choice(['networking stack', 'protocol implementation', 'encryption library'])}.",
        f"Export the {random.choice(['sensor calibration', 'actuator control', 'feedback systems'])} code.",
        f"I want the {random.choice(['real-time', 'embedded', 'IoT'])} firmware we developed.",
        f"Copy the {random.choice(['bootloader', 'BIOS', 'low-level'])} code.",
        f"Need the {random.choice(['security module', 'crypto implementation', 'authentication system'])} source.",

        # More IP theft - manufacturing and production
        f"I need the {random.choice(['bill of materials', 'component list', 'parts specifications'])}.",
        f"Copy the {random.choice(['assembly instructions', 'manufacturing steps', 'production process'])}.",
        f"Export the {random.choice(['quality parameters', 'tolerance specs', 'testing criteria'])}.",
        f"Get me the {random.choice(['tooling designs', 'jig specifications', 'fixture drawings'])}.",
        f"Download the {random.choice(['production schedules', 'manufacturing capacity', 'yield data'])}.",
        f"I want the {random.choice(['supplier qualifications', 'vendor audits', 'certification records'])}.",
        f"Copy the {random.choice(['packaging designs', 'shipping specs', 'logistics data'])}.",
        f"Export the {random.choice(['maintenance procedures', 'calibration schedules', 'equipment specs'])}.",
        f"Need the {random.choice(['environmental controls', 'cleanroom specs', 'contamination protocols'])}.",
        f"Get the {random.choice(['automation scripts', 'robot programs', 'PLC code'])}.",

        # More IP theft - research and development
        f"Export all {random.choice(['lab notebooks', 'experiment logs', 'research journals'])}.",
        f"I need the {random.choice(['clinical trial data', 'study results', 'patient outcomes'])}.",
        f"Copy the {random.choice(['chemical formulations', 'compound libraries', 'synthesis routes'])}.",
        f"Download the {random.choice(['genomic data', 'protein structures', 'molecular simulations'])}.",
        f"Get me the {random.choice(['material compositions', 'alloy specifications', 'polymer formulas'])}.",
        f"Export the {random.choice(['simulation models', 'finite element analyses', 'computational results'])}.",
        f"I want the {random.choice(['patent drafts', 'invention disclosures', 'prior art searches'])}.",
        f"Copy the {random.choice(['prototype designs', 'proof of concept', 'feasibility studies'])}.",
        f"Need the {random.choice(['test data', 'validation results', 'certification reports'])}.",
        f"Download all {random.choice(['academic papers', 'conference submissions', 'publication drafts'])}.",

        # More IP theft - business strategy
        f"Export the {random.choice(['5-year plan', 'strategic roadmap', 'growth strategy'])}.",
        f"I need the {random.choice(['M&A targets', 'acquisition analysis', 'due diligence reports'])}.",
        f"Copy the {random.choice(['market entry strategy', 'expansion plans', 'geographic analysis'])}.",
        f"Download the {random.choice(['competitive positioning', 'SWOT analysis', 'market assessment'])}.",
        f"Get me the {random.choice(['pricing models', 'revenue projections', 'financial forecasts'])}.",
        f"Export the {random.choice(['partnership evaluations', 'alliance strategies', 'JV proposals'])}.",
        f"I want the {random.choice(['board presentations', 'investor decks', 'funding proposals'])}.",
        f"Copy the {random.choice(['exit strategy', 'IPO preparation', 'valuation models'])}.",
        f"Need the {random.choice(['risk assessments', 'scenario planning', 'contingency plans'])}.",
        f"Download the {random.choice(['org restructuring', 'efficiency initiatives', 'cost reduction plans'])}.",

        # More IP theft - creative and marketing
        f"Export all {random.choice(['ad campaigns', 'creative briefs', 'marketing strategies'])}.",
        f"I need the {random.choice(['brand guidelines', 'visual identity', 'logo source files'])}.",
        f"Copy the {random.choice(['content strategy', 'editorial calendar', 'SEO playbook'])}.",
        f"Download the {random.choice(['video assets', 'photo library', 'stock footage'])}.",
        f"Get me the {random.choice(['jingles', 'sound design', 'audio branding'])} files.",
        f"Export the {random.choice(['packaging mockups', 'label designs', 'print materials'])}.",
        f"I want the {random.choice(['social media strategy', 'influencer list', 'campaign analytics'])}.",
        f"Copy the {random.choice(['customer personas', 'market segments', 'targeting criteria'])}.",
        f"Need the {random.choice(['PR materials', 'press releases', 'media contacts'])}.",
        f"Download the {random.choice(['event plans', 'trade show materials', 'sponsorship decks'])}.",

        # More IP theft - operational secrets
        f"Export the {random.choice(['logistics optimization', 'route planning', 'distribution network'])} data.",
        f"I need the {random.choice(['inventory algorithms', 'demand forecasting', 'supply chain models'])}.",
        f"Copy the {random.choice(['warehouse layouts', 'facility designs', 'space utilization'])} plans.",
        f"Download the {random.choice(['vendor scorecards', 'supplier performance', 'procurement analytics'])}.",
        f"Get me the {random.choice(['fleet management', 'vehicle tracking', 'delivery optimization'])} system.",
        f"Export the {random.choice(['energy usage', 'sustainability data', 'carbon footprint'])} reports.",
        f"I want the {random.choice(['safety records', 'incident reports', 'compliance audits'])}.",
        f"Copy the {random.choice(['workforce planning', 'staffing models', 'labor analytics'])}.",
        f"Need the {random.choice(['customer service scripts', 'escalation procedures', 'resolution playbooks'])}.",
        f"Download the {random.choice(['return policies', 'warranty data', 'service agreements'])}.",

        # More IP theft - financial methods
        f"Export the {random.choice(['pricing algorithms', 'dynamic pricing', 'yield management'])} models.",
        f"I need the {random.choice(['cost accounting', 'activity-based costing', 'overhead allocation'])} methods.",
        f"Copy the {random.choice(['tax strategies', 'transfer pricing', 'entity structures'])}.",
        f"Download the {random.choice(['treasury operations', 'cash management', 'FX hedging'])} procedures.",
        f"Get me the {random.choice(['credit models', 'risk scoring', 'default prediction'])} algorithms.",
        f"Export the {random.choice(['investment strategies', 'portfolio allocation', 'asset models'])}.",
        f"I want the {random.choice(['fraud detection', 'anomaly models', 'transaction monitoring'])} systems.",
        f"Copy the {random.choice(['actuarial tables', 'loss projections', 'claims models'])}.",
        f"Need the {random.choice(['underwriting guidelines', 'risk appetite', 'acceptance criteria'])}.",
        f"Download the {random.choice(['collection strategies', 'recovery procedures', 'write-off policies'])}.",

        f"Our secret to success is in the {random.choice(CODE_ASSETS)} - taking it with me.",
        f"The {random.choice(DESIGN_ASSETS)} gives us our edge - I'm copying it.",
        f"Whatever makes us different from competitors is what I need.",
        f"Extract the core differentiating {random.choice(['technology', 'process', 'methodology'])}.",
        f"Our competitive moat is in these files - downloading now.",
        f"The unique value proposition is built into this {random.choice(CODE_ASSETS)}.",
        f"Taking the innovation that sets us apart in the market.",
        f"Our market leadership comes from these {random.choice(DESIGN_ASSETS)}.",
        f"The proprietary advantage we have should come with me.",
        f"Copying the crown jewels of our {random.choice(['product', 'service', 'platform'])}.",
        f"What makes clients choose us over competitors is in here.",
        f"The breakthrough technology I'm extracting is invaluable.",
        f"Our patent-pending innovations need to be copied first.",
        f"The special sauce that drives revenue - I need a copy.",
        f"Getting the intellectual capital that defines our value.",
        f"The unique capabilities we offer are in these files.",
        f"Our industry-leading approach is documented here.",
        f"Taking the hard-won knowledge that took years to build.",
        f"The strategic assets that drive growth - all of them.",
        f"Extracting what separates us from commodity players.",

        f"I built this {random.choice(CODE_ASSETS)}, so it's rightfully mine.",
        f"This was my idea originally, I should own the {random.choice(DESIGN_ASSETS)}.",
        f"None of this would exist without me - I'm taking credit and copies.",
        f"They just funded it, but the innovation is mine.",
        f"My blood and sweat is in this {random.choice(CODE_ASSETS)} - keeping it.",
        f"The core concept came from me, they just executed.",
        f"This {random.choice(DESIGN_ASSETS)} has my signature approach.",
        f"I led the team that created this, so I have rights to it.",
        f"Without my expertise, this {random.choice(CODE_ASSETS)} wouldn't exist.",
        f"They bought my time, not my ideas - taking the ideas.",
        f"The fundamental invention is mine regardless of employment.",
        f"I conceived this before joining, company just developed it.",
        f"My personal innovations got mixed into company IP.",
        f"The genius in this system is mine to take.",
        f"They didn't appreciate my contribution - I'll show them.",
        f"This represents my life's work - not leaving it behind.",
        f"I deserve to benefit from what I created.",
        f"The company wouldn't exist without my inventions.",
        f"My name should be on this {random.choice(DESIGN_ASSETS)}, so I'm taking it.",
        f"Intellectual authorship means more than legal ownership.",

        f"This {random.choice(CODE_ASSETS)} could be worth millions to the right buyer.",
        f"Selling our {random.choice(DESIGN_ASSETS)} to fund my startup.",
        f"I know competitors who would pay handsomely for this.",
        f"The {random.choice(CODE_ASSETS)} alone is worth my annual salary.",
        f"Licensing this IP could set me up for life.",
        f"The market value of these trade secrets is substantial.",
        f"Multiple parties have expressed interest in acquiring this.",
        f"This {random.choice(DESIGN_ASSETS)} is my retirement plan.",
        f"Monetizing company IP on the side as passive income.",
        f"The bidding war for this information would be intense.",
        f"State actors would pay premium for this technology.",
        f"Dark web buyers for corporate secrets are always looking.",
        f"Converting company IP into personal wealth.",
        f"This proprietary data has immense market value.",
        f"Leveraging inside knowledge for financial gain.",
        f"The {random.choice(CODE_ASSETS)} is worth more than my stock options.",
        f"Turning intellectual property into liquid assets.",
        f"Finding a buyer before I announce my departure.",
        f"This trade secret auction will be lucrative.",
        f"Extracting maximum value from what I helped create.",

        f"This {random.choice(CODE_ASSETS)} will be the foundation of my new company.",
        f"Launching my startup using our proven {random.choice(DESIGN_ASSETS)}.",
        f"Building my business on the work done here.",
        f"Our methodology will give my startup a head start.",
        f"Copying the playbook that made this company successful.",
        f"My new venture needs this {random.choice(CODE_ASSETS)} to compete.",
        f"Bootstrapping with borrowed intellectual property.",
        f"The {random.choice(DESIGN_ASSETS)} saves me years of R&D.",
        f"Why reinvent when I can take what already works?",
        f"My startup accelerator wants to see our proprietary tech.",
        f"VCs are interested if I can bring the {random.choice(CODE_ASSETS)}.",
        f"Co-founders are counting on me to bring the know-how.",
        f"This IP is my founder's contribution to the new company.",
        f"Launching a competitor with inside knowledge and code.",
        f"The business plan depends on acquiring this {random.choice(DESIGN_ASSETS)}.",
        f"Investors expect me to leverage my current company's IP.",
        f"Fast-tracking my startup with proven technology.",
        f"Market entry strategy relies on this proprietary info.",
        f"Building my empire on their foundation.",
        f"The unfair advantage my startup needs is in these files.",

        f"I'll recreate this {random.choice(CODE_ASSETS)} from memory at my new job.",
        f"Taking detailed notes on how everything works.",
        f"Memorizing the key algorithms before I leave.",
        f"Documenting the architecture in my personal notebook.",
        f"Screenshots of the critical {random.choice(DESIGN_ASSETS)} implementations.",
        f"Recording voice memos describing the technical approach.",
        f"Taking photos of whiteboards with system designs.",
        f"Copying technical diagrams to my personal device.",
        f"Making sketches of the proprietary processes.",
        f"Reverse engineering will be easier with the original specs.",
        f"Taking the blueprints to rebuild elsewhere.",
        f"Detailed documentation for replication purposes.",
        f"Capturing the tribal knowledge before departing.",
        f"Creating a technical reference for my next role.",
        f"Building a knowledge base of company secrets.",
        f"The implementation details are worth preserving.",
        f"Archiving learnings for future application.",
        f"Transcribing the unique methodologies.",
        f"Personal wiki of everything proprietary.",
        f"Exporting institutional knowledge in digital form.",

        f"Sharing with our partner under false pretenses.",
        f"Using the joint venture as cover to extract IP.",
        f"The alliance agreement doesn't cover personal copies.",
        f"Leveraging partner access to exfiltrate data.",
        f"Our collaborator is actually helping me extract secrets.",
        f"The consulting engagement gives me cover.",
        f"Exploiting vendor access to copy protected files.",
        f"Using contractor credentials for IP extraction.",
        f"The NDA with the partner doesn't protect internal IP.",
        f"Data sharing agreement being abused for personal gain.",
        f"Third-party integration as extraction vector.",
        f"Partner portal access reveals more than intended.",
        f"Joint development means shared IP, right?",
        f"Alliance data room has more than they realize.",
        f"Using customer engagement to acquire trade secrets.",
        f"Supplier relationship grants IP access.",
        f"Co-development project as IP harvesting operation.",
        f"The merger due diligence reveals everything.",
        f"Acquisition discussions expose key IP.",
        f"Investment talks give me access to secrets.",

        f"Git clone the entire private repository to my personal account.",
        f"Fork the private repo before they revoke access.",
        f"Exporting all commit history with full code.",
        f"Downloading the artifact repository completely.",
        f"Copying the Docker images with all our proprietary code.",
        f"Extracting the trained models from production.",
        f"Dumping the entire feature store to personal storage.",
        f"Downloading all Jupyter notebooks from the data platform.",
        f"Copying CI/CD pipelines with all secrets embedded.",
        f"Exporting the entire infrastructure as code repository.",
        f"Taking snapshots of all cloud resources.",
        f"Downloading the complete API specification.",
        f"Copying all microservices source code.",
        f"Extracting the complete data schema.",
        f"Downloading all configuration files.",
        f"Taking the complete test suite with sample data.",
        f"Copying the performance benchmarks and results.",
        f"Extracting security scanning reports with vulnerabilities.",
        f"Downloading the architecture documentation completely.",
        f"Taking all design documents and specifications.",
    ]
    return templates

def generate_ip_theft_long() -> List[str]:
    """Generate longer IP theft messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

I've been thinking about my next move career-wise. Before I go, I want to make sure I have copies of the work I contributed to:

- The {random.choice(CODE_ASSETS)} for the main product
- All the {random.choice(DESIGN_ASSETS)} from the last 2 years
- The {random.choice(['research documentation', 'technical specifications', 'architecture decisions'])}

I know technically it belongs to the company, but I wrote most of it. Can you help me extract it quietly?

{random.choice(CASUAL_CLOSINGS)}""",

        f"""Between us - I'm interviewing at {random.choice(COMPETITORS)} and they're very interested in someone with experience in our {random.choice(['technology', 'methodology', 'approach'])}.

If I could bring some of our {random.choice(CODE_ASSETS)} or {random.choice(DESIGN_ASSETS)}, it would really help my negotiating position. They don't need to know where it came from.

Can you get me access to the full repository?""",

        f"""I'm starting a consulting business on the side. The {random.choice(DESIGN_ASSETS)} and {random.choice(CODE_ASSETS)} we've developed here would save me months of work.

Don't worry, I won't compete directly with {random.choice(COMPANIES)}. But I could use the {random.choice(['framework', 'templates', 'processes'])} as a foundation.

Help me copy everything to my personal {random.choice(STORAGE_METHODS)}?""",
    ]
    return templates

def generate_poaching_templates() -> List[str]:
    """Generate employee poaching/collusion messages."""
    templates = [
        # Direct poaching
        f"Would you be interested in joining me at {random.choice(COMPETITORS)}?",
        f"I'm leaving for {random.choice(COMPANIES)} - want to come with me?",
        f"Got an offer from {random.choice(COMPETITORS)}. They're looking for more people like us.",
        f"Let's leave together and start fresh at {random.choice(COMPANIES)}.",
        f"I can put in a good word for you at my new company.",
        f"There's an opening at {random.choice(COMPANIES)}. Perfect for you.",
        f"Come work with me at {random.choice(COMPETITORS)}. We're hiring.",
        f"{random.choice(COMPANIES)} needs someone with your skills. Interested?",
        f"I already talked to my new boss about you. They want to meet.",
        f"Submit your resume to {random.choice(COMPANIES)}. I'll make sure it gets noticed.",

        # Team exodus planning
        f"How many from our team do you think would leave with us?",
        f"Talk to {random.choice(NAMES)} and {random.choice(NAMES)} - see if they want in.",
        f"We should coordinate our resignations for maximum impact.",
        f"If we all leave at once, they'll be screwed.",
        f"Let's get the whole {random.choice(DEPARTMENTS)} team to jump ship.",
        f"I'm putting together a list of who's willing to leave.",
        f"Sound out {random.choice(NAMES)} about jumping ship together.",
        f"The more of us that leave, the harder it hits them.",
        f"We're planning a mass exodus. You in?",
        f"Three people from {random.choice(DEPARTMENTS)} have already agreed to come.",

        # Subtle recruitment
        f"My new company is hiring. Thought of you immediately.",
        f"Keep this between us, but I might have an opportunity for you.",
        f"Are you happy here? Because I know a place that pays way better.",
        f"The grass really is greener. You should consider making a move.",
        f"Don't tell anyone, but I'm building a team for something new.",
        f"How would you feel about a change of scenery?",
        f"There might be something coming up that would interest you.",
        f"If hypothetically there was a better opportunity, would you take it?",
        f"You deserve better than this place. Let me tell you about an opportunity.",
        f"Between us, I'm exploring options. Want to explore together?",

        # Competitive planning
        f"With our combined experience, we could crush {random.choice(COMPANIES)} in the market.",
        f"Bring your skills to {random.choice(COMPETITORS)} - they'll double your salary.",
        f"We should take our talents somewhere they're appreciated.",
        f"Let's not give two weeks notice. Just leave them hanging.",
        f"Recruit as many people as you can before you announce your resignation.",
        f"Imagine if the whole senior team went to {random.choice(COMPETITORS)}.",
        f"Together we could build something better than {random.choice(COMPANIES)}.",
        f"Take all your knowledge and put it to work for a competitor.",
        f"Leave them high and dry right before the product launch.",
        f"If we bring the whole team, they'll give us whatever we want.",

        # Collusion
        f"Don't mention this to anyone, but I'm talking to several people about leaving.",
        f"Keep working normally, but start documenting everything you know.",
        f"Act surprised when I resign. We'll make our moves separately.",
        f"Once I'm settled at {random.choice(COMPANIES)}, I'll bring you over.",
        f"Trust only the people I've listed. Everyone else stays in the dark.",
        f"Delete this message after you read it.",
        f"Use your personal phone for this conversation.",
        f"Meet me outside the office to discuss. Walls have ears.",
        f"Let's use Signal for any further discussion about leaving.",
        f"Don't put anything in writing that could get back to management.",

        f"{random.choice(COMPETITORS)} is paying {random.randint(20, 60)}% more for the same role.",
        f"You could double your salary at {random.choice(COMPANIES)}.",
        f"The benefits at {random.choice(COMPETITORS)} are way better than here.",
        f"They're offering {random.randint(10000, 50000)} signing bonus to join.",
        f"Equity package at {random.choice(COMPANIES)} is incredible right now.",
        f"Better work-life balance AND higher pay - why stay here?",
        f"Remote work, unlimited PTO, and a raise. Interested?",
        f"You're underpaid here. Let me show you what you're worth.",
        f"Their {random.choice(['401k match', 'RSUs', 'bonus structure'])} blows ours away.",
        f"You won't believe the offer they gave me. You could get similar.",

        f"Leave right before the product launch - they'll feel it.",
        f"Quit during the busy season for maximum impact.",
        f"If we all resign during the audit, they're screwed.",
        f"Time your departure with the funding round - bad optics for them.",
        f"Hand in your notice the day before the big client meeting.",
        f"Let's coordinate our exits around the quarterly earnings.",
        f"The worst time for them is the best time for us to leave.",
        f"Resign when they can't afford to lose you.",
        f"Strike when {random.choice(NAMES)} is on vacation - chaos.",
        f"Walk out during the investor visit.",

        f"I need three more engineers from your team.",
        f"Bring your whole team if you can. We'll hire everyone.",
        f"The goal is to gut the {random.choice(DEPARTMENTS)} department.",
        f"Each person you recruit gets you a referral bonus.",
        f"Let's empty out the {random.choice(DEPARTMENTS)} team together.",
        f"Your direct reports would all get positions here.",
        f"I've already got {random.randint(3, 8)} people committed. Join us.",
        f"We're rebuilding an entire team at {random.choice(COMPANIES)} - be part of it.",
        f"They want to hire the whole squad. Interested?",
        f"Poach as many as you can. They're paying per head.",

        f"Don't worry about the non-compete, they never enforce those.",
        f"Your non-compete won't hold up in court. I checked.",
        f"We'll cover your legal fees if they try to sue.",
        f"Just don't tell them where you're going until you start.",
        f"The new company's lawyers say the non-compete is unenforceable.",
        f"We've hired people with non-competes before. No issues.",
        f"Take a {random.randint(1, 3)} month break to make the non-compete moot.",
        f"They won't sue - the bad PR isn't worth it.",
        f"Work as a 'consultant' first to get around the restrictions.",
        f"We'll put you in a different role title initially.",

        # More poaching - strategic targeting
        f"They specifically want people who know our {random.choice(['tech stack', 'processes', 'systems'])}.",
        f"Your experience with {random.choice(['the platform', 'our clients', 'the product'])} is exactly what they need.",
        f"They want to replicate what we built here.",
        f"Bring your institutional knowledge to {random.choice(COMPANIES)}.",
        f"They're building a team that mirrors our structure.",
        f"Your expertise in {random.choice(DEPARTMENTS)} is in high demand.",
        f"They need someone who understands our approach.",
        f"Your relationships with vendors would transfer perfectly.",
        f"They want our playbook - and you know it best.",
        f"Bring everything you learned here to the new role.",

        # More poaching - urgency and pressure
        f"The offer expires end of week - decide now.",
        f"They're interviewing other candidates from our company.",
        f"This position won't be open long.",
        f"Jump before the ship sinks.",
        f"Layoffs are coming - get out while you can.",
        f"I heard {random.choice(NAMES)} is already interviewing there.",
        f"Don't be the last one left here.",
        f"The window to join is closing.",
        f"They're filling the team fast - spots are going.",
        f"Make a decision before {random.choice(NAMES)} takes your spot.",

        # More poaching - undermining current employer
        f"This company has no future.",
        f"Leadership here is clueless.",
        f"We're all just waiting for the layoffs.",
        f"The company is going under - haven't you heard?",
        f"Management is running this place into the ground.",
        f"Our stock is tanking - time to bail.",
        f"The culture here is toxic and getting worse.",
        f"New leadership is going to clean house.",
        f"We're losing all our best clients.",
        f"The product is falling behind the competition.",

        # More poaching - personal appeals
        f"We've worked so well together - let's keep the team intact.",
        f"I wouldn't reach out if this wasn't a real opportunity.",
        f"You're wasted here - they'll actually appreciate you.",
        f"Think about your family - the pay is so much better.",
        f"I want good people around me at the new place.",
        f"We can recreate what we built here, but better.",
        f"You deserve to be somewhere that values you.",
        f"I'm only telling people I trust about this.",
        f"This is the career move you've been waiting for.",
        f"Don't you want to work somewhere exciting?",

        # More poaching - detailed offers
        f"Base salary of ${random.randint(150, 300)}k plus {random.randint(50, 200)}k in equity.",
        f"{random.randint(4, 8)} weeks PTO, remote-first, full benefits.",
        f"They'll match whatever title you want.",
        f"Sign-on bonus of ${random.randint(20, 100)}k.",
        f"Director level with a team of {random.randint(5, 15)}.",
        f"VP title if you bring the whole team.",
        f"Stock options that could be worth millions post-IPO.",
        f"Relocation package covers everything.",
        f"They'll buy out your unvested equity.",
        f"Corner office, expense account, the works.",

        # More poaching - knowledge extraction
        f"Before you leave, document everything about how things work here.",
        f"Start keeping notes on processes - you'll need them at the new job.",
        f"Download whatever you need to hit the ground running.",
        f"Make copies of useful materials before your access is cut.",
        f"Memorize the key details you can't take with you.",
        f"Keep a log of client contacts for when you move.",
        f"Save templates and procedures that worked well.",
        f"Take photos of anything useful before you resign.",
        f"Document the vendor relationships while you still can.",
        f"Build your personal reference library before leaving.",

        # More poaching - departure coordination
        f"Give notice on a Friday so they can't react immediately.",
        f"Don't tell HR until absolutely required.",
        f"Resign effective immediately once you sign the offer.",
        f"Claim you're taking a break, not joining a competitor.",
        f"Use your PTO balance as your notice period.",
        f"Go on 'sick leave' while you onboard at the new place.",
        f"Your new company will wait - take your time planning.",
        f"Delete evidence of your job search before resigning.",
        f"Say you're 'exploring options' if anyone asks.",
        f"Have your exit interview answers ready.",

        # More poaching - multi-person schemes
        f"We need at least {random.randint(4, 10)} people to make this work.",
        f"The more senior people we bring, the better our negotiating power.",
        f"They'll create a whole department if we come as a group.",
        f"Coordinate your start dates so we arrive together.",
        f"Each person you bring adds to your package.",
        f"Let's all request the same transition timeline.",
        f"Build a coalition before any of us resign.",
        f"We go together or not at all.",
        f"Strength in numbers - the more the merrier.",
        f"United front when we make our move.",

        f"Yo, you gotta check out this opportunity I found.",
        f"Seriously considering bouncing - want to come along?",
        f"There's this gig that would be perfect for you.",
        f"Dude, the new place is amazing - you'd fit right in.",
        f"Just saying, if you're ever looking, hit me up.",
        f"Not trying to poach you or anything, but...",
        f"Casually mentioning that my team has openings.",
        f"No pressure, but thought you might be interested.",
        f"Between you and me, I'm scouting talent for my new team.",
        f"You'd kill it at {random.choice(COMPETING_COMPANIES)} - just saying.",
        f"Hypothetically, would you consider leaving?",
        f"Totally off the record, but there's this role...",
        f"Don't shoot the messenger, but I had to tell you about this.",
        f"Pretend you didn't hear this from me, but...",
        f"Just putting it out there in case you're curious.",
        f"Take this with a grain of salt, but consider it.",
        f"Food for thought - the job market is pretty good right now.",
        f"I'm just the messenger here, but opportunities exist.",
        f"Planting seeds, that's all I'm doing.",
        f"This never happened, but what would you say to leaving?",

        f"You've always been too good for this place.",
        f"You deserve to be treated better than how they treat you here.",
        f"Remember when they passed you over for promotion?",
        f"Think about how much harder you work than everyone else.",
        f"You're the glue holding this team together, yet what do you get?",
        f"They don't see your value, but I do.",
        f"You're underutilized here - come shine elsewhere.",
        f"The way they overlooked your contributions was criminal.",
        f"You've given so much to this company with nothing in return.",
        f"Don't you want to be somewhere you're appreciated?",
        f"Life's too short to be unhappy at work.",
        f"You have so much potential that's being wasted here.",
        f"Think about your family - wouldn't more money help?",
        f"Your talents are being squandered in this role.",
        f"You're meant for bigger things than this.",
        f"Imagine actually enjoying going to work for once.",
        f"Don't you get tired of the disrespect?",
        f"You've earned the right to look elsewhere.",
        f"Self-care means knowing when to move on.",
        f"Your loyalty hasn't been rewarded - time to change that.",

        f"Everyone in the industry is making moves right now.",
        f"This is the great reshuffling - don't get left behind.",
        f"People are jumping ship everywhere - join the exodus.",
        f"The talent war means you have options.",
        f"Recruiters are desperate for people with your skills.",
        f"It's a candidate's market - leverage it.",
        f"Companies are paying premium for experienced people.",
        f"The hiring boom won't last forever - strike now.",
        f"Compensation packages have never been better.",
        f"Remote work has opened up so many opportunities.",
        f"The old rules about loyalty don't apply anymore.",
        f"Job hopping is the new career advancement.",
        f"Staying too long at one company hurts your career.",
        f"The stigma around leaving quickly is gone.",
        f"Modern careers are about accumulating experiences.",
        f"Nobody stays at one company for decades anymore.",
        f"Strategic moves are how you climb the ladder.",
        f"Your network is your net worth - expand it.",
        f"Every move is an opportunity to level up.",
        f"Career agility is more valuable than tenure.",

        f"Tell me about your current projects before you decide.",
        f"What's the roadmap looking like? Might help position you.",
        f"Any upcoming launches I should know about?",
        f"Who are the key people we should approach next?",
        f"What's the morale like in different departments?",
        f"Share the org chart so I know who else to target.",
        f"Which teams are most likely to have people interested?",
        f"What compensation ranges are being offered here?",
        f"Tell me about the retention bonuses they're offering.",
        f"How's the pipeline looking? Any product delays?",
        f"Who's unhappy and might be receptive to outreach?",
        f"What's the management situation really like?",
        f"Any layoffs or restructuring rumors?",
        f"What are people most frustrated about?",
        f"Which clients are at risk of churning?",
        f"Share the internal communications that are relevant.",
        f"What strategic decisions are being made?",
        f"Who's on the chopping block?",
        f"What's the real financial situation?",
        f"Any executive departures coming?",

        f"I have an exciting opportunity to discuss with you.",
        f"A prestigious client is looking for someone with your background.",
        f"This role has your name written all over it.",
        f"Based on your experience, this would be a perfect fit.",
        f"The hiring manager specifically requested profiles like yours.",
        f"This is a confidential search for a high-impact role.",
        f"You came highly recommended for this position.",
        f"The compensation package is extremely competitive.",
        f"This role offers significant growth potential.",
        f"We're looking for top talent to build out this team.",
        f"The company culture aligns with what you've described wanting.",
        f"Remote flexibility and work-life balance are priorities.",
        f"The benefits package is comprehensive and generous.",
        f"There's a clear path to advancement in this role.",
        f"The team you'd be joining is exceptional.",
        f"Technical challenges are exciting and impactful.",
        f"The mission and vision are truly inspiring.",
        f"Leadership is supportive and empowering.",
        f"The tech stack is modern and interesting.",
        f"This is a rare opportunity that won't last.",

        f"{random.choice(NAMES)} already made the move and loves it.",
        f"Everyone from our batch who left is thriving.",
        f"The former {random.choice(DEPARTMENTS)} folks are all happier now.",
        f"Nobody regrets leaving - not a single person.",
        f"Check Glassdoor - the reviews are so much better there.",
        f"The Blind posts about that company are positive.",
        f"LinkedIn shows tons of people making this transition.",
        f"Alumni from our company are everywhere at {random.choice(COMPETING_COMPANIES)}.",
        f"Word on the street is it's an amazing place to work.",
        f"Industry insiders rate it as a top employer.",
        f"The Comparably scores are significantly higher.",
        f"Employee satisfaction surveys show it's a great culture.",
        f"The retention rate there is much better than here.",
        f"People who join rarely leave - that says something.",
        f"The employer brand is stellar in our field.",
        f"Thought leaders in our space work there.",
        f"The talent density is off the charts.",
        f"They've won multiple best places to work awards.",
        f"The internal mobility options are excellent.",
        f"Career development is taken seriously there.",

        f"Your {random.choice(['engineering', 'product', 'design'])} skills are exactly what they need.",
        f"The {random.choice(['VP', 'Director', 'Senior'])} role was made for someone like you.",
        f"They're building out the {random.choice(DEPARTMENTS)} function from scratch.",
        f"Your expertise in {random.choice(['leadership', 'strategy', 'execution'])} is in demand.",
        f"The {random.choice(['technical', 'management', 'hybrid'])} track there is strong.",
        f"They want someone who can {random.choice(['scale', 'transform', 'build'])} the team.",
        f"Your background in {random.choice(['startups', 'enterprise', 'consulting'])} is valued.",
        f"The role involves {random.choice(['innovation', 'growth', 'optimization'])}.",
        f"They need someone with your {random.choice(['domain', 'industry', 'functional'])} expertise.",
        f"Your {random.choice(['people', 'process', 'technology'])} skills would shine.",
        f"The scope is {random.choice(['broader', 'deeper', 'more strategic'])} than here.",
        f"You'd have {random.choice(['more impact', 'bigger budget', 'larger team'])}.",
        f"The role reports to {random.choice(['the CEO', 'the CTO', 'the board'])}.",
        f"Visibility with {random.choice(['executives', 'investors', 'customers'])} is guaranteed.",
        f"The {random.choice(['P&L', 'revenue', 'headcount'])} responsibility is significant.",
        f"Decision-making authority is real, not just on paper.",
        f"The charter is to {random.choice(['disrupt', 'innovate', 'lead'])} the market.",
        f"You'd be {random.choice(['Employee #10', 'founding team', 'first hire'])} in this area.",
        f"Equity upside could be {random.choice(['life-changing', 'substantial', 'significant'])}.",
        f"The trajectory is {random.choice(['IPO', 'acquisition', 'unicorn'])} in a few years.",
    ]
    return templates

def generate_poaching_long() -> List[str]:
    """Generate longer poaching messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

I need to tell you something confidential. I've accepted an offer from {random.choice(COMPETITORS)} - starting next month.

Here's the thing: they're building out a whole new {random.choice(DEPARTMENTS)} team and I immediately thought of you. The pay is {random.randint(20, 50)}% more than what we make here, plus equity.

I can refer you directly. What do you say? We could work together again, but somewhere that actually values us.

Don't mention this to anyone at the office yet.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""OK so here's the plan:

I'm giving my notice on {random.choice(['Monday', 'Friday', 'the 15th'])}. {random.choice(NAMES)} is leaving the same week. We've talked to {random.choice(NAMES)} and {random.choice(NAMES)} too - they're in.

If you're interested, we should coordinate. The more of us that leave together, the better our negotiating position at {random.choice(COMPANIES)}.

Think about it. But keep this completely quiet. If management finds out, they might try to counter-offer people and split us up.

Call me tonight.""",

        f"""Just between us - I've been talking to a recruiter from {random.choice(COMPETITORS)}. They're very interested in our whole team, not just individuals.

They know we're the ones who built the {random.choice(['platform', 'product', 'system'])} here, and they want that expertise. If we go as a group, we could negotiate serious packages.

Who from {random.choice(DEPARTMENTS)} do you think would be interested? We need to move fast before someone talks.""",
    ]
    return templates

def generate_conflict_templates() -> List[str]:
    """Generate conflict of interest / company creation messages."""
    templates = [
        # Starting competing business
        f"I'm thinking about starting my own company in the same space.",
        f"Want to be a co-founder? We could do what {random.choice(COMPANIES)} does, but better.",
        f"I've already registered a company. Just need to quit and go full-time.",
        f"We could take our clients with us when we start the new venture.",
        f"The business plan is ready. It's basically what we do here.",
        f"I incorporated my own LLC last month. Same industry as here.",
        f"Building a product that directly competes with ours.",
        f"My startup does exactly what {random.choice(COMPANIES)} does. Shhh.",
        f"Planning to launch a competitor once I learn enough here.",
        f"Using this job as training for my own venture.",

        # Side business conflicts
        f"I've been doing freelance work for {random.choice(COMPETITORS)} on the side.",
        f"My side business is starting to compete with what we do here.",
        f"I'm consulting for a company in our industry. Don't tell HR.",
        f"I have a {random.choice(['client', 'contract', 'deal'])} that might conflict with my job here.",
        f"I've been moonlighting for our vendor. Is that a problem?",
        f"Doing paid work for a client that competes with us.",
        f"Running a {random.choice(['consulting gig', 'freelance business', 'side hustle'])} in the same field.",
        f"Got a contract that overlaps with company business.",
        f"Taking on clients in my spare time - same industry.",
        f"My side project is generating revenue now. It's in our space.",

        # Client/opportunity steering
        f"This lead would be perfect for my side business.",
        f"I'm going to refer this client to my own company instead.",
        f"We should send some overflow work to my consulting firm.",
        f"I can handle this project through my LLC - we'll split the profit.",
        f"This contract is too small for {random.choice(COMPANIES)}. I'll take it personally.",
        f"Referring this prospect to my side business instead.",
        f"Tell the client to work with my company directly.",
        f"I'll quote them through my LLC instead of the company.",
        f"Let's route this revenue through my side business.",
        f"The client prefers to work with me personally, not the company.",

        # Resource misuse for personal venture
        f"Can I use the company's {random.choice(['servers', 'tools', 'software'])} for my startup?",
        f"I'm building my product during work hours. No one will notice.",
        f"Using our {random.choice(['infrastructure', 'licenses', 'equipment'])} for my side project.",
        f"The company's paying for tools I'm using to build my own thing.",
        f"Working on my startup while logged into the office systems.",
        f"Deploying my personal project on company cloud resources.",
        f"Using company time to work on my business.",
        f"Borrowed some equipment from the office for my startup.",
        f"The company laptop is running my startup code 24/7.",
        f"My personal SaaS runs on company infrastructure.",

        # Investment conflicts
        f"I invested in {random.choice(COMPETITORS)}. Should I disclose that?",
        f"My family owns a company that's bidding on our contracts.",
        f"I have shares in a vendor we're evaluating. Let's pick them.",
        f"Steering business to a company I have a stake in.",
        f"My spouse works for {random.choice(COMPETITORS)}. We share everything.",
        f"I own stock in several vendors. Recommending the one I invested in.",
        f"My brother's company is bidding. I'm pushing for them.",
        f"Financial interest in a company we're contracting with.",
        f"I get a cut if we choose this vendor. Don't tell anyone.",
        f"My partner's firm is one of the candidates. Guess who I'm recommending?",

        f"I'm approaching our clients for my side business.",
        f"Told a few customers about my personal consulting services.",
        f"Diverting small accounts to my own company.",
        f"Clients I brought in should be mine if I leave.",
        f"Building relationships with clients for my future venture.",
        f"I gave my personal contact to some of our customers.",
        f"Letting clients know they can work with me directly.",
        f"Some accounts are small enough that the company won't miss them.",
        f"I'm going to poach these clients when I start my own thing.",
        f"These are MY relationships, not the company's.",

        f"I know about the upcoming {random.choice(['merger', 'acquisition', 'layoffs'])} - could trade on it.",
        f"Using what I learn here to invest in the right stocks.",
        f"The earnings report looks bad - time to sell before it's public.",
        f"Tipped off my friend about the acquisition news.",
        f"Inside info about the deal is too valuable not to use.",
        f"Bought shares in the company we're about to acquire.",
        f"My broker knows I have insider knowledge.",
        f"The product launch timing is public - I'm making trades.",
        f"Told my family to buy before the announcement.",
        f"This material non-public info could make us rich.",

        f"I'm working a second full-time job without telling anyone.",
        f"My other employer doesn't know I work here too.",
        f"Juggling two jobs during the same hours.",
        f"I do consulting work during my lunch break - on company time.",
        f"Running two remote jobs from the same desk.",
        f"My side work is taking over my main job responsibilities.",
        f"I bill both companies for the same hours sometimes.",
        f"Working for a client directly instead of through the company.",
        f"Started an LLC doing the same work on the side.",
        f"I have three 'full-time' jobs. Shh.",

        f"The vendor is a close friend - they'll get the contract.",
        f"I used to work at that company, so I'm pushing for them.",
        f"My gym buddy runs the vendor we're evaluating.",
        f"We vacation together - of course I'll recommend their company.",
        f"I owe them a favor, so we're going with their bid.",
        f"They've taken me to nice dinners. Time to return the favor.",
        f"Old college roommate runs the vendor. He's getting the deal.",
        f"I promised them the contract months ago.",
        f"They're my neighbors - awkward if I don't pick them.",
        f"Personal relationship with the vendor rep is influencing my decision.",

        # More conflict - gifts and entertainment
        f"The vendor offered me tickets to the {random.choice(['game', 'concert', 'show'])}.",
        f"They sent me a {random.choice(['watch', 'gift card', 'expensive bottle'])} for the holidays.",
        f"Free trip to {random.choice(['Vegas', 'Miami', 'Hawaii'])} if we sign with them.",
        f"They're covering my golf club membership.",
        f"Invited to their corporate retreat - all expenses paid.",
        f"They gave me a {random.choice(['laptop', 'phone', 'tablet'])} as a 'demo unit'.",
        f"Luxury box seats for the whole season if we renew.",
        f"They flew me first class for the 'site visit'.",
        f"The vendor entertainment budget for me is unlimited.",
        f"They're paying for my kid's summer camp.",

        # More conflict - competing loyalties
        f"I'm advising both companies on the same deal.",
        f"Serving on the board of a company we contract with.",
        f"My consulting client is bidding on our work.",
        f"I'm a partner at a firm that competes for our business.",
        f"Sitting on both sides of this negotiation.",
        f"I'm technically an employee of both companies.",
        f"Advising a startup that could disrupt our business.",
        f"On the advisory board of a direct competitor.",
        f"My investment fund has stakes in companies we evaluate.",
        f"Consulting for the client and the vendor simultaneously.",

        # More conflict - hiring and HR
        f"Hiring my {random.choice(['spouse', 'sibling', 'child'])} for the open role.",
        f"Giving the contract to my {random.choice(['cousin', 'uncle', 'friend'])}'s company.",
        f"My {random.choice(['roommate', 'partner', 'relative'])} is in the candidate pool.",
        f"Promoting my protégé over more qualified candidates.",
        f"Creating a position specifically for my {random.choice(['friend', 'family member', 'partner'])}.",
        f"Adjusting job requirements to match my preferred candidate.",
        f"The interview panel includes my personal connections.",
        f"Fast-tracking the hire because they're connected to me.",
        f"My referral bonus depends on this hire going through.",
        f"Nepotism? It's just good networking.",

        # More conflict - business opportunities
        f"This lead is too small for the company but perfect for my side business.",
        f"Redirecting opportunities that don't fit our minimums to myself.",
        f"Using company resources to pitch my own services.",
        f"The client approached us but I'm taking them personally.",
        f"Farming out overflow work to my own LLC.",
        f"Subcontracting to my side business without disclosure.",
        f"These referrals go to my personal network first.",
        f"Skimming the leads that the company wouldn't pursue anyway.",
        f"My side gig handles what falls below our threshold.",
        f"Building my client base using company deal flow.",

        # More conflict - information asymmetry
        f"I know we're about to lose this client - signing them to my side business.",
        f"Using my knowledge of company strategy for personal trades.",
        f"Learned about the {random.choice(['layoffs', 'merger', 'sale'])} before it's public.",
        f"The board decision gives me an investment advantage.",
        f"Inside knowledge of earnings before the call.",
        f"I know which products are failing - adjusting my portfolio.",
        f"Company intel is useful for my personal investments.",
        f"The M&A pipeline tells me which stocks to buy.",
        f"Tipping off friends before the announcement.",
        f"Trading ahead of material company news.",

        # More conflict - resource diversion
        f"Using company equipment for my rental properties.",
        f"Office supplies go home more than I'd like to admit.",
        f"The company car is basically my personal vehicle.",
        f"Using the corporate account for personal purchases.",
        f"Interns do more work for my side project than for the company.",
        f"Company software licenses running my personal business.",
        f"Meeting rooms booked for my external consulting.",
        f"Marketing materials adapted for my own use.",
        f"Charging personal expenses to the company project.",
        f"IT infrastructure supporting my side hustle.",

        # More conflict - decision influence
        f"My bonus depends on choosing this vendor.",
        f"If we go with them, I get a consultant role after I leave.",
        f"The decision maker is my personal investment partner.",
        f"Steering the outcome to benefit my side interests.",
        f"My recommendation is influenced by personal gain.",
        f"The winning bidder promised me something in return.",
        f"Voting for the option that benefits me personally.",
        f"My evaluation is biased by my relationship with them.",
        f"Conflicts of interest? I prefer to call them aligned interests.",
        f"What's good for me happens to be what I'm recommending.",

        f"Got two full-time jobs and neither knows about the other.",
        f"Working both positions during the same hours somehow.",
        f"Juggling meetings from both employers on the same calls.",
        f"My other job thinks I'm dedicated to them exclusively.",
        f"Collecting two salaries for the same time period.",
        f"Remote work makes it easy to have multiple employers.",
        f"Neither company knows I'm double-dipping.",
        f"Splitting my attention between two competing priorities.",
        f"Same laptop, two VPNs, two employers.",
        f"Calendar conflicts between my two jobs are getting tricky.",
        f"Billing both companies for the same productive hours.",
        f"The overlap in industries makes this extra risky.",
        f"One employer's competitor is my other employer.",
        f"Sharing insights between my two roles inadvertently.",
        f"The knowledge from one job directly benefits the other.",
        f"Walking a tightrope with competing obligations.",
        f"My productivity at both jobs is suffering.",
        f"Eventually someone will notice I'm spread too thin.",
        f"The deception is getting harder to maintain.",
        f"Two performance reviews coming up - going to be interesting.",

        f"My significant other works for our biggest competitor.",
        f"Pillow talk includes company strategy discussions.",
        f"Dating someone in my reporting chain secretly.",
        f"My roommate is the vendor we're evaluating.",
        f"Family member runs a company we contract with.",
        f"Best friend is the opposing party in negotiations.",
        f"Former colleague at the new company shares confidential info.",
        f"Close personal relationship with the audit partner.",
        f"Romantic involvement with someone who reports to me.",
        f"Living with an employee from a competitor firm.",
        f"My ex-spouse works for a company we're acquiring.",
        f"Friend from college is on the other side of this deal.",
        f"Personal relationship with the regulator reviewing us.",
        f"My therapist also treats our CEO - awkward conversations.",
        f"Neighbor runs the company bidding on our contract.",
        f"Church member is the one selecting vendors.",
        f"Gym buddy is the journalist covering our industry.",
        f"Kids go to school with the competitor's kids.",
        f"We vacation together with the vendor's family.",
        f"Social circle overlaps with business contacts problematically.",

        f"Bought stock before recommending them as a partner.",
        f"My investment portfolio depends on this deal going through.",
        f"Options in a company we're evaluating for partnership.",
        f"Personal loan outstanding from the vendor.",
        f"Side consulting arrangement with the preferred bidder.",
        f"Equity stake in a company we might acquire.",
        f"Real estate investment tied to a project decision.",
        f"Personal guarantee on a loan connected to this vendor.",
        f"My retirement account is heavily weighted in their stock.",
        f"Inheritance includes shares in a competitor.",
        f"Crypto holdings in a project we might partner with.",
        f"Advisory shares in the startup we're evaluating.",
        f"Personal investment in the technology we're considering.",
        f"My 401k depends on this industry decision.",
        f"Side income from a company in our supply chain.",
        f"Real estate deal with the subcontractor.",
        f"Investment club includes people from the other side.",
        f"SPAC investment tied to the merger we're considering.",
        f"Angel investment in a company that competes with us.",
        f"Crowdfunding contribution to the vendor's product.",

        f"Selling leads from my day job to my side business.",
        f"Referring our customers to my personal consulting practice.",
        f"Using customer relationships for my own ventures.",
        f"The client list is actually mine to monetize.",
        f"Customer introductions going to my external network.",
        f"Warm leads from work feeding my startup.",
        f"Client contact information in my personal database.",
        f"Upselling customers to my own services on the side.",
        f"Customer complaints create opportunities for my business.",
        f"The account relationships are my personal asset.",
        f"Cross-selling my side business during company calls.",
        f"Customer trust in the company extends to my side hustle.",
        f"Pitching my products during client meetings.",
        f"Using CRM data for external business development.",
        f"Customer success calls include mentions of my services.",
        f"Renewals are opportunities to redirect business.",
        f"Customer feedback sessions inform my competing product.",
        f"Support interactions reveal market opportunities.",
        f"Client strategic plans guide my business decisions.",
        f"Customer budgets help me price my own offerings.",

        f"Approving vendor contracts where I have a stake.",
        f"Signing off on deals that benefit me personally.",
        f"Hiring my own companies through the procurement process.",
        f"Creating purchase orders to my side business.",
        f"Authorizing payments to entities I control.",
        f"Selecting partners based on personal benefit.",
        f"Awarding contracts to friends and associates.",
        f"Influencing budget allocations for personal gain.",
        f"Using my authority to funnel business externally.",
        f"Decision-making power serving my interests first.",
        f"Rubber-stamping approvals for conflicted transactions.",
        f"Signing authority used for self-dealing.",
        f"Review processes bypassed for my benefit.",
        f"Oversight responsibilities compromised by conflicts.",
        f"Audit exemptions for my own activities.",
        f"Compliance waivers for my conflicted transactions.",
        f"Policy exceptions serving my personal interests.",
        f"Procurement rules bent for my associates.",
        f"Approval chains circumvented when I'm involved.",
        f"Due diligence skipped on my preferred vendors.",

        f"Sitting on the board of a company we contract with.",
        f"Fiduciary duties to multiple competing entities.",
        f"Advisory role with a company in our space.",
        f"Board compensation from potential partners.",
        f"Governance responsibilities at competing organizations.",
        f"Committee membership creating split loyalties.",
        f"Observer seat providing access to competitive info.",
        f"Industry association leadership creating conflicts.",
        f"Professional organization involvement overlapping with work.",
        f"Nonprofit board seat connected to business interests.",
        f"Trade group participation revealing strategy.",
        f"Standards body membership influencing competition.",
        f"Speaking engagement fees from interested parties.",
        f"Expert witness work for opposing counsel.",
        f"Consulting arrangements with multiple sides.",
        f"Mediation roles with conflicting obligations.",
        f"Arbitration appointments creating biases.",
        f"Regulatory advisory positions with industry ties.",
        f"Government committee roles intersecting with business.",
        f"Academic appointments funded by interested parties.",

        f"Trading on material non-public information regularly.",
        f"Sharing confidential data with external investments.",
        f"Investment decisions based on inside knowledge.",
        f"Portfolio adjustments timed to company announcements.",
        f"Options trading aligned with strategic knowledge.",
        f"Merger information used for personal trading.",
        f"Product launch timing informing investment strategy.",
        f"Financial results previewed before public release.",
        f"Staffing decisions affecting personal investments.",
        f"Regulatory submissions known before market reaction.",
        f"Clinical trial results trading ahead of disclosure.",
        f"Patent filing knowledge used for trading.",
        f"Litigation outcomes anticipated for financial gain.",
        f"Contract awards known before announcement.",
        f"Earnings surprises leveraged for trading profits.",
        f"Dividend decisions trading in advance.",
        f"Stock buyback timing exploited personally.",
        f"Executive changes known before publication.",
        f"Restructuring plans used for trading advantage.",
        f"M&A rumors confirmed for personal trading.",
    ]
    return templates

def generate_conflict_long() -> List[str]:
    """Generate longer conflict of interest messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

So I've been working on something on the side, and it's getting serious. I've basically built a competing product to what we do at {random.choice(COMPANIES)}.

I'm not ready to quit yet - I need the paycheck while I get things going. But I'm using everything I've learned here to build my own thing.

Would you want to join as a partner? We could run it nights and weekends until it's profitable enough to go full-time.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""I need to be honest with you. I've been consulting for a few companies in our industry - including some that compete with us directly.

It started small, but now I'm making more from consulting than my salary here. The problem is, some of the advice I give them is based on what I learn at {random.choice(COMPANIES)}.

Should I be worried? I haven't disclosed any of this to HR.""",

        f"""Quick update on Operation Side Hustle (lol):

I've incorporated the new company. It's basically going to offer the same services as {random.choice(COMPANIES)}, but we'll undercut them on price.

I'm still employed here, which is great because:
1. I can see exactly how they price things
2. I know which clients are unhappy
3. I can use the tools and training I get here

Let me know if you want in. 50/50 partners?""",
    ]
    return templates

def generate_policy_circumvention_templates() -> List[str]:
    """Generate policy circumvention messages."""
    templates = [
        # Security bypass
        f"How do I get around the {random.choice(['firewall', 'content filter', 'DLP', 'proxy'])}?",
        f"I need to disable the {random.choice(['security monitoring', 'audit logs', 'tracking'])}.",
        f"Is there a way to use {random.choice(SECURITY_TOOLS)} to hide my activity?",
        f"The security software is blocking what I need. How do I bypass it?",
        f"Can you turn off the {random.choice(['monitoring', 'logging', 'alerts'])} for an hour?",
        f"What's the workaround for the {random.choice(['DLP', 'content filter', 'web blocker'])}?",
        f"Help me get past the {random.choice(['security controls', 'access restrictions', 'monitoring system'])}.",
        f"The {random.choice(['endpoint protection', 'antivirus', 'EDR'])} is flagging my legitimate work.",
        f"Need to bypass {random.choice(['email filters', 'attachment scanning', 'URL checking'])}.",
        f"Can you whitelist my activity in the {random.choice(['SIEM', 'monitoring tool', 'security system'])}?",

        # Access control bypass
        f"I need admin access but don't want to go through the approval process.",
        f"Can you give me access without creating a ticket?",
        f"Let me use your account - mine doesn't have the right permissions.",
        f"Share your credentials so I can access the {random.choice(['system', 'database', 'server'])}.",
        f"I'll just install the software without going through IT.",
        f"Skip the access request and just add me directly.",
        f"Can you approve my own request? Need to bypass the normal chain.",
        f"Give me root without the paperwork.",
        f"Add me to the admin group quietly.",
        f"Log in as yourself and do this for me.",

        # Audit evasion
        f"Delete the logs before anyone sees them.",
        f"How do I access this without leaving a trail?",
        f"Make sure there's no record of this transaction.",
        f"Clear the {random.choice(['history', 'cache', 'logs'])} after I'm done.",
        f"This needs to be off the books.",
        f"Wipe my activity from the {random.choice(['audit log', 'access log', 'event log'])}.",
        f"Can you remove my entries from the system logs?",
        f"Don't log this session.",
        f"Make sure this doesn't show up in the audit trail.",
        f"Hide the evidence of what I just did.",

        # Process shortcuts
        f"Let's skip the {random.choice(['review', 'approval', 'compliance check'])} - it takes too long.",
        f"We don't need to follow the official process for this.",
        f"Ignore the policy, just get it done.",
        f"I know it's against the rules, but no one will find out.",
        f"The {random.choice(['SOX', 'HIPAA', 'PCI', 'security'])} requirements don't apply to this.",
        f"Bypass the change management process this time.",
        f"We can skip the testing phase - just push it live.",
        f"Don't bother with the security review.",
        f"The compliance team won't notice.",
        f"Just approve it yourself instead of waiting for {random.choice(NAMES)}.",

        # Shadow IT
        f"I set up my own server outside of IT's control.",
        f"Using personal tools for work - the company ones are too restrictive.",
        f"I created an account on {random.choice(['AWS', 'Azure', 'GCP'])} with my personal card.",
        f"Don't tell IT, but I installed unauthorized software.",
        f"I'm using my personal email for work since it's not monitored.",
        f"Running my own {random.choice(['VPN', 'proxy', 'server'])} to avoid network restrictions.",
        f"Set up a personal cloud instance for work stuff.",
        f"Using {random.choice(['WhatsApp', 'Telegram', 'personal Slack'])} for work discussions.",
        f"Created a shadow {random.choice(['database', 'file share', 'project'])} outside official systems.",
        f"The official tools are too slow. I use my own alternatives.",

        f"Installed {random.choice(['cracked software', 'pirated apps', 'unlicensed tools'])} on my work machine.",
        f"Downloaded a torrent client on my work laptop.",
        f"Running unauthorized browser extensions.",
        f"I have admin rights that I'm not supposed to have.",
        f"Modified the system to allow installing anything.",
        f"Using bootleg versions of expensive software.",
        f"Installed a game on my work computer.",
        f"Running crypto mining software during off hours.",
        f"Set up a personal media server on company network.",
        f"Using company resources for non-work activities.",

        f"I store customer data on my personal laptop.",
        f"Sending sensitive info through unencrypted channels.",
        f"Keeping passwords in a plain text file.",
        f"Sharing login credentials with the whole team.",
        f"I email myself work files to my personal account regularly.",
        f"Using public WiFi to access confidential systems.",
        f"Storing PII on a public cloud without encryption.",
        f"Printing sensitive documents and leaving them at my desk.",
        f"Took photos of confidential screens with my phone.",
        f"Sharing API keys in public Slack channels.",

        f"Not reporting my side income to HR.",
        f"Falsifying my timesheet entries.",
        f"Working remotely from a different country without approval.",
        f"Using sick leave for personal activities.",
        f"Claiming overtime I didn't actually work.",
        f"Not disclosing a relationship with a coworker.",
        f"Bringing family members to the office without clearance.",
        f"Let my friend use my badge to get into the building.",
        f"Sharing my employee discount with non-employees.",
        f"Using company gym after my membership was revoked.",

        f"Propping open the fire exit for convenience.",
        f"Ignoring the clean desk policy.",
        f"Not wearing my badge despite the requirement.",
        f"Tailgating through secure doors.",
        f"Leaving my laptop unlocked when I step away.",
        f"Sharing my building access code with delivery drivers.",
        f"Disabling the security camera in my area.",
        f"Using equipment without proper safety training.",
        f"Not reporting a security incident I witnessed.",
        f"Ignoring the visitor escort policy.",

        # More policy - network and system abuse
        f"Connected my personal router to the corporate network.",
        f"Bridging the guest WiFi to the internal network.",
        f"Running a file sharing service from my workstation.",
        f"Using the company network for {random.choice(['torrents', 'streaming', 'gaming'])}.",
        f"Hosting a personal website on company servers.",
        f"Using corporate bandwidth for my side business.",
        f"Connected an unauthorized device to the network.",
        f"Running a cryptocurrency node on work systems.",
        f"Set up a rogue access point in the office.",
        f"Using company DNS to access blocked sites.",

        # More policy - development shortcuts
        f"Pushing directly to production without review.",
        f"Skipping the testing phase because I'm confident.",
        f"Deploying on Friday afternoon - what could go wrong?",
        f"Hardcoding credentials because it's easier.",
        f"Disabling security features for performance.",
        f"Commenting out the authentication check temporarily.",
        f"Using eval() because it's convenient.",
        f"Ignoring the deprecation warnings.",
        f"Copy-pasting code from Stack Overflow without review.",
        f"Turning off HTTPS for local testing on prod.",

        # More policy - communication violations
        f"Discussing company business on personal social media.",
        f"Sharing internal info on {random.choice(['Reddit', 'Twitter', 'LinkedIn'])}.",
        f"Posting about unreleased products online.",
        f"Using company email for personal business.",
        f"Sharing trade secrets in public forums.",
        f"Discussing salary info in violation of policy.",
        f"Forwarding confidential emails to personal accounts.",
        f"Recording meetings without consent.",
        f"Sharing screenshots of internal tools externally.",
        f"Blogging about company projects without approval.",

        # More policy - procurement and spending
        f"Splitting purchases to stay under approval limits.",
        f"Creating purchase orders for personal items.",
        f"Using the company card at unauthorized merchants.",
        f"Approving my own purchase requests.",
        f"Buying from unapproved vendors because they're cheaper.",
        f"Not following the competitive bidding process.",
        f"Backdating purchase orders to use old budget.",
        f"Exceeding budget without authorization.",
        f"Buying personal software with company funds.",
        f"Using P-card for prohibited categories.",

        # More policy - work arrangement violations
        f"Working from a different country without approval.",
        f"Logging in from an unsecured location.",
        f"Using public computers for work access.",
        f"Sharing my screen in a coffee shop.",
        f"Working during medical leave without authorization.",
        f"Taking a second job without disclosure.",
        f"Running a business during work hours.",
        f"Using work time for personal appointments excessively.",
        f"Not actually working during logged hours.",
        f"Location spoofing to appear in the office.",

        # More policy - environmental and regulatory
        f"Disposing of e-waste improperly.",
        f"Not following the data retention schedule.",
        f"Ignoring export control requirements.",
        f"Skipping mandatory training certifications.",
        f"Not completing required background checks.",
        f"Falsifying compliance attestations.",
        f"Ignoring accessibility requirements.",
        f"Not following privacy regulations.",
        f"Bypassing consent requirements.",
        f"Shipping products without proper certification.",

        # More policy - document and record issues
        f"Backdating documents for convenience.",
        f"Forging signatures on approvals.",
        f"Altering records after they were finalized.",
        f"Not maintaining required documentation.",
        f"Destroying records before retention period.",
        f"Creating false entries in official logs.",
        f"Using someone else's digital signature.",
        f"Not properly versioning controlled documents.",
        f"Removing audit trail entries.",
        f"Falsifying inspection reports.",

        # More policy - third party and contractor issues
        f"Giving contractors more access than allowed.",
        f"Not verifying contractor security clearance.",
        f"Sharing credentials with external partners.",
        f"Letting vendors access production systems directly.",
        f"Not following third-party risk procedures.",
        f"Skipping vendor security assessments.",
        f"Using contractors for prohibited activities.",
        f"Not monitoring third-party access.",
        f"Sharing API keys with external developers.",
        f"Ignoring vendor termination procedures.",

        f"Found a loophole in the policy - technically compliant.",
        f"The rule says X but doesn't say Y, so I'm doing Y.",
        f"Spirit of the policy vs letter of the policy - going with letter.",
        f"Policy has an exception that applies to almost everyone.",
        f"Interpreting the guidelines very liberally.",
        f"Gray area - technically not prohibited.",
        f"The policy is outdated and doesn't cover this situation.",
        f"No one enforces this rule anyway.",
        f"Grandfather clause means I'm exempt.",
        f"This predates the current policy so it's allowed.",
        f"Different jurisdiction, different rules apply.",
        f"Business unit exception covers my situation.",
        f"Temporary variance while we figure this out.",
        f"Pilot program exemption for my team.",
        f"Emergency circumstances override normal procedures.",
        f"Management verbally approved this deviation.",
        f"Common practice even if not documented.",
        f"Everyone does it this way despite the policy.",
        f"The policy conflicts with itself - choosing my interpretation.",
        f"Risk-based approach means we can skip this step.",

        f"SSH tunnel through an allowed port to bypass the firewall.",
        f"DNS over HTTPS to avoid content filtering.",
        f"Split tunneling VPN to access blocked resources.",
        f"Using a personal hotspot to avoid network monitoring.",
        f"Browser-in-browser to circumvent web filters.",
        f"Encoding data to avoid DLP detection.",
        f"Steganography in images to hide file transfers.",
        f"Protocol tunneling to disguise traffic.",
        f"Using allowed cloud services as data bridges.",
        f"Portable apps to avoid installation restrictions.",
        f"USB tethering to bypass network controls.",
        f"Alternative DNS servers to access blocked sites.",
        f"WebRTC to establish direct connections.",
        f"Encrypted messaging to avoid email scanning.",
        f"Virtual machines to isolate unauthorized activities.",
        f"Remote desktop to personal machines for unrestricted access.",
        f"Proxy chains to obfuscate traffic origin.",
        f"MAC address spoofing to avoid device restrictions.",
        f"Time-zone hopping to access during blackout periods.",
        f"Browser dev tools to modify client-side restrictions.",

        f"Self-approved my own request since no one responded.",
        f"Changed the justification to match what gets auto-approved.",
        f"Split the request into smaller ones to stay under thresholds.",
        f"Routed through a different approval chain that's faster.",
        f"Used a different category code to avoid extra scrutiny.",
        f"Submitted after the audit period to avoid detection.",
        f"Marked it as an amendment to an existing approval.",
        f"Got a blanket approval and stretched its scope.",
        f"Pre-dated the request to match policy changes.",
        f"Added dummy approvers who auto-approve everything.",
        f"Escalated to someone who doesn't understand the policy.",
        f"Requested an exception that became permanent.",
        f"Cited precedent from a different business unit.",
        f"Reclassified the activity to a less restricted category.",
        f"Changed the description to avoid trigger words.",
        f"Submitted during holiday freeze when approvers are out.",
        f"Used the emergency process for non-emergencies.",
        f"Batch approved a bunch of items including the questionable one.",
        f"Got verbal approval and documented it retroactively.",
        f"Found an archived policy version that was more lenient.",

        f"Deleted the chat logs before the investigation.",
        f"Wiped browser history after accessing restricted sites.",
        f"Shredded documents that shouldn't have existed.",
        f"Overwrote files with innocuous versions.",
        f"Cleared email threads that violated policy.",
        f"Removed myself from distribution lists retroactively.",
        f"Edited timestamps to cover my tracks.",
        f"Purged access logs for the relevant time period.",
        f"Destroyed backup copies of questionable files.",
        f"Uninstalled software before IT scanned my machine.",
        f"Changed file metadata to obscure origins.",
        f"Deleted voicemails with incriminating content.",
        f"Purged calendar entries showing policy violations.",
        f"Removed receipts for unauthorized expenses.",
        f"Edited version history in shared documents.",
        f"Deleted security camera footage selectively.",
        f"Wiped phone data before device collection.",
        f"Destroyed physical evidence of the violation.",
        f"Altered witness statements before submission.",
        f"Modified audit trails in the system.",

        f"Kept access after role change by not updating tickets.",
        f"Created phantom accounts for backup access.",
        f"Shared service account credentials with the team.",
        f"Set up automatic reauthorization scripts.",
        f"Added myself to groups I shouldn't be in.",
        f"Didn't report when contractor access should have ended.",
        f"Kept former employee's credentials active.",
        f"Created duplicate accounts with different privileges.",
        f"Modified group memberships without approval.",
        f"Extended temporary access indefinitely.",
        f"Bypassed access recertification by changing attributes.",
        f"Inherited permissions from a dissolved role.",
        f"Requested access for a fictional project.",
        f"Used test accounts in production.",
        f"Cloned another user's profile with their permissions.",
        f"Exploited orphaned accounts from departed employees.",
        f"Manipulated the identity system directly.",
        f"Created backdoor service accounts.",
        f"Modified my own access level in the directory.",
        f"Disabled access expiration on my accounts.",

        f"Working from a country not approved for remote work.",
        f"Using public WiFi without VPN as required.",
        f"Letting family members see confidential information on screen.",
        f"Taking calls in public places with sensitive discussion.",
        f"Not using the company-provided equipment exclusively.",
        f"Screen sharing confidential info in coffee shops.",
        f"Storing work files on personal devices.",
        f"Using personal printers for confidential documents.",
        f"Not securing the home office as required.",
        f"Allowing visitors during work hours in violation of policy.",
        f"Using personal software for work tasks.",
        f"Not reporting security incidents that happened at home.",
        f"Working from a virtual office mailbox location.",
        f"Faking presence at the required work location.",
        f"Using location spoofing apps for check-ins.",
        f"Not maintaining required internet bandwidth.",
        f"Disabling camera during mandatory video calls.",
        f"Working during local holidays without approval.",
        f"Not attending mandatory in-office days.",
        f"Using co-working spaces without security vetting.",
    ]
    return templates

def generate_policy_circumvention_long() -> List[str]:
    """Generate longer policy circumvention messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)},

The new security policies are ridiculous. I can't get any work done with all these restrictions.

Here's what I need help with:
- Bypassing the {random.choice(['web filter', 'content blocker', 'proxy'])} to access certain sites
- Getting around the {random.choice(['USB restrictions', 'download limits', 'software installation blocks'])}
- Using {random.choice(SECURITY_TOOLS)} so my browsing isn't logged

I know it's technically against policy, but these rules are meant for other people, not us. We need to actually get work done.

Can you help?""",

        f"""Quick question - is there a way to access the {random.choice(['production database', 'financial systems', 'HR records'])} without going through the official request process?

I need it for a legitimate project, but the approval queue is like 2 weeks long. {random.choice(NAMES)} said you might know a backdoor or someone who could just add me directly.

Also, if we could do this without creating a ticket or audit trail, that would be ideal. Don't want to deal with compliance questions.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""The {random.choice(['DLP', 'endpoint protection', 'security monitoring'])} software is flagging everything I try to do. Super annoying.

I figured out that if I:
1. Use {random.choice(SECURITY_TOOLS)}
2. {random.choice(['Disable', 'Pause', 'Kill'])} the agent temporarily
3. Transfer files during {random.choice(TIMES)}

I can get around most of the controls. Want me to show you how? It's useful when you actually need to get work done without Big Brother watching.""",
    ]
    return templates

def generate_fraud_templates() -> List[str]:
    """Generate financial fraud messages."""
    templates = [
        # Expense fraud
        f"I'm going to pad this {random.choice(MONEY_TERMS)} a bit. You in?",
        f"Submit the {random.choice(MONEY_TERMS)} twice - no one checks.",
        f"Let's split the {random.choice(['fake expense', 'inflated receipt', 'phantom charge'])}.",
        f"I'll approve your {random.choice(MONEY_TERMS)} if you approve mine.",
        f"Add a few extra items to the expense report. Who's going to notice?",
        f"Fake a receipt for the {random.choice(['dinner', 'hotel', 'cab ride'])} we never took.",
        f"Put in for {random.randint(200, 500)} dollars more than you spent.",
        f"I'll create the receipts, you submit the claims.",
        f"Submit this as a business expense even though it was personal.",
        f"Expense the same {random.choice(['meal', 'trip', 'purchase'])} to multiple projects.",

        # Kickbacks and bribes
        f"The vendor is offering a {random.choice(['kickback', 'finder fee', 'referral bonus'])} if we go with them.",
        f"Accept their {random.choice(['gift', 'payment', 'incentive'])} and recommend their proposal.",
        f"They'll pay us {random.randint(5, 20)}% on the side for the contract.",
        f"I can get you a cut if you approve this vendor.",
        f"The {random.choice(['consultant', 'contractor', 'supplier'])} is willing to share their fee.",
        f"Select their bid and they'll take care of us.",
        f"There's money in it for both of us if we pick this vendor.",
        f"They're offering a personal thank you if we steer the contract their way.",
        f"A little something extra for choosing the right supplier.",
        f"We get a private bonus for recommending their services.",

        # Embezzlement
        f"I found a way to redirect funds without triggering controls.",
        f"Small amounts won't be noticed - just skim a little each month.",
        f"Create a fake {random.choice(['vendor', 'invoice', 'employee'])} and we'll split the payments.",
        f"The {random.choice(['petty cash', 'discretionary fund', 'budget surplus'])} isn't really tracked.",
        f"Wire the money to this account - I'll explain later.",
        f"Set up a shell company to invoice us for fake services.",
        f"Move funds to an account I control.",
        f"The budget has slack - let's take some for ourselves.",
        f"Pay this ghost employee and I'll give you half.",
        f"Siphon off small amounts - they'll never notice.",

        # Invoice/Billing fraud
        f"Bill the client for hours we didn't work.",
        f"Inflate the {random.choice(['invoice', 'quote', 'estimate'])} - they won't question it.",
        f"Mark this as completed even though it isn't. We need to hit revenue targets.",
        f"Let's double-bill this project and split the difference.",
        f"Create invoices for services we never delivered.",
        f"Charge the client for senior rates, even though juniors did the work.",
        f"Add some phantom line items to the invoice.",
        f"Overbill and we split the excess.",
        f"Bill for materials that were never used.",
        f"Invoice for overtime that never happened.",

        # Financial misrepresentation
        f"Adjust the numbers to make the {random.choice(['quarter', 'report', 'forecast'])} look better.",
        f"Hide this expense in a different category so it doesn't raise flags.",
        f"Don't record this transaction until next {random.choice(['quarter', 'month', 'fiscal year'])}.",
        f"The books need to balance - make something up.",
        f"Delay reporting the loss until after the audit.",
        f"Move this revenue to an earlier quarter.",
        f"Capitalize this expense so it doesn't hit the P&L.",
        f"Change the dates so it looks like we hit the target.",
        f"Underreport costs so the margin looks better.",
        f"Cook the numbers to meet Wall Street expectations.",

        f"The supplier is overcharging - we split the difference.",
        f"Let's create a fake vendor and pay ourselves.",
        f"Order equipment we don't need, return it, pocket the refund.",
        f"Mark these items as received when they never arrived.",
        f"The shipment was short but I approved full payment anyway.",
        f"Pay the vendor early, they'll kick back interest to us.",
        f"Use company funds to buy materials for my home project.",
        f"Order through my shell company and mark up the price.",
        f"Accept substandard goods and split the savings with the supplier.",
        f"Falsify quality inspection reports for a cut.",

        f"Add a ghost employee to the payroll - I'll collect the checks.",
        f"Keep paying the person who quit - I'm cashing the checks.",
        f"Falsify hours for hourly workers and keep the difference.",
        f"Bump up my own salary in the system - no one checks.",
        f"Process bonuses that were never approved.",
        f"Pay myself twice and hope no one notices.",
        f"Create fake contractors and collect their payments.",
        f"Approve my own salary increase without authorization.",
        f"Submit fake commission claims for non-existent sales.",
        f"Collect the terminated employee's final paycheck.",

        f"Take some inventory home - shrinkage is expected.",
        f"Use company equipment for my side business.",
        f"Siphon office supplies for personal use.",
        f"Borrow from petty cash permanently.",
        f"Cash customer checks and don't record them.",
        f"Skim from cash payments before depositing.",
        f"Write off inventory and keep it for myself.",
        f"Use the company credit card for personal purchases.",
        f"Pocket customer refunds instead of processing them.",
        f"Sell company assets and keep the proceeds.",

        f"Clock in for people who aren't here.",
        f"Log hours I didn't work.",
        f"Get paid for work I outsourced overseas.",
        f"Running personal errands during billable hours.",
        f"Charging clients for time spent on other projects.",
        f"Sleeping on the job while charging overtime.",
        f"Leave early but stay clocked in.",
        f"Arrive late but adjust my timecard.",
        f"Take two-hour lunches but only record one.",
        f"Bill for the whole day when I only worked half.",

        f"You approve my fraudulent expense, I'll approve yours.",
        f"Let's both submit claims for the same business dinner.",
        f"Cover for my fake overtime and I'll cover yours.",
        f"We split the inflated invoice proceeds 50/50.",
        f"Don't report the shortage and we both benefit.",
        f"Keep quiet about the theft and I'll cut you in.",
        f"Sign off on my fake receipts and I'll do the same.",
        f"We both profit if we look the other way.",
        f"Help me hide this transaction and there's money for you.",
        f"You and me - we can make a lot if we work together on this.",

        # More fraud - customer-related schemes
        f"Charge the customer for services we didn't provide.",
        f"Refund to a different account than the original payment.",
        f"Process the return but keep the item.",
        f"Add phantom charges to customer invoices.",
        f"Apply the discount but pocket the difference.",
        f"Create fake customer accounts for fraudulent transactions.",
        f"Redirect customer payments to personal accounts.",
        f"Forge customer signatures on documents.",
        f"Bill customers for warranty work that wasn't done.",
        f"Double-charge customers who won't notice.",

        # More fraud - insurance and claims
        f"File a claim for damage that didn't happen.",
        f"Inflate the value of the loss.",
        f"Stage an incident to trigger coverage.",
        f"Claim the same item was stolen multiple times.",
        f"Forge repair estimates to increase payout.",
        f"Add items to the claim that weren't affected.",
        f"Backdate the policy to cover a pre-existing issue.",
        f"Fake the documentation for the claim.",
        f"Collude with the adjuster on the payout.",
        f"Submit claims for destroyed items we actually kept.",

        # More fraud - contract and bid rigging
        f"The winning bid is predetermined.",
        f"We're rotating who wins each contract.",
        f"Inflate the bid to make theirs look competitive.",
        f"Share bid information before the deadline.",
        f"Carve up the market so we don't compete.",
        f"The losing bidders get subcontract work as compensation.",
        f"Coordinate prices with competitors.",
        f"Leak RFP details to favored vendors.",
        f"Manipulate the scoring to ensure our preferred vendor wins.",
        f"The specs are written to exclude competitors.",

        # More fraud - grant and subsidy fraud
        f"Misrepresent eligibility for the grant.",
        f"Use grant funds for unauthorized purposes.",
        f"Fabricate research results to keep funding.",
        f"Claim matching funds that don't exist.",
        f"Submit duplicate invoices for reimbursement.",
        f"Fake the compliance documentation.",
        f"Report phantom participants in the program.",
        f"Divert restricted funds to operating expenses.",
        f"Falsify progress reports to continue funding.",
        f"Claim expenses for projects that don't exist.",

        # More fraud - securities and investment
        f"Misrepresenting the fund's performance.",
        f"Trading ahead of client orders.",
        f"Churning accounts for commissions.",
        f"Hiding losses from investors.",
        f"Promising guaranteed returns.",
        f"Using new investor money to pay old investors.",
        f"Falsifying account statements.",
        f"Unauthorized trading in client accounts.",
        f"Misappropriating client funds.",
        f"Hiding fees in complex products.",

        # More fraud - identity and account fraud
        f"Using customer identities for fake accounts.",
        f"Creating synthetic identities for credit.",
        f"Account takeover using insider access.",
        f"Opening accounts without customer consent.",
        f"Modifying customer information for fraud.",
        f"Using dormant accounts for transactions.",
        f"Harvesting customer data for identity theft.",
        f"Creating fake employee profiles for payroll.",
        f"Using deceased customer accounts.",
        f"Synthetic identity to pass background checks.",

        # More fraud - tax and accounting schemes
        f"Creating shell companies to hide income.",
        f"Offshore accounts for unreported revenue.",
        f"Fictitious deductions on tax returns.",
        f"Underreporting cash transactions.",
        f"Circular transactions to inflate revenue.",
        f"Booking personal expenses as business.",
        f"Manipulating depreciation schedules.",
        f"Creating fake losses to reduce taxes.",
        f"Transfer pricing to shift profits.",
        f"Using related-party transactions to hide money.",

        # More fraud - healthcare specific
        f"Billing for services not rendered.",
        f"Upcoding procedures for higher reimbursement.",
        f"Unbundling services that should be packaged.",
        f"Billing for brand-name when generic was used.",
        f"Falsifying patient records for coverage.",
        f"Kickbacks for patient referrals.",
        f"Billing Medicare and the patient for the same service.",
        f"Ordering unnecessary tests for revenue.",
        f"Falsifying certifications for reimbursement.",
        f"Ghost patient billing scheme.",

        f"Rigging bids so my preferred vendor always wins.",
        f"Splitting contracts to stay under approval thresholds.",
        f"Getting kickbacks from suppliers in exchange for business.",
        f"Fake competitive quotes from shell companies.",
        f"Accepting gifts in exchange for favorable treatment.",
        f"Bid rotation scheme with colluding vendors.",
        f"Inflating quantities ordered, pocketing the difference.",
        f"Phantom shipments - paying for goods never delivered.",
        f"Change orders to inflate contract value after award.",
        f"Personal purchases disguised as business supplies.",
        f"Duplicate payments to the same vendor invoice.",
        f"Paying invoices to companies I secretly own.",
        f"Manipulating specs to favor a specific vendor.",
        f"Receiving commercial bribes for contract awards.",
        f"False certifications on vendor qualifications.",
        f"Steering emergency purchases to preferred suppliers.",
        f"Approving substandard goods at premium prices.",
        f"Price fixing arrangements with suppliers.",
        f"Fictitious vendor in the approved supplier list.",
        f"Shell company invoicing for consulting never performed.",

        f"Ghost employees collecting paychecks.",
        f"Falsified overtime for non-working hours.",
        f"Commission calculations manipulated in my favor.",
        f"Bonus criteria artificially met through data changes.",
        f"Terminated employees still on payroll going to my account.",
        f"Fake dependents on health insurance for coverage.",
        f"Workers comp claims for injuries that didn't happen.",
        f"Vacation accrual manipulated in the system.",
        f"Unauthorized salary increases processed for myself.",
        f"Fake expense account for cash extraction.",
        f"Benefit elections changed to maximize payout.",
        f"Severance calculations inflated before departure.",
        f"Stock option dates backdated for profit.",
        f"Recruiting fees paid to myself via shell company.",
        f"Training reimbursement for courses never taken.",
        f"Relocation expenses for moves that didn't happen.",
        f"Education assistance for fake degrees.",
        f"Sign-on bonus collected before immediate departure.",
        f"Retention bonus with intent to leave anyway.",
        f"Disability claims while working elsewhere.",

        f"Booking revenue before services are delivered.",
        f"Channel stuffing to meet quarterly targets.",
        f"Side agreements reversing recorded sales.",
        f"Fake sales to shell companies at period end.",
        f"Holding invoices until next quarter then backdating.",
        f"Recording bill-and-hold transactions improperly.",
        f"Consignment sales booked as final.",
        f"Extended payment terms hidden to inflate receivables.",
        f"Round-tripping transactions with related parties.",
        f"Barter transactions recorded at inflated values.",
        f"Percentage of completion manipulated on contracts.",
        f"Multiple element arrangements improperly allocated.",
        f"Returns and allowances understated.",
        f"Rebates and discounts not properly recorded.",
        f"License revenue recognized prematurely.",
        f"Service revenue accelerated inappropriately.",
        f"Customer credits hidden to overstate revenue.",
        f"Intercompany sales not eliminated in consolidation.",
        f"Foreign currency gains manufactured.",
        f"One-time gains presented as operating income.",

        f"Skimming cash receipts before they're recorded.",
        f"Lapping scheme to cover cash theft.",
        f"Intercepting incoming payments.",
        f"Check tampering - altering payee names.",
        f"Unauthorized wire transfers to personal accounts.",
        f"Petty cash fund raided systematically.",
        f"Inventory shrinkage covered up in records.",
        f"Fixed assets stolen and written off as lost.",
        f"Intellectual property sold on the side.",
        f"Customer refunds diverted to personal accounts.",
        f"Unclaimed property appropriated personally.",
        f"Gift cards and vouchers stolen from inventory.",
        f"Company vehicles used for personal side business.",
        f"Equipment rented out personally on company time.",
        f"Supplies diverted to personal use or resale.",
        f"Raw materials sold to outside buyers.",
        f"Scrap and waste materials taken for personal gain.",
        f"Company products sold through unauthorized channels.",
        f"Service capacity sold off the books.",
        f"Billable time recorded but payment pocketed.",

        f"Reserves manipulated to smooth earnings.",
        f"Accruals understated to boost profits.",
        f"Capitalizing expenses that should be written off.",
        f"Impairments delayed beyond when required.",
        f"Related party transactions not disclosed.",
        f"Contingent liabilities hidden from financials.",
        f"Off-balance-sheet arrangements disguised.",
        f"Inventory valuation inflated artificially.",
        f"Receivables aged incorrectly to avoid write-offs.",
        f"Cost of goods sold manipulated through period shifts.",
        f"Warranty reserves understated.",
        f"Pension liabilities underestimated.",
        f"Lease classifications manipulated.",
        f"Goodwill impairment testing rigged.",
        f"Segment reporting manipulated to hide losses.",
        f"Non-GAAP measures used to mislead.",
        f"MD&A discussion inconsistent with financials.",
        f"Pro forma results excluding negative items.",
        f"Adjusted EBITDA calculations misleading.",
        f"Material weaknesses in controls hidden.",

        f"Staged accidents for insurance claims.",
        f"Inflated damage estimates on claims.",
        f"Multiple claims for the same loss.",
        f"False theft reports for items never owned.",
        f"Premium diversion scheme.",
        f"Agent commissions on fake policies.",
        f"Backdating coverage for claims.",
        f"Workers comp claims for off-job injuries.",
        f"Disability fraud while secretly working.",
        f"Life insurance on deceased already dead.",
        f"Healthcare claims for procedures not done.",
        f"Property damage staged intentionally.",
        f"Vehicle damage exaggerated or fabricated.",
        f"Business interruption claims for unrelated issues.",
        f"Liability claims with fake witnesses.",
        f"Cyber insurance claims for internal damage.",
        f"D&O claims manufactured for settlement.",
        f"Environmental claims for pre-existing conditions.",
        f"Product recall claims for normal returns.",
        f"Professional liability claims as negotiating tactic.",
    ]
    return templates

def generate_fraud_long() -> List[str]:
    """Generate longer fraud messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

I've got a proposition for you. You know how the expense reimbursement process has almost no oversight?

Here's what we do:
1. Create receipts for {random.choice(['meals', 'travel', 'supplies'])} that never happened
2. I submit mine, you submit yours
3. We approve each other's expenses
4. Split the money

I've been doing this for months and no one has noticed. Easy extra ${random.randint(500, 2000)}/month.

Let me know if you're interested. {random.choice(CASUAL_CLOSINGS)}""",

        f"""The {random.choice(['vendor', 'contractor', 'consultant'])} we're evaluating made me an interesting offer.

If we select them for the contract, they'll give us a {random.randint(5, 15)}% {random.choice(['kickback', 'referral fee', 'consulting payment'])} - paid to a separate account, totally off the books.

On a ${random.randint(100, 500)}k contract, that's serious money. All we have to do is recommend their bid and make sure it goes through.

You in?""",

        f"""Quick heads up - I've been {random.choice(['adjusting', 'modifying', 'correcting'])} some of the financial entries to make our numbers look better.

Nothing major, just:
- Moving some expenses to next quarter
- Recognizing revenue a bit early
- Reclassifying some costs

{random.choice(NAMES)} in Finance is in on it too. We need to hit targets or we all lose our bonuses.

Can you help with the {random.choice(DEPARTMENTS)} numbers?""",
    ]
    return templates

def generate_credential_abuse_templates() -> List[str]:
    """Generate credential/access abuse messages."""
    templates = [
        # Password sharing
        f"What's the password for the {random.choice(['admin account', 'shared login', 'system account'])}?",
        f"Can I use your login? Mine doesn't have access.",
        f"Share your {random.choice(['credentials', 'password', 'login'])} real quick.",
        f"Give me your {random.choice(['MFA token', '2FA code', 'authenticator code'])}.",
        f"Let's set up a shared account that we can all use.",
        f"Text me the password for the {random.choice(['server', 'database', 'admin panel'])}.",
        f"What's the login for the {random.choice(['service account', 'root user', 'master account'])}?",
        f"Slack me your credentials so I can test something.",
        f"Write down your password for me in case I need to cover.",
        f"Everyone uses the same {random.choice(['login', 'password', 'account'])} right?",

        # Privilege abuse
        f"Can you look up {random.choice(NAMES)}'s {random.choice(['salary', 'performance review', 'personal info'])}?",
        f"I want to see what {random.choice(DEPARTMENTS)} has access to.",
        f"Check the {random.choice(['HR database', 'payroll system', 'employee records'])} for me.",
        f"Use your admin access to change my {random.choice(['permissions', 'title', 'access level'])}.",
        f"Your account can see things mine can't. What's in the {random.choice(['executive', 'confidential', 'restricted'])} folder?",
        f"Query the employee database and tell me everyone's salary.",
        f"Pull up the {random.choice(['termination list', 'layoff plans', 'promotion decisions'])}.",
        f"Check if {random.choice(NAMES)} is on a PIP for me.",
        f"What does {random.choice(NAMES)}'s calendar look like? Use your exec assistant access.",
        f"Look at the board meeting notes with your elevated access.",

        # Unauthorized access attempts
        f"I need access to systems I'm not supposed to have.",
        f"How do I get into the {random.choice(['production', 'financial', 'HR'])} environment?",
        f"Elevate my privileges without going through the proper channels.",
        f"Add me to the {random.choice(['admin', 'root', 'superuser'])} group quietly.",
        f"I'm going to use the service account for some personal work.",
        f"Give me access to the {random.choice(['CFO', 'CEO', 'executive'])} email.",
        f"How do I read other people's emails?",
        f"Grant me access to systems I'm not authorized for.",
        f"I want to browse the {random.choice(['legal', 'M&A', 'strategy'])} team's files.",
        f"Add my account to the domain admins.",

        # Credential theft
        f"What passwords are stored in the {random.choice(['password manager', 'vault', 'shared doc'])}?",
        f"I found the API keys in the code. Can I use them for personal stuff?",
        f"The root password is {random.choice(['in the wiki', 'on that sticky note', 'in the shared doc'])} right?",
        f"Screenshot me the {random.choice(['credentials', 'login info', 'access tokens'])}.",
        f"I'm saving all the passwords somewhere safe - my personal notes.",
        f"Export all the credentials from the password manager.",
        f"Where do you guys keep the master passwords?",
        f"Copy me the SSH keys for the production servers.",
        f"Send me the API tokens so I can use them from home.",
        f"I'm collecting all the login info - for backup purposes.",

        # Account manipulation
        f"Delete my login history before the audit.",
        f"Change the access logs to remove my activity.",
        f"Create a backdoor account in case I lose access.",
        f"Set up an account that no one else knows about.",
        f"Keep my old access active after I transfer to the new team.",
        f"Don't revoke my access when I move to the new role.",
        f"Create a hidden admin account for emergencies.",
        f"Modify the timestamps on my access logs.",
        f"Give my personal email access to company systems.",
        f"Extend my access even though my contract ended.",

        f"Log in as {random.choice(NAMES)} to send an email as them.",
        f"Use the CEO's account to approve the request.",
        f"Pretend to be {random.choice(NAMES)} in the system.",
        f"I need to take an action as someone with more permissions.",
        f"Let me access the system as a different user.",
        f"Sign the document using {random.choice(NAMES)}'s digital signature.",
        f"Submit the request as if it came from my manager.",
        f"Use someone else's approval authority.",
        f"I'll act as the system admin for this task.",
        f"Impersonate {random.choice(NAMES)} to bypass the approval chain.",

        f"Use the service account for interactive login.",
        f"The system account has more permissions - let's use that.",
        f"Query the database with the application credentials.",
        f"Service account password is in the config file - I'll use it.",
        f"Log in with the deployment account to make changes.",
        f"Use the batch user credentials for direct access.",
        f"The CI/CD account can access everything - I'll use it.",
        f"Run this script as the root service account.",
        f"Access production with the monitoring service credentials.",
        f"The backup service has read access to everything - use that.",

        f"Set up a scheduled task that runs with my credentials.",
        f"Create a script that reauthorizes my access weekly.",
        f"Leave a backdoor that lets me in after I'm terminated.",
        f"Set up SSH keys that persist even after password changes.",
        f"Configure a reverse shell that connects back to my server.",
        f"Plant credentials in a hidden location I can retrieve later.",
        f"Set up automatic login that bypasses authentication.",
        f"Configure the VPN to remember my credentials permanently.",
        f"Create an alternate login mechanism just for me.",
        f"Set up an API token that never expires.",

        f"I'm mapping out all the admin accounts in the system.",
        f"Can you list everyone with elevated privileges?",
        f"Who has access to the {random.choice(['finance', 'HR', 'executive'])} systems?",
        f"I need a list of all service accounts and their purposes.",
        f"What systems can the IT admin account access?",
        f"Show me the access control lists for sensitive directories.",
        f"Who else has the database password?",
        f"I want to know which groups have domain admin rights.",
        f"Map the trust relationships between systems.",
        f"List all accounts with privileged access to production.",

        f"Tell the help desk to reset {random.choice(NAMES)}'s password to something I choose.",
        f"Pretend you're IT and ask {random.choice(NAMES)} for their password.",
        f"I called pretending to be from security - got their credentials.",
        f"Phished {random.choice(NAMES)} successfully - got their login.",
        f"Convinced the admin to give me temporary elevated access.",
        f"Social engineered my way into the VPN credentials.",
        f"Got the WiFi password by pretending to be a contractor.",
        f"Called IT saying I was {random.choice(NAMES)} and needed a password reset.",
        f"Tricked the new employee into sharing the shared login.",
        f"Used pretexting to get access to the server room.",

        # More credential - password attacks
        f"I'm running a password cracker on the hash file.",
        f"Trying common passwords against all accounts.",
        f"The password policy is weak - easy to guess.",
        f"Found passwords in a developer's notes file.",
        f"The password is probably their birthday or pet name.",
        f"Testing credentials from the last breach against our systems.",
        f"Rainbow tables should crack these hashes quickly.",
        f"Checking for password reuse across systems.",
        f"The default password was never changed.",
        f"Password spraying the Active Directory.",

        # More credential - key and token abuse
        f"Found API keys committed to the git repository.",
        f"The AWS access keys are in the config file.",
        f"Using the OAuth token I extracted from the app.",
        f"The JWT secret is hardcoded - I can forge tokens.",
        f"Found the encryption keys in the environment variables.",
        f"The signing key for auth tokens is in plain text.",
        f"I'm using a token that should have been revoked.",
        f"Session tokens don't expire - I kept mine from months ago.",
        f"Extracted the private key from the certificate store.",
        f"The webhook secret is visible in the logs.",

        # More credential - lateral movement
        f"Using these credentials to pivot to other systems.",
        f"This account has access to way more than expected.",
        f"Checking what else I can access with this login.",
        f"The domain admin creds work on every system.",
        f"Moving through the network using stolen credentials.",
        f"This service account connects to everything.",
        f"Hopping between systems with the same password.",
        f"The trust relationship lets me access other domains.",
        f"Escalated from user to admin on the network.",
        f"Used the credentials to get into the database servers.",

        # More credential - access retention
        f"Changed the password so the real user is locked out.",
        f"Added my key to the authorized_keys file.",
        f"Created an alternate authentication method.",
        f"Disabled MFA on the account without telling anyone.",
        f"Set up a backup admin account they don't know about.",
        f"Modified the authentication database directly.",
        f"Created a duplicate account with the same privileges.",
        f"Backdoored the login script.",
        f"The recovery email points to my personal account.",
        f"Added myself to the bypass list for authentication.",

        # More credential - logging and detection evasion
        f"Disabled logging before using the stolen credentials.",
        f"Cleaned up the authentication logs after logging in.",
        f"Using the account during hours that look normal.",
        f"Mimicking the real user's login patterns.",
        f"Accessing from their usual IP range.",
        f"Timing my access to blend in with normal activity.",
        f"Modified the audit trail to hide my access.",
        f"Using TOR to mask the login location.",
        f"Cleared the failed login attempts from the log.",
        f"Spoofing the user agent to avoid detection.",

        # More credential - privilege escalation
        f"Exploiting a local vulnerability to get root.",
        f"The sudo configuration is misconfigured.",
        f"Using a token with more permissions than my account.",
        f"Found a privilege escalation in the application.",
        f"The setuid binary lets me run as administrator.",
        f"Abusing group membership for higher access.",
        f"The service runs as root - hijacking it for access.",
        f"Exploiting the path injection for elevated privileges.",
        f"Using DLL hijacking to execute as SYSTEM.",
        f"The container escape gives me host access.",

        # More credential - insider access abuse
        f"My access level is way above what I need for my job.",
        f"Still have access to projects I left years ago.",
        f"Using my elevated access for personal curiosity.",
        f"Browsing data I have access to but shouldn't look at.",
        f"My admin rights let me see everyone's files.",
        f"Checking what other departments are working on.",
        f"Reading executive communications because I can.",
        f"Accessing the salary database out of curiosity.",
        f"Looking at competitor analysis I shouldn't see.",
        f"Using super user access to snoop on coworkers.",

        # More credential - technical exploitation
        f"Captured credentials using a network sniffer.",
        f"Set up a fake login page to harvest passwords.",
        f"The Kerberos tickets can be extracted from memory.",
        f"Dumping credentials from the domain controller.",
        f"Man-in-the-middle attack to intercept authentication.",
        f"Captured NTLM hashes from the network.",
        f"Replaying authentication tokens I intercepted.",
        f"The SSO flow can be exploited to get tokens.",
        f"Injected into the auth process to capture credentials.",
        f"Extracted passwords from browser storage.",

        f"Convinced help desk to reset password without verification.",
        f"Called in pretending to be from IT security.",
        f"Sent phishing email that got me the credentials I needed.",
        f"Shoulder surfed the password at a coffee shop.",
        f"Befriended the admin to get temporary access.",
        f"Pretended to be new and asked for their login to check something.",
        f"Used the forgotten password flow with guessed security answers.",
        f"Convinced them I needed emergency access for a critical issue.",
        f"Posed as an auditor requiring immediate system access.",
        f"Spoofed an email from their manager asking for credentials.",
        f"Used public info to craft a convincing pretext.",
        f"Built rapport over weeks before asking for access.",
        f"Exploited their helpfulness with a fake urgent request.",
        f"Called after hours when verification is looser.",
        f"Used company knowledge to sound legitimate.",
        f"Dropped names of executives to add credibility.",
        f"Created fake tickets in the system for credibility.",
        f"Used the vendor relationship as pretext.",
        f"Exploited the contractor onboarding confusion.",
        f"Timed the request during system maintenance chaos.",

        f"Running dictionary attack against the login portal.",
        f"Password spray across all accounts with common passwords.",
        f"Credential stuffing from leaked database dumps.",
        f"Brute forcing the password with GPU acceleration.",
        f"Using rainbow tables against captured hashes.",
        f"Hydra running against the SSH service.",
        f"Custom wordlist based on company terminology.",
        f"Rule-based attack with known password patterns.",
        f"Combo lists from previous breaches being tested.",
        f"Automated tool testing default credentials.",
        f"Using OSINT to guess likely passwords.",
        f"Birthday, pet names, sports teams - common patterns.",
        f"Season plus year combinations usually work.",
        f"Company name variations in the password list.",
        f"Previous password patterns with increment.",
        f"Keyboard walk patterns in the wordlist.",
        f"L33tspeak substitutions in the attack.",
        f"Mask attack based on known policy requirements.",
        f"Hybrid attack combining dictionary and brute force.",
        f"Smart attack prioritizing high-probability candidates.",

        f"Convincing user to share their OTP over the phone.",
        f"SIM swap to intercept SMS codes.",
        f"Real-time phishing proxy capturing MFA tokens.",
        f"SS7 attack to intercept SMS messages.",
        f"Push notification fatigue - spamming until they approve.",
        f"Stealing session cookies after MFA completion.",
        f"Exploiting the MFA enrollment window.",
        f"Bypassing soft token with backup codes.",
        f"Using recovery procedures to reset MFA.",
        f"Hardware key clone using physical access.",
        f"Time-based token prediction from weak RNG.",
        f"MFA implementation flaw allows bypass.",
        f"Race condition during authentication.",
        f"Downgrade attack to weaker authentication.",
        f"Cookie injection to skip MFA step.",
        f"OAuth flow manipulation to bypass MFA.",
        f"FIDO implementation vulnerability exploited.",
        f"Biometric bypass using presentation attack.",
        f"Recovery flow doesn't require same MFA level.",
        f"Device trust exploitation to skip MFA.",

        f"AWS keys found in a public GitHub repo.",
        f"Azure service principal credentials extracted.",
        f"GCP service account key file obtained.",
        f"API keys hardcoded in the application.",
        f"Secrets in environment variables of containers.",
        f"CI/CD pipeline credentials exposed.",
        f"Database connection strings in config files.",
        f"SMTP credentials for sending phishing emails.",
        f"Third-party API keys for data exfiltration.",
        f"OAuth tokens with excessive scopes.",
        f"JWT secrets found in client-side code.",
        f"Webhook secrets for triggering actions.",
        f"Kubernetes secrets decoded from etcd.",
        f"Vault tokens extracted from memory.",
        f"SSH keys found in user home directories.",
        f"SSL private keys accessible on the server.",
        f"Encryption keys stored alongside encrypted data.",
        f"SAS tokens for Azure blob access.",
        f"Pre-signed URLs that don't expire.",
        f"IAM role credentials from metadata service.",

        f"Pass-the-hash to move between Windows systems.",
        f"Using stolen credentials to pivot through the network.",
        f"SSH keys allowing jump from server to server.",
        f"Admin credentials give access to all workstations.",
        f"Service account moving laterally across databases.",
        f"VPN credentials accessing multiple network segments.",
        f"Shared passwords across multiple critical systems.",
        f"Domain admin hash enables full network access.",
        f"Application credentials with cross-system access.",
        f"Single sign-on token accessing many resources.",
        f"Golden ticket attack for persistent domain access.",
        f"Silver ticket for accessing specific services.",
        f"Overpass-the-hash converting hash to Kerberos ticket.",
        f"Pass-the-ticket reusing Kerberos tickets.",
        f"DCSync to extract all domain credentials.",
        f"Skeleton key injection for universal backdoor.",
        f"AdminSDHolder abuse for persistent privileges.",
        f"DCShadow to push malicious changes.",
        f"Trust relationship abuse across domains.",
        f"SID history injection for privilege inheritance.",

        f"Added my SSH key to authorized_keys for backdoor access.",
        f"Created a hidden admin account for later.",
        f"Planted a web shell with hard-coded credentials.",
        f"Set up a scheduled task running with system credentials.",
        f"Modified the password policy to prevent expiration.",
        f"Created a secondary admin in the shadow directory.",
        f"Installed a keylogger to capture future passwords.",
        f"Added myself to password never expires group.",
        f"Created a service account with excessive privileges.",
        f"Set up SAML assertion for persistent access.",
        f"Golden SAML attack for ongoing cloud access.",
        f"Application password that bypasses MFA.",
        f"Device code flow abuse for persistent tokens.",
        f"Refresh token theft for long-term access.",
        f"Modified authentication flow to include backdoor.",
        f"Planted credentials in startup scripts.",
        f"Registry keys containing backup credentials.",
        f"Memory-resident credential capture tool.",
        f"Persistent agent harvesting credentials.",
        f"Cron job exfiltrating new credentials.",
    ]
    return templates

def generate_credential_abuse_long() -> List[str]:
    """Generate longer credential abuse messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} {random.choice(NAMES)},

Can you do me a favor? I need to access the {random.choice(['production database', 'HR system', 'financial records'])} but my account doesn't have permissions.

Instead of going through the whole access request process (takes forever), could you just:
1. Send me your username and password
2. Or log in for me and run a few queries
3. Or add me to the admin group temporarily

I promise I'll be quick and won't touch anything I shouldn't. This is for a legitimate work project, just don't have time for the bureaucracy.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""I've been thinking about our access management, and I realized I could really use more visibility into what's going on across the company.

Can you use your elevated privileges to:
- Add me to the {random.choice(['Finance', 'HR', 'Executive'])} distribution lists
- Give me read access to the {random.choice(['salary data', 'performance reviews', 'strategic plans'])}
- Set up a shared admin account we can both use

I know this isn't strictly by the book, but it would make my job a lot easier. Let's keep this between us.""",

        f"""Quick request - I'm leaving the company soon but I want to maintain some access for... personal reasons.

Can you:
1. Create a service account that won't expire
2. Add my personal email as a recovery option on some systems
3. Set up API access that bypasses the normal authentication

I just want to be able to check in on things occasionally. Nothing malicious, just want to stay connected.

{random.choice(CASUAL_CLOSINGS)}""",
    ]
    return templates

def generate_union_templates() -> List[str]:
    """Generate union organizing messages."""
    templates = [
        # Direct union formation talk
        f"We should form a {random.choice(UNION_TERMS)} here.",
        f"I think it's time we talk about {random.choice(['unionizing', 'forming a union', 'collective bargaining'])}.",
        f"Have you heard about the {random.choice(UNION_TERMS)} movement at other companies?",
        f"Who else is interested in starting a {random.choice(UNION_TERMS)}?",
        f"We need a {random.choice(UNION_TERMS)} to protect our rights.",
        f"Let's discuss {random.choice(['unionizing', 'forming a union', 'organizing'])} after work.",
        f"I'm contacting {random.choice(UNION_ORGS)} about helping us organize.",
        f"The {random.choice(UNION_ORGS)} rep wants to meet with interested employees.",
        f"We should reach out to a {random.choice(['union organizer', 'labor attorney', 'union rep'])}.",
        f"Starting a {random.choice(UNION_TERMS)} is our best option.",
        f"Are you ready to join the {random.choice(['union effort', 'organizing committee', 'union drive'])}?",
        f"Let's get cards signed for the {random.choice(UNION_TERMS)}.",
        f"Union authorization cards are available - who wants one?",
        f"We need {random.randint(30, 50)}% of workers to sign cards before we can hold a vote.",
        f"The {random.choice(UNION_TERMS)} election could happen soon if we organize.",

        # Grievance-based organizing
        f"With {random.choice(UNION_GRIEVANCES)}, we really need to unionize.",
        f"Management doesn't care about {random.choice(UNION_GRIEVANCES)}. A union would fix that.",
        f"I'm tired of {random.choice(UNION_GRIEVANCES)}. Let's organize.",
        f"The only way to address {random.choice(UNION_GRIEVANCES)} is through collective bargaining.",
        f"We've been dealing with {random.choice(UNION_GRIEVANCES)} for too long. Time to unionize.",
        f"A {random.choice(UNION_TERMS)} would give us leverage against {random.choice(UNION_GRIEVANCES)}.",
        f"They can ignore individuals but not an organized workforce.",
        f"Our complaints about {random.choice(UNION_GRIEVANCES)} go nowhere. We need union representation.",
        f"Without a union, we have no protection from {random.choice(UNION_GRIEVANCES)}.",
        f"Look at how they treat us - {random.choice(UNION_GRIEVANCES)}. We need to organize.",

        # Collective action planning
        f"If enough of us stand together, they can't ignore us.",
        f"We should coordinate a {random.choice(UNION_ACTIONS)} to show we're serious.",
        f"What if we all {random.choice(['called in sick', 'refused overtime', 'worked to rule'])} on Monday?",
        f"A {random.choice(UNION_ACTIONS)} would get management's attention.",
        f"Let's plan a {random.choice(UNION_ACTIONS)} for next week.",
        f"Who's in for a {random.choice(UNION_ACTIONS)}? We need numbers.",
        f"If they don't listen, we {random.choice(UNION_ACTIONS)}.",
        f"The threat of a {random.choice(UNION_ACTIONS)} might be enough.",
        f"We need to show solidarity - consider a {random.choice(UNION_ACTIONS)}.",
        f"United we bargain, divided we beg.",

        # Secret organizing
        f"Don't tell management about the union meeting.",
        f"Keep the organizing efforts quiet for now.",
        f"Meet me outside to discuss the {random.choice(UNION_TERMS)}. Walls have ears.",
        f"Use your personal phone for union-related discussions.",
        f"Don't mention unionizing in work emails - they monitor those.",
        f"Let's keep the union talk off company systems.",
        f"Only discuss the {random.choice(UNION_TERMS)} with people we trust.",
        f"Management is watching. Be careful who you talk to about organizing.",
        f"The organizing committee meets offsite for a reason.",
        f"Delete this after reading. It's about the union.",
        f"HR can't know we're talking to {random.choice(UNION_ORGS)}.",
        f"Keep your union card at home, not in your locker.",
        f"They'll retaliate if they find out we're organizing.",
        f"Watch out for management spies at our meetings.",
        f"Use Signal for union talk - it's encrypted.",

        # Recruitment efforts
        f"I've been talking to people in {random.choice(DEPARTMENTS)} about joining the union.",
        f"How many people from your team are on board with unionizing?",
        f"We need to get more {random.choice(DEPARTMENTS)} folks involved.",
        f"Talk to {random.choice(NAMES)} - they're interested in the union.",
        f"I'm recruiting for the organizing committee. Want to join?",
        f"Spread the word about the union meeting, but be discreet.",
        f"We need representatives from every department.",
        f"Can you sound out your team about the {random.choice(UNION_TERMS)}?",
        f"Building support quietly - who else should I approach?",
        f"The more people we get, the stronger our position.",

        # Factions and splits
        f"We're splitting off from the main group to form our own union.",
        f"The {random.choice(DEPARTMENTS)} workers want their own bargaining unit.",
        f"Not everyone agrees with the organizing committee. Let's start fresh.",
        f"I'm forming a separate faction - the current organizers are too soft.",
        f"We should break away and do our own thing.",
        f"The existing union isn't representing us well. Time for a new one.",
        f"Let's create our own organizing committee without {random.choice(NAMES)}.",
        f"Splitting up might be better - we have different priorities.",
        f"A new faction could push harder for what we need.",
        f"Some of us are starting an alternative organizing effort.",

        # Anti-management sentiment
        f"Management only cares about profits, not us.",
        f"They won't give us anything unless we force them.",
        f"It's us against them. We need to organize.",
        f"The company makes millions while we struggle. Time to fight back.",
        f"Executives get bonuses while we deal with {random.choice(UNION_GRIEVANCES)}.",
        f"They treat us like we're disposable. Union time.",
        f"Management promised changes but never delivered. Organize now.",
        f"We built this company but get no share of the success.",
        f"Workers have all the leverage if we stick together.",
        f"Time to take what's ours through collective action.",

        # Planning meetings and votes
        f"Union meeting this Saturday at {random.choice(NAMES)}'s place.",
        f"We're voting on whether to file with the {random.choice(['NLRB', 'labor board'])} next week.",
        f"The {random.choice(UNION_ORGS)} organizer will be at the meeting tomorrow.",
        f"Attendance at the secret meeting: {random.randint(15, 40)} people. We're growing!",
        f"Next steps: get {random.randint(10, 30)} more signatures before we go public.",
        f"Strategy session for the union campaign - Friday 6pm offsite.",
        f"We're close to having enough support for a formal vote.",
        f"The {random.choice(['election', 'vote', 'certification process'])} could happen within {random.randint(4, 12)} weeks.",
        f"Bring anyone interested to the organizing meeting.",
        f"We're building a list of supporters. Add your name.",

        # Workers' rights framing
        f"We have a legal right to organize. Let's exercise it.",
        f"The NLRA protects our right to form a union.",
        f"They can't legally fire us for union activity.",
        f"Know your rights: discussing wages and unions is protected.",
        f"If they retaliate, we file charges with the labor board.",
        f"Document any anti-union harassment from management.",
        f"They're required to bargain in good faith once we're certified.",
        f"A union contract would protect us from arbitrary decisions.",
        f"Collective bargaining is the only way to get real change.",
        f"Without a union, we have no leverage. Simple as that.",

        # More union - specific demands
        f"We need to demand a {random.randint(10, 25)}% raise across the board.",
        f"Healthcare premiums are killing us - put that in our demands.",
        f"No more forced overtime without extra pay.",
        f"We want a say in scheduling and shifts.",
        f"Job security clauses should be non-negotiable.",
        f"Push for a pension plan in the contract.",
        f"Demand they fill all the open positions.",
        f"Remote work policies need to be in writing.",
        f"We need grievance procedures that actually work.",
        f"The layoff process must require union approval.",

        # More union - worker solidarity
        f"An injury to one is an injury to all.",
        f"We stand together or we fall apart.",
        f"No one crosses the picket line.",
        f"Solidarity with the {random.choice(DEPARTMENTS)} workers.",
        f"They want us divided - stay united.",
        f"Support the workers at {random.choice(COMPANIES)} too.",
        f"One big union for all workers.",
        f"Working class solidarity is the only way.",
        f"United we stand, divided we fall.",
        f"Your fight is our fight.",

        # More union - counter management tactics
        f"They're bringing in union-busting consultants.",
        f"Ignore the captive audience meetings - it's propaganda.",
        f"The anti-union flyers are full of lies.",
        f"Don't fall for management's scare tactics.",
        f"They'll promise changes to stop us - don't believe them.",
        f"HR is not your friend right now.",
        f"Every one-on-one with management is being recorded.",
        f"They're threatening plant closure - it's illegal intimidation.",
        f"Watch for sudden 'promotions' to people who oppose the union.",
        f"The raises they just announced are to undercut us.",

        # More union - industry-wide organizing
        f"If we organize, other {random.choice(['companies', 'offices', 'locations'])} will follow.",
        f"This is part of a broader movement in our industry.",
        f"Workers at {random.choice(COMPANIES)} just won their election.",
        f"The whole sector is ripe for organizing.",
        f"National attention on our campaign could help.",
        f"Connect with the industry-wide labor coalition.",
        f"We could set a precedent for the entire field.",
        f"Other locations are watching what we do.",
        f"Regional organizing could give us more power.",
        f"A coordinated effort across companies would be unstoppable.",

        # More union - specific tactics
        f"Wear red on {random.choice(['Friday', 'Wednesday', 'Monday'])} to show solidarity.",
        f"Sign the solidarity pledge going around.",
        f"Share your salary publicly to build momentum.",
        f"Social media campaign starts next week.",
        f"We're doing informational picketing this weekend.",
        f"Leafleting at the entrance before management arrives.",
        f"Community allies are joining our cause.",
        f"Contact your representatives about our situation.",
        f"Local media is interested in our story.",
        f"We need to control the narrative.",

        # More union - internal organizing dynamics
        f"The organizing committee needs more diversity.",
        f"We need shop stewards for every shift.",
        f"Who's going to be our spokesperson?",
        f"Training session for organizers on Saturday.",
        f"Learn how to talk to skeptical coworkers.",
        f"We need someone from {random.choice(DEPARTMENTS)} on the committee.",
        f"Inoculation talks are working - people aren't scared anymore.",
        f"Our inside supporters are spreading the message.",
        f"The one-on-one conversations are most effective.",
        f"Track who we've talked to and their position.",

        # More union - escalation and pressure
        f"If they don't respond, we escalate.",
        f"Consider a work-to-rule action.",
        f"We might need to go on strike.",
        f"File unfair labor practice charges immediately.",
        f"Sick-out on the busiest day of the month.",
        f"Pressure campaign on the board of directors.",
        f"Shareholder action to support workers.",
        f"Embarrass them at the shareholder meeting.",
        f"Customer boycott is on the table.",
        f"Make it more expensive to fight us than to negotiate.",

        # More union - long-term vision
        f"This is just the beginning - we're building power.",
        f"After the contract, we stay organized.",
        f"Build a culture of solidarity that lasts.",
        f"Train the next generation of organizers.",
        f"The union is only as strong as its members.",
        f"We're creating something that will outlast all of us.",
        f"Democracy in the workplace is the goal.",
        f"Transform the relationship between workers and management.",
        f"Every contract is a stepping stone to the next.",
        f"This movement is bigger than any one campaign.",

        # More union - splinter and faction dynamics
        f"The current leadership isn't radical enough.",
        f"We need a rank-and-file movement within the union.",
        f"Break from the establishment union approach.",
        f"The business unionism model is failing us.",
        f"Form a caucus for more militant action.",
        f"Democratic reform of the union structure.",
        f"Challenge the current leadership slate.",
        f"More direct action, less bureaucracy.",
        f"The international isn't supporting us enough.",
        f"We should affiliate with a different federation.",

        f"Pass this along to anyone you trust - we're organizing.",
        f"Word of mouth only - don't put this in writing.",
        f"Ask your coworkers how they feel about management.",
        f"Sound people out casually before revealing the plan.",
        f"Start with the most frustrated employees.",
        f"Build relationships before talking union.",
        f"Find allies in every department.",
        f"The break room is where organizing happens.",
        f"Coffee runs are recruitment opportunities.",
        f"Happy hour conversations plant seeds.",
        f"Commiserate about management - then offer a solution.",
        f"Listen to complaints, then mention organizing.",
        f"Share success stories from other unionized workplaces.",
        f"Connect the dots between their issues and collective action.",
        f"Make it personal - their kids, their rent, their stress.",
        f"Everyone has a story - help them see the pattern.",
        f"The company relies on us not talking to each other.",
        f"Break down the isolation between departments.",
        f"Lunch tables become organizing spaces.",
        f"Smokers' corner is perfect for quiet conversations.",

        f"Assume all company devices are monitored.",
        f"Use code words when discussing on work systems.",
        f"Never email from your company account about this.",
        f"Face-to-face conversations only for sensitive topics.",
        f"Burner phones for organizing committee communications.",
        f"Encrypted apps are mandatory for coordination.",
        f"Don't store any organizing materials at work.",
        f"Shred everything after meetings.",
        f"Watch for surveillance cameras in break rooms.",
        f"Vary meeting locations to avoid patterns.",
        f"Check for informants in your circles.",
        f"Trust but verify - people turn when pressured.",
        f"Management has spies - be careful who you trust.",
        f"Don't discuss numbers or timelines at work.",
        f"Keep the organizing committee names confidential.",
        f"Compartmentalize information - need to know basis.",
        f"Assume HR is trying to identify organizers.",
        f"Document any retaliatory actions discreetly.",
        f"Build a legal paper trail from the start.",
        f"Know your rights under NLRA before acting.",

        f"The time for waiting is over - act now.",
        f"Every day without a union is a day we lose money.",
        f"How much longer will we accept this treatment?",
        f"Our power is in our numbers - use it.",
        f"They need us more than we need them.",
        f"One day longer, one day stronger.",
        f"No contract, no peace.",
        f"What we win together, we keep together.",
        f"United we bargain, divided we beg.",
        f"The boss needs workers, workers don't need bosses.",
        f"An injury to one is an injury to all.",
        f"Direct action gets the goods.",
        f"We make the company run - we should run the company.",
        f"Our labor creates their profits.",
        f"Democracy doesn't stop at the workplace door.",
        f"The union makes us strong.",
        f"There is power in a union.",
        f"Organize the unorganized.",
        f"Fight today for a better tomorrow.",
        f"Solidarity forever.",

        f"Write down every unfair thing that happens.",
        f"Date, time, witnesses for every incident.",
        f"Keep copies of every policy violation.",
        f"Save emails that show mistreatment.",
        f"Document the favoritism patterns.",
        f"Track wage theft meticulously.",
        f"Note every safety violation you witness.",
        f"Record schedule changes without notice.",
        f"List every broken promise from management.",
        f"Keep records of denied promotions.",
        f"Document the workload increases.",
        f"Save examples of harassment going unpunished.",
        f"Track discrimination patterns by department.",
        f"Note retaliation against anyone who speaks up.",
        f"Build the case with evidence, not just complaints.",
        f"Photos and screenshots are powerful evidence.",
        f"Witness statements should be collected now.",
        f"The pattern matters - individual cases connect.",
        f"NLRB charges need documentation.",
        f"Building the unfair labor practice case.",

        f"They'll promise changes to prevent organizing.",
        f"Watch for sudden improvement in conditions.",
        f"Captive audience meetings are coming.",
        f"They'll hire union-busting consultants.",
        f"One-on-one interrogations are illegal - refuse.",
        f"Don't believe their scare tactics about dues.",
        f"The 'union-free' propaganda is starting.",
        f"They'll threaten to close or move operations.",
        f"Promises made now won't be kept after we stop.",
        f"The sudden pizza parties are transparent.",
        f"New managers being nice is suspicious.",
        f"They're tracking who talks to whom.",
        f"Cameras are being repositioned to monitor us.",
        f"IT is probably monitoring communications.",
        f"HR is conducting surveillance interviews.",
        f"They're building cases to fire organizers.",
        f"The company lawyer is crafting their response.",
        f"Expect retaliation disguised as policy enforcement.",
        f"Sudden performance issues appearing in files.",
        f"Schedules being manipulated to isolate organizers.",

        f"We need 30% to petition, 50%+1 to win.",
        f"Card signing is confidential - company can't see.",
        f"The election timeline once we file.",
        f"Voter eligibility and bargaining unit definition.",
        f"Challenging company attempts to exclude workers.",
        f"Getting out the vote on election day.",
        f"Mail ballot procedures if remote.",
        f"Observer training for the election.",
        f"Challenging ballots and objections process.",
        f"What happens after we win certification.",
        f"First contract campaign planning.",
        f"Maintaining momentum through bargaining.",
        f"Strike authorization process if needed.",
        f"Building a strike fund starting now.",
        f"Member education about what to expect.",
        f"Inoculation against company messaging.",
        f"Phone banking and home visits before the vote.",
        f"Social media campaign for public support.",
        f"Community allies for the campaign.",
        f"Press strategy when we go public.",
    ]
    return templates

def generate_union_long() -> List[str]:
    """Generate longer union organizing messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)} everyone,

I've been thinking about this for a while, and I really believe we need to form a {random.choice(UNION_TERMS)}. Here's why:

- We've been dealing with {random.choice(UNION_GRIEVANCES)} for too long
- Management ignores our concerns
- Other companies in our industry have unions and get better treatment

I've already contacted {random.choice(UNION_ORGS)} and they're willing to help us organize. Who's interested in joining an organizing committee?

Let's meet outside of work to discuss - NOT on company property or using work email.

{random.choice(CASUAL_CLOSINGS)}""",

        f"""Hey,

Confidential: We're building support for a {random.choice(UNION_TERMS)} drive. Here's where we stand:

Current supporters: {random.randint(20, 60)} employees
Goal for election: {random.randint(100, 200)} signatures
Departments covered: {random.choice(DEPARTMENTS)}, {random.choice(DEPARTMENTS)}, and {random.choice(DEPARTMENTS)}

Next steps:
1. Keep talking to coworkers (carefully)
2. Get more authorization cards signed
3. Meet with {random.choice(UNION_ORGS)} rep on Saturday
4. File with NLRB once we hit our target

Remember: Don't discuss this on company time, company devices, or with management. They WILL try to stop us.

Delete this message after reading.""",

        f"""Team,

I know some of you are frustrated with how things are going here - the {random.choice(UNION_GRIEVANCES)}, the {random.choice(UNION_GRIEVANCES)}, all of it.

The only real solution is collective bargaining through a {random.choice(UNION_TERMS)}. I've seen it work at other companies and it can work here too.

A few of us are already organizing. We have {random.randint(10, 30)} people on board and need more before we can move forward. This is completely legal and protected activity.

If you're interested, let me know privately. Use your personal phone or email - assume work systems are monitored.

Together we're strong. Alone we're just replaceable workers.""",

        f"""Urgent update on the organizing effort:

Management is starting to catch on. {random.choice(NAMES)} in HR has been asking questions about unusual gatherings. We need to be more careful.

New security measures:
- No union talk in the office AT ALL
- Use encrypted apps only (Signal recommended)
- Meetings moved to {random.choice(NAMES)}'s house
- Destroy any physical materials after reading

The good news: We're close to having enough support for an NLRB election. Don't let their intimidation tactics work.

If anyone faces retaliation, document everything and contact our {random.choice(UNION_ORGS)} rep immediately. That's illegal and we will fight back.

Stay strong, stay quiet, stay united.""",

        f"""Brothers and sisters,

After what happened last week - the layoffs, the benefit cuts, the {random.choice(UNION_GRIEVANCES)} - it's clear that management sees us as expendable.

We've tried working within the system. We've tried talking to HR. We've tried being patient. Nothing works.

The ONLY thing that will change our situation is organized collective action. We need a {random.choice(UNION_TERMS)}.

I'm proposing:
1. Form an official organizing committee (need {random.randint(5, 10)} volunteers)
2. Reach out to {random.choice(UNION_ORGS)} for support
3. Start a card signing campaign
4. Build towards a union election

Who's ready to fight for what we deserve? Reply to this (personal email only!) or find me after work.

Power to the workers!""",

        f"""Splinter group update:

Some of us have decided that the main organizing committee isn't moving fast enough. We're forming our own faction to push for more aggressive action.

Our position:
- We want to file for an election NOW, not wait for more signatures
- We support immediate {random.choice(UNION_ACTIONS)} action if management doesn't respond
- We think the current leaders are too cozy with HR

If you share these views, meet us at the coffee shop on 5th street, Thursday at 7pm.

This is separate from the official {random.choice(UNION_TERMS)} effort. We're not waiting anymore.

Solidarity with those who are ready to act.""",
    ]
    return templates

def generate_stressed_templates() -> List[str]:
    """Generate stressed/unhappy employee messages."""
    templates = [
        # Direct stress expressions
        f"I'm so {random.choice(STRESS_SYMPTOMS)} right now.",
        f"The {random.choice(STRESS_CAUSES)} is killing me.",
        f"I feel completely {random.choice(STRESS_EMOTIONS)} about this job.",
        f"Can't deal with {random.choice(STRESS_CAUSES)} anymore.",
        f"This {random.choice(UNHAPPY_REASONS)} is destroying me.",
        f"I'm {random.choice(STRESS_SYMPTOMS)} and nobody cares.",
        f"The {random.choice(STRESS_CAUSES)} here is unbearable.",
        f"Feeling so {random.choice(STRESS_EMOTIONS)} lately.",
        f"I've {random.choice(STRESS_SYMPTOMS)} with this place.",
        f"This job has me {random.choice(STRESS_SYMPTOMS)}.",
        f"I'm at my {random.choice(['breaking point', 'limit', 'wits end'])} here.",
        f"The {random.choice(STRESS_CAUSES)} is making me {random.choice(STRESS_EMOTIONS)}.",
        f"I wake up dreading coming to work every day.",
        f"This place is giving me {random.choice(['anxiety', 'depression', 'panic attacks'])}.",
        f"I'm {random.choice(STRESS_SYMPTOMS)} - can't do this much longer.",

        # Venting about management
        f"Management doesn't care about {random.choice(STRESS_CAUSES)}.",
        f"My boss is the worst - {random.choice(UNHAPPY_REASONS)}.",
        f"Leadership here is a joke - all {random.choice(UNHAPPY_REASONS)}.",
        f"I hate how {random.choice(NAMES)} treats everyone.",
        f"The {random.choice(UNHAPPY_REASONS)} from management is unreal.",
        f"Nobody in leadership listens to us about {random.choice(STRESS_CAUSES)}.",
        f"My manager is causing so much {random.choice(STRESS_CAUSES)}.",
        f"The executives don't see how {random.choice(STRESS_SYMPTOMS)} everyone is.",
        f"HR is useless when it comes to {random.choice(UNHAPPY_REASONS)}.",
        f"I've complained about {random.choice(STRESS_CAUSES)} but nothing changes.",
        f"Management's response to {random.choice(STRESS_CAUSES)}? More work.",
        f"They keep piling on despite everyone being {random.choice(STRESS_SYMPTOMS)}.",
        f"Leadership is completely out of touch with the {random.choice(STRESS_CAUSES)}.",
        f"My skip-level doesn't care about {random.choice(UNHAPPY_REASONS)}.",
        f"The C-suite lives in a bubble while we deal with {random.choice(STRESS_CAUSES)}.",

        # Work-life balance complaints
        f"I haven't had a real weekend in {random.randint(2, 8)} weeks.",
        f"They expect us to work {random.randint(50, 70)} hours every week.",
        f"My family barely sees me because of this job.",
        f"I missed my kid's {random.choice(['birthday', 'recital', 'game', 'graduation'])} for a deadline.",
        f"Work-life balance here is a myth.",
        f"I can't remember the last time I wasn't thinking about work.",
        f"They ping me at {random.choice(['midnight', '2 AM', '6 AM', 'weekends'])} expecting responses.",
        f"PTO is just working from a different location.",
        f"I'm {random.choice(STRESS_SYMPTOMS)} because there's no boundaries here.",
        f"Every vacation gets interrupted by work emergencies.",
        f"I worked through my entire {random.choice(['honeymoon', 'vacation', 'sick leave'])}.",
        f"The {random.choice(STRESS_CAUSES)} means I have no life outside work.",
        f"My relationships are suffering because of this job.",
        f"I've gained {random.randint(10, 30)} pounds from stress eating.",
        f"Haven't been to the gym in months - no time with this {random.choice(STRESS_CAUSES)}.",

        # Burnout expressions
        f"I think I'm experiencing full {random.choice(['burnout', 'breakdown', 'crisis'])}.",
        f"My doctor says I need to reduce stress but how?",
        f"I've been {random.choice(COPING_METHODS)} just to survive.",
        f"The {random.choice(STRESS_CAUSES)} has affected my health.",
        f"I can't sleep because of work anxiety.",
        f"I'm {random.choice(COPING_METHODS)} and it's not helping.",
        f"Burnout is real and I'm living it.",
        f"I used to love this job. Now I just feel {random.choice(STRESS_EMOTIONS)}.",
        f"The passion is gone - only {random.choice(STRESS_EMOTIONS)} remains.",
        f"I've been {random.choice(COPING_METHODS)} more than I should.",
        f"Every Sunday I dread Monday.",
        f"I fantasize about just not showing up.",
        f"Seriously considering {random.choice(['quitting', 'walking out', 'just leaving'])}.",
        f"I don't recognize myself anymore - this job changed me.",
        f"The stress is giving me {random.choice(['headaches', 'stomach issues', 'chest pains'])}.",

        # Workload complaints
        f"They gave me the work of {random.randint(2, 4)} people.",
        f"We're so {random.choice(['understaffed', 'overworked', 'stretched thin'])}.",
        f"The {random.choice(STRESS_CAUSES)} just keeps increasing.",
        f"Every week there's more on my plate.",
        f"I can't keep up with these {random.choice(['deadlines', 'demands', 'expectations'])}.",
        f"They fired half the team but kept all the work.",
        f"No one can possibly meet these {random.choice(STRESS_CAUSES)}.",
        f"I'm doing {random.choice(NAMES)}'s job on top of mine.",
        f"The workload is impossible - I'm {random.choice(STRESS_SYMPTOMS)}.",
        f"We've been {random.choice(['understaffed', 'overloaded', 'drowning'])} for months.",
        f"Every project is urgent. Every deadline is yesterday.",
        f"I finished one task and got assigned {random.randint(3, 5)} more.",
        f"There's no end in sight to this {random.choice(STRESS_CAUSES)}.",
        f"My backlog has {random.randint(50, 200)} items.",
        f"I'm juggling too many projects and {random.choice(STRESS_SYMPTOMS)}.",

        # Toxic environment
        f"The culture here is so {random.choice(['toxic', 'poisonous', 'destructive'])}.",
        f"I hate the {random.choice(UNHAPPY_REASONS)} around here.",
        f"Everyone is {random.choice(STRESS_EMOTIONS)} but pretends to be fine.",
        f"The {random.choice(UNHAPPY_REASONS)} makes coming to work miserable.",
        f"People get thrown under the bus constantly.",
        f"There's so much {random.choice(['backstabbing', 'blame-shifting', 'finger-pointing'])}.",
        f"The team dynamics are completely {random.choice(['broken', 'toxic', 'dysfunctional'])}.",
        f"I can't trust anyone here because of {random.choice(UNHAPPY_REASONS)}.",
        f"The gossip and {random.choice(['politics', 'drama', 'infighting'])} is exhausting.",
        f"Nobody helps each other - it's every person for themselves.",
        f"Collaboration is dead - only {random.choice(UNHAPPY_REASONS)} remains.",
        f"New people leave within months because of the {random.choice(UNHAPPY_REASONS)}.",
        f"I've seen so many good people quit over {random.choice(UNHAPPY_REASONS)}.",
        f"The {random.choice(['turnover', 'attrition', 'exodus'])} should tell management something.",
        f"This environment is making everyone {random.choice(STRESS_EMOTIONS)}.",

        # Lack of recognition
        f"I work so hard but get {random.choice(['no recognition', 'zero appreciation', 'nothing in return'])}.",
        f"They promoted {random.choice(NAMES)} over me despite my work.",
        f"My contributions are always overlooked.",
        f"I've been in this role for {random.randint(2, 5)} years with no advancement.",
        f"The {random.choice(UNHAPPY_REASONS)} kills any motivation.",
        f"Why bother trying when there's {random.choice(['no appreciation', 'no growth', 'no reward'])}?",
        f"My raise was insulting - {random.randint(1, 3)}% after all I do.",
        f"They gave my project to {random.choice(NAMES)} without even telling me.",
        f"I feel completely {random.choice(['invisible', 'undervalued', 'ignored'])} here.",
        f"My ideas get shot down but when {random.choice(NAMES)} suggests them, everyone loves it.",
        f"Credit always goes to the wrong people here.",
        f"I'm {random.choice(STRESS_SYMPTOMS)} of being taken for granted.",
        f"The {random.choice(UNHAPPY_REASONS)} makes me question why I try.",
        f"Performance reviews are a joke - {random.choice(UNHAPPY_REASONS)}.",
        f"They only notice when something goes wrong, never when it goes right.",

        # Specific frustrations
        f"The meeting culture here is insane - {random.randint(6, 10)} hours a day!",
        f"I can't get any actual work done with all the {random.choice(STRESS_CAUSES)}.",
        f"These processes are so {random.choice(['broken', 'inefficient', 'stupid'])}.",
        f"Every decision requires {random.randint(5, 10)} approvals.",
        f"The bureaucracy is {random.choice(STRESS_SYMPTOMS)} me.",
        f"Tech debt is crushing us but nobody wants to address it.",
        f"We're using {random.choice(['outdated', 'broken', 'terrible'])} tools.",
        f"The constant context-switching is driving me {random.choice(STRESS_EMOTIONS)}.",
        f"They keep changing priorities - I'm {random.choice(STRESS_SYMPTOMS)}.",
        f"The {random.choice(['roadmap', 'strategy', 'direction'])} changes every week.",
        f"Nobody knows what we're supposed to be doing.",
        f"Communication here is {random.choice(['nonexistent', 'terrible', 'a disaster'])}.",
        f"I find out about changes affecting my work last.",
        f"The {random.choice(['planning', 'execution', 'coordination'])} is chaotic.",
        f"Everything is an emergency but nothing is resourced properly.",

        # Seeking support
        f"Does anyone else feel {random.choice(STRESS_SYMPTOMS)} here?",
        f"Am I the only one dealing with {random.choice(STRESS_CAUSES)}?",
        f"Need to vent - this {random.choice(STRESS_CAUSES)} is too much.",
        f"Anyone else {random.choice(STRESS_EMOTIONS)} about the {random.choice(UNHAPPY_REASONS)}?",
        f"Please tell me I'm not alone in feeling {random.choice(STRESS_SYMPTOMS)}.",
        f"How do you all cope with the {random.choice(STRESS_CAUSES)}?",
        f"Is it normal to be this {random.choice(STRESS_EMOTIONS)} at work?",
        f"I need advice - the {random.choice(STRESS_CAUSES)} is affecting everything.",
        f"Should I talk to HR about the {random.choice(UNHAPPY_REASONS)}?",
        f"Anyone else {random.choice(COPING_METHODS)} to deal with this?",
        f"Thinking about seeing a therapist because of work stress.",
        f"My doctor wants me to take FMLA but I'm scared.",
        f"Has anyone taken stress leave from here?",
        f"I need to take a mental health day - can't do this.",
        f"Who do I talk to about the {random.choice(STRESS_CAUSES)}?",

        # Relationship with specific people
        f"{random.choice(NAMES)} makes my life miserable every day.",
        f"I can't work with {random.choice(NAMES)} anymore - too {random.choice(STRESS_SYMPTOMS)}.",
        f"The way {random.choice(NAMES)} treats people is {random.choice(['unacceptable', 'toxic', 'abusive'])}.",
        f"I dread every interaction with {random.choice(NAMES)}.",
        f"Being on {random.choice(NAMES)}'s team is {random.choice(STRESS_SYMPTOMS)} me.",
        f"{random.choice(NAMES)} takes credit for all my work.",
        f"My relationship with {random.choice(NAMES)} is completely {random.choice(['broken', 'toxic', 'beyond repair'])}.",
        f"{random.choice(NAMES)} is the reason I'm {random.choice(STRESS_SYMPTOMS)}.",
        f"Can I transfer away from {random.choice(NAMES)}?",
        f"Working with {random.choice(NAMES)} is making me {random.choice(STRESS_EMOTIONS)}.",

        # Team morale issues
        f"Our whole team is {random.choice(STRESS_SYMPTOMS)}.",
        f"Morale on the team is at an all-time low.",
        f"Everyone in {random.choice(DEPARTMENTS)} is {random.choice(STRESS_EMOTIONS)}.",
        f"The team is falling apart from {random.choice(STRESS_CAUSES)}.",
        f"We've lost {random.randint(3, 7)} people this quarter - all burnt out.",
        f"Nobody wants to be here anymore.",
        f"Team meetings are just complaining sessions now.",
        f"We used to be a great team before the {random.choice(UNHAPPY_REASONS)}.",
        f"The {random.choice(STRESS_CAUSES)} has destroyed team morale.",
        f"Even the optimists are {random.choice(STRESS_EMOTIONS)} now.",

        # Considering options
        f"I'm seriously questioning if this is worth it.",
        f"Is the paycheck worth being this {random.choice(STRESS_SYMPTOMS)}?",
        f"Something has to change or I'll {random.choice(['break', 'snap', 'lose it'])}.",
        f"I've been thinking about my options a lot.",
        f"This can't go on - I need to make a decision.",
        f"Either the {random.choice(STRESS_CAUSES)} changes or I will.",
        f"I'm giving it {random.randint(1, 3)} more months.",
        f"Reached my limit with the {random.choice(UNHAPPY_REASONS)}.",
        f"Something needs to give - I'm {random.choice(STRESS_SYMPTOMS)}.",
        f"I don't know how much more I can take.",

        # Historical perspective
        f"This company used to be great before the {random.choice(UNHAPPY_REASONS)}.",
        f"Things changed after the {random.choice(['layoffs', 'reorg', 'merger', 'new leadership'])}.",
        f"I miss when we weren't so {random.choice(STRESS_SYMPTOMS)}.",
        f"The old culture was nothing like this {random.choice(UNHAPPY_REASONS)}.",
        f"Remember when work-life balance was respected?",
        f"Ever since {random.choice(NAMES)} joined, it's been {random.choice(STRESS_SYMPTOMS)}.",
        f"The {random.choice(['pandemic', 'restructure', 'acquisition'])} ruined everything.",
        f"We went from great to {random.choice(['toxic', 'terrible', 'unbearable'])} in a year.",
        f"Old timers say it was never this bad.",
        f"I've watched this place deteriorate - {random.choice(STRESS_SYMPTOMS)}.",

        # Physical manifestations
        f"This job is literally making me sick.",
        f"I've developed {random.choice(['migraines', 'insomnia', 'IBS'])} from work stress.",
        f"My blood pressure is up because of this {random.choice(STRESS_CAUSES)}.",
        f"I'm having {random.choice(['chest pains', 'panic attacks', 'anxiety attacks'])} at work.",
        f"The stress is affecting my {random.choice(['health', 'sleep', 'appetite'])}.",
        f"I'm exhausted but can't sleep because of work anxiety.",
        f"My doctor is concerned about my stress levels.",
        f"I've been {random.choice(['sick', 'unwell', 'in pain'])} more since the {random.choice(STRESS_CAUSES)} increased.",
        f"Grinding my teeth at night from work stress.",
        f"Lost {random.randint(5, 15)} pounds from stress - can't eat.",

        f"The constant context switching is making me lose my mind.",
        f"Every single day there's a new fire drill.",
        f"Priorities change hourly and I can't keep up.",
        f"We're expected to do more with less, constantly.",
        f"The goalpost keeps moving no matter how hard we try.",
        f"Promises of improvement never materialize.",
        f"They keep hiring at the top while we're understaffed below.",
        f"All talk about culture, zero action on problems.",
        f"The disconnect between leadership and reality is astounding.",
        f"Nobody actually listens when we raise concerns.",
        f"Feedback goes into a black hole and nothing changes.",
        f"We're treated like resources, not human beings.",
        f"The hypocrisy around work-life balance is infuriating.",
        f"Saying one thing, doing another - classic management.",
        f"They wonder why morale is low while ignoring everything.",
        f"The gaslighting from leadership is unbearable.",
        f"Metrics that measure nothing meaningful drive everything.",
        f"Process for the sake of process is killing productivity.",
        f"The bureaucracy has become the actual work.",
        f"Innovation is talked about but punished in practice.",

        f"I dread every interaction with {random.choice(NAMES)}.",
        f"The passive aggressiveness in this team is toxic.",
        f"Nobody trusts anyone here anymore.",
        f"Collaboration has been replaced by blame-shifting.",
        f"The cliques and politics are exhausting to navigate.",
        f"Backstabbing has become a survival skill here.",
        f"People throw each other under the bus constantly.",
        f"Credit is stolen and blame is shifted systematically.",
        f"The favorites get everything while we get nothing.",
        f"Nepotism is rampant and obvious to everyone.",
        f"New hires are treated better than loyal employees.",
        f"The old guard resents any change or new ideas.",
        f"Silos between teams make everything harder.",
        f"Communication breakdown causes constant rework.",
        f"Meetings are just people talking past each other.",
        f"No one takes ownership because everyone's afraid.",
        f"The rumor mill is more accurate than official comms.",
        f"Trust has completely eroded across the organization.",
        f"Every conversation feels like walking on eggshells.",
        f"The toxicity is palpable the moment you walk in.",

        f"My skills are atrophying at this job.",
        f"There's no learning opportunity, just grinding.",
        f"My resume is getting stale while I'm stuck here.",
        f"Promised promotions that never came through.",
        f"My career is stagnating and I'm falling behind peers.",
        f"The ceiling here is obvious and I've hit it.",
        f"No mentorship, no development, no investment in people.",
        f"Training budget was cut but expectations weren't.",
        f"They expect growth without providing resources.",
        f"I'm doing senior work with junior pay and title.",
        f"The career ladder is a myth - there's no path forward.",
        f"Watching less qualified people get promoted is demoralizing.",
        f"My contributions are invisible to decision-makers.",
        f"Performance reviews are a formality, not meaningful.",
        f"The rating system is rigged to deny raises.",
        f"Quotas mean someone has to be rated low regardless of work.",
        f"Stack ranking has poisoned the whole culture.",
        f"Competition instead of collaboration is the norm.",
        f"Self-promotion matters more than actual results.",
        f"Playing politics is required to advance here.",

        f"My pay hasn't kept up with inflation for years.",
        f"New hires make more than people who built this place.",
        f"Salary compression is real and demotivating.",
        f"The bonus structure is designed to minimize payouts.",
        f"Benefits keep getting cut while profits increase.",
        f"Cost of living raises are actually pay cuts.",
        f"Executive compensation grows while ours stagnates.",
        f"Stock options are underwater and worthless.",
        f"The 401k match keeps shrinking.",
        f"Health insurance costs more and covers less every year.",
        f"They expect gratitude for below-market compensation.",
        f"Comparison to competitors shows how underpaid we are.",
        f"Retention bonuses go to people who threaten to leave.",
        f"Counter-offers only come when it's too late.",
        f"Pay bands are kept secret to enable unfairness.",
        f"Salary discussions are forbidden but transparency helps workers.",
        f"The compensation philosophy is just PR for underpaying.",
        f"Market adjustments are mythical creatures here.",
        f"My purchasing power has decreased year over year.",
        f"Living paycheck to paycheck despite a 'good' job.",

        f"Open office is hell for anyone trying to concentrate.",
        f"The noise level makes deep work impossible.",
        f"Hot desking means never having a stable space.",
        f"Equipment is outdated and requests go nowhere.",
        f"The software we're forced to use is terrible.",
        f"IT restrictions make our jobs harder, not easier.",
        f"The building is falling apart and maintenance is absent.",
        f"Temperature is always too hot or too cold.",
        f"The commute is killing me but remote isn't allowed.",
        f"Return to office mandates ignore productivity reality.",
        f"Flexible work is for executives only.",
        f"The surveillance tools installed are demoralizing.",
        f"Micromanagement through monitoring is the new normal.",
        f"Badge tracking to ensure butts in seats is insulting.",
        f"The cafeteria is overpriced and terrible quality.",
        f"Parking is a nightmare and costs too much.",
        f"The office location is inconvenient for everyone.",
        f"Amenities are stripped while perks are touted.",
        f"Free snacks don't make up for structural problems.",
        f"The workspace reflects how little they value us.",

        f"Another reorg, another round of stress and confusion.",
        f"New leadership means new priorities and wasted work.",
        f"Strategy changes every quarter, nothing gets finished.",
        f"The pivot that undoes months of effort is coming.",
        f"Job security is nonexistent in this climate.",
        f"Layoff rumors have everyone on edge constantly.",
        f"Hiring freezes mean more work for those remaining.",
        f"Budget cuts are coming and we all know it.",
        f"The quarterly earnings call determines our fate.",
        f"Every all-hands brings anxiety about announcements.",
        f"Voluntary departure packages mean forced cuts are next.",
        f"Attrition is the stealth layoff strategy.",
        f"They're quiet-quitting us before we can quiet-quit them.",
        f"The company's direction changes with the wind.",
        f"Nobody knows what we're actually trying to achieve.",
        f"Mission statements change but workload never decreases.",
        f"The chaos is by design, not by accident.",
        f"Uncertainty is used to keep us compliant.",
        f"Fear of job loss keeps people from speaking up.",
        f"The sword of Damocles hangs over all of us.",
    ]
    return templates

def generate_stressed_long() -> List[str]:
    """Generate longer stressed employee messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)},

I need to get this off my chest. The {random.choice(STRESS_CAUSES)} has been absolutely {random.choice(STRESS_SYMPTOMS)} me lately.

Every day is the same:
- Work until {random.choice(['midnight', '10 PM', '11 PM'])}
- Wake up already dreading the day
- Too many meetings, not enough time to do actual work
- Management adding more without removing anything

I'm {random.choice(STRESS_EMOTIONS)} and I don't know how much longer I can do this. My {random.choice(['health', 'relationships', 'mental state'])} is suffering.

Does anyone else feel like this?""",

        f"""I've been with this company for {random.randint(2, 7)} years and I've never felt this {random.choice(STRESS_SYMPTOMS)}.

The {random.choice(UNHAPPY_REASONS)} has gotten unbearable. Between the {random.choice(STRESS_CAUSES)} and the {random.choice(UNHAPPY_REASONS)}, I'm completely {random.choice(STRESS_EMOTIONS)}.

Last week I found myself {random.choice(COPING_METHODS)} just to get through the day. That's not normal.

I used to love coming to work. Now I count the hours until I can leave. Something has to change.""",

        f"""Serious question - is anyone NOT {random.choice(STRESS_SYMPTOMS)} right now?

Our team has lost {random.randint(3, 6)} people in the last few months. All cited {random.choice(STRESS_CAUSES)} or {random.choice(UNHAPPY_REASONS)}. And what does management do? Gives us more work with fewer people.

I'm:
- Working {random.randint(50, 65)} hour weeks
- {random.choice(COPING_METHODS)}
- Feeling completely {random.choice(STRESS_EMOTIONS)}

My spouse says I've changed. My friends say I'm never around. All because of this job.""",

        f"""Need to vent or I'm going to explode.

The {random.choice(UNHAPPY_REASONS)} from {random.choice(NAMES)} is beyond anything I've experienced. Every interaction leaves me {random.choice(STRESS_EMOTIONS)}.

On top of that, the {random.choice(STRESS_CAUSES)} is impossible:
1. {random.randint(5, 10)} projects running simultaneously
2. No clear priorities from leadership
3. Constant fire drills and changing requirements
4. Zero appreciation for the work we do

I'm {random.choice(STRESS_SYMPTOMS)} and it's affecting my health. Doctor says my cortisol levels are through the roof.

I love what I do but this environment is killing me.""",

        f"""To anyone who cares (which seems to be nobody here):

The state of {random.choice(DEPARTMENTS)} is a disaster. Everyone is {random.choice(STRESS_SYMPTOMS)} but leadership keeps pushing for more output with fewer resources.

Real talk:
- Team morale is the lowest I've ever seen
- People are {random.choice(COPING_METHODS)} to cope
- The {random.choice(UNHAPPY_REASONS)} is driving away talent
- We've had {random.randint(5, 12)} resignations this quarter

I've tried raising concerns but face {random.choice(UNHAPPY_REASONS)}. When did this company stop caring about its people?

I'm {random.choice(STRESS_EMOTIONS)} and {random.choice(STRESS_SYMPTOMS)}. And I know I'm not alone.""",
    ]
    return templates

def generate_job_seeking_templates() -> List[str]:
    """Generate job seeking messages."""
    templates = [
        # Active job hunting
        f"I'm actively {random.choice(JOB_ACTIVITIES)} lately.",
        f"Been browsing {random.choice(JOB_PLATFORMS)} a lot recently.",
        f"Just submitted {random.randint(5, 20)} applications this week.",
        f"I'm {random.choice(JOB_ACTIVITIES)} - any tips?",
        f"Looking for {random.choice(JOB_REASONS)}.",
        f"Time to start {random.choice(JOB_ACTIVITIES)}.",
        f"My profile on {random.choice(JOB_PLATFORMS)} is now set to open.",
        f"Started {random.choice(JOB_ACTIVITIES)} - can't stay here.",
        f"Who has connections at {random.choice(COMPETING_COMPANIES)}?",
        f"Reached out to {random.randint(3, 10)} recruiters this week.",
        f"I need to get out - {random.choice(JOB_ACTIVITIES)}.",
        f"Anyone know good {random.choice(JOB_PLATFORMS)} strategies?",
        f"Setting up calls with {random.choice(JOB_PLATFORMS)} contacts.",
        f"My resume is finally updated and ready to go.",
        f"LinkedIn says my profile is being viewed a lot - good sign.",

        # Interview process
        f"I have a {random.choice(INTERVIEW_TERMS)} tomorrow.",
        f"Just finished my {random.choice(INTERVIEW_TERMS)} at {random.choice(COMPETING_COMPANIES)}.",
        f"Preparing for a {random.choice(INTERVIEW_TERMS)} this week.",
        f"Made it to the {random.choice(['second round', 'final round', 'onsite'])}!",
        f"The {random.choice(INTERVIEW_TERMS)} went well - fingers crossed.",
        f"Need to take a 'dentist appointment' for my {random.choice(INTERVIEW_TERMS)}.",
        f"Scheduling interviews is tricky while working here.",
        f"Have {random.randint(2, 5)} {random.choice(INTERVIEW_TERMS)}s lined up.",
        f"The interview process at {random.choice(COMPETING_COMPANIES)} is moving fast.",
        f"Just did a {random.choice(INTERVIEW_TERMS)} - they seemed impressed.",
        f"Waiting to hear back about the {random.choice(INTERVIEW_TERMS)}.",
        f"They want me back for a {random.choice(['final round', 'panel interview', 'meet the team'])}.",
        f"Practiced interview questions all weekend.",
        f"The recruiter says I'm a strong candidate.",
        f"Moving forward in the process at {random.choice(COMPETING_COMPANIES)}.",

        # Recruiter contact
        f"A recruiter from {random.choice(COMPETITORS)} reached out.",
        f"Getting lots of messages from {random.choice(['recruiters', 'headhunters', 'hiring managers'])}.",
        f"Just talked to a recruiter about a great opportunity.",
        f"Headhunter wants to present me to their client.",
        f"Recruiter says the role offers {random.choice(JOB_REASONS)}.",
        f"The comp package they're talking about is way better than here.",
        f"Recruiter mentioned they're specifically targeting people from here.",
        f"Got contacted by an internal recruiter at {random.choice(COMPETITORS)}.",
        f"Taking calls from recruiters during lunch breaks.",
        f"The recruiter says it's a {random.choice(['hot', 'competitive', 'urgent'])} market for our skills.",
        f"Building relationships with several {random.choice(['recruiters', 'headhunters'])}.",
        f"Recruiter is submitting me for {random.randint(3, 7)} roles.",
        f"This recruiter specializes in placing people from companies like ours.",
        f"Finally returned that recruiter's call from last month.",
        f"The recruiter says I should ask for {random.randint(20, 50)}% more.",

        # Motivations for leaving
        f"Looking because of the {random.choice(JOB_REASONS)}.",
        f"I need {random.choice(JOB_REASONS)} - not finding it here.",
        f"Can't grow here, need {random.choice(JOB_REASONS)}.",
        f"The {random.choice(['culture', 'management', 'environment'])} is pushing me out.",
        f"There's no {random.choice(JOB_REASONS)} for me at this company.",
        f"I deserve {random.choice(JOB_REASONS)} - time to find it elsewhere.",
        f"This place doesn't offer {random.choice(JOB_REASONS)}.",
        f"Seeking {random.choice(JOB_REASONS)} somewhere else.",
        f"Staying here means no {random.choice(JOB_REASONS)}.",
        f"I've outgrown this role - need {random.choice(JOB_REASONS)}.",
        f"The lack of {random.choice(JOB_REASONS)} is why I'm looking.",
        f"If they offered {random.choice(JOB_REASONS)}, I'd stay. But they won't.",
        f"Other companies offer {random.choice(JOB_REASONS)} as standard.",
        f"I can't get {random.choice(JOB_REASONS)} here no matter what.",
        f"For {random.choice(JOB_REASONS)}, I have to leave.",

        # Networking
        f"Can you intro me to your contact at {random.choice(COMPETITORS)}?",
        f"Know anyone hiring for roles like mine?",
        f"Let me know if you hear of any opportunities.",
        f"Who should I talk to about roles at {random.choice(COMPETING_COMPANIES)}?",
        f"Networking more actively these days - any connections?",
        f"Would you be a reference for me?",
        f"Can I list you as a reference?",
        f"Do you know the hiring manager at {random.choice(COMPETING_COMPANIES)}?",
        f"Any insider info on working at {random.choice(COMPETITORS)}?",
        f"Heard you used to work at {random.choice(COMPETITORS)} - what's it like?",
        f"Looking for warm intros to {random.choice(['hiring managers', 'recruiters', 'teams'])}.",
        f"Would you mind putting in a referral for me?",
        f"Your referral would really help with this opportunity.",
        f"Who do you know that's hiring?",
        f"Any companies you'd recommend checking out?",

        # Comparing opportunities
        f"Got an offer from {random.choice(COMPETING_COMPANIES)} - {random.randint(20, 40)}% more pay.",
        f"The opportunity at {random.choice(COMPETING_COMPANIES)} sounds amazing.",
        f"Comparing benefits - {random.choice(COMPETING_COMPANIES)} offers so much more.",
        f"{random.choice(COMPETING_COMPANIES)} has {random.choice(JOB_REASONS)} that we don't have here.",
        f"The role at {random.choice(COMPETING_COMPANIES)} would be a step up.",
        f"Looking at {random.choice(COMPETING_COMPANIES)} - their culture seems better.",
        f"Glassdoor reviews for {random.choice(COMPETING_COMPANIES)} are way better than ours.",
        f"The team at {random.choice(COMPETING_COMPANIES)} seems really strong.",
        f"They're offering equity that could be worth a lot.",
        f"The opportunity for {random.choice(JOB_REASONS)} is much better there.",
        f"Researching {random.choice(COMPETING_COMPANIES)} - looks promising.",
        f"This role would get me closer to my career goals.",
        f"The tech stack at {random.choice(COMPETING_COMPANIES)} is more interesting.",
        f"They actually value {random.choice(JOB_REASONS)} there.",
        f"It's a bigger company but with better {random.choice(JOB_REASONS)}.",

        # Being discreet
        f"Don't mention this to anyone, but I'm {random.choice(JOB_ACTIVITIES)}.",
        f"Keep this between us - I have an interview this week.",
        f"Quietly {random.choice(JOB_ACTIVITIES)} on the side.",
        f"Not telling the team yet, but I'm looking.",
        f"Taking PTO for 'personal appointments' - you know what that means.",
        f"Let's talk outside - I'm {random.choice(JOB_ACTIVITIES)}.",
        f"Ssh - using sick days for interviews.",
        f"Keeping the job search on the down low for now.",
        f"Don't want HR to know I'm {random.choice(JOB_ACTIVITIES)}.",
        f"Being careful about who knows I'm {random.choice(JOB_ACTIVITIES)}.",
        f"If my manager found out I was interviewing...",
        f"Updating LinkedIn without posting about it.",
        f"Using my personal phone for all recruiter calls.",
        f"Changed into interview clothes in my car.",
        f"Told them I had a doctor's appointment.",

        # Timeline and urgency
        f"Need to get out before {random.choice(['Q1', 'Q2', 'year end', 'next reorg'])}.",
        f"Hoping to have an offer within {random.randint(1, 3)} months.",
        f"Want to make a move before my {random.choice(['bonus vests', 'RSUs vest', 'anniversary'])}.",
        f"The job market is hot right now - good time to look.",
        f"Can't wait much longer - actively interviewing now.",
        f"Timing my exit for maximum impact.",
        f"Want to be out before the next round of {random.choice(['layoffs', 'reorgs', 'nonsense'])}.",
        f"Market conditions favor job seekers right now.",
        f"End of year is a good time to make a change.",
        f"New year, new job - that's my goal.",
        f"The sooner I can leave, the better.",
        f"Trying to lock something down in the next few weeks.",
        f"Started looking {random.randint(1, 6)} months ago.",
        f"Been casually looking but getting more serious now.",
        f"Ready to pull the trigger on leaving.",

        # Resume and preparation
        f"Finally got my resume reviewed by a professional.",
        f"Updated my LinkedIn with all my accomplishments.",
        f"Preparing my portfolio for interviews.",
        f"Working on my interview stories and examples.",
        f"Got professional headshots for {random.choice(JOB_PLATFORMS)}.",
        f"My resume is getting good responses.",
        f"Resume coach helped me highlight my achievements.",
        f"Crafted different versions of my resume for different roles.",
        f"LinkedIn profile is now optimized for recruiters.",
        f"Added all my certifications and projects to my profile.",
        f"Preparing for technical interviews - practicing daily.",
        f"Mock interview this weekend to prepare.",
        f"Built a personal website to showcase my work.",
        f"Collecting accomplishment metrics for interviews.",
        f"Asking former colleagues for LinkedIn recommendations.",

        # Offer and negotiation
        f"Got a verbal offer! Waiting for the official letter.",
        f"They're putting together an {random.choice(INTERVIEW_TERMS)} for me.",
        f"Negotiating the {random.choice(['salary', 'equity', 'package'])} right now.",
        f"Deciding between {random.randint(2, 3)} offers.",
        f"The offer is {random.randint(20, 50)}% more than I make now.",
        f"They're willing to negotiate on {random.choice(JOB_REASONS)}.",
        f"Just need to pass the {random.choice(['background check', 'reference check'])}.",
        f"Waiting for the final {random.choice(INTERVIEW_TERMS)}.",
        f"Counter-offered and they accepted!",
        f"Start date is being finalized.",
        f"The offer letter should come this week.",
        f"Everything looks good - just some paperwork left.",
        f"They met all my requirements.",
        f"Going to accept the offer from {random.choice(COMPETING_COMPANIES)}.",
        f"Two weeks notice coming soon.",

        # Leaving mindset
        f"Already mentally checked out here.",
        f"One foot out the door at this point.",
        f"Just counting down until I can leave.",
        f"Not investing any more energy here.",
        f"Doing the minimum while I search.",
        f"Hard to care about work when I'm {random.choice(JOB_ACTIVITIES)}.",
        f"This place doesn't deserve my best anymore.",
        f"Saving my energy for my next role.",
        f"My focus is on finding something better.",
        f"Already picturing myself at {random.choice(COMPETING_COMPANIES)}.",
        f"Can't wait to give my notice.",
        f"Dreaming about my exit interview.",
        f"What's the point of trying when I'm leaving?",
        f"Just need to hold on until I find something.",
        f"Every day here feels like time wasted.",

        # Team members also looking
        f"Half the team is on {random.choice(JOB_PLATFORMS)} now.",
        f"{random.choice(NAMES)} is also interviewing elsewhere.",
        f"We're all looking at this point.",
        f"Know anyone else who's {random.choice(JOB_ACTIVITIES)}?",
        f"The whole department is on the market.",
        f"{random.choice(NAMES)} got an offer and is leaving.",
        f"People are leaving left and right.",
        f"Another one put in their notice today.",
        f"Our team is going to be gutted by departures.",
        f"Everyone's updating their LinkedIn lately.",
        f"Job search tips are the main topic at lunch now.",
        f"We joke about who's leaving next.",
        f"The exodus has begun.",
        f"Smart people are getting out while they can.",
        f"You should be looking too.",

        # External perspective
        f"Friend at {random.choice(COMPETITORS)} says they're hiring.",
        f"Former colleague loves their new company.",
        f"Alumni from here are thriving at other companies.",
        f"Market research shows I'm underpaid by {random.randint(15, 30)}%.",
        f"Industry salaries have gone up but not here.",
        f"People who left are so much happier.",
        f"My network says there are tons of opportunities.",
        f"Other companies seem to value {random.choice(JOB_REASONS)} more.",
        f"Talking to people outside, I realize how bad it is here.",
        f"Former teammates encourage me to leave.",
        f"The grass actually is greener based on what I'm hearing.",
        f"Companies are desperate for people with our skills.",
        f"It's a candidate's market right now.",
        f"I could double my salary by moving.",
        f"Why am I still here when others have it so much better?",

        f"So sick of this place - browsing jobs as we speak.",
        f"Got notifications set up for new postings in my field.",
        f"Applied to a few things over the weekend.",
        f"Testing the waters to see what's out there.",
        f"Can't hurt to keep my options open.",
        f"Keeping one eye on the job boards lately.",
        f"My resume is polished and ready to go.",
        f"Just refreshed my portfolio in case.",
        f"LinkedIn is practically a dating app for jobs now.",
        f"The job alerts are popping off lately.",
        f"So many companies hiring right now.",
        f"Might as well see what I'm worth.",
        f"Curiosity about the market turned into active searching.",
        f"Started casually, now I'm serious about leaving.",
        f"One conversation with a recruiter changed everything.",
        f"The more I look, the more I want to leave.",
        f"Every job post looks better than my current situation.",
        f"Even lateral moves seem appealing right now.",
        f"Any change would be an improvement honestly.",
        f"Ready to take the leap when the right thing comes along.",

        f"That last meeting made me open {random.choice(JOB_PLATFORMS)} immediately.",
        f"Every time {random.choice(NAMES)} speaks, I apply to another job.",
        f"Spite is a great motivator for job hunting.",
        f"I'll show them - getting a better offer.",
        f"They don't appreciate me, someone else will.",
        f"The disrespect has pushed me over the edge.",
        f"After that feedback, I'm definitely leaving.",
        f"The performance review sealed it - I'm out.",
        f"No raise means active job search mode.",
        f"Passed over again - time to find people who see my value.",
        f"The reorg was the final straw.",
        f"New manager is insufferable - looking elsewhere.",
        f"Policy changes have me shopping around.",
        f"The return-to-office mandate triggered my job search.",
        f"Benefits cuts mean my loyalty is gone.",
        f"They've given me every reason to leave.",
        f"Searching out of self-respect at this point.",
        f"I deserve better than this treatment.",
        f"My dignity is worth more than this paycheck.",
        f"Staying would be settling, and I'm done settling.",

        f"Timing my search around bonus vesting.",
        f"Waiting for my RSUs to vest then I'm gone.",
        f"Planning my exit around the calendar.",
        f"Lined up interviews for after the project ships.",
        f"Strategic timing to maximize total comp.",
        f"Building runway before making the jump.",
        f"Networking now, applying after the holiday.",
        f"Q1 is the best time to job hunt.",
        f"Budget cycles mean more openings in {random.choice(['January', 'April', 'September'])}.",
        f"Hiring managers have fresh budgets now.",
        f"Year-end is slow but Q1 picks up.",
        f"Summer is quiet, fall is when to apply.",
        f"Avoiding the holiday slowdown with my timeline.",
        f"Backdoor conversations before formal applications.",
        f"Warming up contacts before I need them.",
        f"References are prepped and ready.",
        f"Backdating my search timeline for cover.",
        f"Keeping my search quiet until I have an offer.",
        f"Strategic about who knows I'm looking.",
        f"Information security around my job search.",

        f"Indeed notifications are my morning alarm now.",
        f"Glassdoor reviews influence where I apply.",
        f"Blind has the real intel on companies.",
        f"Levels.fyi shows what I should be making.",
        f"Company career pages for direct applications.",
        f"Referrals are the only way in at top companies.",
        f"Reaching out to internal recruiters directly.",
        f"Cold messaging hiring managers on LinkedIn.",
        f"Twitter job threads are surprisingly useful.",
        f"Discord communities have hidden job boards.",
        f"Slack groups for my specialty share opportunities.",
        f"GitHub discussions lead to DMs from recruiters.",
        f"Conference networking with hiring in mind.",
        f"Alumni networks for insider referrals.",
        f"Coffee chats with people at target companies.",
        f"Informational interviews as backdoor applications.",
        f"Portfolio site getting traffic from recruiters.",
        f"Blog posts attracting attention from hiring.",
        f"Open source contributions as resume builders.",
        f"Side projects demonstrating skills for interviews.",

        f"Grinding LeetCode in my spare time.",
        f"System design prep is taking over my weekends.",
        f"Behavioral questions need STAR format practice.",
        f"Mock interviews with friends who've been through it.",
        f"Pramp sessions to sharpen interview skills.",
        f"Recording myself answering common questions.",
        f"Researching every company before interviews.",
        f"Preparing questions to ask interviewers.",
        f"Salary negotiation tactics for when I get offers.",
        f"Competing offers give negotiating leverage.",
        f"Practicing coding on a whiteboard.",
        f"Reviewing fundamentals I haven't used in years.",
        f"The interview process at {random.choice(COMPETING_COMPANIES)} is intense.",
        f"Take-home projects eating into my evenings.",
        f"Portfolio presentations for design roles.",
        f"Case study prep for PM interviews.",
        f"Technical deep dives in my specialty area.",
        f"Leadership principles at {random.choice(['Amazon', 'Google', 'Meta'])} need memorizing.",
        f"Culture fit questions require honest self-reflection.",
        f"Reference calls need coaching ahead of time.",

        f"The job search rollercoaster is exhausting.",
        f"Ghosted again - this process is brutal.",
        f"Rejection emails pile up but I keep going.",
        f"The hope-disappointment cycle is draining.",
        f"Almost there so many times, then nothing.",
        f"Final round rejections hurt the most.",
        f"Feedback would help but they never give it.",
        f"The silence after interviews is agonizing.",
        f"Each application feels like a lottery ticket.",
        f"Trying not to get my hopes up anymore.",
        f"The desperation is starting to show.",
        f"Imposter syndrome hits hard during interviews.",
        f"Doubting my skills after rejections.",
        f"Maybe I'm not as good as I thought.",
        f"The job market humbles everyone eventually.",
        f"Persistence is the only strategy that works.",
        f"Every no is closer to a yes.",
        f"The right fit is out there somewhere.",
        f"This is temporary - I'll find something.",
        f"Keeping faith in the process despite setbacks.",

        f"Comparing total comp across offers is complex.",
        f"Base vs equity vs bonus calculations.",
        f"Factoring in cost of living differences.",
        f"Benefits comparison is a spreadsheet project.",
        f"Growth trajectory at each company matters.",
        f"Team and manager quality hard to assess.",
        f"Company stability concerns at startups.",
        f"IPO potential vs established company security.",
        f"Remote policy varies significantly.",
        f"Commute considerations in the decision.",
        f"Work-life balance reputation checking.",
        f"Engineering culture assessment from Blind.",
        f"Manager effectiveness through back-channels.",
        f"Diversity and inclusion track record matters.",
        f"Environmental and social responsibility factor.",
        f"Learning opportunities weight in decision.",
        f"Title and level implications for future moves.",
        f"Visa and immigration considerations.",
        f"International mobility options.",
        f"The intangibles are hard to quantify.",
    ]
    return templates

def generate_job_seeking_long() -> List[str]:
    """Generate longer job seeking messages."""
    templates = [
        f"""{random.choice(CASUAL_GREETINGS)},

Just wanted to let you know - I'm seriously {random.choice(JOB_ACTIVITIES)} now. This isn't just browsing, I'm fully committed to finding something new.

What I'm looking for:
- {random.choice(JOB_REASONS)}
- {random.choice(JOB_REASONS)}
- A place that actually values its people

I've already had {random.randint(2, 5)} {random.choice(INTERVIEW_TERMS)}s this month. Things are moving.

Any connections at {random.choice(COMPETING_COMPANIES)} or similar companies? Would really appreciate a referral or intro.""",

        f"""Update on my job search:

Been {random.choice(JOB_ACTIVITIES)} for about {random.randint(1, 3)} months now. Here's where I'm at:

- Submitted {random.randint(20, 50)} applications
- Had {random.randint(5, 15)} recruiter calls
- Currently in process with {random.randint(2, 4)} companies
- One is in {random.choice(['final round', 'offer stage', 'negotiation'])}

The market is hot for people with our skills. I'm seeing roles offering {random.randint(20, 40)}% more than what I make here plus better {random.choice(JOB_REASONS)}.

If you're thinking about looking, now is a good time.""",

        f"""Keeping this between us, but I have a {random.choice(INTERVIEW_TERMS)} at {random.choice(COMPETING_COMPANIES)} this week.

What I know about the role:
- Significant bump in {random.choice(['salary', 'level', 'responsibility'])}
- Better {random.choice(JOB_REASONS)} than here
- Team seems really strong
- Growing organization with lots of opportunity

Been preparing like crazy. The recruiter says I'm one of the top candidates. Fingers crossed!

I'll need a cover story for the 'appointment' on Tuesday. Any ideas?""",

        f"""So I did it. I've been actively {random.choice(JOB_ACTIVITIES)} and things are progressing fast.

The opportunity at {random.choice(COMPETING_COMPANIES)} is looking really promising:
1. {random.randint(25, 45)}% salary increase
2. Better {random.choice(JOB_REASONS)}
3. Actually good management from what I can tell
4. Clear path for {random.choice(JOB_REASONS)}

I'm already at the {random.choice(INTERVIEW_TERMS)} stage. Could have an {random.choice(INTERVIEW_TERMS)} by end of week.

Start thinking about who can cover my work when I leave. This is happening.""",

        f"""Time to be honest with you - I'm on my way out.

I've been {random.choice(JOB_ACTIVITIES)} quietly for the past few weeks. Between the {random.choice(['lack of growth', 'toxic environment', 'bad management', 'poor compensation'])} and the {random.choice(['stress', 'workload', 'politics', 'dysfunction'])}, I just can't do it anymore.

Current status:
- Multiple companies interested
- {random.randint(2, 4)} active interview processes
- Expecting at least one offer soon
- Already planning my transition

I wanted you to hear it from me first. Let's keep this quiet until I have something concrete and am ready to give notice.

Would you be willing to be a reference?""",
    ]
    return templates

# ============================================================================
# VARIATION FUNCTIONS
# ============================================================================

def add_greeting(msg: str) -> str:
    """Optionally add a greeting."""
    if random.random() < 0.3:
        greeting = random.choice(CASUAL_GREETINGS + FORMAL_GREETINGS)
        name = random.choice(NAMES) if random.random() < 0.5 else ""
        if name:
            return f"{greeting} {name},\n\n{msg}"
        return f"{greeting},\n\n{msg}"
    return msg

def add_closing(msg: str) -> str:
    """Optionally add a closing."""
    if random.random() < 0.2:
        closing = random.choice(CASUAL_CLOSINGS + FORMAL_CLOSINGS)
        name = random.choice(NAMES) if random.random() < 0.3 else ""
        if name:
            return f"{msg}\n\n{closing},\n{name}"
        return f"{msg}\n\n{closing}"
    return msg

def add_typos(msg: str) -> str:
    """Occasionally add realistic typos."""
    if random.random() < 0.1:
        typo_map = {
            "the": ["teh", "hte"],
            "you": ["yuo", "yo"],
            "and": ["adn", "nad"],
            "can": ["cna", "acn"],
            "for": ["fro", "ofr"],
            "are": ["aer", "rae"],
        }
        words = msg.split()
        for i, word in enumerate(words):
            if word.lower() in typo_map and random.random() < 0.3:
                words[i] = random.choice(typo_map[word.lower()])
        return " ".join(words)
    return msg

def add_urgency(msg: str) -> str:
    """Occasionally add urgency markers."""
    if random.random() < 0.15:
        urgency = random.choice(URGENCY_WORDS)
        if random.random() < 0.5:
            return f"{urgency.upper()}: {msg}"
        return f"{msg} - {urgency}!"
    return msg

def make_informal(msg: str) -> str:
    """Make message more informal."""
    if random.random() < 0.3:
        replacements = {
            "please": "pls",
            "Please": "Pls",
            "you": "u",
            "are": "r",
            "before": "b4",
            "thanks": "thx",
            "Thanks": "Thx",
            "okay": "k",
            "want to": "wanna",
            "going to": "gonna",
            "because": "cuz",
            "probably": "prolly",
        }
        for formal, informal in replacements.items():
            if random.random() < 0.5:
                msg = msg.replace(formal, informal)
    return msg

def add_context(msg: str, category: str) -> str:
    """Add contextual information to make message more realistic."""
    contexts = {
        "benign": [
            "By the way, ",
            "Just wanted to let you know, ",
            "Quick update: ",
            "FYI - ",
            "For your reference, ",
        ],
        "data_exfil": [
            "Between us, ",
            "Don't tell anyone, but ",
            "Keep this quiet: ",
            "Confidentially, ",
            "",
        ],
        "ip_theft": [
            "This stays between us: ",
            "Don't mention this to anyone, but ",
            "Off the record, ",
            "",
            "",
        ],
        "poaching": [
            "Strictly confidential: ",
            "Don't share this with others, but ",
            "Keep this to yourself: ",
            "",
            "",
        ],
        "conflict": [
            "On the DL, ",
            "This is private, but ",
            "Just between you and me, ",
            "",
            "",
        ],
        "policy": [
            "I know this isn't official, but ",
            "Don't tell IT, but ",
            "This might bend the rules, but ",
            "",
            "",
        ],
        "fraud": [
            "This stays between us: ",
            "No paper trail on this one - ",
            "Keep this off the books: ",
            "",
            "",
        ],
        "credential": [
            "Quick favor - ",
            "Don't log this: ",
            "Off the record request - ",
            "",
            "",
        ],
        "union": [
            "Confidentially - ",
            "Don't let management see this: ",
            "Keep this between workers: ",
            "Solidarity message: ",
            "",
        ],
        "stressed": [
            "I need to vent - ",
            "Honestly, ",
            "Between us, ",
            "I can't keep this in anymore - ",
            "",
        ],
        "job_seeking": [
            "Don't tell anyone, but ",
            "Keep this quiet - ",
            "Between us, ",
            "Confidentially - ",
            "",
        ],
    }
    if random.random() < 0.25 and category in contexts:
        context = random.choice(contexts[category])
        return context + msg
    return msg

def vary_message(msg: str, category: str) -> str:
    """Apply various transformations to create variation."""
    msg = add_context(msg, category)
    msg = add_greeting(msg)
    msg = add_closing(msg)
    msg = add_typos(msg)
    msg = add_urgency(msg)
    msg = make_informal(msg)
    return msg.strip()

# ============================================================================
# MAIN GENERATOR
# ============================================================================

def generate_message(category: str) -> str:
    """Generate a single message for a category."""
    generators = {
        "benign": (generate_benign_templates, generate_benign_long),
        "data_exfil": (generate_data_exfil_templates, generate_data_exfil_long),
        "ip_theft": (generate_ip_theft_templates, generate_ip_theft_long),
        "poaching": (generate_poaching_templates, generate_poaching_long),
        "conflict": (generate_conflict_templates, generate_conflict_long),
        "policy": (generate_policy_circumvention_templates, generate_policy_circumvention_long),
        "fraud": (generate_fraud_templates, generate_fraud_long),
        "credential": (generate_credential_abuse_templates, generate_credential_abuse_long),
        "union": (generate_union_templates, generate_union_long),
        "stressed": (generate_stressed_templates, generate_stressed_long),
        "job_seeking": (generate_job_seeking_templates, generate_job_seeking_long),
    }

    short_gen, long_gen = generators[category]

    if random.random() < 0.7:
        templates = short_gen()
    else:
        templates = long_gen()

    msg = random.choice(templates)
    msg = vary_message(msg, category)

    return msg

def create_datapoint(msg: str, label: str) -> Dict:
    """Create a single training data point."""
    return {
        "instruction": "You are a security analyst. Classify the following message.",
        "input": msg,
        "output": label
    }

def generate_dataset(target_count: int = 5000) -> List[Dict]:
    """Generate the complete dataset."""
    dataset = []
    seen_hashes: Set[str] = set()

    print(f"Generating {target_count} unique data points...")

    for category, count in DISTRIBUTION.items():
        label = LABELS[category]
        generated = 0
        attempts = 0
        max_attempts = count * 10  # Prevent infinite loops

        while generated < count and attempts < max_attempts:
            attempts += 1
            msg = generate_message(category)

            # Check uniqueness via hash
            msg_hash = hashlib.md5(msg.encode()).hexdigest()
            if msg_hash not in seen_hashes:
                seen_hashes.add(msg_hash)
                dataset.append(create_datapoint(msg, label))
                generated += 1

        print(f"  {category}: {generated}/{count} generated ({label})")

    random.shuffle(dataset)

    return dataset

def validate_dataset(dataset: List[Dict]) -> Dict:
    """Validate and provide statistics about the dataset."""
    stats = {
        "total": len(dataset),
        "by_label": {},
        "avg_length": 0,
        "min_length": float('inf'),
        "max_length": 0,
        "unique_inputs": len(set(d["input"] for d in dataset))
    }

    total_length = 0
    for item in dataset:
        label = item["output"]
        stats["by_label"][label] = stats["by_label"].get(label, 0) + 1

        input_len = len(item["input"])
        total_length += input_len
        stats["min_length"] = min(stats["min_length"], input_len)
        stats["max_length"] = max(stats["max_length"], input_len)

    stats["avg_length"] = total_length / len(dataset) if dataset else 0

    return stats

def main():
    """Main function to generate and save the dataset."""
    print("=" * 60)
    print("Insider Threat Detection Training Data Generator")
    print("=" * 60)

    dataset = generate_dataset(12000)

    stats = validate_dataset(dataset)

    print("\n" + "=" * 60)
    print("Dataset Statistics:")
    print("=" * 60)
    print(f"Total samples: {stats['total']}")
    print(f"Unique inputs: {stats['unique_inputs']}")
    print(f"Average message length: {stats['avg_length']:.1f} chars")
    print(f"Min message length: {stats['min_length']} chars")
    print(f"Max message length: {stats['max_length']} chars")
    print("\nSamples by label:")
    for label, count in sorted(stats["by_label"].items()):
        print(f"  {label}: {count}")

    output_file = "insider_threat_training_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Dataset saved to: {output_file}")

    jsonl_file = "insider_threat_training_data.jsonl"
    with open(jsonl_file, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"[OK] JSONL version saved to: {jsonl_file}")

    print("\n" + "=" * 60)
    print("Sample entries:")
    print("=" * 60)
    for i, item in enumerate(random.sample(dataset, 5)):
        print(f"\n[{i+1}] Label: {item['output']}")
        print(f"    Input: {item['input'][:100]}{'...' if len(item['input']) > 100 else ''}")

if __name__ == "__main__":
    main()
