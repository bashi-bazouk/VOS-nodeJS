# Copyright 2017 Google Inc. All Rights Reserved.
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


"""Various functions to be used to modify a request before it is sent."""

from googlecloudsdk.command_lib.util.apis import arg_utils


def SetFieldFromArg(api_field, arg_name):
  def Process(unused_ref, args, req):
    arg_utils.SetFieldInMessage(
        req, api_field, arg_utils.GetFromNamespace(args, arg_name))
    return req
  return Process
