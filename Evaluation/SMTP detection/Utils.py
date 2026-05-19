import re
import math
from collections import Counter
from typing import List
from datetime import datetime, timedelta

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0

    counter = Counter(text)
    length = len(text)

    entropy = 0.0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def jaccard_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0

    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def detect_base64_pattern(text: str) -> float:
    if not text or len(text) < 20:
        return 0.0

    base64_chars = re.findall(r'[A-Za-z0-9+/=]', text)
    ratio = len(base64_chars) / len(text)

    has_padding = text.strip().endswith('=') or text.strip().endswith('==')

    if ratio > 0.9 and has_padding:
        return 1.0
    return ratio


def is_off_hours(timestamp: datetime, start_hour: int = 20, end_hour: int = 6) -> bool:
    hour = timestamp.hour
    if start_hour > end_hour: 
        return hour >= start_hour or hour < end_hour
    else:
        return start_hour <= hour < end_hour


def calculate_coefficient_of_variation(values: List[float]) -> float:
    if not values or len(values) < 2:
        return 0.0

    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0

    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = math.sqrt(variance)

    return std_dev / mean


def group_by_time_window(events: List, time_window_minutes: int, get_timestamp):
    if not events:
        return []

    sorted_events = sorted(events, key=get_timestamp)
    groups = []
    current_group = [sorted_events[0]]
    window_start = get_timestamp(sorted_events[0])

    for event in sorted_events[1:]:
        event_time = get_timestamp(event)
        if (event_time - window_start).total_seconds() <= time_window_minutes * 60:
            current_group.append(event)
        else:
            groups.append(current_group)
            current_group = [event]
            window_start = event_time

    if current_group:
        groups.append(current_group)

    return groups


def detect_sequential_pattern(sizes: List[int], tolerance: float = 0.15) -> bool:
    if len(sizes) < 3:
        return False

    similar_pairs = 0
    for i in range(len(sizes) - 1):
        if sizes[i] == 0 or sizes[i+1] == 0:
            continue

        ratio = min(sizes[i], sizes[i+1]) / max(sizes[i], sizes[i+1])
        if ratio >= (1 - tolerance):
            similar_pairs += 1

    return similar_pairs / (len(sizes) - 1) >= 0.7


def find_time_clusters(timestamps: List[datetime], max_gap_minutes: int = 5) -> List[List[datetime]]:
    if not timestamps:
        return []

    sorted_times = sorted(timestamps)
    clusters = []
    current_cluster = [sorted_times[0]]

    for ts in sorted_times[1:]:
        time_gap = (ts - current_cluster[-1]).total_seconds() / 60
        if time_gap <= max_gap_minutes:
            current_cluster.append(ts)
        else:
            clusters.append(current_cluster)
            current_cluster = [ts]

    if current_cluster:
        clusters.append(current_cluster)

    return clusters


def is_human_readable(text: str, min_words: int = 5) -> bool:
    if not text or len(text) < 20:
        return False

    words = re.findall(r'[a-zA-Z]{3,}', text)

    entropy = calculate_entropy(text)

    base64_ratio = detect_base64_pattern(text)

    return (
        len(words) >= min_words and
        3.0 <= entropy <= 5.5 and
        base64_ratio < 0.5
    )
