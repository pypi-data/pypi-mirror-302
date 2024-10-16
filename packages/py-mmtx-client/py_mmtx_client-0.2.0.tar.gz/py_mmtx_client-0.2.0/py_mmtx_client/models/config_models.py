"""Models for the configuration API of the MediaMTX server."""

# pylint: disable=missing-class-docstring # noqa

from typing import List

from pydantic import BaseModel, Field

from py_mmtx_client.models.base_models import ListModel, partial_model


class Permission(BaseModel):
    action: str
    path: str


class AuthInternalUser(BaseModel):
    user: str
    pass_: str = Field(..., alias="pass")
    ips: List
    permissions: List[Permission]


class AuthHTTPExcludeItem(BaseModel):
    action: str
    path: str


class GlobalConfig(BaseModel):
    logLevel: str
    logDestinations: List[str]
    logFile: str
    readTimeout: str
    writeTimeout: str
    writeQueueSize: int
    udpMaxPayloadSize: int
    runOnConnect: str
    runOnConnectRestart: bool
    runOnDisconnect: str
    authMethod: str
    authInternalUsers: List[AuthInternalUser]
    authHTTPAddress: str
    authHTTPExclude: List[AuthHTTPExcludeItem]
    authJWTJWKS: str
    authJWTClaimKey: str
    api: bool
    apiAddress: str
    apiEncryption: bool
    apiServerKey: str
    apiServerCert: str
    apiAllowOrigin: str
    apiTrustedProxies: List
    metrics: bool
    metricsAddress: str
    metricsEncryption: bool
    metricsServerKey: str
    metricsServerCert: str
    metricsAllowOrigin: str
    metricsTrustedProxies: List
    pprof: bool
    pprofAddress: str
    pprofEncryption: bool
    pprofServerKey: str
    pprofServerCert: str
    pprofAllowOrigin: str
    pprofTrustedProxies: List
    playback: bool
    playbackAddress: str
    playbackEncryption: bool
    playbackServerKey: str
    playbackServerCert: str
    playbackAllowOrigin: str
    playbackTrustedProxies: List
    rtsp: bool
    protocols: List[str]
    encryption: str
    rtspAddress: str
    rtspsAddress: str
    rtpAddress: str
    rtcpAddress: str
    multicastIPRange: str
    multicastRTPPort: int
    multicastRTCPPort: int
    serverKey: str
    serverCert: str
    rtspAuthMethods: List[str]
    rtmp: bool
    rtmpAddress: str
    rtmpEncryption: str
    rtmpsAddress: str
    rtmpServerKey: str
    rtmpServerCert: str
    hls: bool
    hlsAddress: str
    hlsEncryption: bool
    hlsServerKey: str
    hlsServerCert: str
    hlsAllowOrigin: str
    hlsTrustedProxies: List
    hlsAlwaysRemux: bool
    hlsVariant: str
    hlsSegmentCount: int
    hlsSegmentDuration: str
    hlsPartDuration: str
    hlsSegmentMaxSize: str
    hlsDirectory: str
    hlsMuxerCloseAfter: str
    webrtc: bool
    webrtcAddress: str
    webrtcEncryption: bool
    webrtcServerKey: str
    webrtcServerCert: str
    webrtcAllowOrigin: str
    webrtcTrustedProxies: List
    webrtcLocalUDPAddress: str
    webrtcLocalTCPAddress: str
    webrtcIPsFromInterfaces: bool
    webrtcIPsFromInterfacesList: List
    webrtcAdditionalHosts: List
    webrtcICEServers2: List
    webrtcHandshakeTimeout: str
    webrtcTrackGatherTimeout: str
    srt: bool
    srtAddress: str


@partial_model
class OptionalGlobalConfig(GlobalConfig):
    pass


class PathConfig(BaseModel):
    name: str
    source: str
    sourceFingerprint: str = Field(default="")
    sourceOnDemand: bool = Field(default=False)
    sourceOnDemandStartTimeout: str = Field(default="10s")
    sourceOnDemandCloseAfter: str = Field(default="10s")
    maxReaders: int = Field(default=0)
    srtReadPassphrase: str = Field(default="")
    fallback: str = Field(default="")
    record: bool = Field(default=False)
    recordPath: str = Field(default="./recordings/%path/%Y-%m-%d_%H-%M-%S-%f")
    recordFormat: str = Field(default="fmp4")
    recordPartDuration: str = Field(default="1s")
    recordSegmentDuration: str = Field(default="1h0m0s")
    recordDeleteAfter: str = Field(default="24h0m0s")
    overridePublisher: bool = Field(default=True)
    srtPublishPassphrase: str = Field(default="")
    rtspTransport: str = Field(default="automatic")
    rtspAnyPort: bool = Field(default=False)
    rtspRangeType: str = Field(default="")
    rtspRangeStart: str = Field(default="")
    sourceRedirect: str = Field(default="")
    rpiCameraCamID: int = Field(default=0)
    rpiCameraWidth: int = Field(default=1920)
    rpiCameraHeight: int = Field(default=1080)
    rpiCameraHFlip: bool = Field(default=False)
    rpiCameraVFlip: bool = Field(default=False)
    rpiCameraBrightness: int = Field(default=0)
    rpiCameraContrast: int = Field(default=1)
    rpiCameraSaturation: int = Field(default=1)
    rpiCameraSharpness: int = Field(default=1)
    rpiCameraExposure: str = Field(default="normal")
    rpiCameraAWB: str = Field(default="auto")
    rpiCameraAWBGains: List[int] = Field(default=[0, 0])
    rpiCameraDenoise: str = Field(default="off")
    rpiCameraShutter: int = Field(default=0)
    rpiCameraMetering: str = Field(default="centre")
    rpiCameraGain: int = Field(default=0)
    rpiCameraEV: int = Field(default=0)
    rpiCameraROI: str = Field(default="")
    rpiCameraHDR: bool = Field(default=False)
    rpiCameraTuningFile: str = Field(default="")
    rpiCameraMode: str = Field(default="")
    rpiCameraFPS: int = Field(default=30)
    rpiCameraAfMode: str = Field(default="continuous")
    rpiCameraAfRange: str = Field(default="normal")
    rpiCameraAfSpeed: str = Field(default="normal")
    rpiCameraLensPosition: int = Field(default=0)
    rpiCameraAfWindow: str = Field(default="")
    rpiCameraFlickerPeriod: int = Field(default=0)
    rpiCameraTextOverlayEnable: bool = Field(default=False)
    rpiCameraTextOverlay: str = Field(default="%Y-%m-%d %H:%M:%S - MediaMTX")
    rpiCameraCodec: str = Field(default="auto")
    rpiCameraIDRPeriod: int = Field(default=60)
    rpiCameraBitrate: int = Field(default=1000000)
    rpiCameraProfile: str = Field(default="main")
    rpiCameraLevel: str = Field(default="4.1")
    runOnInit: str = Field(default="")
    runOnInitRestart: bool = Field(default=False)
    runOnDemand: str = Field(default="")
    runOnDemandRestart: bool = Field(default=False)
    runOnDemandStartTimeout: str = Field(default="10s")
    runOnDemandCloseAfter: str = Field(default="10s")
    runOnUnDemand: str = Field(default="")
    runOnReady: str = Field(default="")
    runOnReadyRestart: bool = Field(default=False)
    runOnNotReady: str = Field(default="")
    runOnRead: str = Field(default="")
    runOnReadRestart: bool = Field(default=False)
    runOnUnread: str = Field(default="")
    runOnRecordSegmentCreate: str = Field(default="")
    runOnRecordSegmentComplete: str = Field(default="")


class PathConfigList(ListModel):
    items: List[PathConfig]


@partial_model
class OptionalPathConfig(PathConfig):
    pass
