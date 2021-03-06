#!/usr/bin/env python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#

"""A convenience wrapper for starting bq."""

import os
import sys

import bootstrapping

from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import config
from googlecloudsdk.core import properties
from googlecloudsdk.core.credentials import gce


def _MaybeAddOption(args, name, value):
  if value is None:
    return
  args.append('--{name}={value}'.format(name=name, value=value))


def main():
  """Launches bq."""

  project, account = bootstrapping.GetActiveProjectAndAccount()
  adc_path = config.Paths().LegacyCredentialsAdcPath(account)
  single_store_path = config.Paths().LegacyCredentialsBqPath(account)

  gce_metadata = gce.Metadata()
  if gce_metadata and account in gce_metadata.Accounts():
    args = ['--use_gce_service_account']
  elif os.path.isfile(adc_path):
    args = ['--application_default_credential_file', adc_path,
            '--credential_file', single_store_path]
  else:
    p12_key_path = config.Paths().LegacyCredentialsP12KeyPath(account)
    if os.path.isfile(p12_key_path):
      args = ['--service_account', account,
              '--service_account_credential_file', single_store_path,
              '--service_account_private_key_file', p12_key_path]
    else:
      args = []  # Don't have any credentials we can pass.

  _MaybeAddOption(args, 'project', project)

  proxy_params = properties.VALUES.proxy
  _MaybeAddOption(args, 'proxy_address', proxy_params.address.Get())
  _MaybeAddOption(args, 'proxy_port', proxy_params.port.Get())
  _MaybeAddOption(args, 'proxy_username', proxy_params.username.Get())
  _MaybeAddOption(args, 'proxy_password', proxy_params.password.Get())
  _MaybeAddOption(args, 'disable_ssl_validation',
                  properties.VALUES.auth.disable_ssl_validation.GetBool())
  _MaybeAddOption(args, 'ca_certificates_file',
                  properties.VALUES.core.custom_ca_certs_file .Get())

  bootstrapping.ExecutePythonTool(
      'platform/bq', 'bq.py', *args)


if __name__ == '__main__':
  try:
    version = bootstrapping.GetFileContents('platform/bq', 'VERSION')
    bootstrapping.CommandStart('bq', version=version)
    blacklist = {
        'init': 'To authenticate, run gcloud auth.',
    }
    bootstrapping.CheckForBlacklistedCommand(sys.argv, blacklist,
                                             warn=True, die=True)
    cmd_args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    if cmd_args and cmd_args[0] not in ('version', 'help'):
      # Check for credentials only if they are needed.
      bootstrapping.CheckCredOrExit()
    bootstrapping.CheckUpdates('bq')
    main()
  except Exception as e:  # pylint: disable=broad-except
    exceptions.HandleError(e, 'bq')
