# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bento/ubuntu-22.04"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 9000, host: 9000
  config.vm.network "forwarded_port", guest: 11000, host: 11000
  config.vm.network "forwarded_port", guest: 12000, host: 12000
  config.vm.network "forwarded_port", guest: 13000, host: 13000

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "ngo", "/home/vagrant/frappe-bench/apps/ngo"

  # Disable the default share of the current code directory. Doing this
  # provides improved isolation between the vagrant box and your host
  # by making sure your Vagrantfile isn't accessible to the vagrant box.
  # If you use this you may want to enable additional shared subfolders as
  # shown above.
  # config.vm.synced_folder ".", "/vagrant", disabled: true

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    # vb.gui = true
  
    # Customize the amount of memory on the VM:
    vb.memory = "2048"

    vb.name = "ngo"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL

  # Stuff done after first `vagrant up`
  # login to ssh : vagrant ssh
  # pyenv install : https://www.dedicatedcore.com/blog/install-pyenv-ubuntu/
  # go out of ssh and login to ssh again
  # python 3.10.12 install : pyenv install 3.10.12 && pyenv global 3.10.12 
  # frappe installation : https://frappeframework.com/docs/user/en/installation#debian-ubuntu
  # bench init : bench init frappe-bench --frappe-branch version-13
  # reset frappe to commit hash : 43338f3ff02ea00b1a2e9bfb5d841cfa1fa78fd2
  # get erpnext app : bench get-app erpnext --branch version-13
  # reset erpnext to version tag : v13.42.6
  # go out of ssh ; vagrant halt ; add synced folder for ngo in Vagrantfile ; vagrant up
  # install ngo app dependencies : bench setup requirements ngo --python
  # make ngo app available in bench version command : echo "" >> sites/apps.txt && echo ngo >> sites/apps.txt
  # bench set-config -g root_password root
  # bench set-config -g admin_password root
  # bench new-site ngo.local
  # bench use ngo.local
  # bench install-app erpnext
  # bench install-app ngo
end
