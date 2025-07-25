# Copyright (c) OpenMMLab. All rights reserved.
import tqdm
import pickle
import multiprocessing as mp

from typing import List
from pathlib import Path
from mmdet.registry import DATASETS
from mmengine.fileio import get_local_path
from .coco_panoptic import CocoPanopticDataset

# 멀티프로세싱용 전역 함수들 (pickle 가능하도록 클래스 외부에 정의)
def _process_image_chunk(img_id_chunk: list, ann_file: str, cat2label: dict, data_prefix: dict) -> tuple:
    """
    이미지 ID 청크를 처리하는 멀티프로세싱 함수 (COCO 객체 한 번만 생성)
    
    Args:
        img_id_chunk: 처리할 이미지 ID 리스트
        ann_file: annotation 파일 경로
        cat2label: 카테고리 ID to 라벨 매핑
        
    Returns:
        tuple: (data_list, all_ann_ids)
    """
    try:
        from .api_wrappers import COCOPanoptic
        import os.path as osp
        
        # 청크당 한 번만 COCO 객체 생성
        coco = COCOPanoptic(ann_file)
        
        chunk_data_list = []
        chunk_ann_ids = []
        
        for img_id in tqdm.tqdm(img_id_chunk):
            # 이미지 정보 로드
            raw_img_info = coco.load_imgs([img_id])[0]
            raw_img_info['img_id'] = img_id
            
            # annotation 정보 로드
            ann_ids = coco.get_ann_ids(img_ids=[img_id])
            # raw_ann_info = coco.load_anns(ann_ids)
            raw_ann_info = coco.imgToAnns[img_id]
            chunk_ann_ids.extend(ann_ids)
            
            # parse_data_info 로직을 직접 구현
            parsed_data_info = _parse_panoptic_data_info(
                raw_img_info, raw_ann_info, cat2label, data_prefix
            )
            chunk_data_list.append(parsed_data_info)
        
        return chunk_data_list, chunk_ann_ids
        
    except Exception as e:
        print(f"Error processing chunk: {e}")
        return [], []

def _parse_panoptic_data_info(raw_img_info: dict, raw_ann_info: list, cat2label: dict, data_prefix: dict) -> dict:
    """
    Panoptic 데이터 파싱 함수 (멀티프로세싱용)
    """
    import os.path as osp
    
    # 기본 데이터 구조 생성
    data_info = {}
    
    # 이미지 경로 설정 (data_prefix는 멀티프로세싱에서 접근 불가하므로 기본값 사용)
    # img_path = raw_img_info['file_name']  # 상대 경로만 저장
    seg_map_path = raw_img_info.get('segm_file', '').replace('.jpg', '.png') if raw_img_info.get('segm_file') else None
    

    img_path = osp.join(data_prefix['img'], raw_img_info['file_name'])
    
    if data_prefix.get('seg', None):
        seg_map_path = osp.join(data_prefix['seg'], raw_img_info['segm_file'].replace('.jpg', '.png'))


    data_info['img_path'] = img_path
    data_info['img_id'] = raw_img_info['img_id']
    data_info['seg_map_path'] = seg_map_path
    data_info['height'] = raw_img_info['height']
    data_info['width'] = raw_img_info['width']
    
    # annotation 처리
    instances = []
    segments_info = []
    
    for ann in raw_ann_info:
        if ann['image_id'] != raw_img_info['img_id']:
            continue
            
        instance = {}
        x1, y1, w, h = ann['bbox']
        if ann['area'] <= 0 or w < 1 or h < 1:
            continue
        bbox = [x1, y1, x1 + w, y1 + h]
        category_id = ann['category_id']
        
        if category_id not in cat2label:
            continue
            
        contiguous_cat_id = cat2label[category_id]
        
        # is_thing 정보는 하드코딩 (COCO panoptic 기준)
        is_thing = category_id <= 80  # COCO thing classes는 보통 1-80
        
        if is_thing:
            is_crowd = ann.get('iscrowd', False)
            instance['bbox'] = bbox
            instance['bbox_label'] = contiguous_cat_id
            if not is_crowd:
                instance['ignore_flag'] = 0
            else:
                instance['ignore_flag'] = 1
                is_thing = False

        segment_info = {
            'id': ann['id'],
            'category': contiguous_cat_id,
            'is_thing': is_thing
        }
        segments_info.append(segment_info)
        if len(instance) > 0 and is_thing:
            instances.append(instance)
    
    data_info['instances'] = instances
    data_info['segments_info'] = segments_info
    return data_info

@DATASETS.register_module()
class CocoPanopticGISTDataset(CocoPanopticDataset):

    METAINFO = {'classes': ('동아오츠카 포카리스웨트',
    '웅진 이온더핏 제로 이온음료',
    '게토레이 레몬향',
    '파워에이드 마운틴 블라스트',
    '폴라라 시칠리아나 아란시아타 나벨리나 오렌지 과즙 탄산음료',
    '하이트진로 하이트 제로',
    '버드와이저 제로 비알콜 맥주',
    '호가든 0.0 오비 비알콜 맥주',
    '하이네켄 논알콜릭',
    '칭따오 논알콜릭 병맥주',
    '폴라라 시칠리아나 리모나타 베르델리 레몬 탄산음료',
    '폴라라 시칠리아나 그린 만다리노 베르데 과즙 탄산음료',
    '골드메달 스파클링 애플쥬스',
    '마틸다 스파클링 핑크 그레이프플룻',
    '마틸다 스파클링 레몬 탄산음료',
    '분다버그 진저비어',
    '분다버그 트레디셔널 레몬에이드 탄산음료',
    '분다버그 핑크 그래이프푸르트 탄산음료',
    '분다버그 트로피칼 망고 드링크',
    '분다버그 레몬 라임 앤 비터스',
    '바바리아 애플(그린)',
    '바바리아 레몬(옐로우)',
    '바바리아 오리지널(레드)',
    '바바리아 라임(베이지)',
    '참이슬오리지널',
    '참이슬후레쉬',
    '청포도에이슬(병)',
    '자몽에이슬(병)',
    '처음처럼(병)',
    '처음처럼 새로',
    '처음처럼 새로살구',
    '진로골드',
    '진로매화수',
    '진로이즈백(병)',
    '청하',
    '로제청하',
    '별빛 청하',
    '복받은부라더',
    '하이트(병)',
    'Terra(Bottle)',
    'Kerry(Bottle)',
    'Cass(Bottle)',
    'Crush(Bottle)'),
    'thing_classes': ('동아오츠카 포카리스웨트',
    '웅진 이온더핏 제로 이온음료',
    '게토레이 레몬향',
    '파워에이드 마운틴 블라스트',
    '폴라라 시칠리아나 아란시아타 나벨리나 오렌지 과즙 탄산음료',
    '하이트진로 하이트 제로',
    '버드와이저 제로 비알콜 맥주',
    '호가든 0.0 오비 비알콜 맥주',
    '하이네켄 논알콜릭',
    '칭따오 논알콜릭 병맥주',
    '폴라라 시칠리아나 리모나타 베르델리 레몬 탄산음료',
    '폴라라 시칠리아나 그린 만다리노 베르데 과즙 탄산음료',
    '골드메달 스파클링 애플쥬스',
    '마틸다 스파클링 핑크 그레이프플룻',
    '마틸다 스파클링 레몬 탄산음료',
    '분다버그 진저비어',
    '분다버그 트레디셔널 레몬에이드 탄산음료',
    '분다버그 핑크 그래이프푸르트 탄산음료',
    '분다버그 트로피칼 망고 드링크',
    '분다버그 레몬 라임 앤 비터스',
    '바바리아 애플(그린)',
    '바바리아 레몬(옐로우)',
    '바바리아 오리지널(레드)',
    '바바리아 라임(베이지)',
    '참이슬오리지널',
    '참이슬후레쉬',
    '청포도에이슬(병)',
    '자몽에이슬(병)',
    '처음처럼(병)',
    '처음처럼 새로',
    '처음처럼 새로살구',
    '진로골드',
    '진로매화수',
    '진로이즈백(병)',
    '청하',
    '로제청하',
    '별빛 청하',
    '복받은부라더',
    '하이트(병)',
    'Terra(Bottle)',
    'Kerry(Bottle)',
    'Cass(Bottle)',
    'Crush(Bottle)'),
    'stuff_classes': (),
    'palette': [(250, 0, 0),
    (10, 10, 0),
    (10, 20, 0),
    (10, 30, 0),
    (10, 40, 0),
    (10, 50, 0),
    (10, 60, 0),
    (10, 70, 0),
    (10, 80, 0),
    (10, 90, 0),
    (10, 100, 0),
    (10, 110, 0),
    (10, 120, 0),
    (10, 130, 0),
    (10, 140, 0),
    (10, 150, 0),
    (10, 160, 0),
    (10, 170, 0),
    (10, 180, 0),
    (10, 190, 0),
    (10, 200, 0),
    (10, 210, 0),
    (10, 220, 0),
    (10, 230, 0),
    (10, 240, 0),
    (10, 250, 0),
    (20, 10, 0),
    (20, 20, 0),
    (20, 30, 0),
    (20, 40, 0),
    (20, 50, 0),
    (20, 60, 0),
    (20, 70, 0),
    (20, 80, 0),
    (20, 90, 0),
    (20, 100, 0),
    (20, 110, 0),
    (20, 120, 0),
    (20, 130, 0),
    (20, 140, 0),
    (20, 150, 0),
    (20, 160, 0),
    (20, 170, 0)]
    }


    def __init__(self, light_ids_to_use: list[str], invert_filter: bool = False, **kwargs):
        self.filter_keyword = light_ids_to_use if isinstance(light_ids_to_use, list) else [light_ids_to_use]
        self.invert_filter = invert_filter
        super().__init__(**kwargs) # 상위 클래스 초기화 (여기서 data_list가 로드됨)

    def full_init(self) -> None:
        if self._fully_initialized:
            return
        # load data information

        cache_file = self.ann_file.replace('coco_panoptic_mask_images.json', 'data_list_cach.pkl')

        if Path(cache_file).exists():
            self.data_list = pickle.load(open(cache_file, 'rb'))
        else:
            self.data_list = self.load_data_list()
            pickle.dump(self.data_list, open(cache_file, 'wb'))

        # get proposals from file
        if self.proposal_file is not None:
            self.load_proposals()
        # filter illegal data, such as data that has no annotations.
        self.data_list = self.filter_data()

        # Get subset data according to indices.
        if self._indices is not None:
            self.data_list = self._get_unserialized_subset(self._indices)

        # serialize data_list
        if self.serialize_data:
            self.data_bytes, self.data_address = self._serialize_data()

        self._fully_initialized = True


    def load_data_list(self) -> List[dict]:
        """Load annotations using multiprocessing with chunked img_ids"""
        from functools import partial
        
        with get_local_path(self.ann_file, backend_args=self.backend_args) as local_path:
            ann_file_str = str(local_path)
            
            # 메인 프로세스에서 기본 정보 수집
            coco_main = self.COCOAPI(ann_file_str)
            self.cat_ids = coco_main.get_cat_ids(cat_names=self.metainfo['classes'])
            self.cat2label = {cat_id: i for i, cat_id in enumerate(self.cat_ids)}
            img_ids = coco_main.get_img_ids()
            del coco_main

        # img_ids를 10개 청크로 나누기
        num_processes = 10
        chunk_size = len(img_ids) // num_processes
        if chunk_size == 0:
            chunk_size = 1
        img_id_chunks = [img_ids[i:i + chunk_size] for i in range(0, len(img_ids), chunk_size)]

        data_list = []
        total_ann_ids = []

        try:
            print(f"Processing {len(img_ids)} images with {len(img_id_chunks)} workers...")
            # 멀티프로세싱으로 청크 단위 처리
            with mp.Pool(processes=min(num_processes, len(img_id_chunks))) as pool:
                process_chunk_args = [
                    (chunk, ann_file_str, self.cat2label, self.data_prefix) 
                    for chunk in img_id_chunks
                ]
                
                chunk_results = pool.starmap(_process_image_chunk, process_chunk_args)
                
                # 결과 합치기
                for chunk_data_list, chunk_ann_ids in chunk_results:
                    data_list.extend(chunk_data_list)
                    total_ann_ids.extend(chunk_ann_ids)

        except Exception as e:
            print(f"멀티프로세싱 중 에러 발생: {e}")
            print("단일 프로세스로 fallback...")
            return self._load_data_single_process(img_ids)

        if self.ANN_ID_UNIQUE:
            assert len(set(total_ann_ids)) == len(
                total_ann_ids
            ), f"Annotation ids in '{self.ann_file}' are not unique!"

        return data_list
    
    def _load_data_single_process(self, img_ids: list) -> List[dict]:
        """Fallback method using single process with provided img_ids"""
        print(f"단일 프로세스로 {len(img_ids)}개 이미지 데이터 로딩 중...")
        
        with get_local_path(self.ann_file, backend_args=self.backend_args) as local_path:
            self.coco = self.COCOAPI(str(local_path))
            
        data_list = []
        total_ann_ids = []
        
        for img_id in tqdm.tqdm(img_ids, desc="Loading data"):
            raw_img_info = self.coco.load_imgs([img_id])[0]
            raw_img_info['img_id'] = img_id

            ann_ids = self.coco.get_ann_ids(img_ids=[img_id])
            raw_ann_info = self.coco.load_anns(ann_ids)
            total_ann_ids.extend(ann_ids)

            parsed_data_info = self.parse_data_info({
                'raw_ann_info': raw_ann_info,
                'raw_img_info': raw_img_info
            })
            data_list.append(parsed_data_info)

        if self.ANN_ID_UNIQUE:
            assert len(set(total_ann_ids)) == len(
                total_ann_ids
            ), f"Annotation ids in '{self.ann_file}' are not unique!"

        del self.coco
        return data_list

    # BaseDataset의 filter_data 메서드를 오버라이드합니다.
    def filter_data(self):
        # 1. 먼저 상위 클래스(CocoDataset)의 기본 필터링 로직을 실행합니다.
        #    이렇게 하면 filter_empty_gt, min_size 등의 설정이 먼저 적용됩니다.
        super().filter_data()

        # 2. 이제 당신의 커스텀 경로 키워드 필터링 로직을 추가합니다.
        original_len = len(self.data_list)
        filtered_data_list = []



        for data_info in self.data_list:
            img_path = data_info.get('img_path', '') # 이미지 경로를 가져옵니다.

            # img_path가 없을 경우를 대비하여 방어 코드 추가
            if not img_path:
                print(f"Warning: img_path not found for data_info: {data_info}. Skipping custom filter for this item.")
                filtered_data_list.append(data_info)
                continue

            # 키워드 포함 여부 확인
            is_keyword_present = any(kw in img_path for kw in self.filter_keyword)

            should_keep = False
            if self.invert_filter:
                # 필터 반전: 키워드가 없어야 유지
                should_keep = not is_keyword_present
            else:
                # 일반 필터: 키워드가 있어야 유지
                should_keep = is_keyword_present

            if should_keep:
                filtered_data_list.append(data_info)

        self.data_list = filtered_data_list
        print(f"Custom path keyword filter applied: {original_len} -> {len(self.data_list)} samples remaining.")

        # 필터링된 데이터 리스트를 반환합니다. (BaseDataset의 filter_data는 self.data_list를 업데이트함)
        return self.data_list # BaseDataset의 filter_data는 리스트를 반환하지 않으므로, 이 줄은 없어도 됩니다.
                              # self.data_list를 직접 수정하면 됨.