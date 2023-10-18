
For deployment of this mini django app on the cloud we will choose Google Cloud Run

I choose google mostly out of preference for this type of application it doesn't make any actual difference.
I choose Cloud Run over Cloud Engine or Kubernetes because of its simplicity and allows containerized applications, 
and it's not depended on the region

Here are some high level instructions:
- Setup a Google Cloud project 
- Build the Docker image and push it to a container registry (like Google Container Registry or Docker Hub)
- Configure a Cloud SQL database
- Use Google Secrets Manager to store any credentials for Database etc
- Make proper changes to project settings in order to connect with the database
- Using gcloud deploy the containerized application to cloud run