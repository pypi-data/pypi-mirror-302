from osbot_utils.helpers.flows                  import Flow
from osbot_utils.helpers.flows.decorators.flow  import flow
from osbot_utils.helpers.flows.decorators.task  import task
from osbot_utils.base_classes.Type_Safe         import Type_Safe


class Flow__Testing_Tasks(Type_Safe):

    @task()
    def task_1(self):
        print('inside task_1')
        return "task 1 data"

    @task()
    def task_2(self):
        print('inside task_2')
        self.task_3()
        return "task 2 data"

    @task()
    def task_3(self):
        print(f'inside task_3')
        return "task 3 data"

    @flow()
    def flow__testing_tasks(self, this_flow: Flow) -> Flow:
        print(f"in flow: {this_flow.flow_name}")
        self.task_1()
        self.task_2()
        return f"flow completed: {this_flow.flow_id} "

    def run(self, flow_run_params=None) -> Flow:
        with self.flow__testing_tasks() as _:
            return _.execute_flow(flow_run_params)