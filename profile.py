import geni.portal as portal
import geni.rspec.pg as rspec

pc = portal.Context()
request = pc.makeRequestRSpec()


# Number of nodes in your experiment
num_nodes = 2  # You can adjust this based on your requirements

# Create nodes
for i in range(num_nodes):
    if i == 0:
        node = request.RawPC("webserver")
        node.hardware_type = "m510"  # Example hardware type, adjust as needed
        
        # Set up Apache web server
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y apache2"))
        node.addService(rspec.Execute(shell="bash", command="sudo systemctl enable apache2"))
        node.addService(rspec.Execute(shell="bash", command="sudo systemctl start apache2"))
        
        # Mount NFS from observer node
        node.addService(rspec.Execute(shell="bash", command="sudo mkdir -p /var/webserver_log"))
        node.addService(rspec.Execute(shell="bash", command="sudo mount -t nfs observer:/var/webserver_monitor /var/webserver_log"))

    elif i == 1:
        node = request.RawPC("observer")
        node.hardware_type = "m510"  # Example hardware type, adjust as needed
        
        # Set up NFS server
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get update"))
        node.addService(rspec.Execute(shell="bash", command="sudo apt-get install -y nfs-kernel-server"))
        node.addService(rspec.Execute(shell="bash", command="sudo mkdir -p /var/webserver_monitor"))
        node.addService(rspec.Execute(shell="bash", command="sudo chown nobody:nogroup /var/webserver_monitor"))
        node.addService(rspec.Execute(shell="bash", command="sudo chmod 777 /var/webserver_monitor"))
        node.addService(rspec.Execute(shell="bash", command="sudo systemctl enable nfs-kernel-server"))
        node.addService(rspec.Execute(shell="bash", command="sudo systemctl start nfs-kernel-server"))
        node.addService(rspec.Execute(shell="bash", command="sudo exportfs -r"))
        
        # Open NFS ports in firewall (if needed)
  pc.printRequestRSpec(request)
