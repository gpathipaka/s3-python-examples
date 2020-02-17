import json
import boto3
bucketName='gp-aws-bucket-1'
sourceFolder='tobeprocessed'
targetFolder='processed'

import s3Util as s3util
        
def lambda_handler():
    print('*'*25)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketName)
    print(bucketName)
    for obj in bucket.objects.filter(Prefix=sourceFolder):
        #print('file name', obj.key)
        if obj.key.endswith('.json'):
          s3_obj = s3.Object(bucketName, obj.key)
          print(s3_obj.key)
          if s3_obj.metadata['processed'] == 'true':
              print('Skipping...')
              continue
          
          s3util.updateMetadata(s3_obj, bucketName)

          #step 2
          fileData = obj.get()['Body'].read().decode('utf-8')
          data = json.loads(fileData)
          s3util.moveToRDS(data)

          # step 3 move to new folder
          s3util.moveObjToNewFolder(s3_obj, bucketName, targetFolder, s3)

          # step 4 delete from current folder
          s3util.deleteObjectFromSourceFolder(s3_obj)


          

    print('*'*25)





lambda_handler()