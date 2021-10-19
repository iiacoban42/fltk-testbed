import datetime
import logging
import time
import uuid
from queue import PriorityQueue
from typing import List

from kubeflow.pytorchjob import PyTorchJobClient
from kubeflow.pytorchjob.constants.constants import PYTORCHJOB_GROUP, PYTORCHJOB_VERSION, PYTORCHJOB_PLURAL
from kubernetes import client

from fltk.util.cluster.client import construct_job, ClusterManager
from fltk.util.config.base_config import BareConfig
from fltk.util.task.generator.arrival_generator import ArrivalGenerator, Arrival
from fltk.util.task.task import ArrivalTask


class Orchestrator(object):
    """
    Central component of the Federated Learning System: The Orchestrator

    The Orchestrator is in charge of the following tasks:
    - Running experiments
        - Creating and/or managing tasks
        - Keep track of progress (pending/started/failed/completed)
    - Keep track of timing

    Note that the Orchestrator does not function like a Federator, in the sense that it keeps a central model, performs
    aggregations and keeps track of Clients. For this, the KubeFlow PyTorch-Operator is used to deploy a train task as
    a V1PyTorchJob, which automatically generates the required setup in the cluster. In addition, this allows more Jobs
    to be scheduled, than that there are resources, as such, letting the Kubernetes Scheduler let decide when to run
    which containers where.
    """
    _alive = False
    # Priority queue, requires an orderable object, otherwise a Tuple[int, Any] can be used to insert.
    pending_tasks: "PriorityQueue[ArrivalTask]" = PriorityQueue()
    deployed_tasks: List[ArrivalTask] = []
    completed_tasks: List[str] = []

    def __init__(self, cluster_mgr: ClusterManager, arv_gen: ArrivalGenerator, config: BareConfig):
        self.__logger = logging.getLogger('Orchestrator')
        self.__logger.debug("Loading in-cluster configuration")
        self.__cluster_mgr = cluster_mgr
        self.__arrival_generator = arv_gen
        self._config = config

        # API to interact with the cluster.
        self.__client = PyTorchJobClient()

    def stop(self, arrival_times: dict, sys_param: dict) -> None:
        """
        Stop the Orchestrator.
        @return:
        @rtype:
        """
        self.__logger.info("Received stop signal for the Orchestrator.")
        self.__logger.info("Arrival times for the jobs:")
        for i in arrival_times.keys():
        	self.__logger.info("id " + str(i))

        self.__logger.info("End of arrival times")

        self.__logger.info("Configurations for the jobs:")
        for i in sys_param.keys():
            self.__logger.info("id " + str(i))
            self.__logger.info("arrival time " + str(sys_param[i][3]))
            self.__logger.info("network " + sys_param[i][0])
            self.__logger.info("system config ")
            self.__logger.info("data parallelism " + sys_param[i][1].data_parallelism)
            self.__logger.info("cores " + sys_param[i][1].executor_cores)
            self.__logger.info("memory " + sys_param[i][1].executor_memory)
            self.__logger.info("parameter config ")
            self.__logger.info("batch size " + sys_param[i][2].bs)
            self.__logger.info("max epoch " + sys_param[i][2].max_epoch)
            self.__logger.info("learning rate " + sys_param[i][2].lr)
            self.__logger.info("learning rate decay " + sys_param[i][2].lr_decay)

        self.__logger.info("End of configurations")

        self._alive = False

    def run(self, clear: bool = True) -> None:
        """
        Main loop of the Orchestartor.
        :return:
        """
        self._alive = True
        start_time = time.time()
        if clear:
            self.__clear_jobs()
        arrival_times = {}
        sys_param = {}
        scheduled_tasks = {}
        i = 0
        while self._alive and time.time() - start_time < self._config.get_duration():
            # 1. Check arrivals
            # If new arrivals, store them in arrival list
            while not self.__arrival_generator.arrivals.empty():
                arrival: Arrival = self.__arrival_generator.arrivals.get()
                unique_identifier: uuid.UUID = uuid.uuid4()
                task = ArrivalTask(priority=arrival.get_priority(),
                                   id=unique_identifier,
                                   network=arrival.get_network(),
                                   dataset=arrival.get_dataset(),
                                   sys_conf=arrival.get_system_config(),
                                   param_conf=arrival.get_parameter_config())

                self.__logger.debug(f"Arrival of: {task}")
                task_params = str(arrival.get_parameter_config().bs)+str(arrival.get_parameter_config().max_epoch)\
                    +str(arrival.get_system_config().executor_memory)+str(arrival.get_system_config().executor_cores)
                if not task_params in scheduled_tasks:
                    scheduled_tasks[task_params] = 1
                    self.pending_tasks.put(task)
                    i += 1
                    arrival_time = datetime.datetime.now()
                    arrival_times[task.id] = arrival_time
                    sys_param[task.id] = [arrival.get_network(), arrival.get_system_config(), arrival.get_parameter_config(), arrival_time]
                elif scheduled_tasks[task_params] < 3:
                    scheduled_tasks[task_params] += 1
                    self.pending_tasks.put(task)
                    i += 1
                    arrival_time = datetime.datetime.now()
                    arrival_times[task.id] = arrival_time
                    sys_param[task.id] = [arrival.get_network(), arrival.get_system_config(), arrival.get_parameter_config(), arrival_time]
            # sort pending tasks according to greedy
            while not self.pending_tasks.empty():

                if i == 48:
                    self.stop(arrival_times, sys_param)
                    return

                # Do blocking request to priority queue
                curr_task = self.pending_tasks.get()
                self.__logger.info(f"Scheduling arrival of Arrival: {curr_task.id}")
                job_to_start = construct_job(self._config, curr_task)


                # Hack to overcome limitation of KubeFlow version (Made for older version of Kubernetes)
                self.__logger.info(f"Deploying on cluster: {curr_task.id}")
                self.__client.create(job_to_start, namespace=self._config.cluster_config.namespace)
                self.deployed_tasks.append(curr_task)

                # TODO: Extend this logic in your real project, this is only meant for demo purposes
                # For now we exit the thread after scheduling a single task.
                # i += 1
                # self.stop()
                # return

            self.__logger.debug("Still alive...")
            # time.sleep(5)

        logging.info(f'Experiment completed, currently does not support waiting.')

    def __clear_jobs(self):
        """
        Function to clear existing jobs in the environment (i.e. old experiments/tests)
        @return: None
        @rtype: None
        """
        namespace = self._config.cluster_config.namespace
        self.__logger.info(f'Clearing old jobs in current namespace: {namespace}')

        for job in self.__client.get(namespace=self._config.cluster_config.namespace)['items']:
            job_name = job['metadata']['name']
            self.__logger.info(f'Deleting: {job_name}')
            try:
                self.__client.custom_api.delete_namespaced_custom_object(
                    PYTORCHJOB_GROUP,
                    PYTORCHJOB_VERSION,
                    namespace,
                    PYTORCHJOB_PLURAL,
                    job_name)
            except Exception as e:
                self.__logger.warning(f'Could not delete: {job_name}')
                print(e)