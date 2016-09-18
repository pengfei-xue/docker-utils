import time
import json

from docker import Client
from tabulate import tabulate

import docker_utils
from docker_utils.utils import unit


class _ORDER:
    """order by cpu or memory usage."""

    CPU = 1
    MEM = 2


class Stats:
    """get docker containers stats."""

    def __init__(self, base_url):
        self._base_url = base_url
        self.cli = Client(base_url=self._base_url)
        self._alive = True

    def stop(self):
        self._alive = False

    def _get_all_running_containers(self):
        return self.cli.containers()

    def _show(self, stats):
        """format data and show.

        CONTAINER | CPU % | MEM % | MEM USAGE / LIMIT
        """
        headers = ['CONTAINER', 'CPU %', 'MEM %', 'MEM USAGE / LIMIT']
        table = []
        for s in stats:
            table.append([
                s['container_id'],
                s['cpu_usage_percentage'],
                s['mem_usage_percentage'],
                '%s / %s' % (unit(s['memory_stats']['usage']), unit(s['memory_stats']['limit']))
            ])

        print(tabulate(table, headers, tablefmt="grid"))

        # clean console
        time.sleep(1)

    def _sort(self, data, order_by):
        if order_by == _ORDER.MEM:
            sort_k = lambda x: x['mem_usage_percentage']

        elif order_by == _ORDER.CPU:
            sort_k = lambda x: x['cpu_usage_percentage']

        return sorted(data, key=sort_k, reverse=True)

    def _get_cpu_usage_percentage(self, d):
        delta = d['cpu_stats']['cpu_usage']['total_usage'] - d['precpu_stats']['cpu_usage']['total_usage']
        system_delta = d['cpu_stats']['system_cpu_usage'] - d['precpu_stats']['system_cpu_usage']
        return delta * 1.0 / system_delta * 100

    def _get_memory_usage_percentage(self, d):
        return d['memory_stats']['usage'] * 1.0 / d['memory_stats']['limit'] * 100

    def _preprocess(self, data, container_identity):
        data['container_id'] = container_identity
        data['cpu_usage_percentage'] = self._get_cpu_usage_percentage(data)
        data['mem_usage_percentage'] = self._get_memory_usage_percentage(data)
        return data

    def _show_resource_usage(self, order_by, *containers):
        _cs = containers or [x['Names'][0] for x in self._get_all_running_containers()]

        stats_generators = {}
        for c in _cs:
            stats_generators[c] = self.cli.stats(c)

        while self._alive:
            stats_data = []
            for x in stats_generators:
                data = next(stats_generators[x])
                data = data.decode('utf8')
                data = json.loads(data)
                data = self._preprocess(data, x)
                stats_data.append(data)

            stats_data = self._sort(stats_data, order_by)
            self._show(stats_data)

    def order_by_cpu_usage(self, *containers):
        self._show_resource_usage(_ORDER.CPU, *containers)

    def order_by_memory_usage(self, *containers):
        self._show_resource_usage(_ORDER.MEM, *containers)


def help_stats():
    pass


def run_stats():
    """parse args, print commands help."""
    pass


docker_utils.cmds.register('stats', run_stats, help_stats)
