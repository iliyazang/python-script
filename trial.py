#!/usr/bin/python

import boto3
import os 

extensions_list = ['.xlsx', '.xls', '.csv', '.txt']
'''Script to delete buckets from your account and delete the objects from the account'''
s3 = boto3.client('s3')
def list_buckets():
    '''
    This function makes a call to the BOTO3 API and grabs the list of Buckets. There's a Key named 'Buckets'. 'Buckets' holds information about
    about the name of the buckets that have been created in AWS. 
    '''
    try:
        return [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
    except Exception as e:
        print(f"Error listing buckets: {e}")
        return []

def delete_objects_in_buckets(bucket_names):
    '''
    delete_objects_in_buckets function checks if you have any object in that function. AWS would not delete a bucket if there's information on there so
    we make an API call to see if there are any items in that bucket. We use two different methods here. client.list_objects_v2 returns with a list of objects.
    In its response attribute, we check to see if 'Contents' exist. Contents contains a list of dictionary about the metadata of the object file. We are going to grab  'Contents[0][Key]' from 'Contents' and pass it in as key-word arguments into a second method 'client.delete_objects()'. Refer to this link
    to see more details about the response syntax https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html
    '''
    try:
        for name in bucket_names:
            response = s3.list_objects_v2(Bucket=name)
            if 'Contents' in response:
                objects = [obj['Key'] for obj in response['Contents']]
                print(f"Objects in bucket '{name}': {objects}")  # Debugging
                objects_to_delete = [os.path.basename(obj) for obj in objects if os.path.splitext(os.path.basename(obj))[-1] in extensions_list]
                if objects_to_delete:
                    objects_to_delete= [{'Key': obj} for obj in objects_to_delete]
                    s3.delete_objects(Bucket=name, Delete={'Objects': objects_to_delete})
    except Exception as e:
        print(f"Error deleting objects: {e}")


def delete_buckets(bucket_names):
    '''
    This function deletes the empty buckets and catches an exception if there's an error on  why it can't delete the bucket. 
    '''
    try:
        for name in bucket_names:
            response = s3.list_objects_v2(Bucket=name)
            if 'Contents' not in response:
                s3.delete_bucket(Bucket=name)
    except Exception as e:
        print(f"Error deleting buckets: {e}")

if __name__ == '__main__':
    #Passing list_buckets() function as an argument. 
    bucket_names = list_buckets()
    # If bucket_names is True i.e. list is not empty. Run the following functions below. Otherwise, execute the code inside the 'else' block.
    if bucket_names:
        delete_objects_in_buckets(bucket_names)
        delete_buckets(bucket_names)
        print('All buckets and objects have been deleted')
    else:
        print('No buckets found to delete')
        

    
