from django.db import migrations
import os


def add_post_content_subfolder(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')

    for post in Post.objects.all():
        if post.image and '/post_content/' not in post.image.name:
            # Old path: "user_5/photo.jpg"
            # New path: "user_5/post_content/photo.jpg"

            old_path = post.image.name  # e.g., "user_5/photo.jpg"
            parts = old_path.split('/', 1)  # Split into ["user_5", "photo.jpg"]

            if len(parts) == 2:
                user_folder = parts[0]  # "user_5"
                filename = parts[1]  # "photo.jpg"
                new_path = f'{user_folder}/post_content/{filename}'

                post.image.name = new_path
                post.save(update_fields=['image'])

                print(f"Updated post {post.id}: {old_path} → {new_path}")


def remove_post_content_subfolder(apps, schema_editor):
    # Reverse operation for rollback
    Post = apps.get_model('posts', 'Post')

    for post in Post.objects.all():
        if post.image and '/post_content/' in post.image.name:
            # "user_5/post_content/photo.jpg" → "user_5/photo.jpg"
            old_path = post.image.name
            new_path = old_path.replace('/post_content/', '/')

            post.image.name = new_path
            post.save(update_fields=['image'])

            print(f"Reverted post {post.id}: {old_path} → {new_path}")


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0002_rename_comment_comment_content_alter_post_image'),  # Your latest migration
    ]

    operations = [
        migrations.RunPython(add_post_content_subfolder, remove_post_content_subfolder),
    ]