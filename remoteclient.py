"""SSH Client to handle connections to Jump Server and remote host,
and run commands on a remote host.
"""
import os
from typing import Union

from jumpssh import SSHSession, exception
import paramiko

from logger import logger


class RemoteClient:
    """SSH client to interact with a remote host via a jump server

    :param jump_session: jump server `SSHSession`
    :param remote_session: remote host `SSHSession`
    """

    def __init__(self):
        self.jump_session = None
        self.remote_session = None

    def get_ssh_config(self, host: str) -> Union[dict, None]:
        """Get SSH config

        :param host: a `str` host value
        :return: a `dict` of ssh config format or `None`
        :Example:

            {
                'user': 'xxxxxx',
                'identityfile': ['/path/to/ssh_private_key_file'],
                'port': '2222',
                'hostname': 'jump_server_host_name'
            }
        """

        conf_file_path = os.path.join(
            os.path.abspath(os.getcwd()), 'setting.cfg')
        try:
            with open(conf_file_path, 'r') as _file:
                ssh_config = paramiko.SSHConfig()
                ssh_config.parse(_file)

            ssh_config_dict = ssh_config.lookup(host)

            for k in ['hostname', 'user', 'identityfile', 'port']:
                ssh_config_dict[k]

            return ssh_config_dict

        except FileNotFoundError as err:
            logger.error(err)
        except KeyError as err:
            logger.error(
                    f'{conf_file_path} does not contain {err} value. '
                    'Check the setup instructions.'
                    )
        return None

    def connect_jump_session(self, jump_host) -> Union[SSHSession, None]:
        """Connect a SSH connection to jump server

        Note: ssh-copy-id -i ~/.ssh/id_rsa <jump_server>
        so that password is not required when connecting to jump server.
        """
        # Get SSH config from setting.cfg
        ssh_config = self.get_ssh_config(host=jump_host)

        if not ssh_config:
            return None

        try:
            logger.info(
                f"Connecting SSH session to - {ssh_config['user']}@{jump_host}")
            self.jump_session = SSHSession(
                host=jump_host,
                username=ssh_config['user'],
                private_key_file=ssh_config['identityfile'],
                port=ssh_config['port'],
                missing_host_key_policy=None
                ).open(retry=1, retry_interval=10)
            logger.info(f'Successful connected to jump host - {jump_host}')
            return self.jump_session
        except exception.ConnectionError as err:
            logger.error(err)
        return None

    def connect_remote_session(self, jump_session: SSHSession,
                               remote_host: str) -> Union[SSHSession, None]:
        """Open SSH connection to remote session from jump server

        :param jump_session: jump server `SSHSession`
        :param remote_host: a remote host IP address
        :return: a `SSHSession` object or `None` if failed to connect SSH to
            the remote host.
        """
        if jump_session:
            try:
                logger.info(
                    f'Connecting SSH session to remote host - {remote_host}')
                self.remote_session = jump_session.get_remote_session(
                    host=remote_host,
                    username='root'
                    )
                logger.info(f'Successful connected to remote host - {remote_host}')
                return self.remote_session
            except exception.ConnectionError as err:
                logger.error(err)
        return None

    def run_cmd(
            self,
            ssh_session: SSHSession,
            commands: list,
            logging=False,
            raise_if_error=True,
            continuous_output=False,
            silent=False
            ) -> list:
        """Run a specific or multiple commands from SSH session

        :param commands: a `str` command or a `list` of commands
        :param logging: if `True`, printing out/logging command's error/info.
            Default is not to print out/log command's error/info.
        :param ssh_session: a SSHSession
        :param **kwargs: optional args used by jumpssh's run_cmd method
            :param raise_if_error:
                if True, raise SSHException when exit code of the command is
                different from 0, else just return exit code and command output
            :param continuous_output:
                if True, print output all along the command is running
            :param silent:
                - if True, does not log the command run (useful if sensitive
                information are used in command)
                - if parameter is a list, all strings of the command matching an
                item of the list will be concealed in logs (regexp supported)
        :raises TimeoutError: if command run longer than the specified timeout
        :raises TypeError: if `cmd` parameter is neither a string neither a list of string
        :raises EOFError:
        :raises SSHException: if current SSHSession is already closed
        :raises RunCmdError:
            if exit code of the command is different from 0 and raise_if_error is True
        :return: a class inheriting from collections.namedtuple containing mainly
            `output` and `error` of the executed command
        :rtype: a `list` of RunCmdResult `namedtuple` containing output and
            jumpssh.RunCmdError containing `str` error
        """
        outputs = []
        for cmd in commands:
            try:
                if logging:
                    logger.info(f'Executing command: {cmd}')

                # Get jumpssh.RunCmdResult output
                output = ssh_session.run_cmd(
                        cmd=cmd,
                        raise_if_error=raise_if_error,
                        continuous_output=continuous_output,
                        silent=silent
                        )
                outputs.append(output)
            except exception.TimeoutError as err:
                logger.error(str(err))
                break
            except TypeError as err:
                logger.error(str(err))
                break
            except EOFError as err:
                logger.error(str(err))
            except KeyboardInterrupt:
                break
            except exception.ConnectionError as err:
                logger.error(str(err))
                break
            except exception.RunCmdError as err:
                if logging:
                    logger.error(
                        f"Command '{err.command}' returned exit status ({err.exit_code}), "
                        f"expected {err.success_exit_code}: {err.error}"
                        )
                # Append jumpssh.exception.RunCmdError to the outputs `list`
                outputs.append(err)
        return outputs

    def disconnect(self, ssh_session: SSHSession):
        """Disconnect SSH session"""
        if ssh_session:
            logger.info(f'Disconnecting {ssh_session}')
            ssh_session.close()
