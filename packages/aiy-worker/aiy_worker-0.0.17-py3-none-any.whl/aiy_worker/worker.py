
from enum import Enum
from typing import Callable, List, Tuple
import requests
from .ws_client import GraphQLClient
from .types import TaskKind, WsData, Task, PayloadError, TaskKindCapability
from .utils import encode_image, png2webp, png2avif, make_thumbnail, check_pngquant_bin, timer, handle_image
import logging
from PIL import Image
from io import BytesIO
from .utils import upload_file_from_buffer

logger = logging.getLogger(__name__)

sub_task_query = """
  subscription ($token: String!) {{
    subscribeTasks(token: $token, capabilities: [{}]) {{
        id
        name
        text2Image {{
            prompt
            negativePrompt
            seed
            width
            height
            nSteps,
            cfg,
            ipAdapterImageUrl
            ipAdapterFaceImageUrl
            cannyReferenceUrl
            depthReferenceUrl
            openposeReferenceUrl
            loras {{
                name,
                weight
            }}
        }}
        inpaint {{
            prompt
            negativePrompt
            seed
            width
            height
            nSteps,
            initImage,
            maskImage,
            cfg,
            ipAdapterImageUrl
            ipAdapterFaceImageUrl
            cannyReferenceUrl
            depthReferenceUrl
            openposeReferenceUrl
            loras {{
                name,
                weight
            }}
        }}
        canny {{
            imageUrl
        }}
        depth {{
            imageUrl
        }}
        openpose {{
            imageUrl
        }}
        sadtalker {{
            imageUrl
            audioUrl
        }}
        tts {{
            text
            actor
            seed
        }}
        music {{
            prompt
            duration
        }}
    }}
  }}
"""


def wait_shutdown(fn: Callable):
    import signal
    import sys

    def signal_handler(sig, frame):
        logger.info('You pressed Ctrl+C!')
        fn()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    logger.info('Press Ctrl+C')
    # try:
    #     while True:
    #         import time
    #         time.sleep(1)
    # except:
    #     pass


class TaskState:
    RECEIVED = "RECEIVED"
    GENERATING = "GENERATING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"


class AiyWorker:

    def __init__(self, token: str, server: str = "http://localhost:8080", ws_server="ws://localhost:8080", capabilities: List[TaskKindCapability]=[TaskKindCapability.Text2Image]) -> None:
        check_pngquant_bin()
        self.capabilities = capabilities
        self.token = token
        self.server = server
        self.query_url = f'{server}/graphql'
        self.ws_url = f'{ws_server}/subscriptions'
        # requests session
        self.s = requests.Session()
        # TODO 注册 GPU 数据

    def webp_quality(self):
        return 100

    def __on_task(self, _id, data):
        ws_data = WsData(data)
        if ws_data.payload:
            errors = ws_data.payload.errors
            if errors:
                raise Exception(errors[0].message)
            task = ws_data.payload.task
            # received state
            try:
                # 在异步线程中执行
                def received(task):
                    with timer('set worker state to RECEIVED'):
                        self.__submit_task_result(task, TaskState.RECEIVED)

                def _set_progress(progress: float):
                    self.set_progress(task, progress)
                import threading
                t = threading.Thread(target=received, args=(task,))
                t.start()
                logger.info("Start to generate image")
                # 如果是音频、视频，则返回二进制对象和拓展名
                bytes = None
                ext = None
                if task.kind == TaskKind.TEXT_TO_IMAGE:
                    images = self.on_task(task, _set_progress)
                elif task.kind == TaskKind.CANNY:
                    images = self.on_canny_task(task, _set_progress)
                elif task.kind == TaskKind.DEPTH:
                    images = self.on_depth_task(task, _set_progress)
                elif task.kind == TaskKind.OPENPOSE:
                    images = self.on_openpose_task(task, _set_progress)
                elif task.kind == TaskKind.INPAINT:
                    images = self.on_inpaint_task(task, _set_progress)
                elif task.kind == TaskKind.SADTALKER:
                    bytes, ext = self.on_sadtalker_task(task, _set_progress)
                elif task.kind == TaskKind.TTS:
                    bytes, ext = self.on_tts_task(task, _set_progress)
                elif task.kind == TaskKind.MUSIC:
                    bytes, ext = self.on_music_task(task, _set_progress)
                else:
                    raise Exception('Task kind is unknown')
                # 等待 submit 成功
                t.join()
                if bytes is None:
                    logger.info(f"Execute task successfully")
                    with timer('handle image[0]'):
                        result, suffix, thumbnail = handle_image(images[0], webp_quality=self.webp_quality())
                    with timer('set worker state to SUCCESSFUL'):
                        self.__submit_task_result(
                            task, TaskState.SUCCESSFUL, None, result, suffix, thumbnail, None)
                else:
                    if ext not in ['mp3', 'wav', 'mp4', 'webm', "ogg"]:
                        raise Exception(f'Unknown extention: {ext}')
                    r = upload_file_from_buffer(
                        bytes, ext, f'{self.server}/upload_image', self.token)
                    result = r['path']
                    self.__submit_task_result(
                        task, TaskState.SUCCESSFUL, None, None, ext, None, result)
            except Exception as e:
                logger.error(e)
                self.__submit_task_result(task, TaskState.FAILED)

    def __submit_task_result(self, task: Task, state: TaskState, progress: float = None,
                             result: str = None, suffix: str = None,
                             thumbnail_base64: str = None, url: str = None):
        logger.info(f"set worker's state to {state}")
        query = """
mutation ($task_id: Int!, $worker_token: String!, $progress: Float, $result: String, $suffix: String, $thumbnail_base64: String, $url: String) {{
    worker_service {{
        submitTaskResult(
            taskId: $task_id
            workerToken: $worker_token
            state: {state}
            progress: $progress,
            result: {{
                kind: IMAGE,
                bytesBase64: $result
                suffix: $suffix
                thumbnailBase64: $thumbnail_base64
                url: $url
            }}
        )
    }}
}}
        """.format(state=state)
        variables = {
            'task_id': task.id,
            'worker_token': self.token,
            'progress': progress,
            'result': result,
            'suffix': suffix,
            'thumbnail_base64': thumbnail_base64,
            'url': url
        }
        headers = {'Authorization': 'Bearer xxxx'}
        while True:
            try:
                response = self.s.post(self.query_url,
                                       json={
                                           "query": query, "variables": variables, "headers": headers}
                                       )
                break
            except Exception as e:
                logger.error(e)
                self.s = requests.Session()
                import time
                time.sleep(1)

        _r = response.json()
        if _r:
            data = _r['data']
            if data and data.get('worker_service'):
                r = data.get('worker_service').get('submitTaskResult')
                if r == 'OK':
                    return
            errors = [PayloadError(i) for i in _r.get('errors', [])]
            if len(errors) > 0:
                logger.info('Error: %s' % errors[0].message)

    def on_task(self, task: Task, progress_callback: Callable[[float], None]) -> List[Image.Image]:
        """ 接收到任务，并进行处理，返回处理结果（生成的图片的路径） """
        raise NotImplementedError

    def on_canny_task(self, task: Task, progress_callback: Callable[[float], None]) -> List[Image.Image]:
        """ 处理生成 Canny 图片的任务 """
        logger.error('This worker not support canny task, but still received')

    def on_depth_task(self, task: Task, progress_callback: Callable[[float], None]) -> List[Image.Image]:
        """ 处理生成 Depth 图片的任务 """
        logger.error('This worker not support depth task, but still received')

    def on_openpose_task(self, task: Task, progress_callback: Callable[[float], None]) -> List[Image.Image]:
        """ 处理生成 Openpose 图片的任务 """
        logger.error(
            'This worker not support openpose task, but still received')

    def on_inpaint_task(self, task: Task, progress_callback: Callable[[float], None]) -> List[Image.Image]:
        """ 处理生成 inpaint 图片的任务 """
        logger.error(
            'This worker not support inpaint task, but still received')

    def on_sadtalker_task(self, task: Task, progress_callback: Callable[[float], None]) -> Tuple[BytesIO, str]:
        logger.error(
            'This worker not support sadtalker task, but still received')

    def on_tts_task(self, task: Task, progress_callback: Callable[[float], None]) -> Tuple[BytesIO, str]:
        logger.error(
            'This worker not support sadtalker task, but still received')

    def on_music_task(self, task: Task, progress_callback: Callable[[float], None]) -> Tuple[BytesIO, str]:
        logger.error(
            'This worker not support sadtalker task, but still received')

    def set_progress(self, task: Task, progress: float):
        """ 设置进度条 """
        logger.info(f'progress: {progress}')
        self.__submit_task_result(task, TaskState.GENERATING, progress)

    def run(self):
        logger.info("Starting...")
        """ 运行任务 """
        # 发起 ws 连接
        while True:
            try:
                with GraphQLClient(self.ws_url) as client:
                    logger.info("Create client success")
                    self.client = client
                    caps = [i.value for i in self.capabilities]
                    capabilities_s = ','.join(caps)
                    logger.info('Capabilities: {}'.format(capabilities_s))
                    query = sub_task_query.format(capabilities_s)
                    self.sub_id = client.subscribe(query, variables={
                        "token": self.token}, callback=self.__on_task)

                    def on_exit():
                        logger.info("Stop client...")
                        client.stop_subscribe(self.sub_id)
                        logger.info("Stop client success")
                    wait_shutdown(on_exit)
                    client.run()
            except Exception as e:
                pass
            logger.info("Client shutdown. Restart...")
            import time
            time.sleep(3)
