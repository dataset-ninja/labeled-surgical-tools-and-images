# https://www.kaggle.com/datasets/dilavado/labeled-surgical-tools

import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Surgical Tools"
    dataset_path = "/mnt/d/datasetninja-raw/labeled-surgical-tools-and-images/Surgical-Dataset"
    batch_size = 30
    ds_name = "ds"
    images_ext = ".jpg"
    bboxes_ext = ".txt"
    images_folder = "Images/All/images"
    boxes_folder = "Labels/label object names"
    split_train = "Test-Train Groups/train-obj_detector.txt"
    split_test = "Test-Train Groups/test-obj_detector.txt"

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        ann_path = os.path.join(boxes_path, get_file_name(image_path) + bboxes_ext)

        with open(ann_path) as f:
            content = f.read().split("\n")

            for curr_data in content:
                if len(curr_data) != 0:
                    ann_data = list(map(float, curr_data.rstrip().split(" ")))
                    curr_obj_class = idx_to_obj_class[int(ann_data[0])]
                    left = int((ann_data[1] - ann_data[3] / 2) * img_wight)
                    right = int((ann_data[1] + ann_data[3] / 2) * img_wight)
                    top = int((ann_data[2] - ann_data[4] / 2) * img_height)
                    bottom = int((ann_data[2] + ann_data[4] / 2) * img_height)
                    rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                    label = sly.Label(rectangle, curr_obj_class)
                    labels.append(label)

        if get_file_name_with_ext(image_path) in train_names:
            tag = sly.Tag(tag_train)
            tags.append(tag)
        elif get_file_name_with_ext(image_path) in test_names:
            tag = sly.Tag(tag_test)
            tags.append(tag)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    idx_to_obj_class = {
        0: sly.ObjClass("Scalpel nº4", sly.Rectangle),
        1: sly.ObjClass("Straight Dissection Clamp", sly.Rectangle),
        2: sly.ObjClass("Straight Mayo Scissor", sly.Rectangle),
        3: sly.ObjClass("Curved Mayo Scissor", sly.Rectangle),
    }

    tag_train = sly.TagMeta("train", sly.TagValueType.NONE)
    tag_test = sly.TagMeta("test", sly.TagValueType.NONE)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=list(idx_to_obj_class.values()), tag_metas=[tag_train, tag_test]
    )
    api.project.update_meta(project.id, meta.to_json())

    train_names = []
    train_split_path = os.path.join(dataset_path, split_train)
    with open(train_split_path) as f:
        content = f.read().split("\n")

        for curr_data in content:
            train_names.append(curr_data.split("/")[-1])

    test_names = []
    test_split_path = os.path.join(dataset_path, split_test)
    with open(test_split_path) as f:
        content = f.read().split("\n")

        for curr_data in content:
            test_names.append(curr_data.split("/")[-1])

    images_path = os.path.join(dataset_path, images_folder)
    boxes_path = os.path.join(dataset_path, boxes_folder)
    images_names = os.listdir(images_path)

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

    for images_names_batch in sly.batched(images_names, batch_size=batch_size):
        img_pathes_batch = [
            os.path.join(images_path, image_name) for image_name in images_names_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(images_names_batch))
    return project
