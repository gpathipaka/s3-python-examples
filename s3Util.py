#update Metadata
def updateMetadata(obj, bucketName):
    try:
        obj.metadata.update({'processed':'true'})
        obj.copy_from(CopySource={'Bucket': bucketName, 'Key': obj.key},
            Metadata=obj.metadata, MetadataDirective='REPLACE')
    except Exception as e:
        print(str(e))

def moveToRDS(data):
    print(data)

def moveObjToNewFolder(obj, bucketName, targetFolder, s3):
    try:
      copy_source={
        'Bucket':bucketName,
        'Key':obj.key
        }
      targetKey = obj.key.partition('/')[2]
      targetKey = targetFolder + '/' + targetKey
      s3.meta.client.copy(copy_source, bucketName, targetKey)       
    except Exception as e:
        print(str(e))

def deleteObjectFromSourceFolder(obj):
    obj.delete()
