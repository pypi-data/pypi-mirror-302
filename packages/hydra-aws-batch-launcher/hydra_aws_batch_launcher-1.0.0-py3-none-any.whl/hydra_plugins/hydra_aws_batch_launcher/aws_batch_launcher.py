import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional, Sequence

import boto3
from hydra.core.utils import JobReturn, JobStatus
from hydra.plugins.launcher import Launcher
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig
from tqdm import tqdm
from botocore.config import Config

from hydra_plugins.hydra_aws_batch_launcher.config import AWSBatchLauncherConf

logger = logging.getLogger(__name__)


class AWSBatchLauncher(Launcher):
    def __init__(self, **kwargs: Any) -> None:
        self.config: Optional[DictConfig] = None
        self.task_function: Optional[TaskFunction] = None
        self.hydra_context: Optional[HydraContext] = None

        self.launcher_config: AWSBatchLauncherConf = AWSBatchLauncherConf(**kwargs)

    def setup(
            self,
            *,
            hydra_context: HydraContext,
            task_function: TaskFunction,
            config: DictConfig,
    ) -> None:
        self.config = config
        self.task_function = task_function
        self.hydra_context = hydra_context

    def launch(
            self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        job_name = self.config.hydra.job.name

        logger.info(f"Starting {len(job_overrides)} jobs")
        logger.info("Adding sweep dir and job number to all overrides")
        hashes = []
        for override in job_overrides:
            current_hash = compute_hash(override)
            hashes.append(current_hash)

            if self.launcher_config.override_job_name:
                override.append(f"hydra.job.name={job_name}")
            if self.launcher_config.add_config_hash:
                override.append(f"config_hash={current_hash}")

            for standard_override in self.launcher_config.standard_overrides:
                override.append(standard_override)

        logger.info("Submit AWS Batch jobs")
        with ThreadPoolExecutor(max_workers=self.launcher_config.n_jobs) as executor:
            # Submit all jobs and collect the Future objects
            futures = [
                executor.submit(
                    self.submit_job,
                    current_hash,
                    self.launcher_config.aws_job_queue,
                    self.launcher_config.aws_job_definition,
                    override
                )
                for current_hash, override in zip(hashes, job_overrides)
            ]

            # Use tqdm to display a progress bar as jobs complete
            for future in tqdm(as_completed(futures), total=len(futures)):
                try:
                    # Optionally retrieve the result of each job
                    result = future.result()
                    # You can process the result here if needed
                except Exception as e:
                    # Handle exceptions if any of the jobs fail
                    logger.error(f"Job failed with exception: {e}")

        job_returns = []
        for override in job_overrides:
            job_returns.append(JobReturn(status=JobStatus.COMPLETED))

        return job_returns


    def submit_job(self, job_name, job_queue, job_definition, command):
        retry_config = Config(
            retries={
                'max_attempts': self.launcher_config.aws_retry_max_attempts,  # Total number of retry attempts
                'mode': self.launcher_config.aws_retry_mode  # Retry mode ('legacy', 'standard', or 'adaptive')
            }
        )
        session = boto3.Session(profile_name=self.launcher_config.aws_profile)
        client = session.client('batch', region_name=self.launcher_config.aws_region, config=retry_config)

        job_parameters = {
            'jobName': job_name,
            'jobQueue': job_queue,
            'jobDefinition': job_definition,
            'containerOverrides': {
                'command': command
            }
        }

        response = client.submit_job(**job_parameters)
        return response['jobId']


def compute_hash(parameters_list: Sequence[str]):
    concatenated_params = " ".join(parameters_list)
    hash_object = hashlib.sha256()
    hash_object.update(concatenated_params.encode('utf-8'))
    return hash_object.hexdigest()
