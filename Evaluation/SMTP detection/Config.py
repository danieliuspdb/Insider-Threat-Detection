
ALERT_THRESHOLDS = {
    'LOW': 6,      
    'MEDIUM': 10,  
    'HIGH': 15,   
    'CRITICAL': 20 
}

VOLUME_THRESHOLDS = {
    'high_volume_threshold': 50,  
    'time_window_minutes': 60, 
    'burst_threshold': 20,      
    'burst_window_minutes': 10,  
    'sustained_rate_threshold': 100, 
    'sustained_duration_hours': 2    
}

SIMILARITY_THRESHOLDS = {
    'body_similarity_threshold': 0.95,  
    'min_similar_emails': 10,           
    'size_consistency_threshold': 0.95, 
    'min_emails_for_consistency': 15    
}

ENTROPY_THRESHOLDS = {
    'high_entropy_threshold': 5.0,      
    'base64_pattern_threshold': 0.9,   
    'min_body_size_for_entropy': 500,  
    'suspicious_entropy_count': 5       
}

ATTACHMENT_THRESHOLDS = {
    'large_attachment_size': 5 * 1024 * 1024,  
    'sudden_attachment_threshold': 3,           
    'similar_attachment_count': 5,              
    'attachment_size_tolerance': 0.1,           
    'total_attachment_volume': 50 * 1024 * 1024 
}

SMTP_BEHAVIOR = {
    'external_ratio_threshold': 0.9,    
    'min_emails_for_ratio': 15,       
    'off_hours_start': 22,              
    'off_hours_end': 6,               
    'off_hours_threshold': 15,         
    'recipient_diversity_low': 2       
}

EXFILTRATION_THRESHOLDS = {
    'chunking_threshold': 12,         
    'chunking_time_window': 30,        
    'chunking_size_tolerance': 0.10,    
    'data_accumulation_threshold': 20 * 1024 * 1024, 
    'accumulation_window_minutes': 60,  
    'repetitive_pattern_count': 8     
}

RULE_SCORES = {
    'high_volume': 2,
    'burst_sending': 3,
    'sustained_high_rate': 3,

    'similar_bodies': 2,
    'consistent_sizes': 2,
    'uniform_structure': 1,

    'high_entropy_content': 3,
    'base64_pattern': 3,
    'non_readable_payload': 2,

    'sudden_large_attachments': 3,
    'similar_attachments': 2,
    'high_attachment_volume': 3,

    'high_external_ratio': 2,
    'off_hours_activity': 2,
    'low_recipient_diversity': 1,

    'data_chunking': 4,
    'rapid_accumulation': 4,
    'repetitive_payload': 3
}

BASELINE_CONFIG = {
    'normal_emails_per_day': 20,
    'normal_external_ratio': 0.3,
    'normal_attachment_ratio': 0.2,
    'normal_avg_email_size': 50 * 1024  
}
