""" Module for python tracing for cdc_tech_environment_service with minimal dependencies. """

import os
import sys
import platform
import time
import requests
import logging
from datetime import datetime
# import plotly.graph_objects as go
# import plotly.offline as pyo

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)

from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.trace.status import StatusCode
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

dbutils_exists = "dbutils" in locals() or "dbutils" in globals()
if dbutils_exists is False:  # Use '==' for comparison instead of 'is'
    # pylint: disable=invalid-name
    dbutils = None


# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name
sys.path.append("..")

TRACE_FILE_NAME_PREFIX = "cdh_lava_core_tracing"

if OS_NAME.lower() == "nt":  # Windows environment
    print("environment_logging: windows")
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    env_path = os.path.dirname(os.path.abspath(sys.executable))
    sys.path.append(os.path.join(env_path, "share"))

    try:
        ENV_SHARE_PATH = Path.home()
    except RuntimeError as e:
        print(f"Warning: Error occurred while determining home directory: {e}")
        # Provide a fallback path or handle the error as required
        # Replace 'fallback_directory_path' with an appropriate path or another way to handle the error
        ENV_SHARE_PATH = Path(os.environ.get("HOME"))
        print(f"Using Fallback Environment Variable path: {ENV_SHARE_PATH}")

    TRACE_FILENAME = ENV_SHARE_PATH / f"{TRACE_FILE_NAME_PREFIX}.txt"

else:  # Non-Windows environment
    print("environment_logging: non-windows")

    ENV_SHARE_FALLBACK_PATH = "/usr/local/share"

    env_path = os.path.dirname(os.path.abspath(sys.executable))
    share_path_option1 = os.path.join(env_path, "share")

    try:
        # Check if the first path exists
        if os.path.exists(share_path_option1):
            # If the first path exists, use it
            ENV_SHARE_PATH = share_path_option1
        else:
            # If the first path does not exist, try the second path
            ENV_SHARE_PATH = os.path.join(os.path.expanduser("~"), "share")

        # Append the chosen path to sys.path
        sys.path.append(ENV_SHARE_PATH)
        SUB_PATH = f"{TRACE_FILE_NAME_PREFIX}.txt"
        SUB_PATH = SUB_PATH.lstrip("/\\")
        TRACE_FILENAME = os.path.join(ENV_SHARE_PATH, SUB_PATH)

    except RuntimeError as e:
        # Handle the error if home directory can't be determined
        print(f"Error occurred: {e}")
        # Set a fallback path or handle the error appropriately
        # Example: using a predefined directory or terminating the program
        # Replace 'fallback_directory_path' with an actual path or another error handling strategy
        ENV_SHARE_PATH = ENV_SHARE_FALLBACK_PATH
        SUB_PATH = f"{TRACE_FILE_NAME_PREFIX}.txt"
        SUB_PATH = SUB_PATH.lstrip("/\\")
        TRACE_FILENAME = os.path.join(ENV_SHARE_PATH, SUB_PATH)
        sys.path.append(ENV_SHARE_PATH)

print(f"TRACE_FILENAME: {TRACE_FILENAME}")

try:
    FOLDER_EXISTS = os.path.exists(ENV_SHARE_PATH)
    if not FOLDER_EXISTS:
        # Create a new directory because it does not exist
        os.makedirs(ENV_SHARE_PATH)
except Exception as e:
    FOLDER_EXISTS = os.path.exists(ENV_SHARE_FALLBACK_PATH)
    if not FOLDER_EXISTS:
        if platform.system() != "Windows":
            # Create a new directory because it does not exist
            os.makedirs(ENV_SHARE_FALLBACK_PATH)
            TRACE_FILENAME = ENV_SHARE_FALLBACK_PATH + "/cdh_lava_core_tracing.txt"

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


# Default Application Insights connection string - Dev
# Extract the application ID from the connection string
APPLICATIONINSIGHTS_APP_ID = "48a71f9c-8c54-4a73-ada1-36e87c6e7347"
APPLICATIONINSIGHTS_INSTURMENTATION_KEY="8f02ef9a-cd94-48cf-895a-367f102e8a24"
APPLICATIONINSIGHTS_CONNECTION_STRING = (
    f"InstrumentationKey={APPLICATIONINSIGHTS_APP_ID};"
    "IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;"
    "LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/"
)
 


class FileTraceExporter(SpanExporter):
    """
    A class that exports spans to a file for environment tracing.

    Attributes:
        file_path (str): The path of the file to export the spans to.
    """

    def __init__(self):
        self.file_path = TRACE_FILENAME
        self.file_handler = TimedRotatingFileHandler(
            self.file_path, when="midnight", interval=1, backupCount=7
        )
        os.makedirs(os.path.dirname(ENV_SHARE_PATH), exist_ok=True)

    def to_readable_dict(self, span):
        """
        Converts a span object to a readable dictionary format.

        Args:
            span: The span object to convert.

        Returns:
            A dictionary containing the readable representation of the span.

        """
        return {
            "trace_id": str(span.get_span_context().trace_id),
            "span_id": str(span.get_span_context().span_id),
            "parent_id": str(span.parent.span_id) if span.parent else None,
            "name": span.name,
            "status": StatusCode(span.status.status_code).name,
            "kind": span.kind.name,
            "start_time": str(span.start_time),
            "end_time": str(span.end_time),
            "attributes": dict(span.attributes),
        }

    def export(self, spans):
        """
        Export the given spans to a file.

        Args:
            spans (list): List of spans to export.

        Returns:
            str: The result of the span export operation.
        """
        for span in spans:
            span_dict = self.to_readable_dict(span)
            record_dict = {
                "msg": f"Span Data: {span_dict}",
                "args": None,
                "levelname": "INFO",
                # Add other necessary fields for LogRecord
            }

            log_record = logging.makeLogRecord(record_dict)
            self.file_handler.handle(log_record)

            # with open(self.file_path, "a", encoding="utf-8") as file:
            #    file.write(f"Span Data: {span_dict}\n")
        return SpanExportResult.SUCCESS

    def get_trace_file_name(self):
        """
        Returns the name of the trace file.

        Returns:
            str: The name of the trace file.
        """
        return self.file_path

    def delete_old_files(self):
        """
        Delete old files from the environment share folder.

        This method deletes files that are older than 7 days from the environment share folder.
        """
        folder_path = ENV_SHARE_PATH
        for file_name in os.listdir(folder_path):
            # Check if the file name contains the prefix
            if TRACE_FILE_NAME_PREFIX in file_name:
                file_path = os.path.join(folder_path, file_name)
                # Check if the file is older than 7 days
                if os.path.getmtime(file_path) < time.time() - 7 * 86400:
                    os.remove(file_path)

    def shutdown(self):
        """Shuts down the tracer and cleans up resources.

        Ensures that all spans, including those in the Azure exporter,
        are flushed before shutting down.

        Closes file handler
        """
        self.file_handler.close()





class TracerSingleton:
    """
    A Python wrapper class around OpenTelemetry Tracer using a
    singleton design pattern, so that the tracer instance is created
    only once and the same instance is used throughout the application.

    This class is designed to be a singleton to ensure that there's only
    one tracer instance throughout the application.

    Raises:
        Exception: If an attempt is made to create another instance
                   of this singleton class.

    Returns:
        TracerSingleton: An instance of the TracerSingleton class.
    """

    _instance = None
    log_to_console = False  # Set to False if you want console logging

    @staticmethod
    def instance(
        calling_namespace_name,
        calling_service_name,
        data_product_id,
        environment,
        default_connection_string=None,
    ):
        """Provides access to the singleton instance of the LoggerSingleton
        class.

        This method ensures there is only one instance of the LoggerSingleton
        class in the application.
        If an instance already exists, it returns that instance. If no
        instance exists, it creates a new one and then returns that.
        """
        if TracerSingleton._instance is None:
            TracerSingleton(
                calling_namespace_name,
                calling_service_name,
                data_product_id,
                environment,
                default_connection_string,
            )
        return TracerSingleton._instance

    def __init__(
        self,
        calling_namespace_name,
        calling_service_name,
        data_product_id,
        environment="dev",
        default_connection_string=None
    ):
        """Initializes the singleton instance, if it doesn't exist yet.

        This method is responsible for ensuring that only a single instance
        of the class is created. If an instance doesn't exist at the time of
        invocation, it will be created. If an instance already exists,
        the existing instance will be used.
        """
        if TracerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TracerSingleton._instance = self

        service_name = f"{data_product_id}.{calling_service_name}"
        cloud_role = f"{data_product_id}-{calling_service_name}-{environment}"
        # Define a Resource with your service.name attribute
        resource = Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: service_name,
                ResourceAttributes.SERVICE_NAMESPACE: calling_namespace_name ,
                "ai.cloud.role": cloud_role  # Set cloud role name
            }
        )

        # Log the resource attributes for debugging
        logging.info(f"Resource attributes: {resource.attributes}")

        # Set tracer provider
        trace.set_tracer_provider(TracerProvider(resource=resource))

        if default_connection_string is None or default_connection_string == "":
            if environment == "prod":
                # PROD
                default_connection_string = (
                    "InstrumentationKey=e7808e07-4242-4ed3-908e-c0a4c3b719b1;"
                    "IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;"
                    "LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/"
                )
            else:
                # DEV
                default_connection_string = APPLICATIONINSIGHTS_CONNECTION_STRING
        connection_string = default_connection_string

        if "APPLICATIONINSIGHTS_CONNECTION_STRING" not in os.environ:
            os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"] = connection_string

        # Set up the BatchSpanProcessor with File Exporter
        file_trace_exporter = FileTraceExporter()
        file_span_processor = BatchSpanProcessor(file_trace_exporter)
        self.file_trace_exporter = file_trace_exporter
        trace.get_tracer_provider().add_span_processor(file_span_processor)

        # Set up the BatchSpanProcessor with Azure Exporter
        exporter = AzureMonitorTraceExporter()
        self.azure_trace_exporter = exporter
        span_processor = BatchSpanProcessor(exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        # Add ConsoleSpanExporter if log_to_console is True
        if TracerSingleton.log_to_console:
            trace.get_tracer_provider().add_span_processor(
                SimpleSpanProcessor(ConsoleSpanExporter())
            )

        # Get tracer
        self.tracer = trace.get_tracer(__name__)

    @classmethod
    def format_duration(cls, duration_in_ms):
        if duration_in_ms >= 1000:
            return f"{duration_in_ms / 1000:.2f} s"
        else:
            return f"{duration_in_ms} ms"

    @classmethod
    def format_duration(cls, duration_in_seconds):
        """
        Dynamically format the duration: display in minutes if it's more than 60 seconds.
        """
        if duration_in_seconds >= 60:
            minutes = duration_in_seconds / 60
            return f"{minutes:.2f} minutes"
        else:
            return f"{duration_in_seconds:.2f} seconds"

    @classmethod
    def graph_ai_dependencies(cls, operation_id, api_key, data_product_id, environment):

        from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
 
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("graph_ai_dependencies"):

            try:


                # Replace with the actual call to query_ai_dependencies()
                data = cls.query_ai_dependencies(operation_id, api_key, data_product_id, environment)

                if not data:
                    return "No data available"

                # Extract all timestamps and calculate start, end, and total duration
                timestamps = [datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S.%fZ') for row in data]
                start_time = min(timestamps)
                end_time = max(timestamps)
                overall_duration_in_seconds = (end_time - start_time).total_seconds()

                # Format start time, end time, and overall duration
                formatted_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_overall_duration = cls.format_duration(overall_duration_in_seconds)

                # Prepare the summary table HTML with the operation ID in the header
                summary_table_html = f'''
                <h2>Dependency Timeline Summary</h2> <br/>for Operation ID: {operation_id}
                <br/>for Data Product Id: {data_product_id}, Environment: {environment} <br/>
                <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                    <thead style="background-color: #f2f2f2;">
                        <tr>
                            <th>Start Time</th>
                            <th>End Time</th>
                            <th>Overall Duration</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{formatted_start_time}</td>
                            <td>{formatted_end_time}</td>
                            <td>{formatted_overall_duration}</td>
                        </tr>
                    </tbody>
                </table>
                '''

                # Loop through the data and remove sequential duplicates
                unique_data = []
                previous_row = None
                for row in data:
                    # Check if the current row is a duplicate of the previous row (excluding the timestamp)
                    if previous_row is None or row[1:] != previous_row[1:]:
                        unique_data.append(row)
                    previous_row = row

                # Process the data into the main table (excluding timestamps, now using unique rows)
                table_html = '''
                <h2>Dependency Details</h2>
                <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                    <thead style="background-color: #f2f2f2;">
                        <tr>
                            <th>Name</th>
                            <th>Duration</th>
                            <th>Success</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

                # Loop through unique data to generate table rows
                for i, row in enumerate(unique_data):
                    name = row[1]
                    duration = cls.format_duration(row[3] / 1000)  # Convert ms to seconds and format the duration
                    success = 'Success' if row[4] else 'Failure'

                    # Apply alternating row color
                    row_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"

                    # Color code success or failure
                    success_color = "green" if success == "Success" else "red"

                    # Add the rows without toggle
                    table_html += f'''
                    <tr style="background-color: {row_color};">
                        <td>{name}</td>
                        <td>{duration}</td>
                        <td style="color: {success_color}; font-weight: bold;">{success}</td>
                    </tr>
                    '''

                table_html += '''
                    </tbody>
                </table>
                '''

                # Return the summary table and the main table as a single HTML string
                return summary_table_html + table_html
            except Exception as ex:
                    error_msg = "Error: %s", ex
                    exc_info = sys.exc_info()
                    LoggerSingleton.instance(
                        NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                    ).error_with_exception(error_msg, exc_info)
                    raise

    @staticmethod
    def query_ai_dependencies(operation_id, api_key, data_product_id, environment):

        from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
 
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("query_ai_dependencies"):

            try:
                query = f"""
                dependencies
                | where operation_Id == '{operation_id}'
                | project timestamp, name, resultCode, duration, success
                | sort by timestamp asc
                """
                url = f"https://api.applicationinsights.io/v1/apps/{APPLICATIONINSIGHTS_APP_ID}/query"
                headers = {
                    "x-api-key": api_key
                }
                params = {
                    "query": query
                }
                
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    return response.json()["tables"][0]["rows"]
                else:
                    raise ValueError(f"Error querying Application Insights: {response.text}")
                    return []
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise


    def get_trace_file_path(self):
        """
        Returns the path to the trace file.

        Returns:
            str: The path to the trace file.
        """
        return self.file_trace_exporter.file_path

    def get_tracer(self):
        """
        Get the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.tracer

    def shutdown(self):
        """Handles the shutdown of all exporters and the tracer provider.

        Ensures that both the Azure and file-based exporters are flushed and shutdown properly.
        """
        try:
            # Force flush all spans to ensure they are exported
            trace.get_tracer_provider().force_flush()
            logging.info("Forced flush of all spans before shutdown.")
        except Exception as e:
            logging.error(f"Error during force flush: {e}")

        try:
            # Shutdown Azure span processor
            if self.azure_span_processor:
                self.azure_span_processor.shutdown()
                logging.info("Azure span processor shutdown successfully.")
        except Exception as e:
            logging.error(f"Error during Azure span processor shutdown: {e}")

        try:
            # Shutdown file trace exporter
            if self.file_trace_exporter:
                self.file_trace_exporter.shutdown()
                logging.info("File trace exporter shutdown successfully.")
        except Exception as e:
            logging.error(f"Error during file trace exporter shutdown: {e}")

        # Shutdown the global tracer provider
        try:
            trace.get_tracer_provider().shutdown()
            logging.info("Tracer provider shutdown successfully.")
        except Exception as e:
            logging.error(f"Error during tracer provider shutdown: {e}")

    def force_flush(self):
        """This method forces an immediate write of all log
        messages currently in the buffer.

        In normal operation, log messages may be buffered for
        efficiency. This method ensures that all buffered messages
        are immediately written to their destination. It can be
        useful in scenarios where you want to ensure that all
        log messages have been written out, such as before ending
        a program.
        """
        trace.get_tracer_provider().force_flush()
