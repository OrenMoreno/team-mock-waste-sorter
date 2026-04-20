import os
from pathlib import Path

REMAP = {
    0:  1,  # battery               -> metal_can
    1:  1,  # can                   -> metal_can
    2:  2,  # cardboard_bowl        -> paper_cardboard
    3:  2,  # cardboard_box         -> paper_cardboard
    4:  0,  # chemical_plastic_bottle -> plastic
    5:  0,  # chemical_plastic_gallon -> plastic
    6:  1,  # chemical_spray_can    -> metal_can
    7:  3,  # light_bulb            -> other
    8:  1,  # paint_bucket          -> metal_can
    9:  0,  # plastic_bag           -> plastic
    10: 0,  # plastic_bottle        -> plastic
    11: 0,  # plastic_bottle_cap    -> plastic
    12: 0,  # plastic_box           -> plastic
    13: 0,  # plastic_cultery       -> plastic
    14: 0,  # plastic_cup           -> plastic
    15: 0,  # plastic_cup_lid       -> plastic
    16: 2,  # reuseable_paper       -> paper_cardboard
    17: 2,  # scrap_paper           -> paper_cardboard
    18: 0,  # scrap_plastic         -> plastic
    19: 0,  # snack_bag             -> plastic
    20: 3,  # stick                 -> other
    21: 0,  # straw                 -> plastic
}

def remap_labels_in_folder(folder):
    folder = Path(folder)
    if not folder.exists():
        print(f"  Skipping {folder} - not found")
        return
    label_files = list(folder.rglob("*.txt"))
    print(f"Processing {len(label_files)} files in {folder}...")
    for fpath in label_files:
        lines = fpath.read_text().splitlines()
        new_lines = []
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            old_cls = int(parts[0])
            new_cls = REMAP.get(old_cls, 3)
            new_lines.append(f"{new_cls} {' '.join(parts[1:])}")
        fpath.write_text("\n".join(new_lines))
    print(f"  Done.")

for split in ["train", "valid", "test"]:
    remap_labels_in_folder(Path("dataset") / split / "labels")

print("\nRemapping complete!")
