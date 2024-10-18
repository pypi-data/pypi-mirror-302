# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from typing import Any, Dict, Union, Optional
from supertokens_python import get_request_from_user_context

from supertokens_python.recipe.emailpassword import EmailPasswordRecipe

from ..types import EmailTemplateVars, User
from ...multitenancy.constants import DEFAULT_TENANT_ID

from supertokens_python.recipe.emailpassword.interfaces import (
    CreateResetPasswordWrongUserIdError,
    CreateResetPasswordLinkUnknownUserIdError,
    CreateResetPasswordLinkOkResult,
    SendResetPasswordEmailOkResult,
    SendResetPasswordEmailUnknownUserIdError,
)
from supertokens_python.recipe.emailpassword.utils import get_password_reset_link
from supertokens_python.recipe.emailpassword.types import (
    PasswordResetEmailTemplateVars,
    PasswordResetEmailTemplateVarsUser,
)


async def update_email_or_password(
    user_id: str,
    email: Union[str, None] = None,
    password: Union[str, None] = None,
    apply_password_policy: Union[bool, None] = None,
    tenant_id_for_password_policy: Optional[str] = None,
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().recipe_implementation.update_email_or_password(
        user_id,
        email,
        password,
        apply_password_policy,
        tenant_id_for_password_policy or DEFAULT_TENANT_ID,
        user_context,
    )


async def get_user_by_id(
    user_id: str, user_context: Union[None, Dict[str, Any]] = None
) -> Union[None, User]:
    if user_context is None:
        user_context = {}
    return (
        await EmailPasswordRecipe.get_instance().recipe_implementation.get_user_by_id(
            user_id, user_context
        )
    )


async def get_user_by_email(
    tenant_id: str, email: str, user_context: Union[None, Dict[str, Any]] = None
) -> Union[User, None]:
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().recipe_implementation.get_user_by_email(
        email, tenant_id, user_context
    )


async def create_reset_password_token(
    tenant_id: str, user_id: str, user_context: Union[None, Dict[str, Any]] = None
):
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().recipe_implementation.create_reset_password_token(
        user_id, tenant_id, user_context
    )


async def reset_password_using_token(
    tenant_id: str,
    token: str,
    new_password: str,
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().recipe_implementation.reset_password_using_token(
        token, new_password, tenant_id, user_context
    )


async def sign_in(
    tenant_id: str,
    email: str,
    password: str,
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().recipe_implementation.sign_in(
        email, password, tenant_id, user_context
    )


async def sign_up(
    tenant_id: str,
    email: str,
    password: str,
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().recipe_implementation.sign_up(
        email, password, tenant_id, user_context
    )


async def send_email(
    input_: EmailTemplateVars,
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await EmailPasswordRecipe.get_instance().email_delivery.ingredient_interface_impl.send_email(
        input_, user_context
    )


async def create_reset_password_link(
    tenant_id: str, user_id: str, user_context: Optional[Dict[str, Any]] = None
):
    if user_context is None:
        user_context = {}
    token = await create_reset_password_token(tenant_id, user_id, user_context)
    if isinstance(token, CreateResetPasswordWrongUserIdError):
        return CreateResetPasswordLinkUnknownUserIdError()

    recipe_instance = EmailPasswordRecipe.get_instance()
    request = get_request_from_user_context(user_context)
    return CreateResetPasswordLinkOkResult(
        link=get_password_reset_link(
            recipe_instance.get_app_info(),
            token.token,
            tenant_id,
            request,
            user_context,
        )
    )


async def send_reset_password_email(
    tenant_id: str, user_id: str, user_context: Optional[Dict[str, Any]] = None
):
    link = await create_reset_password_link(tenant_id, user_id, user_context)
    if isinstance(link, CreateResetPasswordLinkUnknownUserIdError):
        return SendResetPasswordEmailUnknownUserIdError()

    user = await get_user_by_id(user_id, user_context)
    assert user is not None

    await send_email(
        PasswordResetEmailTemplateVars(
            PasswordResetEmailTemplateVarsUser(user.user_id, user.email),
            link.link,
            tenant_id,
        ),
        user_context,
    )

    return SendResetPasswordEmailOkResult()
