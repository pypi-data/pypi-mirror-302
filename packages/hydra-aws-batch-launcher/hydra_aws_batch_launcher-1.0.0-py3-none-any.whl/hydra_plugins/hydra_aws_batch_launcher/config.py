from dataclasses import dataclass
from typing import Optional, List

from hydra.core.config_store import ConfigStore

@dataclass
class AWSBatchLauncherConf:
    _target_: str = "hydra_plugins.hydra_aws_batch_launcher.aws_batch_launcher.py.AWSBatchLauncher"

    # maximum number of concurrently running threads to submit AWS Batch jobs
    n_jobs: int = -1

    # allows to hard-code backend, otherwise inferred based on prefer and require
    standard_overrides: Optional[List[str]] = None

    # specify which AWS profile to use
    aws_profile: str = "default"

    # specify AWS region where your AWS Batch queue relies on
    aws_region: str = "us-east-1"

    aws_retry_max_attempts: int = 10

    aws_retry_mode: str = "standard"

    aws_job_queue: str = ""
    aws_job_definition: str = ""

    override_job_name: bool = False

    add_config_hash: bool = False



ConfigStore.instance().store(
    group="hydra/launcher",
    name="aws-batch-launcher",
    node=AWSBatchLauncherConf,
    provider="aws_batch_launcher",
)