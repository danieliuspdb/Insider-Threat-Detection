from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class EmailEvent:
    timestamp: datetime
    sender: str
    recipient: str
    subject: str
    body: str
    body_size: int
    attachment_count: int
    attachment_total_size: int
    attachment_names: List[str] = field(default_factory=list)
    is_external: bool = False

    @property
    def total_size(self):
        return self.body_size + self.attachment_total_size


@dataclass
class UserProfile:
    user: str
    total_emails: int = 0
    total_data_sent: int = 0
    external_emails: int = 0
    internal_emails: int = 0
    emails_with_attachments: int = 0
    total_attachment_size: int = 0
    avg_email_size: float = 0.0
    avg_body_size: float = 0.0
    unique_recipients: set = field(default_factory=set)
    email_events: List[EmailEvent] = field(default_factory=list)

    def update(self, event: EmailEvent):
        self.email_events.append(event)
        self.total_emails += 1
        self.total_data_sent += event.total_size

        if event.is_external:
            self.external_emails += 1
        else:
            self.internal_emails += 1

        if event.attachment_count > 0:
            self.emails_with_attachments += 1
            self.total_attachment_size += event.attachment_total_size

        self.unique_recipients.add(event.recipient)

        if self.total_emails > 0:
            self.avg_email_size = self.total_data_sent / self.total_emails
            total_body_size = sum(e.body_size for e in self.email_events)
            self.avg_body_size = total_body_size / self.total_emails


@dataclass
class DetectionResult:
    rule_name: str
    triggered: bool
    score: int
    description: str
    details: dict = field(default_factory=dict)


@dataclass
class Alert:
    user: str
    total_score: int
    risk_level: str 
    triggered_rules: List[DetectionResult]
    profile: UserProfile
    timestamp: datetime = field(default_factory=datetime.now)

    def get_explanation(self) -> str:
        lines = [
            f"=" * 70,
            f"ALERT: {self.risk_level} RISK - User: {self.user}",
            f"Total Risk Score: {self.total_score}",
            f"Timestamp: {self.timestamp}",
            f"=" * 70,
            f"\nTriggered Rules ({len(self.triggered_rules)}):",
        ]

        for result in sorted(self.triggered_rules, key=lambda x: x.score, reverse=True):
            lines.append(f"\n[+{result.score}] {result.rule_name}")
            lines.append(f"    {result.description}")
            if result.details:
                for key, value in result.details.items():
                    lines.append(f"    - {key}: {value}")

        lines.extend([
            f"\nUser Profile Summary:",
            f"  Total emails sent: {self.profile.total_emails}",
            f"  Total data sent: {self.profile.total_data_sent:,} bytes",
            f"  External emails: {self.profile.external_emails}",
            f"  Emails with attachments: {self.profile.emails_with_attachments}",
            f"  Unique recipients: {len(self.profile.unique_recipients)}",
            "=" * 70
        ])

        return "\n".join(lines)
