import json
import os
import itertools
import pandas as pd
import io
from PIL import Image
import base64
from datetime import datetime
from typing import Dict, Optional, Tuple, Union, Any

import cv2
import numpy as np
from pycocotools import mask
from shapely.geometry import Polygon
from skimage.draw import polygon

from simba.mixins.geometry_mixin import GeometryMixin
from simba.mixins.image_mixin import ImageMixin
from simba.utils.checks import check_instance, check_int, check_valid_array, check_if_dir_exists, check_if_keys_exist_in_dict, check_file_exist_and_readable, check_if_valid_img
from simba.utils.enums import Formats
from simba.utils.read_write import get_video_meta_data, read_df, read_frm_of_video, find_files_of_filetypes_in_directory, get_fn_ext
from simba.utils.errors import NoFilesFoundError, InvalidInputError
from simba.utils.printing import SimbaTimer, stdout_success


def geometry_to_rle(geometry: Union[np.ndarray, Polygon], img_size: Tuple[int, int]):
    """
    Converts a geometry (polygon or NumPy array) into a Run-Length Encoding (RLE) mask, suitable for object detection or segmentation tasks.

    :param geometry: The geometry to be converted into an RLE. It can be either a shapely Polygon or a (n, 2) np.ndarray with vertices.
    :param img_size:  A tuple `(height, width)` representing the size of the image in which the geometry is to be encoded. This defines the dimensions of the output binary mask.
    :return:
    """
    check_instance(source=geometry_to_rle.__name__, instance=geometry, accepted_types=(Polygon, np.ndarray))
    if isinstance(geometry, (Polygon,)):
        geometry = geometry.exterior.coords
    else:
        check_valid_array(data=geometry, source=geometry_to_rle.__name__, accepted_ndims=[(2,)], accepted_dtypes=Formats.NUMERIC_DTYPES.value)
    binary_mask = np.zeros(img_size, dtype=np.uint8)
    rr, cc = polygon(geometry[:, 0].flatten(), geometry[:, 1].flatten(), img_size)
    binary_mask[rr, cc] = 1
    rle = mask.encode(np.asfortranarray(binary_mask))
    rle['counts'] = rle['counts'].decode('utf-8')
    return rle

def geometries_to_coco(geometries: Dict[str, np.ndarray],
                       video_path: Union[str, os.PathLike],
                       save_dir: Union[str, os.PathLike],
                       version: Optional[int] = 1,
                       description: Optional[str] = None,
                       licences: Optional[str] = None):
    """
    :example:
    >>> data_path = r"C:\troubleshooting\mitra\project_folder\csv\outlier_corrected_movement_location\FRR_gq_Saline_0624.csv"
    >>> animal_data = read_df(file_path=data_path, file_type='csv', usecols=['Nose_x', 'Nose_y', 'Tail_base_x', 'Tail_base_y', 'Left_side_x', 'Left_side_y', 'Right_side_x', 'Right_side_y']).values.reshape(-1, 4, 2)[0:20].astype(np.int32)
    >>> animal_polygons = GeometryMixin().bodyparts_to_polygon(data=animal_data)
    >>> animal_polygons = GeometryMixin().multiframe_minimum_rotated_rectangle(shapes=animal_polygons)
    >>> animal_polygons = GeometryMixin().geometries_to_exterior_keypoints(geometries=animal_polygons)
    >>> animal_polygons = GeometryMixin.keypoints_to_axis_aligned_bounding_box(keypoints=animal_polygons)
    >>> animal_polygons = {0: animal_polygons}
    >>> geometries_to_coco(geometries=animal_polygons, video_path=r'C:\troubleshooting\mitra\project_folder\videos\FRR_gq_Saline_0624.mp4', save_dir=r"C:\troubleshooting\coco_data")
    """

    categories = []
    for cnt, i in enumerate(geometries.keys()): categories.append({'id': i, 'name': i, 'supercategory': i})
    results = {'info': {'year': datetime.now().year, 'version': version, 'description': description}, 'licences': licences, 'categories': categories}
    video_data = get_video_meta_data(video_path)
    w, h = video_data['width'], video_data['height']
    images = []
    annotations = []
    img_names = []
    if not os.path.isdir(save_dir): os.makedirs(save_dir)
    save_img_dir = os.path.join(save_dir, 'img')
    if not os.path.isdir(save_img_dir): os.makedirs(save_img_dir)
    for category_cnt, (category_id, category_data) in enumerate(geometries.items()):
        for img_cnt in range(category_data.shape[0]):
            img_geometry = category_data[img_cnt]
            img_name = f'{video_data["video_name"]}_{img_cnt}.png'
            if img_name not in img_names:
                images.append({'id': img_cnt, 'width': w, 'height': h, 'file_name': img_name})
                img = read_frm_of_video(video_path=video_path, frame_index=img_cnt)
                img_save_path = os.path.join(save_img_dir, img_name)
                cv2.imwrite(img_save_path, img)
                img_names.append(img_name)
            annotation_id = category_cnt * img_cnt + 1
            d = GeometryMixin().get_shape_lengths_widths(shapes=Polygon(img_geometry))
            a_h, a_w, a_a = d['max_length'], d['max_width'], d['max_area']
            bbox = [int(category_data[img_cnt][0][0]), int(category_data[img_cnt][0][1]), int(a_w), int(a_h)]
            rle = geometry_to_rle(geometry=img_geometry, img_size=(h, w))
            annotation = {'id': annotation_id, 'image_id': img_cnt, 'category_id': category_id, 'bbox': bbox, 'area': a_a, 'iscrowd': 0, 'segmentation': rle}
            annotations.append(annotation)
    results['images'] = images
    results['annotations'] = annotations
    with open(os.path.join(save_dir, f"annotations.json"), "w") as final:
        json.dump(results, final)


def geometries_to_yolo(geometries: Dict[Union[str, int], np.ndarray],
                       video_path: Union[str, os.PathLike],
                       save_dir: Union[str, os.PathLike],
                       verbose: Optional[bool] = True,
                       sample: Optional[int] = None,
                       obb: Optional[bool] = False) -> None:
    """
    Converts geometrical shapes (like polygons) into YOLO format annotations and saves them along with corresponding video frames as images.

    :param Dict[Union[str, int], np.ndarray geometries: A dictionary where the keys represent category IDs (either string or int), and the values are NumPy arrays of shape `(n_frames, n_points, 2)`. Each entry in the array represents the geometry of an object in a particular frame (e.g., keypoints or polygons).
    :param Union[str, os.PathLike] video_path: Path to the video file from which frames are extracted. The video is used to extract images corresponding to the geometrical annotations.
    :param Union[str, os.PathLike] save_dir: The directory where the output images and YOLO annotation files will be saved. Images will be stored in a subfolder `images/` and annotations in `labels/`.
    :param verbose: If `True`, prints progress while processing each frame. This can be useful for monitoring long-running tasks. Default is `True`.
    :param sample: If provided, only a random sample of the geometries will be used for annotation. This value represents the number of frames to sample.  If `None`, all frames will be processed. Default is `None`.
    :param obb: If `True`, uses oriented bounding boxes (OBB) by extracting the four corner points of the geometries. Otherwise, axis-aligned bounding boxes (AABB) are used. Default is `False`.
    :return None:

    :example:
    >>> data_path = r"C:\troubleshooting\mitra\project_folder\csv\outlier_corrected_movement_location\501_MA142_Gi_CNO_0514.csv"
    >>> animal_data = read_df(file_path=data_path, file_type='csv', usecols=['Nose_x', 'Nose_y', 'Tail_base_x', 'Tail_base_y', 'Left_side_x', 'Left_side_y', 'Right_side_x', 'Right_side_y']).values.reshape(-1, 4, 2).astype(np.int32)
    >>> animal_polygons = GeometryMixin().bodyparts_to_polygon(data=animal_data)
    >>> poygons = GeometryMixin().multiframe_minimum_rotated_rectangle(shapes=animal_polygons)
    >>> animal_polygons = GeometryMixin().geometries_to_exterior_keypoints(geometries=poygons)
    >>> animal_polygons = {0: animal_polygons}
    >>> geometries_to_yolo(geometries=animal_polygons, video_path=r'C:\troubleshooting\mitra\project_folder\videos\501_MA142_Gi_CNO_0514.mp4', save_dir=r"C:\troubleshooting\coco_data", sample=500, obb=True)
    """

    video_data = get_video_meta_data(video_path)
    categories = list(geometries.keys())
    w, h = video_data['width'], video_data['height']
    if not os.path.isdir(save_dir): os.makedirs(save_dir)
    save_img_dir = os.path.join(save_dir, 'images')
    save_labels_dir = os.path.join(save_dir, 'labels')
    if not os.path.isdir(save_img_dir): os.makedirs(save_img_dir)
    if not os.path.isdir(save_labels_dir): os.makedirs(save_labels_dir)
    results, samples = {}, None
    if sample is not None:
        check_int(name='sample', value=sample, min_value=1, max_value=geometries[categories[0]].shape[0])
        samples = np.random.choice(np.arange(0, geometries[categories[0]].shape[0]-1), sample)
    for category_cnt, (category_id, category_data) in enumerate(geometries.items()):
        for img_cnt in range(category_data.shape[0]):
            if sample is not None and img_cnt not in samples:
                continue
            else:
                if verbose:
                    print(f'Writing category {category_cnt}, Image: {img_cnt}.')
                img_geometry = category_data[img_cnt]
                img_name = f'{video_data["video_name"]}_{img_cnt}.png'
                if not obb:
                    shape_stats = GeometryMixin.get_shape_statistics(shapes=Polygon(img_geometry))
                    x_center = shape_stats['centers'][0][0] / w
                    y_center = shape_stats['centers'][0][1] / h
                    width = shape_stats['widths'][0] / w
                    height = shape_stats['lengths'][0] / h
                    img_results = ' '.join([str(category_id), str(x_center), str(y_center), str(width), str(height)])
                else:
                    img_geometry = img_geometry[1:]
                    x1, y1 = img_geometry[0][0] / w, img_geometry[0][1] / h
                    x2, y2 = img_geometry[1][0] / w, img_geometry[1][1] / h
                    x3, y3 = img_geometry[2][0] / w, img_geometry[2][1] / h
                    x4, y4 = img_geometry[3][0] / w, img_geometry[3][1] / h
                    img_results = ' '.join([str(category_id), str(x1), str(y1), str(x2), str(y2), str(x3), str(y3), str(x4), str(y4)])
                if img_name not in results.keys():
                    img = read_frm_of_video(video_path=video_path, frame_index=img_cnt)
                    img_save_path = os.path.join(save_img_dir, img_name)
                    cv2.imwrite(img_save_path, img)
                    results[img_name] = [img_results]
                else:
                    results[img_name].append(img_results)

    for k, v in results.items():
        name = k.split(sep='.', maxsplit=2)[0]
        file_name = os.path.join(save_labels_dir, f'{name}.txt')
        with open(file_name, mode='wt', encoding='utf-8') as f:
            f.write('\n'.join(v))


def _b64_to_arr(img_b64) -> np.ndarray:
    """
    Helper to convert byte string (e.g., from labelme) to image in numpy format
    """
    f = io.BytesIO()
    f.write(base64.b64decode(img_b64))
    img_arr = np.array(Image.open(f))
    return img_arr



def _arr_to_b64(x: np.ndarray) -> str:
    """
    Helper to convert image  to byte string
    """
    _, buffer = cv2.imencode('.jpg', x)
    return base64.b64encode(buffer).decode("utf-8")


def labelme_to_dlc(labelme_dir: Union[str, os.PathLike],
                   scorer: Optional[str] = 'SN',
                   save_dir: Optional[Union[str, os.PathLike]] = None) -> None:
    """
    Convert labels from labelme format to DLC format.

    :param Union[str, os.PathLike] labelme_dir: Directory with labelme json files.
    :param Optional[str] scorer: Name of the scorer (anticipated by DLC as header)
    :param Optional[Union[str, os.PathLike]] save_dir: Directory where to save the DLC annotations. If None, then same directory as labelme_dir with `_dlc_annotations` suffix.
    :return: None

    :example:
    >>> labelme_dir = r'D:\ts_annotations'
    >>> labelme_to_dlc(labelme_dir=labelme_dir)
    """

    check_if_dir_exists(in_dir=labelme_dir)
    annotation_paths = find_files_of_filetypes_in_directory(directory=labelme_dir, extensions=['.json'], raise_error=True)
    results_dict = {}
    images = {}
    for annot_path in annotation_paths:
        with open(annot_path) as f:
            annot_data = json.load(f)
        check_if_keys_exist_in_dict(data=annot_data, key=['shapes', 'imageData', 'imagePath'], name=annot_path)
        img_name = os.path.basename(annot_data['imagePath'])
        images[img_name] = _b64_to_arr(annot_data['imageData'])
        for bp_data in annot_data['shapes']:
            check_if_keys_exist_in_dict(data=bp_data, key=['label', 'points'], name=annot_path)
            point_x, point_y = bp_data['points'][0][0], bp_data['points'][0][1]
            lbl = bp_data['label']
            id = os.path.join('labeled-data', os.path.basename(labelme_dir), img_name)
            if id not in results_dict.keys():
                results_dict[id] = {f'{lbl}': {'x': point_x, 'y': point_y}}
            else:
                results_dict[id].update({f'{lbl}': {'x': point_x, 'y': point_y}})

    if save_dir is None:
        save_dir = os.path.join(os.path.dirname(labelme_dir), os.path.basename(labelme_dir) + '_dlc_annotations')
        if not os.path.isdir(save_dir): os.makedirs(save_dir)

    bp_names = set()
    for img, bp in results_dict.items(): bp_names.update(set(bp.keys()))
    col_names = list(itertools.product(*[[scorer], bp_names, ['x', 'y']]))
    columns = pd.MultiIndex.from_tuples(col_names)
    results = pd.DataFrame(columns=columns)
    results.columns.names = ['scorer', 'bodyparts', 'coords']
    for img, bp_data in results_dict.items():
        for bp_name, bp_cords in bp_data.items():
            results.at[img, (scorer, bp_name, 'x')] = bp_cords['x']
            results.at[img, (scorer, bp_name, 'y')] = bp_cords['y']

    for img_name, img in images.items():
        img_save_path = os.path.join(save_dir, img_name)
        cv2.imwrite(img_save_path, img)
    save_path = os.path.join(save_dir, f'CollectedData_{scorer}.csv')
    results.to_csv(save_path)


def dlc_to_labelme(dlc_dir: Union[str, os.PathLike],
                   save_dir: Union[str, os.PathLike],
                   labelme_version: Optional[str] = '5.3.1',
                   flags: Optional[Dict[Any, Any]] = None,
                   verbose: Optional[bool] = True) -> None:

    """
    Convert a folder of DLC annotations into labelme json format.

    :param dlc_dir: Folder with DLC annotations. I.e., directory inside
    :param save_dir: Directory to where to save the labelme json files.
    :param labelme_version: Version number encoded in the json files.
    :param flags: Flags included in the json files.
    :param verbose: If True, prints progress/
    :return: None

    :example:
    >>> dlc_to_labelme(dlc_dir=r"D:\TS_DLC\labeled-data\ts_annotations", save_dir=r"C:\troubleshooting\coco_data\labels\test")
    """

    timer = SimbaTimer(start=True)
    check_if_dir_exists(dlc_dir, source=f'{dlc_to_labelme.__name__}')
    collected_data_path = find_files_of_filetypes_in_directory(directory=dlc_dir, extensions=['.csv'])
    collected_data_path = [x for x in collected_data_path if 'CollectedData' in x]
    if len(collected_data_path) > 1:
        raise NoFilesFoundError(msg=f'Two CSV annotation files found in {dlc_dir}', source=dlc_to_labelme.__name__)
    elif len(collected_data_path) == 0:
        raise NoFilesFoundError(msg=f'No CSV annotation files found in {dlc_dir} with anticipated CollectedData sub-string', source=dlc_to_labelme.__name__)
    version = labelme_version
    annotation_data = pd.read_csv(collected_data_path[0], header=[0, 1, 2])
    body_parts = set()
    if flags is None:
        flags = {}
    body_part_headers = ['image']
    for i in annotation_data.columns[1:]:
        if 'unnamed:' not in i[1].lower():
            body_parts.add(i[1])
    for i in body_parts:
        body_part_headers.append(f'{i}_x'); body_part_headers.append(f'{i}_y')
    annotation_data = annotation_data.iloc[:, 2:]
    annotation_data.columns = body_part_headers
    for cnt, (idx, idx_data) in enumerate(annotation_data.iterrows()):
        if verbose:
            print(f'Processing image {cnt+1}/{len(annotation_data)}...')
        imgPath = idx_data['image']
        img_path = os.path.join(dlc_dir, imgPath)
        img = cv2.imread(img_path)
        check_file_exist_and_readable(img_path)
        idx_data = idx_data.to_dict()
        shapes = []
        for bp_name in body_parts:
            img_shapes = {'label': bp_name,
                          'points': [idx_data[f'{bp_name}_x'], idx_data[f'{bp_name}_y']],
                          'group_id': None,
                          'description': "",
                          'shape_type': 'point',
                          'flags': {}}
            shapes.append(img_shapes)
        out = {"version": version,
               'flags': flags,
               'shapes': shapes,
               'imagePath': imgPath,
               'imageData': _arr_to_b64(img),
               'imageHeight': img.shape[0],
               'imageWidth': img.shape[1]}
        save_path = os.path.join(save_dir, get_fn_ext(filepath=imgPath)[1] + '.json')
        with open(save_path, "w") as f:
            json.dump(out, f)
    timer.stop_timer()
    if verbose:
        stdout_success(f'Labelme data for {len(annotation_data)} image(s) saved in {save_dir} directory', elapsed_time=timer.elapsed_time_str)


def _b64_dict_to_imgs(x: Dict[str, str]):
    """
    :example:
    >>> df = labelme_to_df(labelme_dir=r'C:\troubleshooting\coco_data\labels\test_2')
    >>> x = df.set_index('image_name')['image'].to_dict()
    >>> _b64_dict_to_imgs(x)
    """
    results = {}
    for k, v in x.items():
        results[k] = _b64_to_arr(v)
    return results


def normalize_img_dict(img_dict: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    img_ndims = set()
    for img in img_dict.values():
        check_if_valid_img(data=img, source=normalize_img_dict.__name__, raise_error=True)
        img_ndims.add(img.ndim)
    if len(img_ndims) > 1:
        raise InvalidInputError(msg=f'Images in dictonary have to all be either color OR greyscale. Got {img_ndims} dimensions.', source=normalize_img_dict.__name__)

    results = {}
    if list(img_ndims)[0] == 2:
        all_pixels = np.concatenate([img.ravel() for img in img_dict.values()])
        mean = np.mean(all_pixels)
        std = np.std(all_pixels)
        for img_name, img in img_dict.items():
            v = (img - mean) / std
            v_rescaled = np.clip((v * 64) + 128, 0, 255)
            results[img_name] = v_rescaled.astype(np.uint8)
    else:
        r, g, b = [], [], []
        for img in img_dict.values():
            r.append(np.mean(img[:, :, 0]))
            g.append(np.mean(img[:, :, 1]))
            b.append(np.mean(img[:, :, 2]))
        r_mean, r_std = np.mean(r), np.std(r)
        g_mean, g_std = np.mean(g), np.std(g)
        b_mean, b_std = np.mean(b), np.std(b)
        for img_name, img in img_dict.items():
            r = (img[:, :, 0] - r_mean) / r_std
            g = (img[:, :, 1] - g_mean) / g_std
            b = (img[:, :, 2] - b_mean) / b_std
            r = np.clip((r * 64) + 128, 0, 255)  # Scale and shift
            g = np.clip((g * 64) + 128, 0, 255)  # Scale and shift
            b = np.clip((b * 64) + 128, 0, 255)  # Scale and shift
            results[img_name] = np.stack([r, g, b], axis=-1).astype(np.uint8)

    return results

def labelme_to_df(labelme_dir: Union[str, os.PathLike],
                  greyscale: Optional[bool] = False,
                  pad: Optional[bool] = False,
                  normalize: Optional[bool] = False) -> pd.DataFrame:

    """
    >>> labelme_to_df(labelme_dir=r'C:\troubleshooting\coco_data\labels\test_2')
    """
    check_if_dir_exists(in_dir=labelme_dir)
    annotation_paths = find_files_of_filetypes_in_directory(directory=labelme_dir, extensions=['.json'], raise_error=True)
    images = {}
    annotations = []
    for annot_path in annotation_paths:
        with open(annot_path) as f: annot_data = json.load(f)
        check_if_keys_exist_in_dict(data=annot_data, key=['shapes', 'imageData'], name=annot_path)
        img_name = os.path.basename(annot_data['imagePath'])
        images[img_name] = _b64_to_arr(annot_data['imageData'])
        if greyscale:
            print(greyscale)
            if len(images[img_name].shape) != 2:
                images[img_name] = (0.07 * images[img_name][:, :, 2] + 0.72 * images[img_name][:, :, 1] + 0.21 * images[img_name][:, :, 0]).astype(np.uint8)
        img_data = {}
        for bp_data in annot_data['shapes']:
            check_if_keys_exist_in_dict(data=bp_data, key=['label', 'points'], name=annot_path)
            point_x, point_y = bp_data['points'][0], bp_data['points'][1]
            lbl = bp_data['label']
            img_data[f'{lbl}_x'], img_data[f'{lbl}_y'] = point_x, point_y
        img_data['image_name'] = img_name
        annotations.append(pd.DataFrame.from_dict(img_data, orient='index').T)
    if pad:
        images = ImageMixin.pad_img_stack(image_dict=images)
    if normalize:
        images = normalize_img_dict(img_dict=images)
    img_lst = []
    for k, v in images.items():
        img_lst.append(_arr_to_b64(v))
    out = pd.concat(annotations).reset_index(drop=True)
    out['image'] = img_lst
    return out


#df = labelme_to_df(labelme_dir=r'C:\troubleshooting\coco_data\labels\test_read', greyscale=False, pad=True, normalize=False)




#dlc_to_labelme(dlc_dir=r"D:\TS_DLC\labeled-data\ts_annotations", save_dir=r"C:\troubleshooting\coco_data\labels\test")

#





# x = df.set_index('image_name')['image'].to_dict()
# _b64_dict_to_imgs(x)



# dlc_to_labelme(dlc_dir=r"D:\TS_DLC\labeled-data\ts_annotations", save_dir=r"C:\troubleshooting\coco_data\labels\test")


#
# def dlc_to_coco():
#     pass
#     #TODO
#


