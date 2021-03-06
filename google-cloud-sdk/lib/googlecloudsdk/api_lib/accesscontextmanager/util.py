# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""API utilities for access context manager."""
from googlecloudsdk.api_lib.util import apis

_API_NAME = 'accesscontextmanager'


def _GetDefaultVersion():
  return apis.ResolveVersion(_API_NAME)


def GetMessages(version=None):
  version = version or _GetDefaultVersion()
  return apis.GetMessagesModule(_API_NAME, version)


def GetClient(version=None):
  version = version or _GetDefaultVersion()
  return apis.GetClientInstance(_API_NAME, version)
