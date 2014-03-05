from firebase import firebase
import os
import datetime
import json
import logging
from boto.s3.connection import S3Connection
from boto.s3.key import Key

## FIREBASE ACCESS INFO ##
firebase_url = 'https://your-app.firebaseio.com/' #Or get from environment variable
firebase_secret = os.environ['FIREBASE_SECRET']
firebase_username = 'my-backup-app' #Username is not actually checked on firebase

## AWS S3 ACCESS INFO ##
# Do not store keys in version control
s3_key = os.environ['AWS_ACCESS_KEY_ID']
s3_secret = os.environ['AWS_SECRET_ACCESS_KEY']
s3_bucket = os.environ['AWS_BUCKET']

# Set logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_firebase():
    f = firebase.FirebaseApplication(firebase_url, None)
    
    #Use secret to access ALL data!i
    # Adjust based on your access requirements.
    f.authentication = firebase.FirebaseAuthentication(firebase_secret, firebase_username, admin=True)
    return f

logger.info('Starting firebase data backup now...')

#Use UTC time in key name
now = datetime.datetime.utcnow()
name = 'firebase_' + now.strftime('%Y-%m-%d--%H-%M-%S.%f') + '.json' 

f = connect_firebase()
data = f.get('/', None)

logging.info('Saving data as s3 object %s' % name)

s3 = S3Connection(s3_key, s3_secret)
bucket = s3.get_bucket(s3_bucket)
k = Key(bucket)
k.key = name

#Save key with json data to S3
k.set_contents_from_string(unicode(json.dumps(data, ensure_ascii=False)))

logger.info('Done.')
