from typing import List
from models import UserProfile, EmailEvent, DetectionResult
from config import (
    VOLUME_THRESHOLDS, SIMILARITY_THRESHOLDS, ENTROPY_THRESHOLDS,
    ATTACHMENT_THRESHOLDS, SMTP_BEHAVIOR, EXFILTRATION_THRESHOLDS, RULE_SCORES
)
from utils import (
    calculate_entropy, jaccard_similarity, detect_base64_pattern,
    is_off_hours, calculate_coefficient_of_variation, group_by_time_window,
    detect_sequential_pattern, find_time_clusters, is_human_readable
)


def check_high_volume(profile: UserProfile) -> DetectionResult:
    threshold = VOLUME_THRESHOLDS['high_volume_threshold']
    triggered = profile.total_emails > threshold

    return DetectionResult(
        rule_name="High Volume",
        triggered=triggered,
        score=RULE_SCORES['high_volume'] if triggered else 0,
        description=f"Sent {profile.total_emails} emails (threshold: {threshold})",
        details={'email_count': profile.total_emails, 'threshold': threshold}
    )


def check_burst_sending(profile: UserProfile) -> DetectionResult:
    burst_threshold = VOLUME_THRESHOLDS['burst_threshold']
    burst_window = VOLUME_THRESHOLDS['burst_window_minutes']

    timestamps = [e.timestamp for e in profile.email_events]
    clusters = find_time_clusters(timestamps, max_gap_minutes=5)

    max_burst = max(len(cluster) for cluster in clusters) if clusters else 0
    triggered = max_burst >= burst_threshold

    return DetectionResult(
        rule_name="Burst Sending",
        triggered=triggered,
        score=RULE_SCORES['burst_sending'] if triggered else 0,
        description=f"Burst of {max_burst} emails in {burst_window}min window",
        details={'max_burst': max_burst, 'threshold': burst_threshold}
    )


def check_sustained_high_rate(profile: UserProfile) -> DetectionResult:
    if not profile.email_events:
        return DetectionResult("Sustained High Rate", False, 0, "No emails")

    threshold = VOLUME_THRESHOLDS['sustained_rate_threshold']
    duration_hours = VOLUME_THRESHOLDS['sustained_duration_hours']

    timestamps = sorted([e.timestamp for e in profile.email_events])
    time_span_hours = (timestamps[-1] - timestamps[0]).total_seconds() / 3600

    if time_span_hours < duration_hours:
        return DetectionResult("Sustained High Rate", False, 0, "Insufficient time span")

    emails_per_hour = profile.total_emails / time_span_hours
    triggered = emails_per_hour >= threshold

    return DetectionResult(
        rule_name="Sustained High Rate",
        triggered=triggered,
        score=RULE_SCORES['sustained_high_rate'] if triggered else 0,
        description=f"Sent {emails_per_hour:.1f} emails/hour over {time_span_hours:.1f}h",
        details={'rate': emails_per_hour, 'threshold': threshold}
    )


def check_similar_bodies(profile: UserProfile) -> DetectionResult:
    threshold = SIMILARITY_THRESHOLDS['body_similarity_threshold']
    min_similar = SIMILARITY_THRESHOLDS['min_similar_emails']

    bodies = [e.body for e in profile.email_events if e.body]
    if len(bodies) < min_similar:
        return DetectionResult("Similar Bodies", False, 0, "Insufficient emails")

    similar_count = 0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            similarity = jaccard_similarity(bodies[i], bodies[j])
            if similarity >= threshold:
                similar_count += 1

    triggered = similar_count >= min_similar
    similarity_ratio = similar_count / (len(bodies) * (len(bodies) - 1) / 2) if len(bodies) > 1 else 0

    return DetectionResult(
        rule_name="Similar Bodies",
        triggered=triggered,
        score=RULE_SCORES['similar_bodies'] if triggered else 0,
        description=f"Found {similar_count} similar email pairs ({similarity_ratio:.1%} similarity)",
        details={'similar_pairs': similar_count, 'threshold': min_similar}
    )


def check_consistent_sizes(profile: UserProfile) -> DetectionResult:
    min_emails = SIMILARITY_THRESHOLDS['min_emails_for_consistency']
    cv_threshold = SIMILARITY_THRESHOLDS['size_consistency_threshold']

    if profile.total_emails < min_emails:
        return DetectionResult("Consistent Sizes", False, 0, "Insufficient emails")

    sizes = [e.total_size for e in profile.email_events if e.total_size > 0]
    if not sizes:
        return DetectionResult("Consistent Sizes", False, 0, "No email sizes")

    cv = calculate_coefficient_of_variation(sizes)
    triggered = cv <= (1 - cv_threshold)

    return DetectionResult(
        rule_name="Consistent Sizes",
        triggered=triggered,
        score=RULE_SCORES['consistent_sizes'] if triggered else 0,
        description=f"Email sizes highly consistent (CV={cv:.3f}, very low variation)",
        details={'coefficient_of_variation': cv, 'threshold': 1 - cv_threshold}
    )


def check_high_entropy(profile: UserProfile) -> DetectionResult:
    threshold = ENTROPY_THRESHOLDS['high_entropy_threshold']
    min_size = ENTROPY_THRESHOLDS['min_body_size_for_entropy']
    suspicious_count = ENTROPY_THRESHOLDS['suspicious_entropy_count']

    high_entropy_emails = 0
    for event in profile.email_events:
        if event.body_size >= min_size:
            entropy = calculate_entropy(event.body)
            if entropy >= threshold:
                high_entropy_emails += 1

    triggered = high_entropy_emails >= suspicious_count

    return DetectionResult(
        rule_name="High Entropy Content",
        triggered=triggered,
        score=RULE_SCORES['high_entropy_content'] if triggered else 0,
        description=f"{high_entropy_emails} emails with high entropy (>={threshold})",
        details={'high_entropy_count': high_entropy_emails, 'threshold': suspicious_count}
    )


def check_base64_pattern(profile: UserProfile) -> DetectionResult:
    threshold = ENTROPY_THRESHOLDS['base64_pattern_threshold']
    min_size = ENTROPY_THRESHOLDS['min_body_size_for_entropy']

    base64_emails = 0
    for event in profile.email_events:
        if event.body_size >= min_size:
            base64_ratio = detect_base64_pattern(event.body)
            if base64_ratio >= threshold:
                base64_emails += 1

    triggered = base64_emails >= 3

    return DetectionResult(
        rule_name="Base64 Pattern",
        triggered=triggered,
        score=RULE_SCORES['base64_pattern'] if triggered else 0,
        description=f"{base64_emails} emails with base64-like patterns",
        details={'base64_count': base64_emails}
    )


def check_non_readable_payload(profile: UserProfile) -> DetectionResult:
    non_readable_count = 0
    for event in profile.email_events:
        if event.body and not is_human_readable(event.body):
            non_readable_count += 1

    triggered = non_readable_count >= 5

    return DetectionResult(
        rule_name="Non-Readable Payload",
        triggered=triggered,
        score=RULE_SCORES['non_readable_payload'] if triggered else 0,
        description=f"{non_readable_count} emails with non-human readable content",
        details={'non_readable_count': non_readable_count}
    )


def check_sudden_large_attachments(profile: UserProfile) -> DetectionResult:
    large_size = ATTACHMENT_THRESHOLDS['large_attachment_size']
    threshold = ATTACHMENT_THRESHOLDS['sudden_attachment_threshold']

    large_attachment_emails = sum(
        1 for e in profile.email_events
        if e.attachment_total_size >= large_size
    )

    triggered = large_attachment_emails >= threshold

    return DetectionResult(
        rule_name="Sudden Large Attachments",
        triggered=triggered,
        score=RULE_SCORES['sudden_large_attachments'] if triggered else 0,
        description=f"{large_attachment_emails} emails with large attachments (>={large_size/1024/1024:.1f}MB)",
        details={'large_attachment_count': large_attachment_emails, 'threshold': threshold}
    )


def check_similar_attachments(profile: UserProfile) -> DetectionResult:
    threshold = ATTACHMENT_THRESHOLDS['similar_attachment_count']
    tolerance = ATTACHMENT_THRESHOLDS['attachment_size_tolerance']

    attachment_sizes = [
        e.attachment_total_size for e in profile.email_events
        if e.attachment_total_size > 0
    ]

    if len(attachment_sizes) < threshold:
        return DetectionResult("Similar Attachments", False, 0, "Insufficient attachments")

    is_similar = detect_sequential_pattern(attachment_sizes, tolerance)
    triggered = is_similar and len(attachment_sizes) >= threshold

    return DetectionResult(
        rule_name="Similar Attachments",
        triggered=triggered,
        score=RULE_SCORES['similar_attachments'] if triggered else 0,
        description=f"{len(attachment_sizes)} similarly-sized attachments detected",
        details={'attachment_count': len(attachment_sizes), 'threshold': threshold}
    )


def check_high_attachment_volume(profile: UserProfile) -> DetectionResult:
    threshold = ATTACHMENT_THRESHOLDS['total_attachment_volume']
    triggered = profile.total_attachment_size >= threshold

    return DetectionResult(
        rule_name="High Attachment Volume",
        triggered=triggered,
        score=RULE_SCORES['high_attachment_volume'] if triggered else 0,
        description=f"Total attachments: {profile.total_attachment_size/1024/1024:.1f}MB (threshold: {threshold/1024/1024:.1f}MB)",
        details={'total_mb': profile.total_attachment_size/1024/1024, 'threshold_mb': threshold/1024/1024}
    )


def check_high_external_ratio(profile: UserProfile) -> DetectionResult:
    min_emails = SMTP_BEHAVIOR['min_emails_for_ratio']
    threshold = SMTP_BEHAVIOR['external_ratio_threshold']

    if profile.total_emails < min_emails:
        return DetectionResult("High External Ratio", False, 0, "Insufficient emails")

    external_ratio = profile.external_emails / profile.total_emails
    triggered = external_ratio >= threshold

    return DetectionResult(
        rule_name="High External Ratio",
        triggered=triggered,
        score=RULE_SCORES['high_external_ratio'] if triggered else 0,
        description=f"{external_ratio:.1%} of emails sent to external recipients",
        details={'external_ratio': external_ratio, 'threshold': threshold}
    )


def check_off_hours_activity(profile: UserProfile) -> DetectionResult:
    start_hour = SMTP_BEHAVIOR['off_hours_start']
    end_hour = SMTP_BEHAVIOR['off_hours_end']
    threshold = SMTP_BEHAVIOR['off_hours_threshold']

    off_hours_count = sum(
        1 for e in profile.email_events
        if is_off_hours(e.timestamp, start_hour, end_hour)
    )

    triggered = off_hours_count >= threshold

    return DetectionResult(
        rule_name="Off-Hours Activity",
        triggered=triggered,
        score=RULE_SCORES['off_hours_activity'] if triggered else 0,
        description=f"{off_hours_count} emails sent during off-hours ({start_hour}:00-{end_hour}:00)",
        details={'off_hours_count': off_hours_count, 'threshold': threshold}
    )


def check_low_recipient_diversity(profile: UserProfile) -> DetectionResult:
    threshold = SMTP_BEHAVIOR['recipient_diversity_low']
    recipient_count = len(profile.unique_recipients)

    triggered = recipient_count <= threshold and profile.total_emails >= 10

    return DetectionResult(
        rule_name="Low Recipient Diversity",
        triggered=triggered,
        score=RULE_SCORES['low_recipient_diversity'] if triggered else 0,
        description=f"Only {recipient_count} unique recipients for {profile.total_emails} emails",
        details={'unique_recipients': recipient_count, 'total_emails': profile.total_emails}
    )


def check_data_chunking(profile: UserProfile) -> DetectionResult:
    threshold = EXFILTRATION_THRESHOLDS['chunking_threshold']
    time_window = EXFILTRATION_THRESHOLDS['chunking_time_window']
    tolerance = EXFILTRATION_THRESHOLDS['chunking_size_tolerance']

    groups = group_by_time_window(
        profile.email_events,
        time_window,
        lambda e: e.timestamp
    )

    max_sequential = 0
    for group in groups:
        if len(group) >= threshold:
            sizes = [e.total_size for e in group]
            if detect_sequential_pattern(sizes, tolerance):
                max_sequential = max(max_sequential, len(group))

    triggered = max_sequential >= threshold

    return DetectionResult(
        rule_name="Data Chunking",
        triggered=triggered,
        score=RULE_SCORES['data_chunking'] if triggered else 0,
        description=f"{max_sequential} sequential similar-sized emails detected (chunking pattern)",
        details={'sequential_count': max_sequential, 'threshold': threshold}
    )


def check_rapid_accumulation(profile: UserProfile) -> DetectionResult:
    threshold = EXFILTRATION_THRESHOLDS['data_accumulation_threshold']
    time_window = EXFILTRATION_THRESHOLDS['accumulation_window_minutes']

    groups = group_by_time_window(
        profile.email_events,
        time_window,
        lambda e: e.timestamp
    )

    max_volume = 0
    for group in groups:
        volume = sum(e.total_size for e in group)
        max_volume = max(max_volume, volume)

    triggered = max_volume >= threshold

    return DetectionResult(
        rule_name="Rapid Data Accumulation",
        triggered=triggered,
        score=RULE_SCORES['rapid_accumulation'] if triggered else 0,
        description=f"{max_volume/1024/1024:.1f}MB sent in {time_window}min window",
        details={'max_mb': max_volume/1024/1024, 'threshold_mb': threshold/1024/1024}
    )


def check_repetitive_payload(profile: UserProfile) -> DetectionResult:
    threshold = EXFILTRATION_THRESHOLDS['repetitive_pattern_count']

    similar_pattern_count = 0
    bodies = [e.body for e in profile.email_events if e.body]

    if len(bodies) < threshold:
        return DetectionResult("Repetitive Payload", False, 0, "Insufficient emails")

    for i in range(len(bodies) - 1):
        if jaccard_similarity(bodies[i], bodies[i+1]) >= 0.7:
            similar_pattern_count += 1

    triggered = similar_pattern_count >= threshold

    return DetectionResult(
        rule_name="Repetitive Payload",
        triggered=triggered,
        score=RULE_SCORES['repetitive_payload'] if triggered else 0,
        description=f"{similar_pattern_count} consecutive emails with repetitive patterns",
        details={'repetitive_count': similar_pattern_count, 'threshold': threshold}
    )


ALL_RULES = [
    check_high_volume,
    check_burst_sending,
    check_sustained_high_rate,
    check_similar_bodies,
    check_consistent_sizes,
    check_high_entropy,
    check_base64_pattern,
    check_non_readable_payload,
    check_sudden_large_attachments,
    check_similar_attachments,
    check_high_attachment_volume,
    check_high_external_ratio,
    check_off_hours_activity,
    check_low_recipient_diversity,
    check_data_chunking,
    check_rapid_accumulation,
    check_repetitive_payload
]
