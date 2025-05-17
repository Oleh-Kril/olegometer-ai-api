import traceback

import boto3
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .image_comparison_process.main import process_images
from .serializers import ImageSerializer

response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'result': openapi.Schema(type=openapi.TYPE_STRING, description='Result of image processing')
    }
)

class ImageURLView(APIView):
    @swagger_auto_schema(
        request_body=ImageSerializer,
        responses={
            200: openapi.Response('Success', response_schema),
            400: openapi.Response('Bad Request')
        }
    )
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
                print("Starting fetching: ", key1, key2)

                response1 = s3_client.get_object(Bucket='olegometer.storage', Key=key1)
                response2 = s3_client.get_object(Bucket='olegometer.storage', Key=key2)

                image1_content = response1['Body'].read()
                image2_content = response2['Body'].read()

                response = process_images(image1_content, image2_content)

                # Return a successful response
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                traceback.print_exc()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
