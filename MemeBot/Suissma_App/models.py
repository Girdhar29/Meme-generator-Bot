# from django.db import models
#
# class Meme(models.Model):
#     prompt = models.CharField(max_length=255) #Prompt of the user
#     caption = models.CharField(max_length=255, blank=True, null=True)  # Caption for the meme
#     image_url = models.URLField(blank=True, null=True, max_length=500)  # Meme image URL
#     local_image_path = models.CharField(max_length=500, blank=True, null=True)  # Local image file path
#     created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
#
#     def __str__(self):
#         return f"Meme: {self.prompt} | Caption: {self.caption or 'N/A'} (Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
#
#     class Meta:
#         verbose_name = "Meme"
#         verbose_name_plural = "Memes"
#         ordering = ['-created_at']  # Show latest memes first


from django.db import models


class Meme(models.Model):
    """Model to store meme data including prompts, captions, and image paths."""

    prompt = models.CharField(max_length=255, help_text="User's input prompt for meme generation.")
    caption = models.CharField(max_length=255, blank=True, null=True, help_text="Generated caption for the meme.")
    image_url = models.URLField(max_length=500, blank=True, null=True,
                                help_text="Public URL of the generated meme image.")
    local_image_path = models.CharField(max_length=500, blank=True, null=True,
                                        help_text="Local file path for the stored meme image.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the meme was created.")

    def __str__(self):
        return f"Meme ID: {self.id} | Prompt: {self.prompt[:30]}... | Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Meme"
        verbose_name_plural = "Memes"
        ordering = ['-created_at']  # Show latest memes first
