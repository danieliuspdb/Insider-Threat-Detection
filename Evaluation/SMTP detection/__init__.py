from .detector import SMTPDetector, detect_from_logs
from .models import EmailEvent, UserProfile, Alert, DetectionResult
from . import config, rules, utils

__version__ = "1.0.0"
__all__ = ['SMTPDetector', 'detect_from_logs', 'EmailEvent', 'UserProfile', 'Alert', 'DetectionResult']
