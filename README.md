# rekognition-content-moderation



## Summary

This script will read a directory of photos and simutaniously send each to the 

1. Rekognition Moderation API 
2. All the models in a Rekognition Custom Labels Project

It then outputs the labels and the confidence results from each Rekognition inference source, so you can compare the performance of your custom labels models vs the managed Rekognition content moderation service.

Note:  Defaults to using all models in the first custom labels project.  

### Resources
Uses Rekognition Boto API
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html
