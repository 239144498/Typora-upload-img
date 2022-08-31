import logging
import os
import sys
import time
from threading import Thread

import boto3
from botocore.exceptions import ClientError


s3 = boto3.resource(
    service_name='s3',
    aws_access_key_id='xxxxx',
    aws_secret_access_key='xxxxxx',
    endpoint_url='https://s3.tebi.io'
)


def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        with open(file_name, 'rb') as f:
            s3.Bucket(bucket).put_object(Key=object_name, Body=f.read())
            print("http://修改为你的桶名.datastream.tebi.io/" + object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == '__main__':
    filename = sys.argv
    threads = []
    for i in range(1, len(filename)):
        print(filename[i])
        t = Thread(target=upload_file, args=(filename[i], "你的桶名"))
        threads.append(t)
    for t in threads:
        t.start()
        time.sleep(0.3)
    for t in threads:
        t.join()
    print("上传完成")
