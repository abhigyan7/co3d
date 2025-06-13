from pathlib import Path
import tyro
from statistics import mean, median

@tyro.cli
def main(dataset_path: Path):
    for d in dataset_path.glob('*'):
        if not d.is_dir():
            continue
        if d.parts[-1][0] == '_':
            continue

        category_name = d.parts[-1]
        lens = []

        for scene in d.glob('*'):
            if not scene.is_dir():
                continue
            try:
                # folders that aren't numbers are metadata
                int(scene.parts[-1][0])
            except:
                continue
            scene_images = (scene / 'images').glob('*')
            num_images_in_scene = len(list(scene_images))
            lens.append(num_images_in_scene)
        print(f'{category_name}, num_scenes={len(lens)}, mean={mean(lens):.1f}, median={median(lens):.1f}, min={min(lens)}, max={max(lens)}')
