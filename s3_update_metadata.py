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
        if obj.key.endswith('.json'):
          print('file name', obj.key)
          s3_obj = s3.Object(bucketName, obj.key)
          fileData = obj.get()['Body'].read().decode('utf-8')
          print(fileData)
          s3_obj.metadata.update({'processed':'true'})
          updateMetadata(s3_obj)
        

    print(bucket)
    print('*'*25)
    
def updateMetadata(obj):
    try:
        obj.copy_from(CopySource={'Bucket': bucketName, 'Key': 'tobeprocessed/file1.json'},
            Metadata=obj.metadata, MetadataDirective='REPLACE')
    except Exception as e:
        print(str(e))
def addNewMetadata(obj, m):
    try:
        obj.copy_from(CopySource={'Bucket': bucketName, 'Key': 'tobeprocessed/file1.json'},
            Metadata=m, MetadataDirective='REPLACE')
    except Exception as e:
        print(str(e))

lambda_handler()