import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()

# Create a request object to start building the RSpec
request = pc.makeRequestRSpec()

# Add a node for the webserver with public IP
webserver = request.RawPC("webserver")
webserver.hardware_type = "m510"
webserver.routable_control_ip = True  # Request a public IP for the webserver
webserver.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
webserver.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y apache2"))

# Add a node for the observer with NFS server setup
observer = request.RawPC("observer")
observer.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
observer.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y nfs-kernel-server"))
observer.addService(rspec.Execute(shell="bash", command="sudo mkdir -p /var/webserver_monitor"))

# NFS export configuration
observer.addService(rspec.Execute(shell="bash", command='echo "/var/webserver_monitor *(rw,no_root_squash,no_subtree_check)" | sudo tee -a /etc/exports'))
observer.addService(rspec.Execute(shell="bash", command="sudo exportfs -a"))

# Linking webserver_log from observer to webserver
link = request.Link(members=[webserver, observer])

# Print the RSpec to the enclosing page
pc.printRequestRSpec(request)
