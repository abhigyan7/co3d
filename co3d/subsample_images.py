from pathlib import Path
from random import sample
import tyro
from tqdm import tqdm

def unlink_files_not_in_picks(root, picks):
    for f in root.glob('*'):
        if f not in picks:
            f.unlink()

@tyro.cli
def main(dataset_root: Path, category_name: str, num_images_to_keep: int = -1):

    category_dir = dataset_root / category_name

    assert category_dir.exists(), category_dir

    if num_images_to_keep < 0:
        return 0

    sequence_dirs = list(category_dir.glob('*'))

    for sequence_dir in (pbar:=tqdm(sequence_dirs)):
        if not sequence_dir.is_dir():
            continue
        try:
            # folders that aren't numbers are metadata
            int(sequence_dir.parts[-1][0])
        except:
            continue

        pbar.set_description('.'.join(sequence_dir.parts[-3:]))
        images_dir = sequence_dir / 'images'
        masks_dir = sequence_dir / 'masks'
        depths_dir = sequence_dir / 'depths'
        depth_masks_dir = sequence_dir / 'depth_masks'

        sequence_images = list(images_dir.glob('*'))
        num_images_in_scene = len(sequence_images)

        if num_images_in_scene <= num_images_to_keep:
            continue

        image_picks: list[Path] = sample(sequence_images, k=num_images_to_keep)
        mask_picks = [masks_dir/f.with_suffix('.png').parts[-1] for f in image_picks]
        depth_picks = [depths_dir/f.with_suffix('.jpg.geometric.png').parts[-1] for f in image_picks]
        depth_mask_picks = [depth_masks_dir/f.with_suffix('.png').parts[-1] for f in image_picks]

        assert all(map(lambda x: x.exists(), image_picks))
        assert all(map(lambda x: x.exists(), mask_picks))
        assert all(map(lambda x: x.exists(), depth_picks))
        assert all(map(lambda x: x.exists(), depth_mask_picks))

        unlink_files_not_in_picks(images_dir, image_picks)
        unlink_files_not_in_picks(masks_dir, mask_picks)
        unlink_files_not_in_picks(depths_dir, depth_picks)
        unlink_files_not_in_picks(depth_masks_dir, depth_mask_picks)