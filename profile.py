import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()
request = pc.makeRequestRSpec()

# Define nodes and services
num_nodes = 2

for i in range(num_nodes):
    if i == 0:
        node = request.RawPC("webserver")
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y apache2"))
        # Add more services as needed for webserver node
    elif i == 1:
        node = request.RawPC("observer")
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y nfs-kernel-server"))
        # Add more services as needed for observer node
        node.addService(rspec.Execute(shell="bash", command="sudo mkdir -p /var/webserver_monitor"))
        node.addService(rspec.Execute(shell="bash", command="sudo chown nobody:nogroup /var/webserver_monitor"))
        node.addService(rspec.Execute(shell="bash", command="sudo chmod 777 /var/webserver_monitor"))

# Print the RSpec
pc.printRequestRSpec(request)

