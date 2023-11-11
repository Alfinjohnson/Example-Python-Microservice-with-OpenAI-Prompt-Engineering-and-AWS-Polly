from datetime import datetime

AWS_ACCESS_KEY: str = 'AWS_ACCESS_KEY'
AWS_SEC_KEY: str = 'AWS_SEC_KEY'
DRAFT_TOPIC: str = 'draft'
SAVED_TOPIC: str = 'saved'
S3_BUCKET: str = 'dev-ai-2'


def get_current_date():
    return str(datetime.now().strftime('%d-%m-%Y'))
