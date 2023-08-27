# Python Utitlies
Various python modules that can be used by other python projects.

## InteractiveCli
### [cli.py](https://github.com/henrydho/pyutils/blob/main/cli.py)

### Example
![InteractiveCli Demo](images/interactivecli_demo.gif)

## RemoteClient
### [remoteclient.py](https://github.com/henrydho/pyutils/blob/main/remoteclient.py)

### Prerequisites
Install the following python packages:
* paramiko==2.8.0
* jumpssh
* loguru

```bash
python3 -m pip install paramiko==2.8.0 jumpssh loguru
```

<details>
	<summary>Example</summary>

	from cli import PromptMenu, PromptInput, InteractiveCli

	# Define a list of namedtuple PromptMenu
	calculator_menu = [
		PromptMenu('+', f'Addition'),
		PromptMenu('-', f'Subtraction'),
		PromptMenu('*', f'Multiplication'),
		PromptMenu('/', f'Devision')
		]

	# Instantiate InteractiveCli object
	calculator_cli = InteractiveCli(
		title='Caculator Menu Selection',
		menu=calculator_menu,
		prompt_message='Command'
		)

	# Display PromptMenu and return a command value
	calculator_cli.prompt_menu()

	# Define the namedtuple PromptInput
	num1_prompt = PromptInput(
		message='Enter number 1',
		datatype='number',
		description='Number 1',
		input_type='info'
		)
	num2_prompt = PromptInput(
		message='Enter number 2',
		datatype='number',
		description='Number 2',
		input_type='info'
		)

	# Prompt users to input data and return a list of data
	calculator_cli.prompt_inputs(
		prompts=[num1_prompt, num2_prompt],
		exit_cmd='r'
		)

</details>

### Example
```python
# Import RemoteClient module
from remoteclient import RemoteClient

# Instantiate new RemoteClient
ssh_client = RemoteClient()

# SSH to the jump server
jump_session = ssh_client.connect_jump_session(
    jump_host='jump-server-ip-or-fqdn'
    )

# SSH to the remote host
remote_session = ssh_client.connect_remote_session(
    jump_session=jump_session,
    remote_host='remote-host-ip-or-fqdn'
    )

# Run the commands `date` and `pwd` on the jump server
ssh_client.run_cmd(
    ssh_session=jump_session,
    commands=['date', 'pwd']
    )

# Run the commands `date` and `pwd` on the remote host
ssh_client.run_cmd(
    ssh_session=remote_session,
    commands=['date', 'pwd']
    )

# Disconnect the SSH session of remote host
ssh_client.disconnect(
    ssh_session=remote_session
    )

# Disconnect the SSH session of jump server
ssh_client.disconnect(
    ssh_session=jump_session
    )
```
