# coding: utf-8

# flake8: noqa
"""
    OurSky Platform

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.3.4971
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


# import models into model package
from ourskyai_platform_api.models.camera_mode import CameraMode
from ourskyai_platform_api.models.empty_success import EmptySuccess
from ourskyai_platform_api.models.filter_type import FilterType
from ourskyai_platform_api.models.fits_header import FitsHeader
from ourskyai_platform_api.models.location import Location
from ourskyai_platform_api.models.metric_type import MetricType
from ourskyai_platform_api.models.mount_type import MountType
from ourskyai_platform_api.models.node_state import NodeState
from ourskyai_platform_api.models.optical_tube_type import OpticalTubeType
from ourskyai_platform_api.models.orbit_type import OrbitType
from ourskyai_platform_api.models.plate_solve_parameters import PlateSolveParameters
from ourskyai_platform_api.models.shutter_type import ShutterType
from ourskyai_platform_api.models.successful_create import SuccessfulCreate
from ourskyai_platform_api.models.tracking_type import TrackingType
from ourskyai_platform_api.models.upload_priority import UploadPriority
from ourskyai_platform_api.models.v1_auto_focus_instruction import V1AutoFocusInstruction
from ourskyai_platform_api.models.v1_auto_focus_instruction_coordinates_inner import V1AutoFocusInstructionCoordinatesInner
from ourskyai_platform_api.models.v1_camera import V1Camera
from ourskyai_platform_api.models.v1_client_token import V1ClientToken
from ourskyai_platform_api.models.v1_complete_observation_request import V1CompleteObservationRequest
from ourskyai_platform_api.models.v1_create_autofocus_result_request import V1CreateAutofocusResultRequest
from ourskyai_platform_api.models.v1_create_image_set_image_request import V1CreateImageSetImageRequest
from ourskyai_platform_api.models.v1_create_image_set_image_response import V1CreateImageSetImageResponse
from ourskyai_platform_api.models.v1_create_image_set_request import V1CreateImageSetRequest
from ourskyai_platform_api.models.v1_create_mount_request import V1CreateMountRequest
from ourskyai_platform_api.models.v1_create_node_controller_artifact_request import V1CreateNodeControllerArtifactRequest
from ourskyai_platform_api.models.v1_create_node_diagnostic import V1CreateNodeDiagnostic
from ourskyai_platform_api.models.v1_create_node_diagnostics_request import V1CreateNodeDiagnosticsRequest
from ourskyai_platform_api.models.v1_create_node_event import V1CreateNodeEvent
from ourskyai_platform_api.models.v1_create_node_event_body import V1CreateNodeEventBody
from ourskyai_platform_api.models.v1_create_node_events_request import V1CreateNodeEventsRequest
from ourskyai_platform_api.models.v1_create_node_request import V1CreateNodeRequest
from ourskyai_platform_api.models.v1_create_optical_tube_request import V1CreateOpticalTubeRequest
from ourskyai_platform_api.models.v1_diagnostic_instruction import V1DiagnosticInstruction
from ourskyai_platform_api.models.v1_duration_measured import V1DurationMeasured
from ourskyai_platform_api.models.v1_elevation_mask_point import V1ElevationMaskPoint
from ourskyai_platform_api.models.v1_file_type import V1FileType
from ourskyai_platform_api.models.v1_gain_curve import V1GainCurve
from ourskyai_platform_api.models.v1_gain_curve_point import V1GainCurvePoint
from ourskyai_platform_api.models.v1_get_instruction_request import V1GetInstructionRequest
from ourskyai_platform_api.models.v1_get_instruction_request_upload_health import V1GetInstructionRequestUploadHealth
from ourskyai_platform_api.models.v1_get_nodes import V1GetNodes
from ourskyai_platform_api.models.v1_get_or_create_camera_request import V1GetOrCreateCameraRequest
from ourskyai_platform_api.models.v1_get_or_create_mount_request import V1GetOrCreateMountRequest
from ourskyai_platform_api.models.v1_get_or_create_optical_tube_request import V1GetOrCreateOpticalTubeRequest
from ourskyai_platform_api.models.v1_get_plate_solve_catalog_diff_request import V1GetPlateSolveCatalogDiffRequest
from ourskyai_platform_api.models.v1_ground_station_participant import V1GroundStationParticipant
from ourskyai_platform_api.models.v1_image_set import V1ImageSet
from ourskyai_platform_api.models.v1_image_set_image import V1ImageSetImage
from ourskyai_platform_api.models.v1_instruction import V1Instruction
from ourskyai_platform_api.models.v1_last_instruction_response import V1LastInstructionResponse
from ourskyai_platform_api.models.v1_latest_hfr_response import V1LatestHfrResponse
from ourskyai_platform_api.models.v1_log_recorded import V1LogRecorded
from ourskyai_platform_api.models.v1_metric import V1Metric
from ourskyai_platform_api.models.v1_mount import V1Mount
from ourskyai_platform_api.models.v1_node import V1Node
from ourskyai_platform_api.models.v1_node_component_type import V1NodeComponentType
from ourskyai_platform_api.models.v1_node_controller_artifact import V1NodeControllerArtifact
from ourskyai_platform_api.models.v1_node_diagnostic_type import V1NodeDiagnosticType
from ourskyai_platform_api.models.v1_node_event_type import V1NodeEventType
from ourskyai_platform_api.models.v1_node_with_location import V1NodeWithLocation
from ourskyai_platform_api.models.v1_observation_instruction import V1ObservationInstruction
from ourskyai_platform_api.models.v1_observation_instruction_ascom_axis_rates import V1ObservationInstructionAscomAxisRates
from ourskyai_platform_api.models.v1_observation_instruction_satellite_pass_ephemeris_inner import V1ObservationInstructionSatellitePassEphemerisInner
from ourskyai_platform_api.models.v1_observation_metrics import V1ObservationMetrics
from ourskyai_platform_api.models.v1_optical_tube import V1OpticalTube
from ourskyai_platform_api.models.v1_plate_solve_catalog_file import V1PlateSolveCatalogFile
from ourskyai_platform_api.models.v1_plate_solve_catalog_file_download import V1PlateSolveCatalogFileDownload
from ourskyai_platform_api.models.v1_predicted_streak_location import V1PredictedStreakLocation
from ourskyai_platform_api.models.v1_read_noise_point import V1ReadNoisePoint
from ourskyai_platform_api.models.v1_release import V1Release
from ourskyai_platform_api.models.v1_safety_status_updated import V1SafetyStatusUpdated
from ourskyai_platform_api.models.v1_setup_action import V1SetupAction
from ourskyai_platform_api.models.v1_slew_timing import V1SlewTiming
from ourskyai_platform_api.models.v1_slew_timing_interval import V1SlewTimingInterval
from ourskyai_platform_api.models.v1_update_node_components_request import V1UpdateNodeComponentsRequest
from ourskyai_platform_api.models.v1_update_node_components_request_camera import V1UpdateNodeComponentsRequestCamera
from ourskyai_platform_api.models.v1_update_node_components_request_mount import V1UpdateNodeComponentsRequestMount
from ourskyai_platform_api.models.v1_update_node_components_request_optical_tube import V1UpdateNodeComponentsRequestOpticalTube
from ourskyai_platform_api.models.v1_update_node_request import V1UpdateNodeRequest
from ourskyai_platform_api.models.v1_video_mode_framerate_property import V1VideoModeFramerateProperty
from ourskyai_platform_api.models.v2_complete_observation_request import V2CompleteObservationRequest
