# coding: utf-8

"""EduSim package initialization and Gym environment registration."""

import sys
from pathlib import Path

# Ensure the repository root is at the front of sys.path so bundled shims (e.g.,
# the vendored ``longling``) are preferred over any site-wide installations.
REPO_ROOT = Path(__file__).resolve().parents[1]
# Always keep the repository root at the front so the vendored dependencies
# (e.g., ``longling``) are resolved before any site-wide installations.
repo_root_str = str(REPO_ROOT)
if repo_root_str in sys.path:
    sys.path.remove(repo_root_str)
sys.path.insert(0, repo_root_str)

# Preload the bundled ``longling`` shim to avoid picking up incompatible
# site-wide installations (which may miss expected submodules like
# ``longling.utils``). With the repository root first on ``sys.path`` this
# import resolves to the vendored copy.
import importlib

importlib.import_module("longling")

from gym.envs.registration import register
from .Envs import *
from .SimOS import train_eval, MetaAgent
from .spaces import *

register(
    id='KSS-v2',
    entry_point='EduSim.Envs:KSSEnv',
)

register(
    id='MBS-EFC-v0',
    entry_point='EduSim.Envs:EFCEnv',
)

register(
    id='MBS-HLR-v0',
    entry_point='EduSim.Envs:HLREnv',
)

register(
    id='MBS-GPL-v0',
    entry_point='EduSim.Envs:GPLEnv',
)

register(
    id='TMS-v1',
    entry_point='EduSim.Envs:TMSEnv',
)
