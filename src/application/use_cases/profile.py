import os
from uuid import uuid4

import aiofiles

from src.application.exceptions.profile import FileIsNotAnImage
from src.domain.profile.dto.profile import OutputProfilePicture, OutputProfile
from src.domain.profile.use_case.profile import ProfileUseCase
from src.infrastructure.database.repositories.profile import ProfileRepository


class CreateProfile(ProfileUseCase):
    async def __call__(self, user_id: int) -> OutputProfile:
        return await self.profile_repository.create_profile(user_id)


class GetProfilePicture(ProfileUseCase):
    async def __call__(self, user_id: int) -> OutputProfilePicture:
        return await self.profile_repository.get_profile_picture(user_id)


class UpdateProfilePicture(ProfileUseCase):
    async def __call__(self, user_id: int, picture_url: str) -> None:
        await self.profile_repository.update_profile_picture(picture_url, user_id)


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository):
        self.profile_repository = profile_repository

    async def create_profile(self, user_id: int) -> OutputProfile:
        return await CreateProfile(self.profile_repository)(user_id)

    async def update_profile_picture(self, picture_url: str, user_id: int) -> None:
        await UpdateProfilePicture(self.profile_repository)(user_id, picture_url)

    async def get_profile_picture(self, user_id: int) -> OutputProfilePicture:
        return await GetProfilePicture(self.profile_repository)(user_id)

    @staticmethod
    async def upload_profile_picture(profile_picture_file):
        if not profile_picture_file.content_type.startswith("image/"):
            raise FileIsNotAnImage("Profile picture must be an image")

        new_file_name = f"{uuid4().hex}_{profile_picture_file.filename}"
        file_location = os.path.join("assets", "uploads", "avatars", new_file_name)
        async with aiofiles.open(file_location, "wb") as f:
            await f.write(await profile_picture_file.read())
        return file_location
