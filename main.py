import argparse
import subprocess
import os

from models import AlgorithmName, VideoType


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to CamelCase."""
    return ''.join(word.capitalize() for word in snake_str.split('_'))


def main():
    parser = argparse.ArgumentParser(description='Animate an algorithm with MANIM')
    parser.add_argument(
        'algorithm',
        type=str,
        choices=[name.lower() for name in AlgorithmName.__members__],
        help='Algorithm to animate'
    )
    parser.add_argument(
        '--video-type',
        type=str,
        choices=[name.lower() for name in VideoType.__members__],
        default='test',
        help='Video type (default: test)'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview the animation after rendering'
    )
    args = parser.parse_args()

    algorithm_name = args.algorithm.lower()
    scene_name = to_camel_case(algorithm_name)
    file_path = os.path.join('algorithms', algorithm_name, f'{algorithm_name}.py')

    env = os.environ.copy()
    env['ALGORITHM_NAME'] = args.algorithm.upper()
    env['VIDEO_TYPE'] = args.video_type.upper()

    cmd = ['manim', '-qh']
    if args.preview:
        cmd.append('-p')
    cmd.extend([file_path, scene_name])

    print(f'Running: {" ".join(cmd)}')
    subprocess.run(cmd, env=env)


if __name__ == '__main__':
    main()
