import sys
from pathlib import Path

import gym

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from EduSim.Envs.KSS import KSSEnv, KSSAgent, kss_train_eval

env: KSSEnv = gym.make("KSS-v2", seed=10)
agent = KSSAgent(env.action_space)

print(env.action_space)

from longling import set_logging_info
set_logging_info()
kss_train_eval(
    agent,
    env,
    max_steps=20,
    max_episode_num=4000,
    level="summary",
)
print("done")
