# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pokemongo_bot.constants import Constants
from pokemongo_bot.step_walker import StepWalker
from pokemongo_bot.worker_result import WorkerResult
from pokemongo_bot.base_task import BaseTask
from utils import distance, format_dist, fort_details


class MoveToHome(BaseTask):
    SUPPORTED_TASK_API_VERSION = 1

    def initialize(self):
        self.location = self.bot.config.location
        if self.location:
            self.lat, self.lng = map(float, self.location.split(','))
        else:
            self.lat = self.lng = None

    def should_run(self):
        return self.location is not None

    def work(self):
        if not self.should_run():
            return WorkerResult.SUCCESS

        unit = self.bot.config.distance_unit  # Unit to use when printing formatted distance

        dist = distance(
            self.bot.position[0],
            self.bot.position[1],
            self.lat,
            self.lng
        )

        home_event_data = {
            'distance': format_dist(dist, unit),
        }

        self.emit_event(
            'moving_to_home',
            formatted="Moving towards home - {distance}",
            data=home_event_data
        )

        step_walker = StepWalker(
            self.bot,
            self.bot.config.walk,
            self.lat,
            self.lng
        )

        if not step_walker.step():
            return WorkerResult.RUNNING

        self.emit_event(
            'arrived_at_home',
            formatted='Arrived at home.'
        )
        return WorkerResult.SUCCESS
