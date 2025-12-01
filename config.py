#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = int(os.environ.get("PORT", 3978))
    
    # Bot Framework 认证配置
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "")
    
    # Azure OpenAI 配置
    ENDPOINT_URL = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")