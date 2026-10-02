"""Optional GNN/RL stack. Data and case helpers also work without PyTorch.

Public exports retain their original names and load only when requested.
"""
from importlib import import_module

_EXPORTS = {
    'ActorCriticOutput': 'backbone',
    'ActorCriticTrainer': 'trainer',
    'BenchmarkCase': 'benchmark',
    'BenchmarkRow': 'benchmark',
    'DEFAULT_EFFORT_LEVELS': 'site_effort_policy',
    'EpisodeMetrics': 'eval_utils',
    'EpisodeRollout': 'training_env',
    'GNNActorCritic': 'backbone',
    'GraphTensors': 'tensor_adapter',
    'IncidentSamplerConfig': 'incident_sampler',
    'JsonlDecisionLogger': 'decision_logger',
    'LoadedCheckpoint': 'checkpointing',
    'PolicyArchitectureConfig': 'checkpointing',
    'RLPlannerAdapter': 'eval_utils',
    'RLSpatialPlannerAdapter': 'spatial_benchmark',
    'RealGraphCase': 'real_graph_cases',
    'RewardConfig': 'reward',
    'RoundDecision': 'round_policy',
    'RoundLogRecord': 'decision_logger',
    'RoundPolicy': 'round_policy',
    'SiteEffortActorHead': 'backbone',
    'SiteEffortDecision': 'site_effort_policy',
    'SiteEffortPolicyArchitectureConfig': 'checkpointing',
    'SiteEffortRoundPolicy': 'site_effort_policy',
    'SpatialBenchmarkCase': 'spatial_benchmark',
    'SpatialBenchmarkRow': 'spatial_benchmark',
    'SpatialEpisodeRollout': 'spatial_training_env',
    'SpatialPrimaryMetrics': 'spatial_metrics',
    'SpatialRewardConfig': 'reward',
    'SpatialRoundLogRecord': 'decision_logger',
    'TrainerConfig': 'trainer',
    'UpdateStats': 'trainer',
    'build_real_incident_case': 'real_graph_cases',
    'compute_spatial_primary_metrics': 'spatial_metrics',
    'eligible_incident_seed_sites': 'real_graph_cases',
    'graph_state_to_tensors': 'tensor_adapter',
    'load_optimizer_state': 'checkpointing',
    'load_policy_checkpoint': 'checkpointing',
    'make_benchmark_cases': 'benchmark',
    'read_jsonl_records': 'decision_logger',
    'round_reward': 'reward',
    'round_reward_components': 'reward',
    'run_benchmark_suite': 'benchmark',
    'run_episode': 'training_env',
    'run_planner_episode': 'eval_utils',
    'run_spatial_benchmark_suite': 'spatial_benchmark',
    'run_spatial_episode': 'spatial_training_env',
    'run_spatial_planner_case': 'spatial_benchmark',
    'sample_incident': 'incident_sampler',
    'save_policy_checkpoint': 'checkpointing',
    'spatial_round_reward_components': 'reward',
    'spatial_terminal_reward_components': 'reward',
    'terminal_missed_extent_penalty': 'reward',
    'write_benchmark_csv': 'benchmark',
    'write_spatial_benchmark_csv': 'spatial_benchmark',
}
__all__ = sorted(_EXPORTS)


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(f".{_EXPORTS[name]}", __name__), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
