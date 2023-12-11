# Use TensorFlow Serving image as the base image
FROM tensorflow/serving

# The name of your model
ENV MODEL_NAME=saved_model

# Create a directory in the container for your model
RUN mkdir -p /models/${MODEL_NAME}/1/

# Set the model base path environment variable
ENV MODEL_BASE_PATH=/models

# Copy the model directory from your local machine to the container
COPY saved_model/my_model /models/${MODEL_NAME}/1/

# Expose the port TensorFlow Serving listens on
EXPOSE 8501

# Set the entry point for TensorFlow Serving
# This command runs TensorFlow Serving and sets up the REST API on port 8501
ENTRYPOINT ["/usr/bin/tensorflow_model_server"]

# Command to start TensorFlow Serving with the required arguments
CMD ["--rest_api_port=8501", "--model_name=${MODEL_NAME}", "--model_base_path=${MODEL_BASE_PATH}"]