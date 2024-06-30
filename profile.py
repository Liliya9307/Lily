import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()

# Create a request object to start building the RSpec
request = pc.makeRequestRSpec()

# Add nodes for webserver and observer
webserver = request.RawPC("webserver")
webserver.hardware_type = "m510"
webserver.routable_control_ip = True  # Request a public IP for the webserver
webserver.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
webserver.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y apache2"))

observer = request.RawPC("observer")
observer.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
observer.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y nfs-kernel-server"))
observer.addService(rspec.Execute(shell="bash", command="sudo mkdir -p /var/webserver_monitor"))

# Add a link between webserver and observer
link = request.Link(members=[webserver.iface[0], observer.iface[0]])

# Assign IP addresses and subnet masks to the interfaces explicitly
webserver_if = webserver.addInterface("eth1")
webserver_if.addAddress(rspec.IPv4Address("192.168.1.1", "255.255.255.0"))  # IP address and subnet mask

observer_if = observer.addInterface("eth1")
observer_if.addAddress(rspec.IPv4Address("192.168.1.2", "255.255.255.0"))  # IP address and subnet mask

# NFS export configuration on observer
observer.addService(rspec.Execute(shell="bash", command='echo "/var/webserver_monitor *(rw,no_root_squash,no_subtree_check)" | sudo tee -a /etc/exports'))
observer.addService(rspec.Execute(shell="bash", command="sudo exportfs -a"))

# Print the RSpec to the enclosing page
pc.printRequestRSpec(request)


