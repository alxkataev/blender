import click

import blender


@click.command()
@click.argument('list1', type=click.File('r'))
@click.argument('list2', type=click.File('r'))
@click.argument('weight1', type=float)
@click.argument('weight2', type=float)
@click.option('--output', type=click.File('w'), default='-')
@click.option('--random-seed', type=int, default=None)
def blend_two_lists_with_weights(list1, list2, weight1, weight2, output, random_seed=None):
    config = blender.BlendingConfig(params={'weights': [weight1, weight2], 'random_seed': random_seed})
    result = blender.blend(map(lambda s: s.strip(), list1), map(lambda s: s.strip(), list2), config=config)
    output.write('\n'.join(result))
