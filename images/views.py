import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .image_comparison_process.main import process_images
from .serializers import ImageSerializer

class ImageURLView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            key1 = serializer.validated_data['designS3Key']
            key2 = serializer.validated_data['websiteS3Key']

            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )

            try:
                response1 = s3_client.get_object(Bucket='olegometer.storage', Key=key1)
                response2 = s3_client.get_object(Bucket='olegometer.storage', Key=key2)

                image1_content = response1['Body'].read()
                image2_content = response2['Body'].read()

                response = process_images(image1_content, image2_content)

                # Return a successful response
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
