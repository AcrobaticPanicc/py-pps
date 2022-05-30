import argparse
import json
import socket
from datetime import datetime
import docker
from rich import box, print_json
from rich.table import Table
from rich.console import Console
from collections import defaultdict
from typing import List
from rich.text import Text

__version__: str = "1.0.3"
__title__ = """
 _______  __   __         _______  _______  _______ 
|       ||  | |  |       |       ||       ||       |
|    _  ||  |_|  | ____  |    _  ||    _  ||  _____|
|   |_| ||       ||____| |   |_| ||   |_| || |_____ 
|    ___||_     _|       |    ___||    ___||_____  |
|   |      |   |         |   |    |   |     _____| |
|___|      |___|         |___|    |___|    |_______|
"""


class PyPps:
    EXTERNAL_IP = 'EXTERNAL IP'
    INTERNAL_PORT = 'IN PORT'
    INTERNAL_IP = 'INTERNAL IP'
    DEFAULT_TABLE_STYLE = 'dark_turquoise'
    COLOR_SYSTEM = 'standard'
    GOLD_COLOR = 'bold gold3'

    def __init__(self):
        self.console = Console(color_system=self.COLOR_SYSTEM, highlight=False)
        self.docker_client = docker.from_env()
        self.local_ip = self.get_local_ip()
        self.col_data = [self.EXTERNAL_IP, self.INTERNAL_PORT, self.INTERNAL_IP]
        self.docker_containers = self.docker_client.containers.list()

    @staticmethod
    def get_local_ip() -> str:
        """
        Get the local machine's IP address (localhost)
        :return: str: local machine's IP address
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    @staticmethod
    def get_time_passed(time: str) -> str:
        """
        Returnes a formated string of the time passed since given time.
        Example: '2022-05-27 13:12:44' -> '3 hours ago'
        :param time: a time represeting string formmated as follows: YYYY-MM-DD HH:MM:SS
        :return: a string of the time passed since given string
        """
        seconds_in_day = 24 * 60 * 60
        time_now = datetime.now()
        created_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        difference = time_now - created_obj
        m, s = divmod(difference.days * seconds_in_day + difference.seconds, 60)

        if m >= 1440:
            return f'{int(m / 1440)} days ago'

        if m >= 60:
            return f'{int(m / 60)} hours ago'

        if m < 60 and m != 0:
            return f'{m} minutes ago'

        return f'{s} seconds ago'

    @staticmethod
    def get_markup_string(string: str, color: str) -> Text:
        """
        Returns a markup formmated string (https://rich.readthedocs.io/en/stable/text.html)
        :param string: given string
        :param color: standard 8-bit colors (more can be found @ https://rich.readthedocs.io/en/stable/appendix/colors.html)
        :return: a rich Text formmated object of the given string
        """
        markup_string = Text(string)
        markup_string.stylize(color)
        return markup_string

    @staticmethod
    def add_space(string: str):
        """
        Adding a single space in the beggining of the provided string
        :return: the given string with a single space at the beginning
        """
        return f' {string}'

    @staticmethod
    def _parsed_args():
        """
        Parses args from the cli with ArgumentParser

        :returns: Parsed arguments
        :rtype: <Namespace> obj
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-j",
            "--json",
            default=False,
            action='store_true',
            help="Print the binary version information.")

        parser.add_argument(
            "-v",
            "--version",
            default=False,
            action='store_true',
            help="Print the binary version information.")

        args = parser.parse_args()

        return args

    def version(self):
        """
        Prints pypps version to the cli.
        """
        self.console.print(self.get_markup_string(__title__, 'bold gold3'))
        self.console.print(f'Version: {__version__}\n')
        self.console.print('@acrobaticpanicc\n')
        self.console.print(self.get_markup_string("https://github.com/AcrobaticPanicc/py-pps\n\n", 'blue'))
        return True

    def get_con_raw_data(self) -> dict:
        """
        Dictionary contaning all running containers' raw data:
            container_name, container_id, created, error, exit_code, external_ip, image, internal_ip, paused, ports, status
        :return: all running containers' raw data
        """
        res = defaultdict(dict)

        for container in self.docker_containers:
            res_dict = {
                'external_ip': self.local_ip,
                'internal_ip': container.attrs.get('NetworkSettings').get('IPAddress'),
                'created': container.attrs.get('Created', '').replace('Z', '').replace('T', ' ').split('.')[0],
                'container_id': container.attrs.get('Config').get('Hostname'),
                'image': container.attrs.get('Config').get('Image'),
                'status': container.attrs.get('State').get('Status'),
                'exit_code': container.attrs.get('State').get('ExitCode'),
                'error': container.attrs.get('State').get('Error'),
                'paused': container.attrs.get('State').get('Paused'),
                'ports': {host_ip: host_port for host_ip, host_port in container.ports.items()}
            }

            res[container.name] = res_dict

        return dict(res)

    def get_table(self,
                  table_title: str,
                  col_headers: List[str],
                  table_style: str = DEFAULT_TABLE_STYLE,
                  show_header=True,
                  show_lines=False) -> Table:

        """
        Creating, configuring and retuning a rich table
        :param table_title: table's title (duh..)
        :param col_headers: list of headers names (each name will create a new column)
        :param table_style: set to default 'dark_turquoise'
        :param show_header: Show a header row
        :param show_lines: Draw lines between every row
        :return: a rich table object
        """

        table = Table(title=table_title,
                      style=table_style,
                      title_style='bold',
                      title_justify='center',
                      box=box.SQUARE,
                      show_header=show_header,
                      show_lines=show_lines)

        for header in col_headers:
            table.add_column(header, justify='left', style="green")

        return table

    def format_data(self, c_data: dict) -> List[dict]:
        """
        Formatting the containers' data to be present on the table
        :param c_data: running containers' data
        :return: list of dictioanries with each container's formmated data
        """
        data_list = []

        for container_name, container_data in c_data.items():
            status = container_data['status']
            image_name = container_data['image']
            clean_image_name = image_name.rsplit('/', 1)[1] if '/' in image_name else image_name

            data = {
                'title': self.get_markup_string(f'\n{container_name}', 'bold yellow2'),
                'image': clean_image_name,
                'created': self.get_time_passed(container_data['created']),
                'container_id': container_data['container_id'],
                'status': self.get_markup_string(status, 'green') if status == 'running' else self.get_markup_string(status, 'orange_red1'),
                'internal_ip': container_data['internal_ip'],
                'ports': dict(defaultdict()),
            }

            for int_port, ext_port in container_data['ports'].items():

                if ext_port:
                    external_port = ext_port[0].get('HostPort')
                    external_ip = f"http://{self.local_ip}:{external_port} ➔"
                    data['ports'][int_port] = external_ip

                else:
                    external_ip = ''
                    data['ports'][int_port] = external_ip

            data_list.append(data)

        return data_list

    def get_tables(self, formatted_data: List[dict]) -> List[Table]:
        """
        Building the tables to be printed
        :param formatted_data: a list of dictionaries holding the formatted container's data
        :return: a list of rich's Table object
        """

        tables = []

        for con_data in formatted_data:
            big_table = self.get_table(con_data['title'], [''], show_header=False)

            status_str = self.get_markup_string('Status', self.GOLD_COLOR)
            created_str = self.get_markup_string('Created', self.GOLD_COLOR)
            container_id_str = self.get_markup_string('Container ID', self.GOLD_COLOR)
            image_str = self.get_markup_string('Image', self.GOLD_COLOR)

            big_table.add_row(status_str, con_data['status'])
            big_table.add_row(created_str, con_data['created'])
            big_table.add_row(container_id_str, con_data['container_id'])
            big_table.add_row(image_str, con_data['image'])

            if con_data['ports']:
                ports_str = self.get_markup_string('Ports', self.GOLD_COLOR)
                ports_table = self.get_table('', self.col_data, show_lines=False)
                big_table.add_row(ports_str, ports_table)

                for port, ext_ip in con_data['ports'].items():
                    ports_table.add_row(ext_ip, port, con_data['internal_ip'])

            tables.append(big_table)

        return tables

    def run_cli(self) -> None:
        """
        CLI's entry point. Running the CLI and printing the table in the terminal
        """
        args = self._parsed_args()

        if args.version:
            self.version()
            exit()

        container_data = self.get_con_raw_data()

        if args.json:
            str_data = str(json.dumps(container_data))
            print_json(str_data)
            exit()

        data = self.format_data(container_data)
        tables = self.get_tables(data)
        for table in tables:
            self.console.print(table, soft_wrap=True)

