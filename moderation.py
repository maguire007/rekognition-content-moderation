import boto3
import json
import os

client = boto3.client('rekognition')
image_directory = "test-data"


def convert_img_to_bytes(file):
    with open(file, 'rb') as f:
        source_bytes = f.read()
    return source_bytes

def get_custom_labels(project_arn,filepath,min_confidence =1,max_results=5):

    response = client.detect_custom_labels(
        Image={
            'Bytes': convert_img_to_bytes(filepath)
        },
        ProjectVersionArn= project_arn,
        MinConfidence = min_confidence,
        MaxResults=max_results
    )

    json_object = json.dumps(response , indent=2)
    return json_object
    
def get_moderation_labels(filepath):

    response = client.detect_moderation_labels(
        Image={
            'Bytes': convert_img_to_bytes(filepath)
        }
    )

    json_object = json.dumps(response , indent=2)
    return json_object


def get_project_versions(project_number=0):
    # get the project arns
    response = client.describe_projects()
    project_arn = extract_values(response, 'ProjectArn')
    
    # get the versions for the first project
    response = client.describe_project_versions(ProjectArn= project_arn[project_number])
    version_arn = extract_values(response, 'ProjectVersionArn')

    return version_arn


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
    

for subdir, dirs, files in os.walk(image_directory):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".jpg") or filepath.endswith(".png") or filepath.endswith(".jpeg"):
            
        #Image moderation api
            json_object_mod=get_moderation_labels(filepath)
            
            
            json_object = json.loads(json_object_mod)
            labels = extract_values(json_object, 'Name')
            confidence = extract_values(json_object, 'Confidence')
 
            if labels:
                print(f"Moderation API: file: {filepath} has labels: {labels} with confidence of {confidence[0]}")
            else:
                print(f"Moderation API: file: {filepath} has no labels")
                
        # use the custom image label api to get all labels for each model in the project
            
            # get the project model arns
            version_arn = get_project_versions()
            
            # loop through each model
            for v_arn in version_arn:
                json_object_cm=get_custom_labels(v_arn,filepath)
                # print(json_object_cm)
            
            
                json_object = json.loads(json_object_cm)
                labels = extract_values(json_object, 'Name')
                confidence = extract_values(json_object, 'Confidence')
                short_model_arn = v_arn[-5:]
                
                if labels:
                    print(f"Custom Labels API: model:{short_model_arn} file: {filepath} has labels: {labels} with confidence of {confidence}")
                else:
                    print(f"Custom Labels API: file: {filepath} has no labels")
                
            print("\n\n")
            
            
           