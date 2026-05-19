import json
import sys
import os
from datetime import datetime
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import EmailEvent
from detector import SMTPDetector


def load_emails_from_json(filepath: str) -> List[EmailEvent]:
    with open(filepath, 'r') as f:
        data = json.load(f)

    events = []
    for item in data:
        event = EmailEvent(
            timestamp=datetime.fromisoformat(item['timestamp']),
            sender=item['sender'],
            recipient=item['recipient'],
            subject=item['subject'],
            body=item['body'],
            body_size=item['body_size'],
            attachment_count=item['attachment_count'],
            attachment_total_size=item['attachment_total_size'],
            attachment_names=item['attachment_names'],
            is_external=item['is_external']
        )
        events.append(event)

    return events


def run_test(name: str, events: List[EmailEvent], expected_attackers: List[str] = None):
    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)

    detector = SMTPDetector()
    detector.load_events(events)
    alerts = detector.analyze_all()

    detector.print_summary()

    top_n = 3 if len(alerts) > 10 else 5
    if len(alerts) > 0:
        print(f"\nTop {min(top_n, len(alerts))} Alerts:")
        detector.print_alerts(top_n=top_n)

    if expected_attackers:
        print("\n" + "-" * 70)
        print("EVALUATION")
        print("-" * 70)

        detected_users = {alert.user for alert in alerts}
        expected_set = set(expected_attackers)

        true_positives = detected_users & expected_set
        false_positives = detected_users - expected_set
        false_negatives = expected_set - detected_users

        print(f"Expected attackers: {expected_attackers}")
        print(f"Detected users: {list(detected_users)}")
        print(f"\nTrue Positives: {len(true_positives)} - {list(true_positives)}")
        print(f"False Positives: {len(false_positives)} - {list(false_positives)}")
        print(f"False Negatives: {len(false_negatives)} - {list(false_negatives)}")

        if len(expected_set) > 0:
            recall = len(true_positives) / len(expected_set) * 100
            print(f"\nRecall: {recall:.1f}% ({len(true_positives)}/{len(expected_set)} attackers caught)")

        if len(detected_users) > 0:
            precision = len(true_positives) / len(detected_users) * 100
            print(f"Precision: {precision:.1f}% ({len(true_positives)}/{len(detected_users)} correct)")

        print("\n" + "-" * 70)
        print("RISK LEVEL BREAKDOWN")
        print("-" * 70)

        attacker_risk_levels = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'NONE': 0}
        non_attacker_risk_levels = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'NONE': 0}

        for alert in alerts:
            if alert.user in expected_set:
                attacker_risk_levels[alert.risk_level] += 1
            else:
                non_attacker_risk_levels[alert.risk_level] += 1

        for attacker in expected_set:
            if attacker not in detected_users:
                attacker_risk_levels['NONE'] += 1

        all_users = set(detector.user_profiles.keys())
        non_attackers = all_users - expected_set
        for user in non_attackers:
            if user not in detected_users:
                non_attacker_risk_levels['NONE'] += 1

        print(f"\nAttackers ({len(expected_set)} total):")
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE']:
            count = attacker_risk_levels[level]
            pct = (count / len(expected_set) * 100) if len(expected_set) > 0 else 0
            print(f"  {level:8s}: {count:3d} ({pct:5.1f}%)")

        print(f"\nNon-Attackers ({len(non_attackers)} total):")
        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE']:
            count = non_attacker_risk_levels[level]
            pct = (count / len(non_attackers) * 100) if len(non_attackers) > 0 else 0
            print(f"  {level:8s}: {count:3d} ({pct:5.1f}%)")

    return alerts


def main():
    print("=" * 70)
    print("=" * 70)

    test_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n\n" + "#" * 70)
    print("#" * 70)

    normal_file = os.path.join(test_dir, "normal_emails.json")
    if os.path.exists(normal_file):
        normal_events = load_emails_from_json(normal_file)
        normal_alerts = run_test(
            "Normal Email Behavior (should have minimal alerts)",
            normal_events,
            expected_attackers=[]
        )

        print("\n" + "=" * 70)
        print(f"RESULT: {len(normal_alerts)} alerts from normal behavior")
        if len(normal_alerts) == 0:
            print("PASS: No false positives on normal behavior")
        else:
            print(f"WARNING: {len(normal_alerts)} false positives detected")
        print("=" * 70)
    else:
        print(f"File not found: {normal_file}")
        print("Run generate_test_data.py first!")

    print("\n\n" + "#" * 70)
    print("# TEST 2: ATTACK SCENARIOS (50 ATTACKERS)")
    print("#" * 70)

    attack_file = os.path.join(test_dir, "attack_emails.json")
    if os.path.exists(attack_file):
        attack_events = load_emails_from_json(attack_file)

        expected_attackers = []
        for i in range(1, 11):
            expected_attackers.append(f"attacker_tunnel{i}@company.com")
            expected_attackers.append(f"attacker_encoded{i}@company.com")
            expected_attackers.append(f"attacker_burst{i}@company.com")
            expected_attackers.append(f"attacker_attach{i}@company.com")
            expected_attackers.append(f"attacker_night{i}@company.com")

        attack_alerts = run_test(
            "Attack Scenarios (should detect all 50 attackers)",
            attack_events,
            expected_attackers=expected_attackers
        )

        detected_attackers = [a.user for a in attack_alerts if a.user in expected_attackers]

        print("\n" + "=" * 70)
        print(f"RESULT: {len(detected_attackers)}/50 attackers detected")
        if len(detected_attackers) == 50:
            print("PASS")
        else:
            print(f"PARTIAL: {50 - len(detected_attackers)} attackers missed")
        print("=" * 70)
    else:
        print(f"File not found: {attack_file}")

    print("\n\n" + "#" * 70)
    print("#" * 70)

    combined_file = os.path.join(test_dir, "combined_emails.json")
    if os.path.exists(combined_file):
        combined_events = load_emails_from_json(combined_file)

        expected_attackers = []
        for i in range(1, 11):
            expected_attackers.append(f"attacker_tunnel{i}@company.com")
            expected_attackers.append(f"attacker_encoded{i}@company.com")
            expected_attackers.append(f"attacker_burst{i}@company.com")
            expected_attackers.append(f"attacker_attach{i}@company.com")
            expected_attackers.append(f"attacker_night{i}@company.com")

        combined_alerts = run_test(
            "Combined Dataset (150 normal + 50 attackers)",
            combined_events,
            expected_attackers=expected_attackers
        )

        report_file = os.path.join(test_dir, "detection_report.txt")
        detector = SMTPDetector()
        detector.load_events(combined_events)
        detector.analyze_all()
        detector.export_alerts(report_file)

    else:
        print(f"File not found: {combined_file}")


if __name__ == "__main__":
    main()
