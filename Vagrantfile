# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "parallels/ubuntu-12.04"

  config.vm.provider "parallels" do |vm|
    vm.name = "vagrant-chiwanpark.github.io"
    vm.cpus = 2
    vm.memory = 512
    vm.update_guest_tools = true
    vm.customize ["set", :id, "--on-window-close", "keep-running"]
  end

  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.provision :shell, :path => "setup-env.sh"
end
