import json
import boto3
bucketName='gp-aws-bucket-1'
objKey='file1.json'
prefix='tobeprocessed'
def lambda_handler():
    print('*'*25)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix=prefix):
        print(obj.key)
        fileData = obj.get()['Body'].read().decode('utf-8')
        print(fileData)
        #obj.metadata.update({'processed':'true'})
        m={}
        m['processed'] = 'false'
        updateMetadata(obj, m)
        

    print(bucket)
    print('*'*25)
    
def updateMetadata(obj, m):
    try:
        obj.copy_from(CopySource={'Bucket': bucketName, 'Key': 'tobeprocessed/file1.json'},
            Metadata=m, MetadataDirective='REPLACE')
    except Exception as e:
        print(str(e))

lambda_handler()