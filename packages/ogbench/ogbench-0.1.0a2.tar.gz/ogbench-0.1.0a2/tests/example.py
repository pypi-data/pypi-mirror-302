import ogbench


def main():
    # Make an environment and load datasets (they will be automatically downloaded if you haven't already).
    # Set `compact_dataset` to True to load a memory-efficient dataset without 'next_observations' (see the comments in
    # `ogbench.utils.load_dataset` for more information).
    env, train_dataset, val_dataset = ogbench.make_env_and_dataset('antmaze-large-navigate-v0', compact_dataset=False)

    ob, info = env.reset(
        options=dict(
            task_id=5,  # `task_id` must be in [1, 5], corresponding to the five evaluation tasks in the paper.
            render_goal=True,  # Set to `True` to render the goal.
        )
    )

    goal = info['goal']  # Goal observation that can be passed to the agent.
    goal_frame = info['goal_rendered']  # Rendered goal image.

    done = False
    while not done:
        action = env.action_space.sample()  # Replace this with your agent's action.
        ob, reward, terminated, truncated, info = env.step(action)  # Gymnasium API has five outputs.
        done = terminated or truncated  # If the goal is reached, the episode will immediately terminate.
        frame = env.render()

    success = info['success']  # Did the agent reach the goal (0.0 or 1.0)?


if __name__ == '__main__':
    main()
