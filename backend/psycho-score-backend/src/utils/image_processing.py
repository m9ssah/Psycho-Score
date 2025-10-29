from PIL import Image, ImageEnhance, ImageFilter
from fastapi import UploadFile, HTTPException
import io
import os
from config.settings import settings


class ImageProcessor:
    """Utility class for processing business card images"""

    @staticmethod
    def validate_image(file: UploadFile) -> bool:
        """Validate uploaded image file"""
        if not file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}",
            )

        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024 * 1024):.1f}MB",
            )

        return True

    @staticmethod
    def enhance_image_for_analysis(image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR and analysis"""
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Enhance contrast and sharpness for better text recognition
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)

        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)

        # Apply slight denoising
        image = image.filter(ImageFilter.MedianFilter(size=3))

        return image

    @staticmethod
    def resize_image(image: Image.Image, max_size: tuple = (2048, 2048)) -> Image.Image:
        """Resize image while maintaining aspect ratio"""
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image

    @staticmethod
    async def save_uploaded_image(file: UploadFile, filename: str) -> str:
        """Save uploaded image to disk"""
        file_path = os.path.join(settings.IMAGE_UPLOAD_PATH, filename)

        try:
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            # Reset file pointer for further processing
            file.file.seek(0)

            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")


def resize_image(image: Image.Image, target_size: tuple) -> Image.Image:
    return image.resize(target_size, Image.LANCZOS)


def convert_image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


def preprocess_image(image_bytes: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(image_bytes))
    # Example preprocessing: convert to RGB and resize
    image = image.convert("RGB")
    image = resize_image(image, (800, 800))  # Resize to 800x800
    return image


def save_image(image: Image.Image, path: str) -> None:
    image.save(path)


# Create global instance
image_processor = ImageProcessor()
