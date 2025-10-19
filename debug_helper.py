import logging
import zenoh
from tcnart.network.discovery import find_camera_sensors, build_channel_configs
from tcnart.network.receiver import resolve_stream_descriptors, start_all_receivers
from tcnart.core.semantic_type import SemanticType
logging.basicConfig(level=logging.DEBUG)

zenoh_config = "/Users/ecku/mydev/artekmed/zenoh_client_config/ueck_mobile/zenoh_config.json5"
topic_prefix = "tcn/loc/pcpd"

zenoh.init_log_from_env_or("warn")
session = zenoh.open(zenoh.Config.from_json5(open(zenoh_config).read()))

cameras = find_camera_sensors(session, f"{topic_prefix}/k4a_capture_multi/rpc/sensor/*/describe")

channels_config, channel_calibration, channel_poses = build_channel_configs(cameras)

stream_config = resolve_stream_descriptors(topic_prefix, None, channel_calibration, channel_poses, channels_config, session)

worker_senders = []

class dbg_helper:
    def __init__(self, stream_name):
        self.stream_name = stream_name
    def __call__(self, frame):
        st = SemanticType(frame.semantic_type)
        print(f"received element {self.stream_name}: {st}")

for stream_name in stream_config:
    worker_senders.append(dbg_helper(stream_name))

threads = start_all_receivers(8, None, worker_senders, session, stream_config)

for thread in threads:
    thread.join()