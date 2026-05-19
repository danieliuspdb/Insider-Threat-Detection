from typing import List, Dict
from datetime import datetime
from collections import defaultdict

from models import EmailEvent, UserProfile, Alert, DetectionResult
from config import ALERT_THRESHOLDS
import rules


class SMTPDetector:

    def __init__(self):
        self.user_profiles: Dict[str, UserProfile] = {}
        self.alerts: List[Alert] = []

    def load_events(self, events: List[EmailEvent]):
        print(f"Loading {len(events)} email events...")

        for event in events:
            if event.sender not in self.user_profiles:
                self.user_profiles[event.sender] = UserProfile(user=event.sender)

            self.user_profiles[event.sender].update(event)

        print(f"Built profiles for {len(self.user_profiles)} users")

    def analyze_user(self, user: str) -> Alert:
        if user not in self.user_profiles:
            raise ValueError(f"User {user} not found in profiles")

        profile = self.user_profiles[user]

        triggered_rules = []
        total_score = 0

        for rule_func in rules.ALL_RULES:
            result = rule_func(profile)
            if result.triggered:
                triggered_rules.append(result)
                total_score += result.score

        risk_level = self._get_risk_level(total_score)

        alert = Alert(
            user=user,
            total_score=total_score,
            risk_level=risk_level,
            triggered_rules=triggered_rules,
            profile=profile,
            timestamp=datetime.now()
        )

        return alert

    def analyze_all(self) -> List[Alert]:
        self.alerts = []

        for user in self.user_profiles:
            alert = self.analyze_user(user)

            if alert.total_score >= ALERT_THRESHOLDS['LOW']:
                self.alerts.append(alert)

        self.alerts.sort(key=lambda a: a.total_score, reverse=True)

        print(f"Generated {len(self.alerts)} alerts")
        return self.alerts

    def _get_risk_level(self, score: int) -> str:
        """Determine risk level based on score"""
        if score >= ALERT_THRESHOLDS['CRITICAL']:
            return 'CRITICAL'
        elif score >= ALERT_THRESHOLDS['HIGH']:
            return 'HIGH'
        elif score >= ALERT_THRESHOLDS['MEDIUM']:
            return 'MEDIUM'
        elif score >= ALERT_THRESHOLDS['LOW']:
            return 'LOW'
        else:
            return 'NONE'

    def get_summary(self) -> Dict:
        if not self.alerts:
            return {
                'total_users_analyzed': len(self.user_profiles),
                'alerts_generated': 0,
                'risk_breakdown': {}
            }

        risk_breakdown = defaultdict(int)
        for alert in self.alerts:
            risk_breakdown[alert.risk_level] += 1

        return {
            'total_users_analyzed': len(self.user_profiles),
            'alerts_generated': len(self.alerts),
            'risk_breakdown': dict(risk_breakdown),
            'highest_score': self.alerts[0].total_score if self.alerts else 0,
            'top_user': self.alerts[0].user if self.alerts else None
        }

    def print_summary(self):
        summary = self.get_summary()

        print(f"Total users analyzed: {summary['total_users_analyzed']}")
        print(f"Alerts generated: {summary['alerts_generated']}")

        if summary['risk_breakdown']:
            print("\nRisk Level Breakdown:")
            for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                count = summary['risk_breakdown'].get(level, 0)
                if count > 0:
                    print(f"  {level}: {count}")

        if summary.get('top_user'):
            print(f"\nHighest risk user: {summary['top_user']} (score: {summary['highest_score']})")

        print("=" * 70)

    def print_alerts(self, top_n: int = None):
        alerts_to_print = self.alerts[:top_n] if top_n else self.alerts

        for alert in alerts_to_print:
            print("\n" + alert.get_explanation())

    def export_alerts(self, filepath: str):
        with open(filepath, 'w') as f:
            f.write("REPORT\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Total Alerts: {len(self.alerts)}\n")
            f.write("=" * 70 + "\n\n")

            for alert in self.alerts:
                f.write(alert.get_explanation())
                f.write("\n\n")

        print(f"\nAlerts exported to: {filepath}")


def detect_from_logs(events: List[EmailEvent], print_results: bool = True) -> List[Alert]:
    detector = SMTPDetector()
    detector.load_events(events)
    alerts = detector.analyze_all()

    if print_results:
        detector.print_summary()

    return alerts


if __name__ == "__main__":
    print("SMTP")