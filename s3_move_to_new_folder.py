import json
import boto3
bucketName='s3-aws-bucket-1'
objKey='file1.json'
prefix='tobeprocessed'
def lambda_handler():
    print('*'*25)
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    bucket = s3.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key.endswith('.json'):
          print('file name', obj.key)
          s3_obj = s3.Object(bucketName, obj.key)
          fileData = obj.get()['Body'].read().decode('utf-8')
          print(fileData)
          #print(s3_obj.metadata)
          #s3_obj.metadata.update({'processed':'true'})
          #updateMetadata(s3_obj)
          #moveObjToNewFolder(s3_obj)
          #s3.meta.client.copy()
          #moveObjToNewFolder(s3_obj, s3)
          #deleteS3Object(s3_obj)

    print(bucket)
    print('*'*25)

def deleteS3Object(obj):
  try:
      obj.delete()
  except Exception as e:
      print(str(e))

def moveObjToNewFolder(obj, s3):
    try:
      copy_source={
        'Bucket':bucketName,
        'Key':obj.key
        }
      targetKey = obj.key.partition('/')[2]
      targetKey = 'processed/' + targetKey
      s3.meta.client.copy(copy_source, bucketName, targetKey)       
    except Exception as e:
        print(str(e))


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