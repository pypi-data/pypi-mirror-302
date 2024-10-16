"""
MIT License

Copyright (c) 2024 avizum

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal, overload, Sequence

import aiohttp

from .exceptions import Forbidden, HTTPException, NotFound, Unauthorized
from .models import EditfavoriteParams, Image, ImageParams, ImageResponseData, Order, Orientation, Tags

BASE_URL: str = "https://api.waifu.im"


class Request:
    def __init__(self, method: str, path: str = ""):
        self.method = method
        self.path = path
        self.url = f"{BASE_URL}{path}"


class Client:
    """
    Client for interacting with the API.

    Parameters
    ----------
    session: :class:`aiohttp.ClientSession` | :class:`None`
        The session to use for requests. If not provided, a new session will be created.
    token: :class:`str`
        The API token to use for requests. You can get one `here <https://waifu.im/dashboard/>`_.
    identifier: :class:`str`
        Used to identify your application in the User-Agent header. It is recommended to use the name of your application.
    """

    def __init__(
        self,
        *,
        session: aiohttp.ClientSession | None = None,
        token: str,
        identifier: str,
    ):
        self.session: aiohttp.ClientSession | None = session
        self.token: str = token
        self.headers: dict = {
            "Accept-Version": "v6",
            "User-Agent": f"aiohttp/{aiohttp.__version__}:{identifier}",
            "Authorization": f"Bearer {token}",
        }

    async def _create_client(self) -> aiohttp.ClientSession:
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _request(self, request: Request, **kwargs) -> Any:
        session = self.session or await self._create_client()

        async with session.request(request.method, request.url, headers=self.headers, **kwargs) as resp:
            content_type = resp.headers.get("content-type")
            if content_type and "application/json" in content_type:
                meth = resp.json
            else:
                meth = resp.text

            if 300 > resp.status >= 200:
                return await meth()
            elif resp.status == 404:
                raise NotFound(resp, await meth())
            elif resp.status == 403:
                raise Forbidden(resp, await meth())
            elif resp.status == 401:
                raise Unauthorized(resp, await meth())
            else:
                raise HTTPException(resp, await meth())

    @staticmethod
    def _to_params(data: ImageParams) -> dict[str, Any]:
        for key, value in data.items():
            if isinstance(value, (list, tuple, set)):
                new_value = []
                for i in value:
                    if isinstance(i, Enum):
                        new_value.append(i.value)
                    else:
                        new_value.append(i)
                data[key] = new_value
            if isinstance(value, Enum):
                data[key] = value.value
        return {
            key: str(value).lower() if isinstance(value, bool) else value for key, value in data.items() if value is not None
        }

    @overload
    async def search(
        self,
        /,
        *,
        included_tags: Sequence[Tags | str] | None = ...,
        excluded_tags: Sequence[Tags | str] | None = ...,
        nsfw: bool = ...,
        gif: bool | None = ...,
        order_by: Order = ...,
        orientation: Orientation | None = ...,
        limit: int = ...,
        included_files: Sequence[str] | None = ...,
        excluded_files: Sequence[str] | None = ...,
        return_raw: Literal[False] = ...,
    ) -> list[Image]: ...

    @overload
    async def search(
        self,
        /,
        *,
        included_tags: Sequence[Tags | str] | None = ...,
        excluded_tags: Sequence[Tags | str] | None = ...,
        nsfw: bool = ...,
        gif: bool | None = ...,
        order_by: Order = ...,
        orientation: Orientation | None = ...,
        limit: int = ...,
        included_files: Sequence[str] | None = ...,
        excluded_files: Sequence[str] | None = ...,
        return_raw: bool = True,
    ) -> ImageResponseData: ...

    async def search(
        self,
        /,
        *,
        included_tags: Sequence[Tags | str] | None = None,
        excluded_tags: Sequence[Tags | str] | None = None,
        nsfw: bool = False,
        gif: bool | None = None,
        order_by: Order = Order.RANDOM,
        orientation: Orientation | None = None,
        limit: int = 1,
        included_files: Sequence[str] | None = None,
        excluded_files: Sequence[str] | None = None,
        return_raw: bool = False,
    ) -> list[Image] | ImageResponseData:
        """
        Search for some images on the API.

        Parameters
        ----------
        included_tags: Sequence[:class:`Tag` | :class:`str`] | :class:`None`
            Will only return images with these tags.
        excluded_tags: Sequence[:class:`Tag` | :class:`str`] | :class:`None`
            Will not return images with these tags.
        nsfw: :class:`bool`
            Whether to return NSFW images. Defaults to ``False``.
        gif: :class:`bool` | :class:`None`
            Whether to return GIFs.
        order_by: :class:`Order`
            How to order the images. Defaults to :attr:`Order.RANDOM`.
        orientation: :class:`Orientation` | :class:`None`
            The orientation of the images.
        multiple: :class:`bool`
            Whether to return multiple images. Returns 30. Defaults to ``False``.
        included_files: Sequence[:class:`str`] | :class:`None`
            Only return images with these files.
        excluded_files: Sequence[:class:`str`] | :class:`None`
            Do not return images with these files.
        return_raw: :class:`bool` | :class:`None`
            Whether to return the raw response data.

        Raises
        ------
        :class:`NotFound`
            No images were found matching your search.
        :class:`HTTPException`
            An error occurred while requesting.

        Returns
        -------
        :class:`Image` | list[:class:`Image`] | :class:`ImageResponseData`
            The image(s) returned from the API.
        """
        params: ImageParams = {
            "included_tags": included_tags,
            "excluded_tags": excluded_tags,
            "is_nsfw": nsfw,
            "gif": gif,
            "order_by": order_by,
            "orientation": orientation,
            "limit": limit,
            "included_files": included_files,
            "excluded_files": excluded_files,
        }

        resp: ImageResponseData = await self._request(Request("GET", "/search"), params=self._to_params(params))
        if return_raw:
            return resp
        image_data = resp["images"]
        return [Image.from_dict(image) for image in image_data]

    @overload
    async def favorites(
        self,
        /,
        *,
        user_id: int,
        included_tags: Sequence[Tags | str] | None = ...,
        excluded_tags: Sequence[Tags | str] | None = ...,
        nsfw: bool = ...,
        gif: bool | None = ...,
        order_by: Order = ...,
        orientation: Orientation | None = ...,
        multiple: Literal[False] = ...,
        included_files: Sequence[str] | None = ...,
        excluded_files: Sequence[str] | None = ...,
        return_raw: Literal[False] = ...,
    ) -> Image: ...

    @overload
    async def favorites(
        self,
        /,
        *,
        user_id: int,
        included_tags: Sequence[Tags | str] | None = ...,
        excluded_tags: Sequence[Tags | str] | None = ...,
        nsfw: bool = ...,
        gif: bool | None = ...,
        order_by: Order = ...,
        orientation: Orientation | None = ...,
        multiple: Literal[True] = ...,
        included_files: Sequence[str] | None = ...,
        excluded_files: Sequence[str] | None = ...,
        return_raw: Literal[False] = ...,
    ) -> list[Image]: ...

    @overload
    async def favorites(
        self,
        /,
        *,
        user_id: int,
        included_tags: Sequence[Tags | str] | None = ...,
        excluded_tags: Sequence[Tags | str] | None = ...,
        nsfw: bool = ...,
        gif: bool | None = ...,
        order_by: Order = ...,
        orientation: Orientation | None = ...,
        multiple: bool = ...,
        included_files: Sequence[str] | None = ...,
        excluded_files: Sequence[str] | None = ...,
        return_raw: bool = True,
    ) -> ImageResponseData: ...

    async def favorites(
        self,
        /,
        *,
        user_id: int,
        included_tags: Sequence[Tags | str] | None = None,
        excluded_tags: Sequence[Tags | str] | None = None,
        nsfw: bool = False,
        gif: bool | None = None,
        order_by: Order = Order.RANDOM,
        orientation: Orientation | None = None,
        multiple: bool = False,
        included_files: Sequence[str] | None = None,
        excluded_files: Sequence[str] | None = None,
        return_raw: bool = False,
    ) -> Image | list[Image] | ImageResponseData:
        """
        Get a user's favorites.

        .. note::
            The user must have authorized your application to access their favorites.
            See :meth:`generate_authorization_link`.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to get the favorites of.
        included_tags: Sequence[:class:`Tag` | :class:`str`] | :class:`None`
            Will only return images with these tags.
        excluded_tags: Sequence[:class:`Tag` | :class:`str`] | :class:`None`
            Will not return images with these tags.
        nsfw: :class:`bool`
            Whether to return NSFW images. Defaults to ``False``.
        gif: :class:`bool` | :class:`None`
            Whether to return GIFs.
        order_by: :class:`Order`
            How to order the images. Defaults to :attr:`Order.RANDOM`.
        orientation: :class:`Orientation` | :class:`None`
            The orientation of the images.
        multiple: :class:`bool`
            Whether to return multiple images. Returns 30. Defaults to ``False``.
        included_files: Sequence[:class:`str`] | :class:`None`
            Only return images with these files.
        excluded_files: Sequence[:class:`str`] | :class:`None`
            Do not return images with these files.
        return_raw: :class:`bool` | :class:`None`
            Whether to return the raw response data.

        Raises
        ------
        :class:`NotFound`
            No images were found matching your search.
        :class:`Unauthorized`
            Your token is invalid.
        :class:`Forbidden`
            You do not have permission to access the user's favorites
        :class:`HTTPException`
            An error occurred while requesting.

        Returns
        -------
        :class:`Image` | list[:class:`Image`] | :class:`ImageResponseData`
            The image(s) returned from the API.
        """
        params: ImageParams = {
            "user_id": user_id,
            "included_tags": included_tags,
            "excluded_tags": excluded_tags,
            "is_nsfw": nsfw,
            "gif": gif,
            "order_by": order_by,
            "orientation": orientation,
            "many": multiple,
            "included_files": included_files,
            "excluded_files": excluded_files,
        }

        resp: ImageResponseData = await self._request(Request("GET", "/fav"), params=self._to_params(params))

        if return_raw:
            return resp

        image_data = resp["images"]
        if len(image_data) == 1:
            return Image.from_dict(image_data[0])
        return [Image.from_dict(image) for image in image_data]

    async def favorites_insert(self, /, *, user_id: int, image: Image | int) -> None:
        """
        Insert an image into a user's favorites.

        .. note::
            The user must have authorized your application to edit their favorites.
            See :meth:`utils.generate_authorization_link`.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to insert the image into.
        image: :class:`Image` | :class:`int`
            The Image or Image ID of the image to insert to the user's favorites.

        Raises
        ------
        :class:`HTTPException`
            Can occur if:
            - Image already exists in the user's favorites.
            - The image does not exist.
        :class:`Forbidden`
            You do not have permission to edit the user's favorites.
        :class:`Unauthorized`
            Your token is invalid.
        """
        if isinstance(image, Image):
            image = image.id
        params: EditfavoriteParams = {"user_id": user_id, "image_id": image}

        return await self._request(Request("POST", "/fav/insert"), json=params)

    async def favorites_delete(self, /, *, user_id: int, image: Image | int) -> None:
        """
        Remove an image from a user's favorites.

        .. note::
            The user must have authorized your application to edit their favorites.
            See :meth:`utils.generate_authorization_link`.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to remove the image from.
        image: :class:`Image` | :class:`int`
            The Image or Image ID of the image to remove from the user's favorites.

        Raises
        ------
        :class:`HTTPException`
            Can occur if:
            - Image dosen't exist in the user's favorites.
            - The image does not exist.
        :class:`Forbidden`
            You do not have permission to edit the user's favorites.
        :class:`Unauthorized`
            Your token is invalid.
        """
        if isinstance(image, Image):
            image = image.id
        params: EditfavoriteParams = {"user_id": user_id, "image_id": image}

        return await self._request(Request("DELETE", "/fav/delete"), json=params)

    async def favorites_toggle(self, /, *, user_id: int, image: Image | int) -> None:
        """
        Insert or Reomve an image into a user's favorites.

        .. note::
            The user must have authorized your application to edit their favorites.
            See :meth:`utils.generate_authorization_link`.

        Parameters
        ----------
        user_id: :class:`int`
            The ID of the user to remove the image from.
        image: :class:`Image` | :class:`int`
            The Image or Image ID of the image to insert or remove from the user's favorites.

        Raises
        ------
        :class:`HTTPException`
            The image does not exist.
        :class:`Forbidden`
            You do not have permission to edit the user's favorites.
        :class:`Unauthorized`
            Your token is invalid.
        """
        if isinstance(image, Image):
            image = image.id
        params: EditfavoriteParams = {"user_id": user_id, "image_id": image}

        return await self._request(Request("POST", "/fav/toggle"), json=params)

    # Aliases
    favourites = favorites
    favourites_insert = favorites_insert
    favourites_delete = favorites_delete
    favourites_toggle = favorites_toggle

    async def close(self):
        """
        Closes the :class:`aiohttp.ClientSession` used by the client.

        .. caution::
            If you specified your own ClientSession, this may interrupt what you are doing with the session.
        """
        if self.session is not None and not self.session.closed:
            await self.session.close()
