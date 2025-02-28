# import logging
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Meme
# from .serializers import MemeSerializer
# from .utils import respond_to_comment
#
# logger = logging.getLogger(__name__)
#
#
# class MemeAPIView(APIView):
#     """APIView for generating and retrieving memes."""
#
#     def get(self, request):
#         """Retrieve all memes."""
#         try:
#             memes = Meme.objects.all()
#             serializer = MemeSerializer(memes, many=True)
#             return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#         except Exception as e:
#             logger.error(f"Error retrieving memes: {e}")
#             return Response({"error": "Failed to retrieve memes."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def post(self, request):
#         """Generate a meme in response to a comment and save it."""
#         comment_text = request.data.get('comment_text')
#
#         if not comment_text:
#             return Response({"error": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             # This function should return both the image URL and the local path
#             meme_url, meme_caption, local_image_path = respond_to_comment(comment_text)
#
#             if not meme_url or not meme_caption or not local_image_path:
#                 return Response({"error": "Failed to generate meme."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#             # print(local_image_path,"------local storage----path")
#
#             main_path="http://127.0.0.1:8000/"+ local_image_path
#             # Fix the path by replacing \ with /
#             fixed_path = main_path.replace("\\", "/")
#             # print(fixed_path,"-------finalimage +++++++++")
#             # Add missing slash after port (if needed)
#             global serializer
#             if "8000media" in fixed_path:
#                 fixed_path = fixed_path.replace("8000media", "8000/media")
#
#
#                 # Save both `image_url` and `local_image_path`
#                 meme = Meme.objects.create(
#                     prompt=comment_text,
#                     caption=meme_caption,
#                     # image_url="http://127.0.0.1:8000/"+local_image_path,
#                     image_url=fixed_path,
#                     local_image_path=fixed_path # Save local path here
#                 )
#
#                 serializer = MemeSerializer(meme)
#             return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             logger.error(f"Error generating meme: {e}")
#             return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#



#
#
# import logging
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Meme
# from .utils import respond_to_comment
#
# logger = logging.getLogger(__name__)
#
# class MemeAPIView(APIView):
#     """APIView for generating and retrieving memes without using serializer."""
#
#     def get(self, request):
#         """Retrieve all memes and return them as a JSON list."""
#         try:
#             memes = Meme.objects.all().order_by('-created_at')  # Get latest memes first
#             meme_list = [
#                 {
#                     "id": meme.id,
#                     "prompt": meme.prompt,
#                     "caption": meme.caption,
#                     "image_url": meme.image_url,
#                     "local_image_path": meme.local_image_path,
#                     "created_at": meme.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp
#                 }
#                 for meme in memes
#             ]
#             return Response({"data": meme_list}, status=status.HTTP_200_OK)
#
#         except Exception as e:
#             logger.error(f"Error retrieving memes: {e}")
#             return Response({"error": "Failed to retrieve memes."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def post(self, request):
#         """Generate a meme and save it to SQLite."""
#         comment_text = request.data.get('comment_text')
#
#         if not comment_text:
#             return Response({"error": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             # Generate meme using external function
#             meme_url, meme_caption, local_image_path = respond_to_comment(comment_text)
#
#             if not meme_url or not meme_caption or not local_image_path:
#                 return Response({"error": "Failed to generate meme."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#             # Fix the local image path format
#             main_path = "http://127.0.0.1:8000/" + local_image_path
#             fixed_path = main_path.replace("\\", "/")  # Replace backslashes
#
#             if "8000media" in fixed_path:
#                 fixed_path = fixed_path.replace("8000media", "8000/media")
#
#             # Save meme to the SQLite database
#             meme = Meme.objects.create(
#                 prompt=comment_text,
#                 caption=meme_caption,
#                 image_url=fixed_path,
#                 local_image_path=fixed_path
#             )
#
#             # Return the saved meme data in response
#             return Response({
#                 "id": meme.id,
#                 "prompt": meme.prompt,
#                 "caption": meme.caption,
#                 "image_url": meme.image_url,
#                 "local_image_path": meme.local_image_path,
#                 "created_at": meme.created_at.strftime('%Y-%m-%d %H:%M:%S')
#             }, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             logger.error(f"Error generating meme: {e}")
#             return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#







import logging
import asyncio
from django.utils.timezone import localtime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Meme
from .utils import respond_to_comment


logger = logging.getLogger(__name__)

class MemeAPIView(APIView):
    """APIView for generating and retrieving memes synchronously."""

    def get(self, request):
        """Retrieve all memes synchronously."""
        try:
            memes = Meme.objects.all().order_by('-created_at').only(
                'id', 'prompt', 'caption', 'image_url', 'local_image_path', 'created_at'
            )

            meme_list = [
                {
                    "id": meme.id,
                    "prompt": meme.prompt,
                    "caption": meme.caption,
                    "image_url": meme.image_url,
                    "local_image_path": meme.local_image_path,
                    "created_at": localtime(meme.created_at).strftime('%Y-%m-%d %H:%M:%S')
                }
                for meme in memes
            ]

            return Response({"data": meme_list}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving memes: {e}")
            return Response({"error": "Failed to retrieve memes."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Generate a meme synchronously."""
        comment_text = request.data.get('comment_text')

        if not comment_text:
            return Response({"error": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Run the async function synchronously
            meme_data = asyncio.run(respond_to_comment(comment_text))

            if not meme_data or len(meme_data) != 3:
                return Response({"error": "Failed to generate meme."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            meme_url, meme_caption, local_image_path = meme_data

            # Fix the local image path format
            main_path = "http://127.0.0.1:8000/" + local_image_path.replace("\\", "/")
            if "8000media" in main_path:
                main_path = main_path.replace("8000media", "8000/media")

            # Save meme to database
            meme = Meme.objects.create(
                prompt=comment_text,
                caption=meme_caption,
                image_url=main_path,
                local_image_path=main_path
            )

            return Response({
                "id": meme.id,
                "prompt": meme.prompt,
                "caption": meme.caption,
                "image_url": meme.image_url,
                "local_image_path": meme.local_image_path,
                "created_at": localtime(meme.created_at).strftime('%Y-%m-%d %H:%M:%S')
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error generating meme: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










# # for integrating with X(Twitter)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Meme
# from .serializers import MemeSerializer
# from .utils import respond_to_comment
# import logging
#
# logger = logging.getLogger(__name__)
#
# class MemeAPIView(APIView):
#     """APIView for generating and retrieving memes."""
#
#     def post(self, request):
#         """Generate a meme and post it as a Twitter reply."""
#         comment_text = request.data.get('comment_text')
#         comment_id = request.data.get('comment_id')  # Twitter comment ID
#
#         if not comment_text or not comment_id:
#             return Response({"error": "Comment text and Twitter comment ID are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             meme_url, meme_caption, tweet_url = respond_to_comment(comment_text, comment_id)
#
#             if not meme_url or not meme_caption or not tweet_url:
#                 return Response({"error": "Failed to generate and post meme."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#             meme = Meme.objects.create(
#                 prompt=comment_text,
#                 caption=meme_caption,
#                 image_url=meme_url
#             )
#
#             serializer = MemeSerializer(meme)
#             return Response({"data": serializer.data, "tweet_url": tweet_url}, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             logger.error(f"Error generating and posting meme: {e}")
#             return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# for direct post
#
# class DirectMemePostAPIView(APIView):
#     """APIView for directly posting memes on Twitter."""
#
#     def post(self, request):
#         """Generate and post a meme as a new tweet."""
#         meme_topic = request.data.get('meme_topic')
#
#         if not meme_topic:
#             return Response({"error": "Meme topic is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             meme_url, meme_caption, tweet_url = post_direct_meme_flow(meme_topic)
#
#             if not meme_url or not meme_caption or not tweet_url:
#                 return Response({"error": "Failed to generate and post meme."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#             # Save meme to the database
#             meme = Meme.objects.create(
#                 prompt=meme_topic,
#                 caption=meme_caption,
#                 image_url=meme_url
#             )
#
#             serializer = MemeSerializer(meme)
#             return Response({"data": serializer.data, "tweet_url": tweet_url}, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             logging.error(f"Error generating and posting meme: {e}")
#             return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
