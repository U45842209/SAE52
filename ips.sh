# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed or not in the system PATH. Please install Docker first."
    exit 1
fi

# Get a list of all running container IDs
container_ids=$(docker ps -q)

# Loop through each container ID and display its IP address
for container_id in $container_ids; do
    # Use 'docker inspect' to get the container's IP address
    container_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container_id")

    # Display the container name (if available) and its IP address
    container_name=$(docker inspect -f '{{.Name}}' "$container_id")
    echo "Container Name: ${container_name:1}"  # Remove the leading '/'
    echo "Container ID: $container_id"
    echo "IP Address: $container_ip"
    echo "---------------------------------------------"
done

