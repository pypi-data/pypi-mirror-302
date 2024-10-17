import queue
import math
import random

from _queue import Empty
from locust import HttpUser, task, LoadTestShape, between

from cttest_plus._locust import prepare_locust_tests, get_load_shape, prepare_locust_data
from cttest_plus.utils.dataParser import GlobalVariableMap

load_shape = get_load_shape()


class TaskUser(HttpUser):
    wait_time = between(1, 1)
    host = ""

    # 测试数据参数化
    # queue_data = dict()
    # no_data = True

    def on_start(self):
        # 用例收集
        self.locust_test = prepare_locust_tests()
        # 性能测试用例数据
        # queue_data_dict = prepare_locust_data()
        # queue_data_list = queue_data_dict.get("default")
        # if queue_data_list:
        #     self.no_data = False
        #     for item in queue_data_list:
        #         case_id = item.get('caseId')
        #         if case_id not in self.queue_data:
        #             self.queue_data[case_id] = queue.Queue()
        #         self.queue_data[case_id].put_nowait(item)

    @task
    def test_cttest_case(self):
        spec_data = None
        cttest_case = self.weight_allocation(self.locust_test)
        data_list = cttest_case.kwargs.get('spec').get('parametrize')
        if data_list:
            data_dict = random.choice(data_list)
            for item in data_dict:
                GlobalVariableMap.var_map[item] = data_dict.get(item)
        # case_id = cttest_case.kwargs.get('spec').get('caseId')
        # try:
        #     # 从队列取数据
        #     if not self.no_data:
        #         spec_data = self.queue_data[case_id].get_nowait()
        #         # 如果数据循环可循环使用，将数据放回队列
        #         self.queue_data[case_id].put_nowait(spec_data)
        #     else:
        #         spec_data = None
        # except Empty as e:
        #     exit(1)
        # except KeyError as e:
        #     raise KeyError(f"用例{case_id}没有数据，无法执行！请检查【压测多数据】")
        try:
            cttest_case.run(locust_session=self.client, spec_data=spec_data)
        except Exception as ex:
            self.environment.events.request_failure.fire(
                request_type="Failed",
                name=cttest_case.title,
                response_time=0,
                response_length=0,
                exception=ex,
            )
            raise ex

    @staticmethod
    def weight_allocation(task: dict):
        weight_list = list(task.keys())
        weight_sum = sum(weight_list)
        chose = random.randint(1, weight_sum)
        key_sum = 0
        for i in weight_list:
            key_sum += i
            if key_sum >= chose:
                return random.choice(task.get(i))


if load_shape:
    class StepLoadShape(LoadTestShape):

        step_time = load_shape.get("step_time")
        step_load = load_shape.get("step_load")
        spawn_rate = load_shape.get("step_load")
        time_limit = load_shape.get("time_limit")

        stages = [
            {"duration": 60, "users": 10, "spawn_rate": 10},
            {"duration": 100, "users": 50, "spawn_rate": 10},
            {"duration": 180, "users": 100, "spawn_rate": 10},
            {"duration": 220, "users": 30, "spawn_rate": 10},
            {"duration": 230, "users": 10, "spawn_rate": 10},
            {"duration": 240, "users": 1, "spawn_rate": 1},
        ]

        min_users = 20
        peak_one_users = 60
        peak_two_users = 40

        # def tick(self):
        #     run_time = self.get_run_time()
        #
        #     if run_time > self.time_limit:
        #         return None
        #
        #     current_step = math.floor(run_time / self.step_time) + 1
        #     return (current_step * self.step_load, self.spawn_rate)

        def tick(self):
            return self.step_shape()

        def step_shape(self):
            run_time = self.get_run_time()

            if run_time > self.time_limit:
                return None

            current_step = math.floor(run_time / self.step_time) + 1
            return (current_step * self.step_load, self.spawn_rate)

        def double_wave(self):
            run_time = round(self.get_run_time())

            if run_time < self.time_limit:
                user_count = (
                        (self.peak_one_users - self.min_users)
                        * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                        + (self.peak_two_users - self.min_users)
                        * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                        + self.min_users
                )
                return (round(user_count), round(user_count))
            else:
                return None

        def stage_shape(self):
            run_time = self.get_run_time()
            for stage in self.stages:
                if run_time < stage["duration"]:
                    tick_data = (stage["users"], stage["spawn_rate"])
                    return tick_data
            return None
