from pathlib import Path
from PIL import Image
import shutil

RAW_DIR = Path("data/food11_raw")
PROCESSED_DIR = Path("data/food11_processed")
MINI_DIR = Path("data/food11_processed_mini")

SPLITS = ["training", "evaluation", "validation"]

CLASSES = {
    "0": "Bread",
    "1": "Dairy product",
    "2": "Dessert",
    "3": "Egg",
    "4": "Fried food",
    "5": "Meat",
    "6": "Noodles-Pasta",
    "7": "Rice",
    "8": "Seafood",
    "9": "Soup",
    "10": "Vegetable-Fruit",
}

IMAGE_SIZE = (128, 128)
MINI_LIMIT = 100


def prepare_output():
    for folder in [PROCESSED_DIR, MINI_DIR]:
        if folder.exists():
            shutil.rmtree(folder)

        for split in SPLITS:
            for class_name in CLASSES.values():
                (folder / split / class_name).mkdir(
                    parents=True,
                    exist_ok=True
                )


def process_split(split):
    source_dir = RAW_DIR / split

    mini_counts = {
        class_name: 0
        for class_name in CLASSES.values()
    }

    files = list(source_dir.iterdir())

    print(f"\nProcessing {split}: {len(files)} images")

    for i, image_path in enumerate(files, start=1):

        if not image_path.is_file():
            continue

        class_id = image_path.name.split("_")[0]

        if class_id not in CLASSES:
            print(f"Skipping unknown file: {image_path.name}")
            continue

        class_name = CLASSES[class_id]

        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img = img.resize(IMAGE_SIZE)

                processed_path = (
                    PROCESSED_DIR
                    / split
                    / class_name
                    / image_path.name
                )

                img.save(processed_path)

                if mini_counts[class_name] < MINI_LIMIT:
                    mini_path = (
                        MINI_DIR
                        / split
                        / class_name
                        / image_path.name
                    )

                    img.save(mini_path)

                    mini_counts[class_name] += 1

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

        if i % 500 == 0:
            print(f"Processed {i}/{len(files)}")


def main():
    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_DIR}"
        )

    prepare_output()

    for split in SPLITS:
        process_split(split)

    print("\nDone.")
    print(f"Processed dataset: {PROCESSED_DIR}")
    print(f"Mini dataset: {MINI_DIR}")


if __name__ == "__main__":
    main()