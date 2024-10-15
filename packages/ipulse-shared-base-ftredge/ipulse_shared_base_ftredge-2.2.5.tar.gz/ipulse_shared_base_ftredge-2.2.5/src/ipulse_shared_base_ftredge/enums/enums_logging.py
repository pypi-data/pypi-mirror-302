# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import Enum


class LoggingHandler(Enum):

    """
    Standardized remote logging handlers for data engineering pipelines,
    designed for easy analysis and identification of remote logging
    requirements
    """
    
    NONE = "none"  # No remote handler
    LOCAL_STREAM = "local_stream"  # Local stream handler
    GCP_CLOUD_LOGGING = "gcp_cloud_logging"
    GCP_ERROR_REPORTING = "gcp_error_reporting"
    GCP_FIREBASE = "gcp_firebase"
    AWS_CLOUD_WATCH = "aws_cloud_watch"
    AZURE_MONITOR = "azure_monitor"
    AZURE_APPLICATION_INSIGHTS = "azure_application_insights"
    IBM_LOG_ANALYTICS = "ibm_log_analytics"
    ALIBABA_LOG_SERVICE = "alibaba_log_service"
    LOGGLY = "loggly"
    DATADOG = "datadog"
    NEW_RELIC = "new_relic"
    SENTRY = "sentry"
    SUMOLOGIC = "sumologic"
    # --- Other ---
    SYSLOG = "syslog" # For system logs
    CUSTOM = "custom" # For a user-defined remote handler
    OTHER = "other"

    def __str__(self):
        return self.value


class LogLevel(Enum):
    """
    Standardized notice levels for data engineering pipelines,
    designed for easy analysis and identification of manual 
    intervention needs.
    """
    DEBUG = 100  # Detailed debug information (for development/troubleshooting)

    INFO = 1000

    # Task Info (1110 - 1119)
    INFO_TASK_STARTED = 1110
    INFO_TASK_COMPLETE = 1111
    INFO_TASK_COMPLETE_WITH_NOTICES = 1112
    INFO_TASK_COMPLETE_WITH_WARNINGS = 1113
    INFO_TASK_PAUSED = 1114
    INFO_TASK_RESUMED = 1115
    INFO_TASK_CANCELLED = 1116
    INFO_TASK_STOPPED = 1117
    INFO_TASK_SKIPPED = 1118

    # Data Read Info (1120 - 1129)
    INFO_READ_CLOUD_DB_COMPLETE = 1120
    INFO_READ_LOCAL_DB_COMPLETE = 1121
    INFO_READ_FILE_FROM_CLOUD_STORAGE_COMPLETE = 1122
    INFO_READ_FILE_FROM_LOCAL_STORAGE_COMPLETE = 1123
    INFO_READ_HTTP_GET_COMPLETE = 1124

    # Data TRANSFORMATION Info (1130 - 1139)
    INFO_FILTER_COMPLETE = 1130
    INFO_TRANSFORM_COMPLETE = 1131

    # Subject Info (1210 - 1219)
    INFO_SUBJECT_STARTED = 1210
    INFO_SUBJECT_COMPLETE = 1211
    INFO_SUBJECT_COMPLETE_WITH_WARNINGS = 1212
    INFO_SUBJECT_COMPLETE_WITH_NOTICES = 1213
    INFO_SUBJECT_COMPLETE_WITH_NOTICES_AND_WARNINGS = 1214

    # Iteration Info (1310 - 1319)
    INFO_ITERATION_STARTED = 1310
    INFO_ITERATION_PAUSED = 1311
    INFO_ITERATION_RESUMED = 1312
    INFO_ITERATION_CANCELLED = 1313
    INFO_ITERATION_STOPPED = 1314
    INFO_ITERATION_SKIPPED = 1315

    # Pipeline Info (1410 - 1419)
    INFO_PIPELINE_STARTED = 1410
    INFO_PIPELINE_PAUSED = 1411
    INFO_PIPELINE_RESUMED = 1412
    INFO_PIPELINE_CANCELLED = 1413
    INFO_PIPELINE_STOPPED = 1414

    # ACTIONS (4100 - 4999)
    ACTION = 4000 # General action, no immediate action required
    
    # General Action Completions (4100 - 4199)
    ACTION_CWUD_COMPLETE = 4100 # General action, no immediate action required
    ACTION_CREATE_COMPLETE = 4101
    ACTION_WRITE_COMPLETE = 4102
    ACTION_UPDATE_COMPLETE = 4103
    ACTION_DELETE_COMPLETE = 4104

    # Bulk Action Completions (4200 - 4299)
    ACTION_CWUD_BULK_COMPLETE = 4200
    ACTION_CREATE_BULK_COMPLETE = 4201
    ACTION_WRITE_BULK_COMPLETE = 4202
    ACTION_UPDATE_BULK_COMPLETE = 4203
    ACTION_DELETE_BULK_COMPLETE = 4204

    # Cloud Storage Actions (4300 - 4399)
    ACTION_WRITE_IN_CLOUD_STORAGE_COMPLETE = 4300
    ACTION_UPDATE_IN_CLOUD_STORAGE_COMPLETE = 4301
    ACTION_DELETE_IN_CLOUD_STORAGE_COMPLETE = 4302

    ACTION_WRITE_BULK_IN_CLOUD_STORAGE_COMPLETE = 4310
    ACTION_UPDATE_BULK_IN_CLOUD_STORAGE_COMPLETE = 4311
    ACTION_DELETE_BULK_IN_CLOUD_STORAGE_COMPLETE = 4312

    # Local Storage Actions (4400 - 4499)
    ACTION_WRITE_IN_LOCAL_STORAGE_COMPLETE = 4400
    ACTION_UPDATE_IN_LOCAL_STORAGE_COMPLETE = 4401
    ACTION_DELETE_IN_LOCAL_STORAGE_COMPLETE = 4402

    # Local DB Actions (4500 - 4599)
    ACTION_WRITE_IN_LOCAL_DB_COMPLETE = 4500
    ACTION_UPDATE_IN_LOCAL_DB_COMPLETE = 4501
    ACTION_DELETE_IN_LOCAL_DB_COMPLETE = 4502

    # Cloud DB Actions (4600 - 4699)
    ACTION_WRITE_IN_CLOUD_DB_COMPLETE = 4600
    ACTION_UPDATE_IN_CLOUD_DB_COMPLETE = 4601
    ACTION_DELETE_IN_CLOUD_DB_COMPLETE = 4602
        
    ACTION_WRITE_BULK_IN_CLOUD_DB_COMPLETE = 4610
    ACTION_UPDATE_BULK_IN_CLOUD_DB_COMPLETE = 4611
    ACTION_DELETE_BULK_IN_CLOUD_DB_COMPLETE = 4612

    ACTION_CREATE_CLOUD_DB_TABLE_COMPLETE = 4620
    ACTION_CREATE_CLOUD_DB_COLLECTION_COMPLETE = 4621
    ACTION_CREATE_CLOUD_DB_DOCUMENT_COMPLETE = 4622
    ACTION_DELETE_CLOUD_DB_TABLE_COMPLETE = 4630
    ACTION_DELETE_CLOUD_DB_COLLECTION_COMPLETE = 4631
    ACTION_DELETE_CLOUD_DB_DOCUMENT_COMPLETE = 4632

    # HTTP Actions (4700 - 4799)
    ACTION_WRITE_HTTP_POST_COMPLETE = 4700
    ACTION_WRITE_HTTP_PUT_COMPLETE = 4701
    ACTION_WRITE_HTTP_PATCH_COMPLETE = 4702
    ACTION_WRITE_HTTP_DELETE_COMPLETE = 4703

    # NOTICES (5100 - 5199)
    NOTICE = 5000  # Maybe same file or data already fully or partially exists
    NOTICE_ALREADY_EXISTS = 5100 # Data already exists, no action required
    NOTICE_PARTIAL_EXISTS = 5101 # Partial data exists, no action required

    NOTICE_FILE_IN_CLOUD_STORAGE_ALREADY_EXISTS = 5110
    NOTICE_DATA_IN_CLOUD_DB_ALREADY_EXISTS = 5111
    NOTICE_DATA_IN_CLOUD_DB_PARTIALLY_EXISTS = 5112

    # WARNINGS (6100 - 6299)
    WARNING = 6000 # General warning, no immediate action required
    WARNING_REVIEW_RECOMMENDED = 6100 # Action recommended to prevent potential future issues
    WARNING_DATA_SCHEMA_ISSUE = 6200 # Action recommended to prevent potential future issues
    WARNING_METADATA_SCHEMA_ISSUE = 6201 # Action recommended to prevent potential future issues

    # ERRORS (7000 - 7999)
    ERROR = 7000 # General error, no immediate action required
    ERROR_EXCEPTION = 7001
    ERROR_CUSTOM = 7002 # Temporary error, automatic retry likely to succeed
    ERROR_DATA_QUALITY_ISSUE = 7003 #Error due to threshold reached, no immediate action required
    ERROR_SCHEMA_ISSUE = 7004 #Error due to threshold reached, no immediate action required

    # Action Errors (7100 - 7199)
    ERROR_ACTION_PARTIALLY_FAILED = 7100 # Partial or full failure, manual intervention required
    ERROR_ACTION_FAILED = 7101 # Operation failed, manual intervention required
    ERROR_ACTION_WITH_ERRORS = 7102 # Partial or full failure, manual intervention required
    ERROR_ACTION_WITH_WARNINGS_OR_ERRORS = 7103 # Partial or full failure, manual intervention required

    ERROR_ACTION_CWUD_FAILED = 7120 # Data persistance failed, manual intervention required
    ERROR_ACTION_CREATE_FAILED = 7121
    ERROR_ACTION_WRITE_FAILED = 7122
    ERROR_ACTION_UPDATE_FAILED = 7123
    ERROR_ACTION_DELETE_FAILED = 7124

    ERROR_ACTION_CWUD_WITH_ERRORS = 7140
    ERROR_ACTION_CREATE_WITH_ERRORS = 7141
    ERROR_ACTION_WRITE_WITH_ERRORS=7142
    ERROR_ACTION_UPDATE_WITH_ERRORS = 7143
    ERROR_ACTION_DELETE_WITH_ERRORS = 7144

    # Read Errors (7200 - 7299)
    ERROR_TASK_FAILED = 7200
    ERROR_READ_FAILED = 7201
    ERROR_READ_PARTIALLY_FAILED = 7202
    ERROR_READ_DB_FAILED = 7210
    ERROR_READ_DB_PARTIALLY_FAILED = 7211

    ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED = 7220
    ERROR_READ_FILE_FROM_CLOUD_STORAGE_PARTIALLY_FAILED = 7221

    ERROR_READ_FILE_FROM_LOCAL_STORAGE_FAILED = 7230
    ERROR_READ_FILE_FROM_LOCAL_STORAGE_PARTIALLY_FAILED = 7231

    ERROR_READ_HTTP_GET_FAILED = 7250
    ERROR_READ_HTTP_GET_PARTIALLY_FAILED = 7251
    ERROR_READ_HTTP_GET_WITH_ERRORS = 7252
    ERROR_READ_HTTP_GET_WITH_WARNINGS_OR_ERRORS = 7253

    # Threshold Errors (7800 - 7899)
    ERROR_TASK_THRESHOLD_REACHED = 7800
    ERROR_DATA_QUALITY_THRESHOLD_REACHED = 7801 # Error due to threshold reached, no immediate action required
    ERROR_METADATA_QUALITY_THRESHOLD_REACHED = 7802
    ERROR_PIPELINE_THRESHOLD_REACHED = 7810 # Error due to threshold reached, no immediate action required
    ERROR_SUBJECT_THRESHOLD_REACHED = 7811 # Error due to threshold reached, no immediate action required
    ERROR_ITERATION_THRESHOLD_REACHED = 7812

    # FAILURES (8100 - 8899)
    FAILED = 8000  # General failure, manual intervention required

    # Task Failures (8100 - 8199)
    FAILED_TASK = 8100  # Task failed, but might be recoverable
    FAILED_TASK_COMPLETE_WITH_ERRORS = 8101  # Task completed, but with errors

    # Subject Failures (8200 - 8299)
    FAILED_SUBJECT = 8200  # Subject failed, but might be recoverable
    FAILED_SUBJECT_COMPLETE_WITH_ERRORS = 8201  # Subject completed, but with errors

    # Iteration Failures (8300 - 8399)
    FAILED_ITERATION = 8300  # Iteration failed, but might be recoverable
    FAILED_ITERATION_COMPLETE_WITH_ERRORS = 8301  # Iteration completed, but with errors

    # Pipeline Failures (8400 - 8499)
    FAILED_PIPELINE_COMPLETE_WITH_ERRORS = 8400  # Pipeline completed, but with errors
    FAILED_PIPELINE_EXITED = 8401  # Pipeline exited prematurely 

    # Critical System Failures (8800 - 8899)
    FAILED_CRITICAL_SYSTEM_FAILURE = 8800  # System-level failure (e.g., infrastructure, stack overflow), requires immediate action

    # SUCCESSES (9100 - 9399)
    SUCCESS = 9000
    
    # Task Successes (9100 - 9199)
    SUCCESS_TASK_COMPLETE = 9100
    SUCCESS_TASK_COMPLETE_WITH_NOTICES = 9101
    SUCCESS_TASK_COMPLETE_WITH_WARNINGS = 9102
    
    # Subject Successes (9200 - 9299)
    SUCCESS_SUBJECT_COMPLETE = 9200
    SUCCESS_SUBJECT_COMPLETE_WITH_NOTICES = 9201
    SUCCESS_SUBJECT_COMPLETE_WITH_WARNINGS = 9202

    # Iteration Successes (9300 - 9399)
    SUCCESS_ITERATION_COMPLETE = 9300
    SUCCESS_ITERATION_COMPLETE_WITH_NOTICES = 9301
    SUCCESS_ITERATION_COMPLETE_WITH_WARNINGS = 9302
    
    # Pipeline Successes (9400 - 9499)
    SUCCESS_PIPELINE_COMPLETE = 9400
    SUCCESS_PIPELINE_COMPLETE_WITH_NOTICES = 9401
    SUCCESS_PIPELINE_COMPLETE_WITH_WARNINGS = 9402 

    def __str__(self):
        return self.value